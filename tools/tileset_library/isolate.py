"""Lift a prop out of art it is tangled with, onto its set's own `fixes.png` sheet.

    python tools/tileset_library/isolate.py [--preview page.png] [--dry-run]

Some props cannot be fixed with a rectangle: a robot arm reaches over its neighbour, a
tray sits inside the arm's box, a second claw pokes in from the next prop. The art is
shared, so it cannot be blanked on the vendor's sheet either. Instead the prop's own
pixels are copied to `assets/new-tilesets/<set>/fixes.png` and its registration points
there; the vendor's sheet is not touched.

rooms/tileset-library/isolate.json, chosen by eye on a gridded render:

    {"el-137": {"from": {"source": "res://…/tile-B-03.png", "region": [x, y, w, h]},
                "grow": [0, 14, 0, 0],            left, top, right, bottom: art outside the box
                "drop": [[0, 45, 26, 81]],        rects in the prop's own pixels to erase
                "main": true}}                    then keep only the largest connected piece

`from` is written on the first run and never changed, so every run rebuilds fixes.png
from the vendor's sheets: the same spec always gives the same sheet. Remove an entry,
put `from` back into props.json by hand, and the prop is as it was.
"""
import argparse, collections

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from common import ART, LIB, OPAQUE, PROPS, REPO, RES_ART, load_json, load_props, load_rgba, save_json, save_png_atomic, set_geometry, trim

SPEC = LIB / "isolate.json"
WIDTH = 512
EIGHT = np.ones((3, 3), bool)


def lifted(how):
    x, y, w, h = [int(v) for v in how["from"]["region"]]
    gl, gt, gr, gb = how.get("grow", [0, 0, 0, 0])
    A = load_rgba(REPO / how["from"]["source"].replace("res://", ""))
    x0, y0 = max(0, x - gl), max(0, y - gt)
    art = A[y0:min(A.shape[0], y + h + gb), x0:min(A.shape[1], x + w + gr)].copy()
    for dx0, dy0, dx1, dy1 in how.get("drop", []):            # in the prop's own pixels, before growing
        art[max(0, dy0 + (y - y0)):dy1 + (y - y0), max(0, dx0 + (x - x0)):dx1 + (x - x0)] = 0
    solid = art[..., 3] >= OPAQUE
    if how.get("main") and solid.any():
        labels, n = ndimage.label(solid, structure=EIGHT)
        sizes = ndimage.sum(solid, labels, range(1, n + 1)); big = int(np.argmax(sizes)) + 1
        near = ndimage.binary_dilation(labels == big, EIGHT, iterations=3)
        keep = np.zeros_like(solid)
        for i in range(1, n + 1):
            if i == big or (near & (labels == i)).any(): keep |= labels == i     # a spark, an antenna
        art[~keep] = 0
    box = trim(art[..., 3] >= OPAQUE, 0, 0, art.shape[1], art.shape[0])
    return None if box is None else art[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--preview"); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    spec = load_json(SPEC, {}); props = load_props(); by_id = {e["id"]: e for e in props}
    for pid, how in spec.items():
        if "from" not in how and pid in by_id:
            how["from"] = {"source": by_id[pid]["source"], "region": by_id[pid]["region"]}
    by_set = collections.defaultdict(list)
    for pid, how in spec.items():
        if pid in by_id and "from" in how: by_set[how["from"]["source"].replace(RES_ART, "").split("/")[0]].append(pid)
    shots = []
    for slug, ids in by_set.items():
        arts = [(pid, lifted(spec[pid])) for pid in sorted(ids)]
        arts = [(p, a) for p, a in arts if a is not None]
        x = y = 2; row = 0; places = []
        for pid, a in arts:                                   # shelves, two pixels apart
            if x + a.shape[1] + 2 > WIDTH: x = 2; y += row + 2; row = 0
            places.append((pid, a, x, y)); x += a.shape[1] + 2; row = max(row, a.shape[0])
        sheet = np.zeros((y + row + 2, WIDTH, 4), np.uint8)
        for pid, a, px, py in places: sheet[py:py + a.shape[0], px:px + a.shape[1]] = a
        mask = sheet[..., 3] >= OPAQUE
        for pid, a, px, py in places:
            e = by_id[pid]; e["source"] = f"{RES_ART}{slug}/fixes.png"
            set_geometry(e, mask, *trim(mask, px, py, a.shape[1], a.shape[0]))
            shots.append((pid, spec[pid], a))
            print(f"   {pid:<12} {e.get('title', e['label'])[:40]:<40} {a.shape[1]}x{a.shape[0]}")
        if not args.dry_run: save_png_atomic(ART / slug / "fixes.png", sheet)
    if args.preview and shots:
        cell = 300; cols = 6; rows = (len(shots) + cols - 1) // cols
        page = Image.new("RGBA", (cols * cell, rows * cell * 2), (120, 132, 128, 255)); d = ImageDraw.Draw(page)
        for i, (pid, how, a) in enumerate(shots):
            x, y, w, h = [int(v) for v in how["from"]["region"]]
            before = load_rgba(REPO / how["from"]["source"].replace("res://", ""))[y:y + h, x:x + w]
            for r, arr in ((0, before), (1, a)):
                im = Image.fromarray(arr, "RGBA"); s = min((cell - 20) / im.width, (cell - 30) / im.height, 3.0)
                im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.NEAREST)
                page.alpha_composite(im, ((i % cols) * cell + 10, (i // cols) * cell * 2 + r * cell + 16))
            d.text(((i % cols) * cell + 10, (i // cols) * cell * 2 + 2), pid, fill="white")
        page.save(args.preview)
    if not args.dry_run:
        save_json(SPEC, spec, indent=1); save_json(PROPS, props)
    print("dry run: nothing written" if args.dry_run else f"{len(shots)} props lifted onto fixes sheets")


if __name__ == "__main__":
    main()
