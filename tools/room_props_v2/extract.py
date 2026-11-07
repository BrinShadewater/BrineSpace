"""Cut individual props out of the Codex room design sheets.

Each design is a 1254 px top-down room: a metal wall frame around an 8x8 floor
grid with props standing on it. The floor repeats, so the median of its 64
tiles is a clean floor. Anything that differs from that floor (allowing a few
pixels of drift, because the painted grid is not perfectly regular) is a prop.

    python tools/room_props_v2/extract.py --designs "<design folder>" --out <dir>

Writes <out>/<sheet>/<n>.png cutouts, <out>/props.json and a contact sheet per
design. tools/room_props_v2/overrides.json can reject, merge or re-box cuts.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

# Floor area inside the wall frame, in design pixels. Most sheets share this
# frame; interior() measures each sheet because a few are painted smaller.
INTERIOR = (95, 85, 1160, 1145)
GRID = 8
WALL_SHARE = 0.0415  # wall frame thickness / frame size, measured on galley
DRIFT = 5  # painted tiles wander by a few pixels
THRESHOLD = 55.0  # summed RGB difference that counts as "not floor"
SOFT = 25.0  # alpha ramps in over this much difference above the threshold
MIN_AREA_TILES = 0.30
MIN_SIDE_TILES = 0.30
RIVET_AREA = 150  # raw pieces smaller than this are floor rivets, not prop
MARGIN = 3
SKIP = {"corridor", "corner", "tee_corridor"}
THEMES = {
    "Operations": "operations",
    "Engineering": "engineering",
    "Science": "science",
    "Life Support": "life_support",
    "Recreation": "recreation",
    "Anomaly": "anomaly",
}


def interior(rgba):
    """Every sheet sits on a transparent (or black) margin; the wall frame is the
    opaque square inside it and its thickness is a steady share of its size."""
    solid = (rgba[..., 3] > 200) & (rgba[..., :3].astype(np.int32).sum(axis=2) > 45)
    xs = np.where(solid.mean(axis=0) > 0.5)[0]
    ys = np.where(solid.mean(axis=1) > 0.5)[0]
    ix = round(WALL_SHARE * (xs[-1] - xs[0]))
    iy = round(WALL_SHARE * (ys[-1] - ys[0]))
    return (int(xs[0] + ix), int(ys[0] + iy), int(xs[-1] - ix), int(ys[-1] - iy))


def clean_floor(rgb):
    x0, y0, x1, y1 = INTERIOR
    pw, ph = (x1 - x0) / GRID, (y1 - y0) / GRID
    tw, th = int(round(pw)), int(round(ph))
    tiles = []
    for gy in range(GRID):
        for gx in range(GRID):
            box = (int(round(x0 + gx * pw)), int(round(y0 + gy * ph)),
                   int(round(x0 + (gx + 1) * pw)), int(round(y0 + (gy + 1) * ph)))
            tile = Image.fromarray(rgb[box[1]:box[3], box[0]:box[2]]).resize((tw, th), Image.BILINEAR)
            tiles.append(np.asarray(tile, dtype=np.float32))
    median = np.median(np.stack(tiles), axis=0).astype(np.uint8)
    floor = np.zeros_like(rgb, dtype=np.float32)
    for gy in range(GRID):
        for gx in range(GRID):
            box = (int(round(x0 + gx * pw)), int(round(y0 + gy * ph)),
                   int(round(x0 + (gx + 1) * pw)), int(round(y0 + (gy + 1) * ph)))
            tile = Image.fromarray(median).resize((box[2] - box[0], box[3] - box[1]), Image.BILINEAR)
            floor[box[1]:box[3], box[0]:box[2]] = np.asarray(tile, dtype=np.float32)
    return floor, (pw + ph) / 2.0


def difference(rgb, floor):
    x0, y0, x1, y1 = INTERIOR
    img = rgb[y0:y1, x0:x1].astype(np.float32)
    ref = np.pad(floor[y0:y1, x0:x1], ((DRIFT, DRIFT), (DRIFT, DRIFT), (0, 0)), mode="edge")
    h, w = img.shape[:2]
    best = np.full((h, w), np.inf, dtype=np.float32)
    for dy in range(0, 2 * DRIFT + 1):
        for dx in range(0, 2 * DRIFT + 1):
            d = np.abs(img - ref[dy:dy + h, dx:dx + w]).sum(axis=2)
            np.minimum(best, d, out=best)
    full = np.zeros(rgb.shape[:2], dtype=np.float32)
    full[y0:y1, x0:x1] = best
    return full


def is_floor_detail(rgb, floor, region, sl):
    """Vent grilles and hatch outlines are darker than the floor, never brighter."""
    pix = rgb[sl][region].astype(np.float32)
    base = float(np.median(floor[sl][region].mean(axis=1)))
    grey = np.percentile(pix.max(axis=1) - pix.min(axis=1), 98) < 40
    return grey and np.percentile(pix.mean(axis=1), 90) < base + 20


def components(diff, pitch, rgb, floor):
    mask = diff > THRESHOLD
    mask = ndimage.binary_opening(mask, iterations=2)
    mask = ndimage.binary_closing(mask, iterations=6)
    mask = ndimage.binary_fill_holes(mask)
    labels, count = ndimage.label(mask)
    found = []
    for index, sl in enumerate(ndimage.find_objects(labels), start=1):
        if sl is None:
            continue
        region = labels[sl] == index
        area = int(region.sum())
        h, w = region.shape
        if area < MIN_AREA_TILES * pitch * pitch or min(w, h) < MIN_SIDE_TILES * pitch:
            continue
        if area < pitch * pitch and is_floor_detail(rgb, floor, region, sl):
            continue
        found.append({"box": [sl[1].start, sl[0].start, sl[1].stop, sl[0].stop], "label": index})
    return labels, found


def cut(rgba, diff, labels, item):
    x0, y0, x1, y1 = item["box"]
    margin = MARGIN if item["label"] is not None else 0
    x0, y0 = max(0, x0 - margin), max(0, y0 - margin)
    x1, y1 = min(rgba.shape[1], x1 + margin), min(rgba.shape[0], y1 + margin)
    window = labels[y0:y1, x0:x1]
    if item.get("solid"):
        inside = np.ones(window.shape, dtype=bool)  # prop fills its hand-drawn box
    elif item["label"] is None:
        inside = ndimage.binary_fill_holes(window > 0)
    else:
        inside = window == item["label"]
    near = ndimage.binary_dilation(inside, iterations=MARGIN)
    ramp = np.clip((diff[y0:y1, x0:x1] - THRESHOLD * 0.6) / SOFT, 0.0, 1.0)
    alpha = np.where(inside, 1.0, np.where(near, ramp, 0.0))
    alpha = ndimage.gaussian_filter(alpha, 0.6) * near
    # Floor rivets beside the prop survive as small detached dots; drop them.
    islands, count = ndimage.label(alpha > 0.05)
    if count > 1:
        sizes = np.bincount(islands.ravel())
        sizes[0] = 0
        alpha[(sizes[islands] < RIVET_AREA) & (islands != sizes.argmax())] = 0.0
    out = rgba[y0:y1, x0:x1].copy()
    out[..., 3] = (alpha * 255).astype(np.uint8)
    return out, [x0, y0, x1, y1]


def wall_contact(box, pitch):
    x0, y0, x1, y1 = INTERIOR
    reach = pitch * 0.45
    sides = []
    if box[1] - y0 < reach: sides.append("north")
    if y1 - box[3] < reach: sides.append("south")
    if box[0] - x0 < reach: sides.append("west")
    if x1 - box[2] < reach: sides.append("east")
    return sides


def sheets(designs):
    for path in sorted(designs.glob("*.png")):
        if path.stem not in SKIP:
            yield path, path.stem, None
    for folder, theme in THEMES.items():
        for path in sorted((designs / folder).glob("*.png")):
            number = "".join(ch for ch in path.stem if ch.isdigit()) or "1"
            yield path, "%s-extra%s" % (theme, number), theme


def checker(size, cell=12):
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    c = (((xx // cell) + (yy // cell)) % 2) * 40 + 70
    return Image.fromarray(np.dstack([c, c, c + 10]).astype(np.uint8)).convert("RGBA")


def contact_sheet(src, cutouts, path):
    thumb = 150
    rows = max(1, (len(cutouts) + 3) // 4)
    sheet = Image.new("RGBA", (627 + 4 * (thumb + 10) + 10, max(627, rows * (thumb + 28) + 10)), (24, 28, 32, 255))
    preview = src.convert("RGBA").resize((627, 627))
    draw = ImageDraw.Draw(preview)
    for n, (_, box, _) in enumerate(cutouts, start=1):
        b = [v / 2 for v in box]
        draw.rectangle(b, outline=(255, 90, 60, 255), width=2)
        draw.text((b[0] + 3, b[1] + 2), str(n), fill=(255, 255, 0, 255))
    sheet.alpha_composite(preview, (0, 0))
    sd = ImageDraw.Draw(sheet)
    for n, (img, _, name) in enumerate(cutouts):
        cx, cy = 637 + (n % 4) * (thumb + 10), 10 + (n // 4) * (thumb + 28)
        im = Image.fromarray(img)
        im.thumbnail((thumb, thumb))
        tile = checker((thumb, thumb))
        tile.alpha_composite(im, ((thumb - im.width) // 2, (thumb - im.height) // 2))
        sheet.alpha_composite(tile, (cx, cy))
        sd.text((cx, cy + thumb + 4), name, fill=(230, 230, 230, 255))
    sheet.convert("RGB").save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--designs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    designs, out = Path(args.designs), Path(args.out)
    overrides_path = Path(__file__).with_name("overrides.json")
    overrides = json.loads(overrides_path.read_text()) if overrides_path.exists() else {}
    only = {s for s in args.only.split(",") if s}
    records = []
    for path, sheet, theme in sheets(designs):
        if only and sheet not in only:
            continue
        src = Image.open(path)
        rgba = np.asarray(src.convert("RGBA")).copy()
        rgb = rgba[..., :3]
        global INTERIOR
        INTERIOR = interior(rgba)
        floor, pitch = clean_floor(rgb)
        diff = difference(rgb, floor)
        labels, found = components(diff, pitch, rgb, floor)
        found.sort(key=lambda f: (round(f["box"][1] / pitch), f["box"][0]))
        rule = overrides.get(sheet, {})
        reject = set(rule.get("reject", []))
        # Hand-drawn boxes (design pixels) trim a cut that dragged in floor
        # piping, or split props that touch in the painting.
        for n, box in rule.get("rebox", {}).items():
            found[int(n) - 1] = {"box": box, "label": None}
        for box in rule.get("add", []):
            found.append({"box": box, "label": None})
        for n in rule.get("solid", []):
            found[int(n) - 1]["solid"] = True
        (out / sheet).mkdir(parents=True, exist_ok=True)
        cutouts = []
        for n, item in enumerate(found, start=1):
            if n in reject:
                continue
            img, box = cut(rgba, diff, labels, item)
            name = "%s-%d" % (sheet, n)
            Image.fromarray(img).save(out / sheet / ("%d.png" % n))
            cutouts.append((img, box, name))
            records.append({
                "id": name,
                "sheet": sheet,
                "design": str(path.relative_to(designs)).replace("\\", "/"),
                "theme": theme,
                "room": None if theme else sheet,
                "box": box,
                "anchor": [(box[0] + box[2]) / 2.0, float(box[3])],
                "size": [box[2] - box[0], box[3] - box[1]],
                "pitch": pitch,
                "walls": wall_contact(box, pitch),
                "interior": list(INTERIOR),
            })
        contact_sheet(src, cutouts, out / ("%s.contact.png" % sheet))
        print("%-28s %d props  interior %s" % (sheet, len(cutouts), INTERIOR))
    (out / "props.json").write_text(json.dumps(records, indent=1))
    print("total", len(records))


if __name__ == "__main__":
    main()
