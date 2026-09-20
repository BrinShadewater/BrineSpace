"""Cut a prop whose objects were drawn touching, where refit.py finds no gap: by eye.

    python tools/tileset_library/cut.py cuts.json [--preview page.png] [--dry-run]

cuts.json says how many objects someone SAW in each prop, never where to cut:

    {"uw1-12": {"cols": 2}, "hs-40": {"rows": 3}, "lab-7": {"cols": 3, "at": [41, 97]},
     "wall-3": {"cols": 2, "rows": 2}}          both: a grid; "at_rows" gives the row lines

For N columns the cut lines are the emptiest columns of art near each N-th of the width
(within a third of a part either way); "at" gives the lines outright, in the prop's own
pixels, when the objects are unequal. Each part is trimmed to its art. The first keeps
the id, so placed copies still resolve; the others get a never-used id (free_id), the
next label number, and "(part N)" on the title until someone names them.

Look at --preview before writing. Undo with `split.py --undo <id>`.
"""
import argparse

import numpy as np
from PIL import Image, ImageDraw

from common import OPAQUE, PROPS, REPO, free_id, load_json, load_props, load_rgba, next_numbers, save_json, set_geometry, sheet_of, trim


def lines(counts, n, at=None):
    if at: return sorted(int(v) for v in at)
    length = len(counts); out = []
    for k in range(1, n):
        target = k * length / float(n); reach = max(2, int(length / float(n) * 0.33))
        lo, hi = max(1, int(target - reach)), min(length - 1, int(target + reach))
        out.append(min(range(lo, hi), key=lambda i: (counts[i], abs(i - target))))
    return out


def cut(spec, dry_run=False, preview=None):
    props = load_props(); by_id = {e["id"]: e for e in props}; added, shots = [], []
    for pid, how in spec.items():
        e = by_id.get(pid)
        if e is None: print(f"   {pid}: not registered"); continue
        A = load_rgba(REPO / sheet_of(e)); mask = A[..., 3] >= OPAQUE
        x, y, w, h = [int(v) for v in e["region"]]
        inner = mask[y:y + h, x:x + w]
        xs = [0] + (lines(inner.sum(0), int(how["cols"]), how.get("at")) if "cols" in how else []) + [w]
        ys = [0] + (lines(inner.sum(1), int(how["rows"]), how.get("at_rows")) if "rows" in how else []) + [h]
        # both given: a grid (a wall of monitors, shelving two wide and two high)
        boxes = [(x + xa, y + ya, xb - xa, yb - ya) for ya, yb in zip(ys, ys[1:]) for xa, xb in zip(xs, xs[1:])]
        parts = [p for p in (trim(mask, *b) for b in boxes) if p is not None and p[2] >= 4 and p[3] >= 4]
        if len(parts) < 2: print(f"   {pid}: nothing to cut"); continue
        title = e.get("title", "")
        for n, part in enumerate(parts):
            target = e
            if n:
                target = dict(e); target["id"] = free_id(pid, by_id); by_id[target["id"]] = target
                kind = e["label"].rpartition(" ")[0]
                target["label"] = f"{kind} {next_numbers(props + added).get(kind, 0) + 1:03d}"
                if title: target["title"] = f"{title} (part {n + 1})"
                added.append(target)
            set_geometry(target, mask, *part)
        print(f"   {pid}: {len(parts)} parts")
        shots.append((A[y:y + h, x:x + w], [(p[0] - x, p[1] - y, p[2], p[3]) for p in parts], pid))
    if preview and shots:
        s = 3; W = 1800; px = py = 10; row = 0; places = []
        for art, parts, pid in shots:
            if px + art.shape[1] * s + 10 > W: px = 10; py += row + 26; row = 0
            places.append((art, parts, pid, px, py)); px += art.shape[1] * s + 14; row = max(row, art.shape[0] * s)
        page = Image.new("RGBA", (W, py + row + 30), (190, 60, 190, 255)); d = ImageDraw.Draw(page)
        for art, parts, pid, ox, oy in places:
            im = Image.fromarray(art, "RGBA"); im = im.resize((im.width * s, im.height * s), Image.NEAREST); page.alpha_composite(im, (ox, oy))
            for bx, by, bw, bh in parts: d.rectangle([ox + bx * s, oy + by * s, ox + (bx + bw) * s - 1, oy + (by + bh) * s - 1], outline=(255, 255, 0, 255))
            d.text((ox, oy + im.height + 2), pid, fill="white")
        page.save(preview)
    if not dry_run: save_json(PROPS, props + added)
    return added


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cuts"); ap.add_argument("--preview"); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    added = cut(load_json(args.cuts), args.dry_run, args.preview)
    print(f"{len(added)} new props" + ("; dry run: nothing written" if args.dry_run else ""))


if __name__ == "__main__":
    main()
