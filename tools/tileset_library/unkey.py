"""Fill the holes a vendor's white chroma key punched into the art.

    python tools/tileset_library/unkey.py --sources "vendor-art/New Tilesets" "vendor-art/Another Pass/extracted" [--dry-run] [--contact out.png]

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

STATUS: NOT SAFE TO RUN LIBRARY-WIDE. Two attempts, both reverted or limited:
  1. Strict enclosure with a near-white rim: correct but timid. It fixed clean props
     (run on Infirmary and Ghost Deck only, 56 props, kept) and missed the worst damage,
     because the key usually ate through the prop's edge and the hole is then open to the
     background, not enclosed.
  2. Closed silhouette plus a looser rim: reached those holes but painted them DARK
     (black blotches on a CT scanner and on pillows), and before the enclosure and
     foliage guards it also filled crater corners and the gaps between kelp fronds.
     Reverted in full.
  3. Flat fill from the bright 40% of the rim: no more black, but the patch is still
     visibly darker than the surface (a grey rectangle for a white pillow), because the
     only pixels left beside a keyed hole are the dark fringe the key left behind. Previewed
     only, never written. The owner's Ghost Deck pillows were still not reached.
Checked against a fresh extraction of the vendor's .rar: the working copies are byte for
byte the archive's files, the holes are in the vendor's art, and the colour under the key
is erased (black), so re-pulling the originals cannot help.
Automatic repair is not converging. For props the owner actually uses, patch by hand:
a region and a colour chosen by eye, per prop.
The detection in (2) is close; the FILL is what is wrong. Bleeding colour inward from
the whole rim drags in keyline and shadow from the far side of the neck. The next
attempt should fill flat with the median of the rim's BRIGHT pixels only, and must be
judged on a rendered before/after of the owner's starred props before it writes.
"""
import argparse, collections

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from common import LUMA, REPO, load_props, load_rgba, save_png_atomic, sheet_of
from tone import match_sources

ENCLOSED = 0.85        # share of a hole's border that must be art
CLOSE = 3              # px the silhouette is closed by: the width of neck the key may have eaten
RIM_BRIGHT = 0.38      # source luminance of the rim; grimy whites sit near 0.40
RIM_SAT = 0.16
RIM_DARK_SHARE = 0.22  # at most this share of the rim may be keyline
MAX_SHARE = 0.45       # a hole this big relative to its prop is a gap, not a highlight


def holes_to_fill(C, O, boxes):
    """Boolean mask of transparent pixels to fill on one sheet.

    "Inside the prop" means inside its closed silhouette, not strictly enclosed: the key
    often ate through a prop's edge, which leaves the hole open to the background through
    a ragged neck, and a strict-enclosure test then refuses the worst damage (the owner's
    Ghost Deck pillows). Closing the silhouette by a few pixels and filling it recovers
    those. The rim test is what still refuses a real gap, which is rimmed by keyline."""
    opaque = C[..., 3] >= 24
    inside = np.zeros(opaque.shape, bool)
    for x, y, w, h in boxes: inside[y:y + h, x:x + w] = True
    yy, xx = np.ogrid[-CLOSE:CLOSE + 1, -CLOSE:CLOSE + 1]
    disk = (xx * xx + yy * yy) <= CLOSE * CLOSE
    padded = np.pad(opaque, CLOSE)
    silhouette = ndimage.binary_fill_holes(ndimage.binary_closing(padded, structure=disk))[CLOSE:-CLOSE, CLOSE:-CLOSE]
    candidates = silhouette & ~opaque & inside
    labels, n = ndimage.label(candidates)
    paint = np.zeros(C.shape[:2] + (3,), np.float32)
    if n == 0: return np.zeros_like(opaque), paint
    src = O[..., :3].astype(np.float32) / 255.0
    lum = src @ LUMA; mx = src.max(-1); sat = np.where(mx > 1e-6, (mx - src.min(-1)) / np.maximum(mx, 1e-6), 0)
    fill = np.zeros_like(opaque)
    for index, sl in enumerate(ndimage.find_objects(labels), 1):
        if sl is None: continue
        ys, xs = sl; pad = (slice(max(0, ys.start - 1), ys.stop + 1), slice(max(0, xs.start - 1), xs.stop + 1))
        region = labels[pad] == index
        border = ndimage.binary_dilation(region) & ~region
        rim = border & opaque[pad]
        if rim.sum() < 4: continue
        # A keyed hole is walled by art nearly all the way round, even when the key ate a
        # narrow neck through the edge. A notch in the silhouette (a crater's corner, the
        # space between coral branches) is open along a whole side; closing alone filled those.
        if rim.sum() < ENCLOSED * border.sum(): continue
        rl = lum[pad][rim]; rs = sat[pad][rim]
        if np.median(rl) < RIM_BRIGHT or np.median(rs) > RIM_SAT or (rl < 0.25).mean() > RIM_DARK_SHARE: continue
        # Flat fill from the BRIGHT part of the rim only. The key ate white surfaces right
        # up to the prop's dark outline, so half of a hole's rim can be keyline; bleeding
        # colour in from the whole rim painted pillows and scanner housings dark. The vendor
        # also erased the colour under the key (it is black), so nothing can be recovered
        # from the file itself: the surface's own surviving pixels are the only evidence.
        bright = rim & (lum[pad] >= np.percentile(rl, 60))
        colour = np.median(C[pad][..., :3][bright].astype(np.float32), axis=0)
        fill[pad] |= region
        paint[pad][region] = colour
    return fill, paint


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
        fill, paint = holes_to_fill(C, O, boxes)
        for e, (x, y, w, h) in zip(entries, boxes):       # a big hole relative to its prop is a gap
            share = fill[y:y + h, x:x + w].sum() / float(max(1, (C[y:y + h, x:x + w, 3] >= 24).sum()))
            if share > MAX_SHARE: fill[y:y + h, x:x + w] = False
            # The gaps between leaves and fronds are real, and well enclosed; leave foliage alone.
            art = O[y:y + h, x:x + w].astype(np.float32); m = art[..., 3] >= 24
            if m.sum():
                r, g, b = art[..., 0][m], art[..., 1][m], art[..., 2][m]
                if e["category"] == "Plants & growing" or ((g > r * 1.08) & (g > b * 1.08)).mean() > 0.30:
                    fill[y:y + h, x:x + w] = False
        if not fill.any(): continue
        before = C.copy()
        C[..., :3] = np.where(fill[..., None], paint, C[..., :3]).clip(0, 255).astype(np.uint8)
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
