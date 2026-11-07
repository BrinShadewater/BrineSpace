"""Group look-alike props so the Studio tray can show one tile per family.

    python tools/tileset_library/variants.py [--dry-run] [--contact groups.png]

The packs ship the same rack with different guns on it, the same porthole with a
different view, the same monitor with a different screen. They are variants, not
duplicates: only four props in ten thousand were pixel-identical. Never delete them;
group them, so the tray shows one and the owner opens the family when they want it.

A family is props from one set, the same size to within two pixels, whose thumbnails
differ by less than THRESHOLD. Each prop is compared with a family's first member only:
comparing with any member chains unrelated props together through a run of neighbours
(an earlier pass grew a "family" of 262 that way).

Writes rooms/tileset-library/variants.json: {"groups": [[id, id, ...], ...]}.
sweep.py and merge.py keep it free of ids that no longer exist.
"""
import argparse, collections

import numpy as np
from PIL import Image, ImageDraw

from common import LIB, load_props, save_json, sheet_of

THRESHOLD = 0.035
SIDE = 12


def feature(crop):
    t = np.asarray(crop.resize((SIDE, SIDE), Image.BILINEAR), np.float32) / 255.0
    a = t[..., 3:]
    return np.concatenate([(t[..., :3] * a).ravel(), a.ravel()])


def families(props):
    by_sheet = collections.defaultdict(list)
    for e in props: by_sheet[sheet_of(e)].append(e)
    feats, crops = {}, {}
    for sheet, entries in by_sheet.items():
        im = Image.open(sheet).convert("RGBA")
        for e in entries:
            x, y, w, h = [int(v) for v in e["region"]]
            crops[e["id"]] = im.crop((x, y, x + w, y + h)); feats[e["id"]] = feature(crops[e["id"]])
    groups = []                                   # [set, w, h, first feature, [ids]]
    for e in sorted(props, key=lambda e: (e["tileset"], e["id"])):
        w, h = int(e["region"][2]), int(e["region"][3])
        for g in groups:
            if g[0] == e["tileset"] and abs(g[1] - w) <= 2 and abs(g[2] - h) <= 2 and float(np.abs(g[3] - feats[e["id"]]).mean()) < THRESHOLD:
                g[4].append(e["id"]); break
        else:
            groups.append([e["tileset"], w, h, feats[e["id"]], [e["id"]]])
    return [g[4] for g in groups if len(g[4]) > 1], crops


def contact(groups, crops, props, path, rows=24, cols=10, cell=92):
    by_id = {e["id"]: e for e in props}
    shown = sorted(groups, key=len, reverse=True)[:rows]
    img = Image.new("RGBA", (cols * cell + 20, len(shown) * (cell + 16) + 30), (150, 160, 150, 255)); d = ImageDraw.Draw(img)
    d.text((8, 6), "largest families, one per row (first ten members)", fill=(20, 20, 20, 255))
    for r, g in enumerate(shown):
        for c, pid in enumerate(g[:cols]):
            im = crops[pid]; s = min((cell - 8) / im.width, (cell - 8) / im.height, 2.0)
            im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.NEAREST)
            img.alpha_composite(im, (10 + c * cell + (cell - im.width) // 2, 26 + r * (cell + 16) + (cell - im.height) // 2))
        d.text((12, 26 + r * (cell + 16) + cell), f"{len(g)} × {by_id[g[0]]['tileset']} · {by_id[g[0]].get('title') or by_id[g[0]]['label']}", fill=(20, 20, 20, 255))
    img.save(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--contact")
    args = ap.parse_args()
    props = load_props()
    groups, crops = families(props)
    folded = sum(len(g) - 1 for g in groups)
    sizes = collections.Counter(min(len(g), 10) for g in groups)
    print(f"{len(groups)} families fold {folded} of {len(props)} props out of the tray ({100 * folded / len(props):.0f}%); "
          f"largest {max(len(g) for g in groups)}; by size (10 = ten or more): {dict(sorted(sizes.items()))}")
    if args.contact: contact(groups, crops, props, args.contact)
    if not args.dry_run: save_json(LIB / "variants.json", {"groups": groups}, indent=None)


if __name__ == "__main__":
    main()
