"""Model cutout for station props: BiRefNet + SAM 2.1 masks, merged and cleaned.

extract.py finds each prop (its box); this cuts it from the painting. Needs the
cutout venv (rembg[gpu], ultralytics, scipy, pillow), not the system Python:

    C:/Users/Alex/.venvs/brine-cutout/Scripts/python tools/room_props_v2/model_cut.py \
        --designs "<design folder>" --cut <extract.py --out dir> --out <dir> [--only a,b] [--install]

--install writes each cut into assets/station-props-v2/sp-<id>.png on the same
canvas as the extract.py cut, so catalog sizes and saved layouts stay put. Run it
after build_catalog.py. A cut reaching past that canvas grows it, and the
catalog region and default-layout positions are adjusted so the art stays put
(owner layouts are not rewritten; a grown prop there shifts by those few px).
Per-prop repairs live in overrides.json "_model_cut_fixes" (see its _note).
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

import extract

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PAD = 40          # context around the detection box
WORK = 1024       # both models see the crop at this size
SPECK = 150       # native px; smaller detached islands are floor bolts
THIN_MIN = 60     # native px; smaller agreed slivers on the outline are ticks
PEEL = 5          # native px: deepest the floor-strip peel reaches into a mask
POINT_UP = 2      # click repairs run SAM at twice native size
MARGIN = 3        # extract.py cut margin, for --install alignment


class Cutter:
    def __init__(self, designs):
        from rembg import new_session
        from ultralytics import SAM
        self.designs = Path(designs)
        self.bir = new_session("birefnet-general", providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
        self.sam = SAM("sam2.1_b.pt")
        self.floors = {}
        self.rugs = {}

    def floor_maps(self, design):
        """Clean-floor estimate and difference map from extract.py."""
        if design not in self.floors:
            rgba = np.asarray(Image.open(self.designs / design).convert("RGBA"))
            extract.INTERIOR = extract.interior(rgba)
            floor, _ = extract.clean_floor(rgba[..., :3].copy())
            self.floors[design] = (extract.difference(rgba[..., :3], floor), floor)
        return self.floors[design]

    def crop(self, record):
        sheet = Image.open(self.designs / record["design"]).convert("RGB")
        x0, y0, x1, y1 = record["box"]
        box = (max(0, x0 - PAD), max(0, y0 - PAD), min(sheet.width, x1 + PAD), min(sheet.height, y1 + PAD))
        return sheet.crop(box), box

    def cut(self, record):
        from rembg import remove
        crop, box = self.crop(record)
        x0, y0, x1, y1 = record["box"]
        k = WORK / max(crop.size)
        big = crop.resize((round(crop.width * k), round(crop.height * k)), Image.LANCZOS)
        pb = np.asarray(remove(big, session=self.bir, only_mask=True)).astype(np.float32) / 255.0
        g = 8
        bb = [(x0 - box[0] - g) * k, (y0 - box[1] - g) * k, (x1 - box[0] + g) * k, (y1 - box[1] + g) * k]
        ps = self.sam(np.asarray(big)[..., ::-1], bboxes=[bb], verbose=False)[0].masks.data[0].cpu().numpy().astype(np.float32)
        if ps.shape != pb.shape:
            ps = np.asarray(Image.fromarray((ps * 255).astype(np.uint8)).resize(big.size, Image.BILINEAR)) / 255.0
        # SAM sometimes returns the floor around a light prop instead of the prop.
        # If it barely overlaps BiRefNet, flip it inside the box.
        inbox = np.zeros(pb.shape, bool)
        inbox[max(0, int(bb[1])):int(bb[3]), max(0, int(bb[0])):int(bb[2])] = True
        if ((pb > 0.5) & (ps > 0.5)).sum() < 0.3 * max(1, (pb > 0.5).sum()):
            ps = (inbox & ~(ps > 0.5)).astype(np.float32)
        arr = np.asarray(big).astype(np.float32)
        grey = (arr.max(2) - arr.min(2)) < 30
        lum = arr.mean(2)
        diff, floor = self.floor_maps(record["design"])
        dcrop = np.asarray(Image.fromarray(diff[box[1]:box[3], box[0]:box[2]]).resize(big.size, Image.BILINEAR))
        fl = np.asarray(Image.fromarray(floor[box[1]:box[3], box[0]:box[2]].astype(np.uint8)).resize(big.size, Image.BILINEAR)).astype(np.float32).mean(2)
        # Where both models agree is the prop. Pixels only one claims must also look
        # unlike the floor and its shadow (grey, a little darker than floor; ink is
        # near black), and survive a small opening (rivets, specks).
        core = (pb > 0.5) & (ps > 0.5)
        extra = ((pb > 0.5) | (ps > 0.5)) & ~core
        floorlike = (dcrop < 55) | (grey & (lum < fl - 4) & (lum > 32))
        extra = ndimage.binary_opening(extra & ~floorlike, iterations=max(1, round(k)))
        lab, _ = ndimage.label(core | extra)
        touching = np.unique(lab[core]); touching = touching[touching > 0]
        union = ndimage.binary_fill_holes(np.isin(lab, touching))
        # Floor and shadow on the outside edge are peeled in to the ink line; shading
        # inside the outline stays (owner: keep shadows within the asset's edges).
        peelable = floorlike | (grey & (lum > 28) & (lum < fl + 15))
        rim = union & ~ndimage.binary_erosion(union, iterations=max(1, round(PEEL * k)))
        seeds = rim & peelable & ndimage.binary_dilation(~union, iterations=1)
        union = ndimage.binary_fill_holes(union & ~ndimage.binary_propagation(seeds, mask=rim & peelable))
        # Models trim the outermost highlight and ink line; grow back into pixels
        # that are clearly not floor or shadow.
        agreed = union.copy()
        reach = ndimage.binary_dilation(union, iterations=max(1, round(5 * k)))
        union = ndimage.binary_propagation(union, mask=union | (reach & ~floorlike))
        # Shave ticks the grow-back attached, but keep thin parts both models agree
        # on when they are real parts (a pole, a claw).
        opened = ndimage.binary_opening(union, structure=np.ones((3, 3)), iterations=max(1, round(1.5 * k)))
        thin = agreed & core & union & ~opened
        lab, n = ndimage.label(thin)
        if n:
            sizes = np.bincount(lab.ravel()); sizes[0] = 0
            thin = (sizes >= THIN_MIN * k * k)[lab] & (lab > 0)
        union = ndimage.binary_fill_holes(opened | thin)
        union = keep_pieces(union, SPECK * k * k)
        # Area-average the high-res mask down: a smooth one-pixel edge that never
        # samples the floor or its shadow.
        alpha = np.asarray(Image.fromarray(union.astype(np.uint8) * 255).resize(crop.size, Image.BOX)).astype(np.float32) / 255.0
        alpha[alpha < 0.1] = 0
        return np.dstack([np.asarray(crop), (alpha * 255).astype(np.uint8)])

    def sam_points(self, crop, points, box=None):
        """One SAM object from clicks (padded-crop px), optionally with the prop box."""
        big = crop.resize((crop.width * POINT_UP, crop.height * POINT_UP), Image.LANCZOS)
        kwargs = {"points": [[[x * POINT_UP, y * POINT_UP] for x, y in points]], "labels": [[1] * len(points)]}
        if box is not None:
            kwargs["bboxes"] = [[v * POINT_UP for v in box]]
        m = self.sam(np.asarray(big)[..., ::-1], verbose=False, **kwargs)[0].masks.data[0].cpu().numpy() > 0.5
        return np.asarray(Image.fromarray(m.astype(np.uint8) * 255).resize(crop.size, Image.BOX)) > 127

    def repair(self, record, cut, fix):
        crop, box = self.crop(record)
        rgb = np.asarray(crop)
        if "sam_object_points" in fix:  # the clicks and box are the whole prop
            x0, y0, x1, y1 = record["box"]
            m = self.sam_points(crop, fix["sam_object_points"], [x0 - box[0], y0 - box[1], x1 - box[0], y1 - box[1]])
            cut = np.dstack([rgb, (ndimage.binary_fill_holes(m) * 255).astype(np.uint8)])
            cut[..., 3] = keep_pieces(cut[..., 3] > 127, SPECK) * 255
        for point in fix.get("add_points", []):  # a missed part, one click each
            m = self.sam_points(crop, [point])
            if m.sum() > 0.6 * (cut[..., 3] > 127).sum():
                continue  # SAM took the floor, not a part
            cut[..., 3] = np.maximum(cut[..., 3], ndimage.binary_fill_holes(m) * 255)
        if "add_points" in fix:
            cut[..., 3] = keep_pieces(cut[..., 3] > 127, SPECK) * 255
        for x0, y0, x1, y1 in fix.get("solid_rects", []):
            cut[y0:y1, x0:x1, 3] = 255
        if "peel_shadow" in fix:
            spec = fix["peel_shadow"]
            before = cut.copy()
            cut = peel_shadow(cut, spec.get("depth", 10))
            for x0, y0, x1, y1 in spec.get("protect_rects", []):
                cut[y0:y1, x0:x1, 3] = before[y0:y1, x0:x1, 3]
        if "floor_split" in fix:
            # A rug under furniture: the whole cut becomes the floor layer ("-rug"),
            # and the prop keeps only the furniture, one SAM object per [box, clicks].
            self.rugs[record["id"]] = cut.copy()
            furniture = np.zeros(cut.shape[:2], bool)
            for obj_box, points in fix["floor_split"]:
                furniture |= ndimage.binary_fill_holes(self.sam_points(crop, points, obj_box))
            cut = cut.copy()
            cut[..., 3] = np.where(furniture, cut[..., 3], 0)
        if "clear_below_y" in fix:
            y = fix["clear_below_y"]["y"]
            src = rgb.astype(int)
            green = (src[..., 1] > src[..., 0] + 8) & (src[..., 1] > src[..., 2] + 8)
            low = np.zeros(green.shape, bool); low[y:] = True
            cut[..., 3][low & ~green] = 0
        return cut


def keep_pieces(mask, min_size):
    """The largest piece plus every piece of at least min_size px."""
    lab, n = ndimage.label(mask)
    if n <= 1:
        return mask
    sizes = np.bincount(lab.ravel()); sizes[0] = 0
    keep = (sizes >= min_size) | (np.arange(len(sizes)) == sizes.argmax()); keep[0] = False
    return keep[lab]


def peel_shadow(rgba, depth=10, lo=22, hi=58, chroma=22):
    """Remove painted drop shadow (dark, grey) reachable from outside, stopped by the
    near-black ink outline, at most depth px in."""
    rgba = rgba.copy()
    a = rgba[..., 3] > 127
    rgb = rgba[..., :3].astype(int)
    lum = rgb.mean(2); chroma_v = rgb.max(2) - rgb.min(2)
    shadow = a & (lum >= lo) & (lum <= hi) & (chroma_v <= chroma)
    band = a & ~ndimage.binary_erosion(a, iterations=depth)
    seeds = shadow & band & ndimage.binary_dilation(~a, iterations=1)
    rgba[..., 3][ndimage.binary_propagation(seeds, mask=shadow & band)] = 0
    rgba[..., 3] = np.where(keep_pieces(rgba[..., 3] > 127, SPECK), rgba[..., 3], 0)
    return rgba


def install(record, cut, pid, suffix=""):
    """Place the cut on the extract.py canvas so the catalog region and saved
    layouts are unchanged. A cut that reaches past that canvas grows it; returns
    the growth (left, top, right, bottom) so the catalog and layouts can follow."""
    target = ROOT / "assets" / "station-props-v2" / ("sp-%s%s.png" % (pid, suffix))
    base = ROOT / "assets" / "station-props-v2" / ("sp-%s.png" % pid)
    w, h = Image.open(base).size
    x0, y0 = record["box"][0], record["box"][1]
    ox = max(0, x0 - PAD) - max(0, x0 - MARGIN)
    oy = max(0, y0 - PAD) - max(0, y0 - MARGIN)
    ys, xs = np.where(cut[..., 3] > 0)
    grow = (max(0, -(xs.min() + ox)), max(0, -(ys.min() + oy)),
            max(0, xs.max() + ox + 1 - w), max(0, ys.max() + oy + 1 - h))
    canvas = Image.new("RGBA", (w + grow[0] + grow[2], h + grow[1] + grow[3]), (0, 0, 0, 0))
    canvas.alpha_composite(Image.fromarray(cut, "RGBA"), (ox + grow[0], oy + grow[1]))
    # Transparent pixels carry no colour, so edge filtering never bleeds floor in.
    arr = np.asarray(canvas).copy(); arr[arr[..., 3] == 0, :3] = 0
    Image.fromarray(arr, "RGBA").save(target)
    return tuple(int(v) for v in grow)


def follow_growth(grown):
    """Grow catalog regions and move layout positions so grown art stays in place."""
    catalog_path = ROOT / "rooms" / "station-props-v2" / "props.json"
    catalog = json.loads(catalog_path.read_text())
    scales = {}
    for entry in catalog:
        g = grown.get(entry["id"])
        if not g: continue
        w, h = entry["region"][2], entry["region"][3]
        scale = entry["display_width"] / w
        w, h = w + g[0] + g[2], h + g[1] + g[3]
        entry["region"] = [0, 0, w, h]
        entry["pieces"] = [[[0, 0], [w, 0], [w, h], [0, h]]]
        entry["display_width"] = round(w * scale, 1)
        scales[entry["id"]] = (scale, g)
    catalog_path.write_text(json.dumps(catalog, indent=1))
    for path in [ROOT / "rooms" / "full-wall-v1" / "default-layouts.json"]:
        data = json.loads(path.read_text())
        for layout in data["layouts"].values():
            for key, value in layout.items():
                base = key.split("#")[0]
                if base.startswith("library/") and base[8:] in scales and isinstance(value, list):
                    scale, g = scales[base[8:]]
                    layout[key] = [round(value[0] - g[0] * scale, 1), round(value[1] - g[1] * scale, 1)]
        # Same shape as the hand-kept file (2-space JSON, CRLF).
        path.write_bytes((json.dumps(data, indent=2) + "\n").replace("\n", "\r\n").encode())
    return sorted(scales)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--designs", required=True)
    ap.add_argument("--cut", required=True, help="extract.py --out directory (props.json)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default="")
    ap.add_argument("--resume", action="store_true", help="reuse cuts already in --out")
    ap.add_argument("--install", action="store_true")
    args = ap.parse_args()
    records = {r["id"]: r for r in json.loads((Path(args.cut) / "props.json").read_text())}
    fixes = json.loads((HERE / "overrides.json").read_text()).get("_model_cut_fixes", {})
    only = [s for s in args.only.split(",") if s] or list(records)
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    cutter = None
    grown = {}
    for pid in only:
        path = out / (pid + ".png")
        if args.resume and path.exists():
            cut = np.asarray(Image.open(path).convert("RGBA")).copy()
        else:
            cutter = cutter or Cutter(args.designs)
            cut = cutter.cut(records[pid])
            if pid in fixes:
                cut = cutter.repair(records[pid], cut, fixes[pid])
            Image.fromarray(cut, "RGBA").save(path)
            if pid in cutter.rugs:
                Image.fromarray(cutter.rugs[pid], "RGBA").save(out / (pid + "-rug.png"))
        rug = out / (pid + "-rug.png")
        if args.install and rug.exists():
            install(records[pid], np.asarray(Image.open(rug).convert("RGBA")), pid, "-rug")
        if args.install:
            g = install(records[pid], cut, pid)
            if any(g): grown["sp-" + pid] = g
        print(pid, flush=True)
    if grown:
        print("grew canvas (catalog and default layouts follow):", follow_growth(grown))


if __name__ == "__main__":
    main()
