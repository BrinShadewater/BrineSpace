"""Find the props on a converted pack's sheets and draw a numbered sheet to pick from.

    python tools/tileset_library/scan.py "C:/converted/Pack" --code cyb --out scan.json --contact pick.png

Two passes per sheet, a strict one and a gap-tolerant one, because a prop drawn in
separate pieces needs the gap and touching neighbours need it off. Both survive, so
expect a blob *and* its parts for touching objects; merge.py resolves that, not this.

Picking is by eye, from the contact sheet, at prop level. A sheet of mechs also holds
lockers; a pack called "Nuclear Shelter" holds bunks and produce crates. Look.
"""
import argparse, glob, hashlib
from collections import deque

import numpy as np
from PIL import Image, ImageDraw

from common import save_json


def alpha_of(im):
    """Real alpha, or a key from a painted background colour."""
    A = np.asarray(im)
    if A[..., 3].min() <= 250:
        return A[..., 3]
    edge = np.concatenate([A[0, :, :3], A[-1, :, :3], A[:, 0, :3], A[:, -1, :3]])
    bg = np.median(edge, axis=0)
    d = np.abs(A[..., :3].astype(np.int16) - bg).sum(-1)
    return np.where(d > 26, 255, 0).astype(np.uint8)


def tile_size(im):
    for t in (48, 64, 32, 16):
        if im.width % t == 0 and im.height % t == 0 and im.width // t >= 8:
            return t
    return None


def components(mask, min_px, gap):
    m = mask > 24
    pad = m.copy()
    for dy in range(-gap, gap + 1):
        for dx in range(-gap, gap + 1):
            pad |= np.roll(np.roll(m, dy, 0), dx, 1)
    h, w = pad.shape
    seen = np.zeros((h, w), bool)
    out = []
    for sy in range(h):
        for sx in range(w):
            if not pad[sy, sx] or seen[sy, sx]:
                continue
            q = deque([(sy, sx)]); seen[sy, sx] = True; ys, xs = [], []
            while q:
                y, x = q.popleft(); ys.append(y); xs.append(x)
                for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                    if 0 <= ny < h and 0 <= nx < w and pad[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True; q.append((ny, nx))
            y0, y1, x0, x1 = min(ys), max(ys) + 1, min(xs), max(xs) + 1
            if m[y0:y1, x0:x1].sum() >= min_px:
                out.append((x0, y0, x1, y1))
    return out


def scan(root, code):
    root = root.replace("\\", "/").rstrip("/") + "/"
    out, seen = [], set()
    for p in sorted(glob.glob(root + "**/*.png", recursive=True)):
        rel = p.replace("\\", "/").replace(root, "")
        if "Auto-tile" in rel or "Tile_A" in rel:
            continue
        im = Image.open(p).convert("RGBA")
        T = tile_size(im)
        if T is None:
            continue
        mask = alpha_of(im)
        found = components(mask, int(T * T * 0.18), gap=1) + components(mask, int(T * T * 0.18), gap=0)
        boxes = sorted(set(found), key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
        keep = []
        for b in boxes:
            inside = [k for k in keep if k[0] >= b[0] - 2 and k[1] >= b[1] - 2 and k[2] <= b[2] + 2 and k[3] <= b[3] + 2]
            bw, bh = (b[2] - b[0]) // T, (b[3] - b[1]) // T
            # A long container is a merged row of neighbours; a 4x4 machine is built
            # from parts and must survive being made of several components.
            if len(inside) >= 2 and (bw >= 5 or bh >= 5):
                continue
            if len(inside) == 1 and bw < 5 and bh < 5 and (b[2] - b[0]) * (b[3] - b[1]) > 2.4 * max(
                    (k[2] - k[0]) * (k[3] - k[1]) for k in inside):
                continue
            keep.append(b)
        for x0, y0, x1, y1 in keep:
            w, h = round((x1 - x0) / T), round((y1 - y0) / T)
            if not (1 <= w <= 8 and 1 <= h <= 8):
                continue
            cx, cy = round(x0 / T), round(y0 / T)
            if abs(x0 - cx * T) > T // 4 or abs(y0 - cy * T) > T // 4:
                continue
            if (cx + w) * T > im.width or (cy + h) * T > im.height:
                continue
            sub = mask[cy * T:(cy + h) * T, cx * T:(cx + w) * T]
            fill = float((sub > 128).mean())
            if fill < (0.45 if w * h == 1 else 0.11):
                continue
            key = hashlib.md5(np.asarray(im.crop((cx * T, cy * T, (cx + w) * T, (cy + h) * T))).tobytes()).hexdigest()
            if key in seen:
                continue
            seen.add(key)
            out.append(dict(sheet=rel, col=cx, row=cy, w=w, h=h, tile=T, fill=round(fill, 3)))
    out.sort(key=lambda e: (e["sheet"], e["row"], e["col"]))
    for n, e in enumerate(out, 1):
        e["id"] = f"{code}-{n:03d}"
    return out


def contact_sheet(root, items, path, cell=104, cols=12):
    """One numbered cell per prop, grouped by sheet. The number is the index within its sheet."""
    root = root.replace("\\", "/").rstrip("/") + "/"
    by = {}
    for e in items:
        by.setdefault(e["sheet"], []).append(e)
    rows = []
    for sheet in sorted(by):
        rows.append(("H", sheet, len(by[sheet])))
        listed = list(enumerate(by[sheet]))
        rows += [("R", listed[i:i + cols], None) for i in range(0, len(listed), cols)]
    height = sum(26 if r[0] == "H" else cell + 16 for r in rows) + 20
    img = Image.new("RGBA", (cols * cell + 20, height), (22, 28, 34, 255)); d = ImageDraw.Draw(img)
    cache, y = {}, 10
    for kind, payload, n in rows:
        if kind == "H":
            d.text((8, y + 6), f"{payload}  [{n}]", fill=(255, 214, 120, 255)); y += 26; continue
        x = 10
        for index, e in payload:
            if e["sheet"] not in cache:
                cache[e["sheet"]] = Image.open(root + e["sheet"]).convert("RGBA")
            t = e["tile"]
            c = cache[e["sheet"]].crop((e["col"] * t, e["row"] * t, (e["col"] + e["w"]) * t, (e["row"] + e["h"]) * t))
            s = min((cell - 10) / c.width, (cell - 10) / c.height, 1.0)
            c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.NEAREST)
            img.alpha_composite(c, (x + (cell - c.width) // 2, y + (cell - c.height) // 2))
            d.text((x + 3, y + cell), str(index), fill=(150, 220, 255, 255)); x += cell
        y += cell + 16
    img.save(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("converted", help="folder of one converted pack")
    ap.add_argument("--code", required=True, help="short id prefix, unique in the registry (e.g. cyb)")
    ap.add_argument("--out", default="scan.json")
    ap.add_argument("--contact", help="write a numbered contact sheet PNG here")
    args = ap.parse_args()
    items = scan(args.converted, args.code.lower())
    save_json(args.out, items)
    print(f"{len(items)} props on {len({e['sheet'] for e in items})} sheets -> {args.out}")
    if args.contact:
        contact_sheet(args.converted, items, args.contact)
        print(f"contact sheet -> {args.contact}  (numbers are per-sheet indices for the picks file)")


if __name__ == "__main__":
    main()
