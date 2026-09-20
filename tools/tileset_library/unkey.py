"""Fill the holes a vendor's white chroma key punched into the art.

    python tools/tileset_library/unkey.py --sources "C:/New Tilesets" ... [--dry-run] [--contact out.png]

Several packs were keyed against white, so white pillows, bed sheets and highlights went
transparent along with the background. The conversion never touches alpha, so the holes
came through untouched; the owner sees pieces of a prop "keying out" over the floor.

A keyed hole and a real gap look the same to alpha alone. They differ at the rim:
  * a keyed hole is ragged and its rim is near-white with no outline, because the key
    ate into a white surface;
  * a real gap (between bed rails, under a chair, inside a shelf) is rimmed by the dark
    keyline every object in these packs is drawn with.
So a transparent region is filled only when it is enclosed by art, its rim in the SOURCE
is bright and unsaturated, and almost none of the rim is keyline. It is filled with the
rim's own converted colour bled inward, so the patch takes the tone of the surface around
it. Nothing outside a registered prop is touched.
"""
import argparse, collections

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from common import LUMA, REPO, load_props, load_rgba, save_png_atomic, sheet_of
from tone import match_sources

RIM_BRIGHT = 0.62      # source luminance of the rim
RIM_SAT = 0.22
RIM_DARK_SHARE = 0.22  # at most this share of the rim may be keyline
MAX_SHARE = 0.45       # a hole this big relative to its prop is a gap, not a highlight


def holes_to_fill(C, O, boxes):
    """Boolean mask of transparent pixels to fill on one sheet."""
    opaque = C[..., 3] >= 24
    inside = np.zeros(opaque.shape, bool)
    for x, y, w, h in boxes: inside[y:y + h, x:x + w] = True
    labels, n = ndimage.label(~opaque)
    if n == 0: return np.zeros_like(opaque)
    edge = np.zeros_like(opaque); edge[0, :] = edge[-1, :] = edge[:, 0] = edge[:, -1] = True
    outside = set(np.unique(labels[edge & ~opaque])) | set(np.unique(labels[~inside & ~opaque]))
    src = O[..., :3].astype(np.float32) / 255.0
    lum = src @ LUMA; mx = src.max(-1); sat = np.where(mx > 1e-6, (mx - src.min(-1)) / np.maximum(mx, 1e-6), 0)
    fill = np.zeros_like(opaque)
    slices = ndimage.find_objects(labels)
    for index, sl in enumerate(slices, 1):
        if index in outside or sl is None: continue
        ys, xs = sl; pad = (slice(max(0, ys.start - 1), ys.stop + 1), slice(max(0, xs.start - 1), xs.stop + 1))
        region = labels[pad] == index
        rim = ndimage.binary_dilation(region) & ~region & opaque[pad]
        if rim.sum() < 4: continue
        rl = lum[pad][rim]; rs = sat[pad][rim]
        if np.median(rl) < RIM_BRIGHT or np.median(rs) > RIM_SAT or (rl < 0.25).mean() > RIM_DARK_SHARE: continue
        fill[pad] |= region
    return fill


def bleed(rgb, known, target):
    """Carry the rim's colour inward until the target is covered."""
    out = rgb.astype(np.float32).copy(); known = known.copy(); todo = target & ~known
    for _ in range(64):
        if not todo.any(): break
        acc = np.zeros_like(out); cnt = np.zeros(out.shape[:2], np.float32)
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            k = np.roll(np.roll(known, dy, 0), dx, 1).astype(np.float32)
            acc += np.roll(np.roll(out, dy, 0), dx, 1) * k[..., None]; cnt += k
        ready = todo & (cnt > 0)
        out[ready] = acc[ready] / cnt[ready][..., None]
        known |= ready; todo &= ~ready
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sources", nargs="+", required=True)
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--contact")
    ap.add_argument("--only", nargs="+", help="set folders under assets/new-tilesets/ to limit the repair to")
    args = ap.parse_args()
    props = load_props(); by = collections.defaultdict(list)
    for e in props:
        if not args.only or sheet_of(e).split("/")[2] in args.only: by[sheet_of(e)].append(e)
    found, missing = match_sources(sorted(by), args.sources)
    per_set = collections.Counter(); touched_props = 0; pixels = 0; sheets = 0; examples = []
    for sheet, entries in sorted(by.items()):
        if sheet not in found: continue
        C = load_rgba(REPO / sheet).copy(); O = load_rgba(found[sheet])
        if O.shape != C.shape: continue
        boxes = [[int(v) for v in e["region"]] for e in entries]
        fill = holes_to_fill(C, O, boxes)
        for e, (x, y, w, h) in zip(entries, boxes):       # a big hole relative to its prop is a gap
            share = fill[y:y + h, x:x + w].sum() / float(max(1, (C[y:y + h, x:x + w, 3] >= 24).sum()))
            if share > MAX_SHARE: fill[y:y + h, x:x + w] = False
        if not fill.any(): continue
        before = C.copy()
        C[..., :3] = np.where(fill[..., None], bleed(C[..., :3], C[..., 3] >= 24, fill), C[..., :3]).clip(0, 255).astype(np.uint8)
        C[..., 3] = np.where(fill, 255, C[..., 3])
        sheets += 1; pixels += int(fill.sum())
        for e, (x, y, w, h) in zip(entries, boxes):
            n = int(fill[y:y + h, x:x + w].sum())
            if n:
                touched_props += 1; per_set[e["tileset"]] += 1
                if n > 120 and len(examples) < 14: examples.append((e, before[y:y + h, x:x + w], C[y:y + h, x:x + w]))
        if not args.dry_run: save_png_atomic(REPO / sheet, C)
    print(f"{'would fill' if args.dry_run else 'filled'} {pixels} keyed-out pixels in {touched_props} props on {sheets} sheets")
    for name, n in per_set.most_common(10): print(f"   {n:>4}  {name}")
    if args.contact and examples:
        cell = 170; img = Image.new("RGBA", (len(examples) * cell + 20, 2 * cell + 50), (230, 40, 200, 255)); d = ImageDraw.Draw(img)
        d.text((8, 4), "over magenta - top: before   bottom: after", fill=(255, 255, 255, 255))
        for i, (e, a, b) in enumerate(examples):
            for row, arr in ((0, a), (1, b)):
                im = Image.fromarray(arr, "RGBA"); s = min((cell - 10) / im.width, (cell - 10) / im.height, 3.0)
                im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.NEAREST)
                img.alpha_composite(im, (10 + i * cell + (cell - im.width) // 2, 20 + row * cell + (cell - im.height) // 2))
            d.text((12 + i * cell, 2 * cell + 26), (e.get("title") or e["label"])[:24], fill=(255, 255, 255, 255))
        img.save(args.contact)


if __name__ == "__main__":
    main()
