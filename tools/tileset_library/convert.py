"""Convert a bought art pack toward the station's look.

    python tools/tileset_library/convert.py "C:/path/to/pack" "C:/path/to/converted/Pack"

Measured against the owner's directional prop banks the packs were twice as bright
and carried three times the edge energy: hard keylines and pixel noise are the tell.
Every step is per-pixel or a small local filter. Nothing moves, nothing resamples and
alpha is never changed, so the tile grid survives and a converted sheet can always be
matched back to its source by alpha.

Prop sheets get the full pass. Floor (Tile_A2) and wall (Auto-tile) sheets are
converted block by block without the tone curve: a whole-sheet mean crushes a pale
floor to near black.

The conversion lands props under the owner's own art; tone.py measures and repairs that.
"""
import argparse, glob, os, time

import numpy as np
from PIL import Image, ImageFilter

TILE = 48


def _dilate_colour(rgb, a, iters=3):
    """Bleed opaque colour into transparent pixels so local filters near a
    silhouette do not drag the void in and leave a dark halo."""
    out = rgb.astype(np.float32).copy()
    known = a > 8
    for _ in range(iters):
        if known.all():
            break
        s = np.zeros_like(out); n = np.zeros(out.shape[:2], np.float32)
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)):
            sh = np.roll(np.roll(out, dy, 0), dx, 1)
            km = np.roll(np.roll(known, dy, 0), dx, 1).astype(np.float32)
            s += sh * km[..., None]; n += km
        fill = (n > 0) & ~known
        out[fill] = (s[fill] / n[fill][..., None])
        known = known | fill
    return out


def deline(rgb, strength=0.75, radius=2):
    """Lift hard dark keylines toward their surrounding surface colour."""
    im = Image.fromarray(rgb.clip(0, 255).astype(np.uint8))
    med = np.asarray(im.filter(ImageFilter.MedianFilter(radius * 2 + 1)), np.float32)
    lum = rgb @ (0.299, 0.587, 0.114)
    mlum = med @ (0.299, 0.587, 0.114)
    line = np.clip((mlum - lum) / 46.0, 0, 1) ** 0.8
    w = (line * strength)[..., None]
    return rgb * (1 - w) + med * w


def smooth(rgb, amount=0.42, radius=1):
    """Take the speckle out without blurring shapes."""
    im = Image.fromarray(rgb.clip(0, 255).astype(np.uint8))
    med = np.asarray(im.filter(ImageFilter.MedianFilter(radius * 2 + 1)), np.float32)
    return rgb * (1 - amount) + med * amount


def dull_highlights(rgb, knee=0.72, amount=0.72):
    """Flatten specular whites so metal reads as painted steel, not chrome."""
    v = rgb.max(-1) / 255.0
    over = np.clip((v - knee) / max(1e-6, 1 - knee), 0, 1)[..., None]
    return rgb * (1 - amount * over) + (rgb * knee / np.maximum(v[..., None], 1e-6)) * (amount * over)


def tone(rgb, a, target_mean, lo=0.35, hi=4.0, mode="gamma"):
    """Darken by solving a gamma on the value channel for the wanted mean.
    Channels scale together, so hue and saturation are left alone."""
    v = rgb.max(-1) / 255.0
    k = a > 200
    if k.sum() < 50:
        return rgb
    cur = v[k]
    if mode == "scale":
        # A near-white floor needs a gamma around 13 to reach the target, which
        # crushes its panel detail; scaling reads as lower light instead.
        return rgb * min(1.0, target_mean / max(1e-4, cur.mean()))
    for _ in range(40):
        g = (lo + hi) / 2
        if (cur ** g).mean() > target_mean: lo = g
        else: hi = g
    g = (lo + hi) / 2
    scale = np.where(v > 1e-4, (v ** g) / np.maximum(v, 1e-4), 0.0)[..., None]
    return rgb * scale


def convert(img, brightness=0.281, line=0.45, soft=0.22, gloss=0.72, mode="gamma"):
    """Full pass. Returns RGBA with the original alpha. brightness=None skips the tone curve."""
    src = img.convert("RGBA")
    a = np.asarray(src)[..., 3]
    rgb = _dilate_colour(np.asarray(src)[..., :3], a)
    if brightness is not None:
        rgb = tone(rgb, a, brightness, mode=mode)
    rgb = deline(rgb, line)
    rgb = smooth(rgb, soft)
    rgb = dull_highlights(rgb, amount=gloss)
    out = np.dstack([rgb.clip(0, 255).astype(np.uint8), a])
    out[..., 3] = a                                        # alpha never changes
    return Image.fromarray(out, "RGBA")


def convert_plant(img):
    """Foliage converted once, from the untouched source, with a gentler profile.
    Darkening and then brightening the greens back was two passes over the same
    pixels and it showed: blown highlights, no mid tones."""
    return convert(img, brightness=0.40, line=0.28, soft=0.12, gloss=0.45)


def _surface(tile):
    return convert(tile, brightness=0.33, line=0.30, soft=0.16, mode="scale")


def a2_sheet(im):
    """Floor autotiles: 2x3 blocks, converted per 48px tile as the renderer extracts them."""
    out = im.copy()
    for by in range(im.height // (TILE * 3)):
        for bx in range(im.width // (TILE * 2)):
            x, y = bx * TILE * 2, by * TILE * 3
            for ty in range(3):
                for tx in range(2):
                    box = (x + tx * TILE, y + ty * TILE, x + (tx + 1) * TILE, y + (ty + 1) * TILE)
                    out.paste(_surface(im.crop(box)), box[:2])
    return out


def a4_sheet(im):
    """Wall autotiles: alternating 2x3 wall-top and 2x2 wall-side bands, 8 blocks across."""
    out = im.copy()
    cols = im.width // (TILE * 2)
    y = 0
    while y < im.height:
        for h in (TILE * 3, TILE * 2):
            if y + h > im.height:
                break
            for bx in range(cols):
                box = (bx * TILE * 2, y, bx * TILE * 2 + TILE * 2, y + h)
                out.paste(_surface(im.crop(box)), box[:2])
            y += h
    return out


def convert_sheet(path):
    im = Image.open(path).convert("RGBA")
    name = os.path.basename(path)
    if "Tile_A2" in name:
        return a2_sheet(im)
    if "Auto-tile" in name:
        return a4_sheet(im)
    return convert(im)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("source", help="folder of the untouched pack")
    ap.add_argument("destination", help="folder to write converted sheets into")
    args = ap.parse_args()
    src = args.source.replace("\\", "/").rstrip("/") + "/"
    dst = args.destination.replace("\\", "/").rstrip("/") + "/"
    paths = sorted(glob.glob(src + "**/*.png", recursive=True))
    t0 = time.time()
    for p in paths:
        rel = p.replace("\\", "/").replace(src, "")
        os.makedirs(os.path.dirname(dst + rel) or dst, exist_ok=True)
        convert_sheet(p).save(dst + rel)
    print(f"converted {len(paths)} sheets in {time.time() - t0:.0f}s -> {dst}")


if __name__ == "__main__":
    main()
