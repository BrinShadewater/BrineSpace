"""Register four clean carry quarter turns and derive all twelve directions.

The four generated source sheets are preserved. Reverse turns reverse frame order,
and half-turns join two quarter turns at one exact shared cardinal pose.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from prepare_marsh_carry_chain import palette_module


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "character/marsh-carry-chain-v1"
CARRY = ROOT / "character/marsh-carry-match-v1/frames"
OUT = BASE / "turns-matched"
SHEETS = {
    "east-north": ("turn-east-north-sheet-02.png", [(120, 320), (538, 728), (986, 1149), (1440, 1584), (1871, 2026)]),
    "west-north": ("turn-west-north-sheet-02.png", [(111, 329), (558, 764), (1003, 1173), (1436, 1590), (1872, 2033)]),
    "east-south": ("turn-east-south-sheet-02.png", [(128, 309), (563, 722), (999, 1155), (1431, 1587), (1869, 2036)]),
    "west-south": ("turn-west-south-sheet-02.png", [(114, 321), (566, 742), (1001, 1152), (1437, 1596), (1871, 2032)]),
}


def read(direction: str) -> Image.Image:
    return Image.open(CARRY / direction / "000.png").convert("RGBA")


def save_state(name: str, frames: list[Image.Image]) -> None:
    folder = OUT / name
    folder.mkdir(parents=True, exist_ok=True)
    contact = Image.new("RGB", (184 * len(frames), 210), (33, 39, 44))
    pen = ImageDraw.Draw(contact)
    for i, frame in enumerate(frames):
        frame.save(folder / f"{i:03}.png")
        contact.paste(frame, (184 * i, 0), frame)
        pen.text((184 * i + 4, 188), str(i), fill="white")
    contact.save(folder / "contact.png")


def build_pair(pair: str, palette) -> tuple[list[Image.Image], dict]:
    name, bands = SHEETS[pair]
    origin, destination = pair.split("-")
    source = Image.open(BASE / "sources" / name).convert("RGBA")
    alpha = np.asarray(source.getchannel("A"))
    boxes = []
    for x0, x1 in bands:
        ys = np.where(alpha[:, x0 : x1 + 1] > 32)[0]
        if len(ys) == 0:
            raise ValueError(f"Empty carry turn cell: {pair}")
        boxes.append((x0, x1, int(ys.min()), int(ys.max())))
    endpoint_heights = [boxes[i][3] - boxes[i][2] + 1 for i in (0, 4)]
    scale = 148.0 / float(np.median(endpoint_heights))
    foot = max(box[3] for box in boxes)
    review = BASE / "review" / f"turn-{pair}"
    review.mkdir(parents=True, exist_ok=True)
    frames = [read(origin)]
    for i in (1, 2, 3):
        x0, x1, _, _ = boxes[i]
        crop = source.crop((x0, 0, x1 + 1, source.height))
        size = (round(crop.width * scale), round(crop.height * scale))
        sprite = crop.resize(size, Image.Resampling.LANCZOS)
        frame = Image.new("RGBA", (184, 184))
        frame.alpha_composite(sprite, (92 - size[0] // 2, round(172 - foot * scale)))
        data = np.asarray(frame).copy()
        data[:, :, 3] = np.where(data[:, :, 3] >= 80, 255, 0).astype(np.uint8)
        frame = Image.fromarray(data, "RGBA")
        bbox = frame.getchannel("A").getbbox()
        if bbox is None or min(bbox[0], bbox[1], 184 - bbox[2], 184 - bbox[3]) < 2:
            raise ValueError(f"Clipped carry turn {pair}/{i}")
        unmapped = review / f"{i:03}-unmapped.png"
        frame.save(unmapped)
        mapped = review / f"{i:03}-mapped.png"
        if mapped.exists():
            mapped.unlink()
        palette.map_file("marsh", unmapped, mapped)
        frames.append(Image.open(mapped).convert("RGBA"))
    frames.append(read(destination))
    record = {"pair": pair, "source": name, "bands": bands, "scale": scale,
              "footSourceY": foot, "status": "candidate_not_installed",
              "endpoints": "exact new carry frame zero"}
    (review / "registration.json").write_text(json.dumps(record, indent=2) + "\n")
    save_state("carry-turn-" + pair, frames)
    save_state("carry-turn-" + destination + "-" + origin, list(reversed(frames)))
    return frames, record


def build() -> dict:
    palette = palette_module()
    quarters = {}
    records = []
    for pair in SHEETS:
        quarters[pair], record = build_pair(pair, palette)
        records.append(record)
    # East to west through north; north to south through east.
    half = {
        "east-west": quarters["east-north"] + list(reversed(quarters["west-north"]))[1:],
        "north-south": list(reversed(quarters["east-north"])) + quarters["east-south"][1:],
    }
    for pair, frames in half.items():
        if len(frames) != 9:
            raise ValueError(f"Bad half-turn {pair}")
        origin, destination = pair.split("-")
        save_state("carry-turn-" + pair, frames)
        save_state("carry-turn-" + destination + "-" + origin, list(reversed(frames)))
        records.append({"pair": pair, "method": "two selected quarter-turns with shared center once",
                        "status": "candidate_not_installed"})
    result = {"quarterPairs": 4, "oppositePairs": 2, "directedStates": 12,
              "records": records, "status": "candidate_not_installed"}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    print(build()["directedStates"], "directed carry turns")
