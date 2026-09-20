"""Refit props whose box is wrong: art cut off by the box, or several objects in one box.

    python tools/tileset_library/refit.py --starred [--dry-run] [--page before-after.png]
    python tools/tileset_library/refit.py <prop-id> [<prop-id> ...]

The scanner boxed by grid, so some boxes stop halfway down a crystal and others hold two
corals. The owner stars what looks wrong; this looks at the art itself:

  * every connected piece of art that touches the box is given to the prop whose box
    holds most of it, so a neighbour's art is never taken and a piece nobody holds more
    of comes home;
  * pieces a few pixels apart are one object (an antenna, a spark); objects further
    apart are separate props. The first keeps the id, so placed copies still resolve;
    the others get the id plus a letter, as Split does, and "(part N)" on the title so
    they can be found and named;
  * a box that would grow past GROW times its area, or an object still touching its
    neighbour (two bunks drawn side by side), is left alone and listed: someone must
    cut those by eye with split.py or the Studio.

Undo a separation with `split.py --undo <id>`.
"""
import argparse

import numpy as np
from scipy import ndimage

from common import (LIB, OPAQUE, free_id, PREFIX, PROPS, REPO, load_json, load_props, load_rgba, next_numbers, save_json,
                    set_geometry, sheet_of)

GROW = 4.0      # a refit may not grow a box past this many times its area
JOIN = 2        # pieces this close (pixels) are one object; 3 glued two crystals standing base to tip
MAJOR = 0.12    # an object under this share of the largest is a fragment, not a prop
EIGHT = np.ones((3, 3), bool)


def bbox(mask):
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max() - xs.min()) + 1, int(ys.max() - ys.min()) + 1


def plan(entry, mask, labels, boxes):
    """(objects, note): each object a boolean sheet mask; note says why nothing can be done."""
    x, y, w, h = [int(v) for v in entry["region"]]
    touching = [i for i in np.unique(labels[y:y + h, x:x + w]) if i]
    mine = np.zeros(mask.shape, bool)
    for i in touching:
        piece = labels == i
        held = int(piece[y:y + h, x:x + w].sum())
        if held < 6: continue
        rival = max((int(piece[by:by + bh, bx:bx + bw].sum()) for bx, by, bw, bh in boxes), default=0)
        if held >= rival: mine |= piece
    if not mine.any(): return [], "no art of its own"
    groups, n = ndimage.label(ndimage.binary_dilation(mine, EIGHT, iterations=1), structure=EIGHT)   # joins gaps up to JOIN
    sizes = {g: int((mine & (groups == g)).sum()) for g in range(1, n + 1)}
    largest = max(sizes.values())
    def real(g):                                      # big enough to be a prop, not a crumb
        bw, bh = bbox(mine & (groups == g))[2:]
        return sizes[g] >= max(40, MAJOR * largest) and bw >= 6 and bh >= 6
    major = [g for g in sizes if real(g)]
    if not major: return [], "almost no art of its own: a crumb of a neighbour?"
    objects = {g: mine & (groups == g) for g in major}
    for g in sizes:                                   # a fragment goes to the nearest object
        if g in major: continue
        frag = mine & (groups == g); fx, fy, fw, fh = bbox(frag); centre = np.array([fx + fw / 2, fy + fh / 2])
        def gap(m):
            ox, oy, ow, oh = bbox(m)
            return max(ox - centre[0], centre[0] - ox - ow, 0) + max(oy - centre[1], centre[1] - oy - oh, 0)
        near = min(objects, key=lambda k: gap(objects[k]))
        if gap(objects[near]) <= 12: objects[near] |= frag
    out = sorted(objects.values(), key=lambda m: (bbox(m)[1] // 24, bbox(m)[0]))
    for m in out:
        bx, by, bw, bh = bbox(m)
        if bw * bh > GROW * w * h and bw * bh > 4000: return [], "art runs into its neighbours: cut by eye"
    return out, ""


def refit(ids, dry_run=False):
    props = load_props(); by_id = {e["id"]: e for e in props}
    sheets, report = {}, {"refit": [], "separated": [], "unchanged": [], "by-eye": []}
    added = []
    for pid in ids:
        e = by_id.get(pid)
        if e is None: continue
        s = sheet_of(e)
        if s not in sheets:
            m = load_rgba(REPO / s)[..., 3] >= OPAQUE
            sheets[s] = (m, ndimage.label(m, structure=EIGHT)[0])
        mask, labels = sheets[s]
        boxes = [[int(v) for v in o["region"]] for o in props if o["source"] == e["source"] and o is not e]
        objects, note = plan(e, mask, labels, boxes)
        if not objects: report["by-eye"].append((pid, note)); continue
        old = [int(v) for v in e["region"]]
        title = e.get("title", "")
        for n, obj in enumerate(objects):
            target = e
            if n:
                target = dict(e); target["id"] = free_id(pid, by_id); by_id[target["id"]] = target
                kind = e["label"].rpartition(" ")[0]
                target["label"] = f"{kind} {next_numbers(props + added).get(kind, 0) + 1:03d}"
                if title: target["title"] = f"{title} (part {n + 1})"
                added.append(target)
            # geometry from this object's own art, so a neighbour inside the box casts no footprint
            set_geometry(target, obj, *bbox(obj))
        if len(objects) > 1: report["separated"].append((pid, len(objects)))
        elif [int(v) for v in e["region"]] != old: report["refit"].append((pid, old, e["region"]))
        else: report["unchanged"].append(pid)
    if not dry_run:
        save_json(PROPS, props + added)
    return report, added


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ids", nargs="*"); ap.add_argument("--starred", action="store_true", help="everything the owner has starred")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    ids = list(args.ids)
    if args.starred:
        alias = load_json(LIB / "merged.json", {})
        ids += [alias.get(k, k) for k in (i.replace(PREFIX, "") for i in load_json(LIB / "favourites.json", []) if i.startswith(PREFIX))]
    report, added = refit(list(dict.fromkeys(ids)), args.dry_run)
    print(f"refit {len(report['refit'])}, separated {len(report['separated'])} into {len(report['separated']) + len(added)} props, "
          f"already right {len(report['unchanged'])}, needs cutting by eye {len(report['by-eye'])}")
    for pid, note in report["by-eye"]: print(f"   {pid}: {note}")
    if args.dry_run: print("dry run: nothing written")


if __name__ == "__main__":
    main()
