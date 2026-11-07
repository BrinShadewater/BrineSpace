"""Prepare this generated pack. Run --write only after local cleanup is authorized.

Without --write this only reports masks and registration measurements.
Originals are preserved. Each frame keeps the full common canvas; only translation
aligns the generated foot point before an exact 4:1 nearest-neighbor bake.
"""
from pathlib import Path
import argparse
import hashlib
import json

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
SOURCES = {"flame": "flame-source-v1.png", "smoke": "smoke-source-v1.png", "embers": "embers-source-v1.png"}
CELL = (384, 512)
PIVOT = (192, 472)


def label(mask):
    """Four-connected components without a third-party image-processing runtime."""
    labels = np.zeros(mask.shape, dtype=np.int32)
    height, width = mask.shape
    count = 0
    for y, x in zip(*np.where(mask)):
        if labels[y, x]:
            continue
        count += 1
        labels[y, x] = count
        stack = [(int(y), int(x))]
        while stack:
            cy, cx = stack.pop()
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < height and 0 <= nx < width and mask[ny, nx] and not labels[ny, nx]:
                    labels[ny, nx] = count
                    stack.append((ny, nx))
    return labels, count


def foreground(rgb, kind):
    r, g, b = rgb.astype(np.int16).transpose(2, 0, 1)
    if kind == "flame":
        # The failed transparency was neutral checkerboard, flame is warm.
        mask = (r - b > 18) & (g - b > 5) & (r >= g)
    else:
        # The other sources use a magenta production matte. Preserve neutral smoke.
        mask = ~((r - g > 20) & (b - g > 20))
    labels, count = label(mask)
    areas = np.bincount(labels.ravel(), minlength=count + 1)
    keep = areas >= 4
    keep[0] = False
    return keep[labels]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    records = []
    for kind, name in SOURCES.items():
        path = ROOT / name
        image = Image.open(path).convert("RGB")
        if image.size != (1536, 1024):
            raise ValueError(f"Unexpected source grid: {name}: {image.size}")
        raw = np.asarray(image)
        frames = []
        measurements = []
        for index in range(8):
            x, y = (index % 4) * CELL[0], (index // 4) * CELL[1]
            rgb = raw[y:y + CELL[1], x:x + CELL[0]]
            mask = foreground(rgb, kind)
            yy, xx = np.where(mask)
            if not len(xx):
                raise ValueError(f"Empty frame: {kind}/{index}")
            labels, count = label(mask)
            areas = np.bincount(labels.ravel(), minlength=count + 1)
            areas[0] = 0
            base = labels == areas.argmax()
            by, bx = np.where(base)
            foot_y = int(by.max())
            foot_x = round(float(np.median(bx[by >= foot_y - 8])))
            offset = (PIVOT[0] - foot_x, PIVOT[1] - foot_y)
            bounds = [int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1]
            translated = [bounds[0] + offset[0], bounds[1] + offset[1], bounds[2] + offset[0], bounds[3] + offset[1]]
            if translated[0] < 0 or translated[1] < 0 or translated[2] > CELL[0] or translated[3] > CELL[1]:
                raise ValueError(f"Registration clips {kind}/{index}: {translated}")
            measurements.append({"frame": index, "foreground_pixels": int(mask.sum()), "bounds": bounds, "translation": list(offset)})
            if args.write:
                rgba = np.zeros((*mask.shape, 4), dtype=np.uint8)
                rgba[:, :, :3] = rgb
                rgba[:, :, 3] = mask.astype(np.uint8) * 255
                rgba[~mask, :3] = 0
                registered = Image.new("RGBA", CELL)
                registered.paste(Image.fromarray(rgba), offset)
                frames.append(registered)
        record = {"id": kind, "source": name, "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "grid": [4, 2], "source_cell": list(CELL), "runtime_cell": [96, 128], "pivot": [48, 118], "suggested_fps": 8, "frames": measurements}
        if args.write:
            atlas = Image.new("RGBA", (1536, 1024))
            for index, frame in enumerate(frames):
                atlas.paste(frame, ((index % 4) * CELL[0], (index // 4) * CELL[1]))
            atlas_path = ROOT / f"{kind}-atlas.png"
            runtime_path = ROOT / f"{kind}-96x128.png"
            if atlas_path.exists() or runtime_path.exists():
                raise FileExistsError("Use a sibling version for a rebake; originals are never overwritten")
            atlas.save(atlas_path)
            atlas.resize((384, 256), Image.Resampling.NEAREST).save(runtime_path)
            record.update(atlas=atlas_path.name, runtime_atlas=runtime_path.name, stage="cleaned; visual and loop review pending")
        records.append(record)
    if args.write:
        (ROOT / "manifest.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
