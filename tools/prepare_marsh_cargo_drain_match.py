"""Register four authored cargo-drain sheets between exact selected endpoints."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label

from prepare_marsh_carry_chain import palette_module


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "character/marsh-cargo-drain-match-v1"
RUNTIME = ROOT / "character/marsh-v2"
DIRECTIONS = ("south", "north", "east", "west")
BOTTOMS = {
    "south": (179, 177, 175, 173, 172, 173),
    "north": (197, 190, 181, 175, 172, 173),
    "east": (176, 176, 175, 173, 172, 173),
    "west": (160, 164, 168, 171, 172, 171),
}


def components(image: Image.Image) -> list[tuple[int, tuple[int, int, int, int]]]:
    alpha = np.asarray(image.getchannel("A")) > 40
    labels, _ = label(alpha)
    sizes = np.bincount(labels.ravel())
    ids = [i for i in range(1, len(sizes)) if sizes[i] > 10000]
    result = []
    for index in ids:
        ys, xs = np.where(labels == index)
        result.append((index, (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)))
    result.sort(key=lambda row: row[1][0])
    if len(result) != 6:
        raise ValueError(f"Expected six source figures, found {len(result)}")
    return result, labels


def exact_endpoints(direction: str) -> tuple[Image.Image, Image.Image]:
    first = Image.open(RUNTIME / f"supplemental/loaded-swim-{direction}/swim-carry-{direction}-000.png").convert("RGBA")
    carry = Image.open(RUNTIME / f"frames/bare/carry-{direction}/000.png").convert("RGBA")
    last = Image.new("RGBA", (224, 208))
    last.alpha_composite(carry, (20, 0))
    return first, last


def make(direction: str, palette) -> dict:
    source_path = BASE / "sources" / f"{direction}-sheet-01.png"
    source = Image.open(source_path).convert("RGBA")
    parts, labels = components(source)
    first, last = exact_endpoints(direction)
    last_bbox = last.getchannel("A").getbbox()
    source_height = parts[5][1][3] - parts[5][1][1]
    scale = (last_bbox[3] - last_bbox[1]) / source_height
    first_bbox = first.getchannel("A").getbbox()
    centers = ((first_bbox[0] + first_bbox[2]) / 2, (last_bbox[0] + last_bbox[2]) / 2)
    review = BASE / "review" / direction
    frames = BASE / "frames" / f"cargo-drain-{direction}"
    review.mkdir(parents=True, exist_ok=True)
    frames.mkdir(parents=True, exist_ok=True)
    first.save(frames / "000.png")
    last.save(frames / "005.png")
    records = []
    for phase in range(1, 5):
        component_id, (x0, y0, x1, y1) = parts[phase]
        patch = np.asarray(source.crop((x0, y0, x1, y1))).copy()
        patch[np.asarray(labels[y0:y1, x0:x1]) != component_id] = 0
        sprite = Image.fromarray(patch, "RGBA")
        size = (round(sprite.width * scale), round(sprite.height * scale))
        sprite = sprite.resize(size, Image.Resampling.LANCZOS)
        center_x = round(centers[0] + (centers[1] - centers[0]) * phase / 5)
        frame = Image.new("RGBA", (224, 208))
        frame.alpha_composite(sprite, (center_x - size[0] // 2, BOTTOMS[direction][phase] - size[1]))
        rgba = np.asarray(frame).copy()
        rgba[:, :, 3] = np.where(rgba[:, :, 3] >= 80, 255, 0).astype(np.uint8)
        frame = Image.fromarray(rgba, "RGBA")
        box = frame.getchannel("A").getbbox()
        if box is None or min(box[0], box[1], 224 - box[2], 208 - box[3]) < 2:
            raise ValueError(f"Clipped {direction} phase {phase}: {box}")
        unmapped = review / f"{phase:03}-unmapped.png"
        frame.save(unmapped)
        target = frames / f"{phase:03}.png"
        if target.exists():
            target.unlink()
        palette.map_file("marsh", unmapped, target)
        records.append({"phase": phase, "sourceBox": [x0, y0, x1, y1],
                        "sourceComponent": component_id, "scale": scale,
                        "centerX": center_x, "bottom": BOTTOMS[direction][phase],
                        "registeredBox": box})
    row = [Image.open(frames / f"{i:03}.png").convert("RGBA") for i in range(6)]
    contact = Image.new("RGB", (6 * 224, 244), "#21272c")
    draw = ImageDraw.Draw(contact)
    for i, frame in enumerate(row):
        contact.paste(frame, (i * 224, 8), frame)
        draw.text((i * 224 + 8, 225), str(i), fill="white")
    contact.save(review / "contact.png")
    previews = []
    for frame in row:
        board = Image.new("RGB", (280, 244), "#21272c")
        board.paste(frame, (28, 12), frame)
        previews.append(board)
    previews[0].save(review / "motion.gif", save_all=True, append_images=previews[1:],
                     duration=[500, 180, 220, 220, 180, 700], loop=0)
    record = {"direction": direction, "source": source_path.relative_to(ROOT).as_posix(),
              "sourceSha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
              "scaleFromStandingHeight": scale, "components": records,
              "endpoints": "exact installed swim-carry frame zero and dry carry frame zero",
              "status": "candidate_not_installed"}
    (review / "registration.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


if __name__ == "__main__":
    palette = palette_module()
    result = [make(direction, palette) for direction in DIRECTIONS]
    (BASE / "registration.json").write_text(json.dumps(result, indent=2) + "\n")
    print("Registered", len(result), "cargo-drain directions")
