"""One object, one box: rejoin props the scanner split, and drop the blobs it double-boxed.

    python tools/tileset_library/merge.py --dry-run
    python tools/tileset_library/merge.py                      # work on the live registry
    python tools/tileset_library/merge.py --base 055d7b35e     # rebuild from a commit's boxes

Always work from the untouched scanner boxes, never by patching a merged result. The
guards below each exist because a real pass got it wrong without them:

  blob pre-pass   the scanner boxes touching objects as one blob AND boxes each part;
                  a box holding 2+ boxes covering most of it is that blob, so keep the
                  parts. Skipping this "absorbed" single chairs into chair pairs.
  seam guard      two objects placed flush do not continue each other's shading.
  size cap        a merge over CAP px a side is a row of shelf units, not a prop.
  no overgrowth   extension is for art nobody registered; never grow over a registered
                  box, or the absorb step swallows a neighbour past the seam guard.

There is no automatic split. Of 227 two-tile-tall boxes with a pinched seam nearly all
were single objects (hydrants, bunk beds, sinks, potted plants); the Studio's Split
button gives that call to the owner.
"""
import argparse, collections, json, subprocess

import numpy as np

from common import (LIB, PROPS, REPO, OPAQUE, load_json, load_props, load_rgba, print_marks,
                    remap_marks, save_json, set_geometry, sheet_of, trim)

RUN = 0.6          # share of a shared edge that must be one opaque run
STEP = 48          # extension strip
MAXSTEP = 3
CAP = 240
OPP = {"E": "W", "W": "E", "N": "S", "S": "N"}


def longest(row):
    best = cur = 0
    for v in row:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best


def continues(A, box, side):
    """Art crosses this edge: a long opaque run on the edge and art just beyond it."""
    x, y, w, h = box; H, W = A.shape
    if side == "N":
        if y <= 0: return False
        edge, beyond = A[y, x:x + w], A[y - 1, x:x + w]
    elif side == "S":
        if y + h >= H: return False
        edge, beyond = A[y + h - 1, x:x + w], A[y + h, x:x + w]
    elif side == "W":
        if x <= 0: return False
        edge, beyond = A[y:y + h, x], A[y:y + h, x - 1]
    else:
        if x + w >= W: return False
        edge, beyond = A[y:y + h, x + w - 1], A[y:y + h, x + w]
    return len(edge) >= 12 and longest(edge) >= RUN * len(edge) and beyond.mean() >= 0.4


def shared(a, b):
    ax, ay, aw, ah = a; bx, by, bw, bh = b
    if ax + aw == bx and ay < by + bh and by < ay + ah: return "E"
    if bx + bw == ax and ay < by + bh and by < ay + ah: return "W"
    if ay + ah == by and ax < bx + bw and bx < ax + aw: return "S"
    if by + bh == ay and ax < bx + bw and bx < ax + aw: return "N"
    return None


def seam_is_two_objects(A, RGB, a, b, side):
    """Opaque runs either side do not line up, or the shading does not continue."""
    if side in ("N", "S"):
        top, bot = (a, b) if side == "S" else (b, a)
        x0 = max(top[0], bot[0]); x1 = min(top[0] + top[2], bot[0] + bot[2])
        if x1 - x0 < 12: return True
        ya, yb = top[1] + top[3], bot[1]
        above, below = RGB[ya - 3:ya, x0:x1], RGB[yb:yb + 3, x0:x1]
        oa, ob = A[ya - 3:ya, x0:x1].all(0), A[yb:yb + 3, x0:x1].all(0)
    else:
        left, right = (a, b) if side == "E" else (b, a)
        y0 = max(left[1], right[1]); y1 = min(left[1] + left[3], right[1] + right[3])
        if y1 - y0 < 12: return True
        xa, xb = left[0] + left[2], right[0]
        above = RGB[y0:y1, xa - 3:xa].transpose(1, 0, 2); below = RGB[y0:y1, xb:xb + 3].transpose(1, 0, 2)
        oa, ob = A[y0:y1, xa - 3:xa].all(1), A[y0:y1, xb:xb + 3].all(1)
    both = oa & ob
    if both.sum() < 0.6 * max(oa.sum(), ob.sum(), 1): return True
    return float(np.abs(above.mean(0) - below.mean(0)).mean(-1)[both].mean() / 255.0) > 0.16


def merge_sheet(path, entries, alias, removed, counts):
    rgba = load_rgba(path).astype(np.float32)
    A = rgba[..., 3] >= OPAQUE; RGB = rgba[..., :3]; H, W = A.shape
    boxes = {e["id"]: [int(v) for v in e["region"]] for e in entries}
    ids = list(boxes)

    def inside(inner, outer):
        return (inner[0] >= outer[0] and inner[1] >= outer[1] and inner[0] + inner[2] <= outer[0] + outer[2]
                and inner[1] + inner[3] <= outer[1] + outer[3])

    blobs = {}
    for c in ids:
        parts = [k for k in ids if k != c and inside(boxes[k], boxes[c])]
        if len(parts) >= 2 and sum(boxes[k][2] * boxes[k][3] for k in parts) >= 0.7 * boxes[c][2] * boxes[c][3]:
            blobs[c] = max(parts, key=lambda k: boxes[k][2] * boxes[k][3])
    for c, part in blobs.items():
        while part in blobs: part = blobs[part]
        alias[c] = part
    counts["blobs"] += len(blobs)
    ids = [i for i in ids if i not in blobs]

    parent = {i: i for i in ids}

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i

    def union_box(members):
        x0 = min(boxes[m][0] for m in members); y0 = min(boxes[m][1] for m in members)
        return [x0, y0, max(boxes[m][0] + boxes[m][2] for m in members) - x0,
                max(boxes[m][1] + boxes[m][3] for m in members) - y0]

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = boxes[ids[i]], boxes[ids[j]]
            # trimmed boxes of one object may sit a pixel or two apart
            side = shared([a[0] - 1, a[1] - 1, a[2] + 2, a[3] + 2], [b[0] - 1, b[1] - 1, b[2] + 2, b[3] + 2]) or shared(a, b)
            if side is None or not (continues(A, a, side) and continues(A, b, OPP[side])): continue
            if seam_is_two_objects(A, RGB, a, b, side):
                counts["two_objects"] += 1; continue
            ra, rb = find(ids[i]), find(ids[j])
            if ra == rb: continue
            if max(union_box([k for k in ids if find(k) in (ra, rb)])[2:]) > CAP:
                counts["capped"] += 1; continue
            parent[ra] = rb

    groups = collections.defaultdict(list)
    for i in ids: groups[find(i)].append(i)
    final = {}
    for root, members in groups.items():
        box, grew = union_box(members), False
        others = [boxes[k] for k in ids if find(k) != root]
        for side in "NSWE":
            for _ in range(MAXSTEP):
                if max(box[2], box[3]) >= CAP or not continues(A, box, side): break
                if side == "N": nxt = [box[0], max(0, box[1] - STEP), box[2], box[3] + min(STEP, box[1])]; strip = [nxt[0], nxt[1], nxt[2], box[1] - nxt[1]]
                elif side == "S": nxt = [box[0], box[1], box[2], min(H - box[1], box[3] + STEP)]; strip = [box[0], box[1] + box[3], box[2], nxt[3] - box[3]]
                elif side == "W": nxt = [max(0, box[0] - STEP), box[1], box[2] + min(STEP, box[0]), box[3]]; strip = [nxt[0], nxt[1], box[0] - nxt[0], nxt[3]]
                else: nxt = [box[0], box[1], min(W - box[0], box[2] + STEP), box[3]]; strip = [box[0] + box[2], box[1], nxt[2] - box[2], box[3]]
                if any(o[0] < strip[0] + strip[2] and strip[0] < o[0] + o[2] and o[1] < strip[1] + strip[3] and strip[1] < o[1] + o[3] for o in others):
                    break
                box, grew = nxt, True
        final[root] = (members, box, grew)
    for r in list(final):
        if r not in final: continue
        members, box, grew = final[r]
        for r2 in list(final):
            if r2 != r and r2 in final and inside(final[r2][1], box):
                members = members + final[r2][0]; del final[r2]
        final[r] = (members, box, grew)

    out = []
    by_id = {e["id"]: e for e in entries}
    for members, box, grew in final.values():
        for m in members: alias.pop(m, None)             # a surviving part must not stay aliased
        survivor = max(members, key=lambda i: boxes[i][2] * boxes[i][3])
        if len(members) > 1: counts["merged"] += 1; counts["absorbed"] += len(members) - 1
        if grew: counts["extended"] += 1
        for m in members:
            if m != survivor: alias[m] = survivor
        e = by_id[survivor]
        tight = trim(A, *box)
        if tight is None or e["id"] in removed:           # swept, or its art was blanked
            counts["dropped"] += 1; continue
        out.append(set_geometry(e, A, *tight))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base", help="git revision whose props.json holds the untouched boxes; default is the live registry")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.base:
        props = json.loads(subprocess.run(["git", "show", f"{args.base}:rooms/tileset-library/props.json"],
                                          capture_output=True, cwd=REPO).stdout.decode("utf-8"))
        alias = {}
    else:
        props, alias = load_props(), load_json(LIB / "merged.json", {})
    removed = load_json(LIB / "removed.json", {})
    by = collections.defaultdict(list)
    for e in props: by[sheet_of(e)].append(e)
    counts = collections.Counter(); out = []
    for sheet, entries in by.items():
        out += merge_sheet(REPO / sheet, entries, alias, removed, counts)
    for k in list(alias):
        while alias[k] in alias: alias[k] = alias[alias[k]]
    print(f"{len(props)} -> {len(out)} props | blobs split {counts['blobs']}, objects rejoined {counts['merged']} "
          f"({counts['absorbed']} halves), extended {counts['extended']}, refused: {counts['two_objects']} two objects, "
          f"{counts['capped']} over {CAP}px | dropped {counts['dropped']} swept or empty")
    if args.dry_run:
        same = alias == load_json(LIB / "merged.json", {})
        print(f"dry run: nothing written. Alias map {'matches' if same else 'differs from'} merged.json ({len(alias)} aliases)")
        return
    print("owner marks before remap:"); print_marks()
    save_json(PROPS, out); save_json(LIB / "merged.json", alias, indent=1)
    print("marks remapped:", remap_marks(alias))


if __name__ == "__main__":
    main()
