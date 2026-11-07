"""Hand-patch the holes a vendor's white key left in props the owner actually uses.

    python tools/tileset_library/patch_holes.py --sources "vendor-art/New Tilesets" "vendor-art/Another Pass/extracted" [--preview out.png] [--dry-run]

Automatic repair (unkey.py) did not converge: the colour under the key is erased in the
vendor's own files, and the pixels left beside a hole are its dark fringe. So the regions
here were chosen by eye on an enlarged, gridded render of each prop, and live in
rooms/tileset-library/hole-patches.json:

    {"h22-01": [{"rect": [30, 2, 156, 56], "mode": "enclosed", "seal": 2, "sample": [42, 60, 52, 120]}]}

rect and sample are [x0, y0, x1, y1] in the prop's own pixels. A patch fills the pixels
that are transparent in the SOURCE inside rect, so a re-run changes nothing and an
earlier bad fill is painted over.
  mode "all"       every such pixel in rect: for a rect that lies wholly inside the prop.
  "ellipse"        [cx, cy, rx, ry] limits an "all" patch to a round silhouette (a scanner housing)
                   when the hole runs off the rect and cannot be shown to be enclosed.
  mode "enclosed"  only those not reachable from the rect's border through transparency,
                   after sealing outline gaps by `seal` px: for a rect that also holds
                   background. `max` caps a hole's size, so a see-through opening stays.
The colour is the median of the brightest third of the opaque pixels in `sample` (default:
rect), which is the surface's own surviving colour rather than the fringe; or "colour".
  "keyed": 0.6     with "enclosed": only holes ringed by light pixels in the source, which is
                   what a white key leaves; an opening ringed by dark outline is left open.
                   `--suggest-starred` writes such a patch for every starred prop it would change.
  {"origin": [x, y]} records where the prop's box began when its rects were chosen, so a
                   later refit of the box does not slide the patches.
  {"solid": [x0, y0, x1, y1]} makes half-transparent pixels opaque; {"lift": rect, "gamma": 0.6,
  "below": 0.22} brightens near-black pixels (soil) from the source.
  {"whiten": [x0, y0, x1, y1], "to": 0.8} then lifts a white surface (pillow, sheet) as a
  whole, because the conversion turns whites grey. Put it after that surface's patches.
"""
import argparse, collections

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from common import LIB, LUMA, REPO, load_json, load_props, load_rgba, save_png_atomic, sheet_of
from tone import match_sources


def surface_colour(C, box, O=None):
    x0, y0, x1, y1 = box
    px = C[y0:y1, x0:x1].reshape(-1, 4).astype(np.float32)
    # Only pixels that survive in the SOURCE: sampling an earlier run's fill beside the
    # hole made one sheet drift on every run.
    px = px[(px[:, 3] >= 200) & ((O[y0:y1, x0:x1, 3].reshape(-1) >= 200) if O is not None else True)]
    if len(px) < 6: return None
    lum = (px[:, :3] / 255.0) @ LUMA
    return np.median(px[lum >= np.percentile(lum, 67)][:, :3], axis=0)


def apply(C, O, region, patches):
    """C, O: the prop's crops (converted, source). Returns pixels filled."""
    filled = 0
    for p in patches:
        if "origin" in p: continue
        if "solid" in p:
            # Soft key: pixels the key left half transparent read as a ragged rim or a see-through
            # patch. Inside a rect chosen by eye they become fully opaque, colour unchanged.
            x0, y0, x1, y1 = p["solid"]; sub = C[y0:y1, x0:x1]
            sub[..., 3] = np.where(sub[..., 3] >= 40, 255, sub[..., 3]); continue
        if "fill" in p:
            # Holes the SOURCE does not show (an earlier pass made them): whatever is still
            # transparent on the sheet inside a rect that lies wholly within the prop.
            x0, y0, x1, y1 = p["fill"]; sub = C[y0:y1, x0:x1]; gap = sub[..., 3] < 200
            if "ellipse" in p:
                cx, cy, rx, ry = p["ellipse"]; yy, xx = np.mgrid[y0:y1, x0:x1]
                gap &= ((xx - cx) / float(rx)) ** 2 + ((yy - cy) / float(ry)) ** 2 <= 1.0
            sub[gap, :3] = np.array(p["colour"], np.uint8); sub[gap, 3] = 255; filled += int(gap.sum()); continue
        if "lift" in p:
            # Soil drawn near black vanishes after the conversion. Lift only the darkest pixels,
            # from the SOURCE, by a gamma that cannot clip.
            x0, y0, x1, y1 = p["lift"]; sub = C[y0:y1, x0:x1]; src = O[y0:y1, x0:x1].astype(np.float32)
            lum = (src[..., :3] / 255.0) @ LUMA; dark = (src[..., 3] >= 128) & (lum < float(p.get("below", 0.22)))
            sub[dark, :3] = (((src[dark, :3] / 255.0) ** float(p.get("gamma", 0.6))) * 255.0 * 0.52).clip(0, 255).astype(np.uint8); continue
        if "whiten" in p:
            # A white surface came out of the conversion grey, like everything else, and a
            # patch matched to it is grey too. Lift the surface as a whole (its surviving
            # pixels and its patches together, so they still match) until its median
            # reaches `to`. Only bright, unsaturated pixels: the outline and the blue sheet stay.
            x0, y0, x1, y1 = p["whiten"]
            # A pure function of the SOURCE, so a re-run cannot drift. Two earlier versions
            # read the sheet being edited: one recruited the pixels the last run had
            # brightened, the other had the patches and the lift chasing each other.
            sub = C[y0:y1, x0:x1]; src = O[y0:y1, x0:x1].astype(np.float32); srgb = src[..., :3]
            slum = (srgb / 255.0) @ LUMA; smx = srgb.max(-1); ssat = np.where(smx > 1, (smx - srgb.min(-1)) / np.maximum(smx, 1), 0)
            white = (src[..., 3] >= 128) & (slum >= 0.55) & (ssat <= 0.20)
            if white.sum() < 6: continue
            k = float(p.get("to", 0.80)) / float(np.median(slum[white]))
            sub[white, :3] = (srgb[white] * k).clip(0, 255).astype(np.uint8)
            holes = (src[..., 3] < 128) & (sub[..., 3] >= 200)          # what the patches filled
            bright = white & (slum >= np.percentile(slum[white], 67))
            sub[holes, :3] = (np.median(srgb[bright], axis=0) * k).clip(0, 255).astype(np.uint8)
            continue
        x0, y0, x1, y1 = p["rect"]
        hole = O[y0:y1, x0:x1, 3] < 128
        if "ellipse" in p:                       # [cx, cy, rx, ry]: keep to a round housing's silhouette
            cx, cy, rx, ry = p["ellipse"]
            yy, xx = np.mgrid[y0:y1, x0:x1]
            hole &= ((xx - cx) / float(rx)) ** 2 + ((yy - cy) / float(ry)) ** 2 <= 1.0
        if p.get("mode", "all") == "enclosed":
            solid = ~hole
            seal = int(p.get("seal", 1))
            if seal: solid = ndimage.binary_closing(np.pad(solid, seal), iterations=seal)[seal:-seal, seal:-seal] | solid
            labels, n = ndimage.label(~solid)
            edge = np.zeros_like(hole); edge[0, :] = edge[-1, :] = edge[:, 0] = edge[:, -1] = True
            outside = set(np.unique(labels[edge])) - {0}
            keep = np.zeros_like(hole)
            for i in range(1, n + 1):
                comp = labels == i
                if i in outside or comp.sum() > int(p.get("max", 10 ** 9)): continue
                if "keyed" in p:
                    # A hole the white key made sits in a light surface; a real opening (chair
                    # slats, a handle) is ringed by the dark outline. Judge by the SOURCE ring.
                    ring = ndimage.binary_dilation(comp, iterations=2) & ~comp & (O[y0:y1, x0:x1, 3] >= 200)
                    if ring.sum() < 4: continue
                    lum = (O[y0:y1, x0:x1, :3][ring].astype(np.float32) / 255.0) @ LUMA
                    if float(np.median(lum)) < float(p["keyed"]): continue
                keep |= comp
            # the sealed-over outline gaps belong to whichever hole they border
            hole = hole & (keep | (ndimage.binary_dilation(keep, iterations=max(1, seal)) & hole & solid))
        if not hole.any(): continue
        sub = C[y0:y1, x0:x1]
        if "colour" in p or "sample" in p or p.get("mode", "all") == "all":
            colour = np.array(p["colour"], np.float32) if "colour" in p else surface_colour(C, p.get("sample", p["rect"]), O)
            if colour is None: continue
            sub[hole, :3] = colour.clip(0, 255).astype(np.uint8); sub[hole, 3] = 255
            filled += int(hole.sum()); continue
        # Scattered small holes: each takes the colour of the surface right around it. One
        # colour for the whole prop put a white bar under a grey monitor.
        labels, n = ndimage.label(hole)
        for i, sl in enumerate(ndimage.find_objects(labels), 1):
            ys, xs = sl
            box = [x0 + max(0, xs.start - 4), y0 + max(0, ys.start - 4), x0 + xs.stop + 4, y0 + ys.stop + 4]
            colour = surface_colour(C, box, O)
            if colour is None: continue
            comp = labels[sl] == i
            sub[sl][comp, :3] = colour.clip(0, 255).astype(np.uint8); sub[sl][comp, 3] = 255
            filled += int(comp.sum())
    return filled


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sources", nargs="+", required=True)
    ap.add_argument("--preview"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--suggest-starred", action="store_true", help="add a keyed-hole patch for each starred prop it would change")
    args = ap.parse_args()
    spec = load_json(LIB / "hole-patches.json", {})
    props = {e["id"]: e for e in load_props()}
    if args.suggest_starred:
        from common import PREFIX, save_json
        for key in load_json(LIB / "favourites.json", []):
            pid = key.replace(PREFIX, "")
            if pid in props and pid not in spec:
                x, y, w, h = [int(v) for v in props[pid]["region"]]
                spec[pid] = [{"origin": [x, y]}, {"rect": [0, 0, w, h], "mode": "enclosed", "seal": 1, "max": 400, "keyed": 0.6}]
        suggested = set(spec) - set(load_json(LIB / "hole-patches.json", {}))
    by = collections.defaultdict(list)
    for pid in spec:
        if pid in props: by[sheet_of(props[pid])].append(pid)
    found, missing = match_sources(sorted(by), args.sources)
    shots = []
    for sheet, ids in by.items():
        if sheet not in found:
            print("no source for", sheet)
            if args.suggest_starred:
                for pid in ids:
                    if pid in suggested: del spec[pid]
            continue
        C = load_rgba(REPO / sheet).copy(); O = load_rgba(found[sheet])
        for pid in ids:
            x, y, w, h = [int(v) for v in props[pid]["region"]]
            for p in spec[pid]:
                if "origin" in p:                  # rects were drawn against this corner
                    ox, oy = p["origin"]; w, h = x + w - ox, y + h - oy; x, y = ox, oy
            before = C[y:y + h, x:x + w].copy()
            n = apply(C[y:y + h, x:x + w], O[y:y + h, x:x + w], None, spec[pid])
            # Twice: a small patch beside a pillow samples its colour before the pillow is
            # whitened on the first pass. The second pass is the fixed point, so one run of
            # this tool always gives the same sheet.
            apply(C[y:y + h, x:x + w], O[y:y + h, x:x + w], None, spec[pid])
            if args.suggest_starred and pid in suggested and n < 4:
                C[y:y + h, x:x + w] = before; del spec[pid]; continue      # nothing to patch here
            print(f"   {pid:<9} {(props[pid].get('title') or props[pid]['label']):<32} {n:>5} px")
            shots.append((props[pid], before, C[y:y + h, x:x + w].copy()))
        if not args.dry_run: save_png_atomic(REPO / sheet, C)
    if args.preview and shots:
        cell = 230
        img = Image.new("RGBA", (len(shots) * cell + 20, 2 * cell + 50), (120, 132, 128, 255)); d = ImageDraw.Draw(img)
        d.text((8, 4), "over a floor grey - top: before   bottom: patched", fill=(255, 255, 255, 255))
        for i, (e, a, b) in enumerate(shots):
            for row, arr in ((0, a), (1, b)):
                im = Image.fromarray(arr, "RGBA"); s = min((cell - 12) / im.width, (cell - 12) / im.height, 3.0)
                im = im.resize((int(im.width * s), int(im.height * s)), Image.NEAREST)
                img.alpha_composite(im, (10 + i * cell + (cell - im.width) // 2, 20 + row * cell + (cell - im.height) // 2))
        img.save(args.preview)
    if args.suggest_starred and not args.dry_run: save_json(LIB / "hole-patches.json", spec, indent=1)
    print("dry run: nothing written" if args.dry_run else "written")


if __name__ == "__main__":
    main()
