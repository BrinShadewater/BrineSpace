"""Build dry Marsh pickup and unload candidates with exact idle/carry endpoints."""

from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "character/marsh-carry-chain-v1"
CARRY = ROOT / "character/marsh-carry-match-v1/frames"
RUNTIME = ROOT / "character/marsh-v2/frames/bare"
SPECS = {
    "south": ("pickup-south-sheet-01.png", 443, [(142, 310), (585, 764), (1043, 1212), (1490, 1667)]),
    "north": ("pickup-north-sheet-01.png", 0, [(215, 455), (707, 951), (1199, 1463), (1709, 1951)]),
    "east": ("pickup-east-sheet-01.png", 443, [(179, 270), (573, 805), (1048, 1242), (1523, 1658)]),
    "west": ("pickup-west-sheet-01.png", 443, [(178, 278), (575, 807), (1027, 1206), (1494, 1634)]),
}


def palette_module():
    path = ROOT / "character/palette-standard-v1/standardize.py"
    spec = importlib.util.spec_from_file_location("marsh_palette", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def build(direction: str, palette) -> dict:
    name, row, bands = SPECS[direction]
    source = Image.open(BASE / "sources" / name).convert("RGBA")
    alpha = np.asarray(source.getchannel("A"))
    boxes = []
    for x0, x1 in bands:
        ys = np.where(alpha[row:, x0 : x1 + 1] > 32)[0]
        if len(ys) == 0:
            raise ValueError(f"Empty pickup-{direction} source band")
        boxes.append((x0, x1, int(ys.min()), int(ys.max())))
    upright = [boxes[0][3] - boxes[0][2] + 1, boxes[3][3] - boxes[3][2] + 1]
    scale = 148.0 / float(np.median(upright))
    foot = max(box[3] for box in boxes)
    review = BASE / "review" / direction
    review.mkdir(parents=True, exist_ok=True)
    pickup = BASE / "frames" / f"pickup-{direction}"
    pickup.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(RUNTIME / f"idle-{direction}" / "000.png", pickup / "000.png")
    shutil.copyfile(CARRY / direction / "000.png", pickup / "003.png")
    for i in (1, 2):
        x0, x1, _, _ = boxes[i]
        crop = source.crop((x0, row, x1 + 1, source.height))
        size = (round(crop.width * scale), round(crop.height * scale))
        sprite = crop.resize(size, Image.Resampling.LANCZOS)
        frame = Image.new("RGBA", (184, 184))
        frame.alpha_composite(sprite, (92 - size[0] // 2, round(172 - foot * scale)))
        data = np.asarray(frame).copy()
        data[:, :, 3] = np.where(data[:, :, 3] >= 80, 255, 0).astype(np.uint8)
        frame = Image.fromarray(data, "RGBA")
        bbox = frame.getchannel("A").getbbox()
        if bbox is None or min(bbox[0], bbox[1], 184 - bbox[2], 184 - bbox[3]) < 2:
            raise ValueError(f"Clipped pickup-{direction} frame {i}")
        unmapped = review / f"{i:03}-unmapped.png"
        frame.save(unmapped)
        destination = pickup / f"{i:03}.png"
        if destination.exists():
            destination.unlink()
        palette.map_file("marsh", unmapped, destination)
    for action in ("unload", "cargo-unload"):
        out = BASE / "frames" / f"{action}-{direction}"
        out.mkdir(parents=True, exist_ok=True)
        for i in range(4):
            shutil.copyfile(pickup / f"{3-i:03}.png", out / f"{i:03}.png")
    contact = Image.new("RGB", (4 * 184, 210), (33, 39, 44))
    draw = ImageDraw.Draw(contact)
    for i in range(4):
        frame = Image.open(pickup / f"{i:03}.png").convert("RGBA")
        contact.paste(frame, (i * 184, 0), frame)
        draw.text((i * 184 + 4, 188), str(i), fill="white")
    contact.save(review / "pickup-contact.png")
    result = {"direction": direction, "source": name, "row": row, "bands": bands,
              "scale": scale, "footSourceY": foot,
              "status": "candidate_not_installed",
              "endpointPolicy": "exact current idle frame zero and selected carry candidate frame zero"}
    (review / "registration.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    palette = palette_module()
    for direction in SPECS:
        print(direction, build(direction, palette)["scale"])
