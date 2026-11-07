"""Register the reviewed Marsh run/carry identity studies as non-runtime candidates.

Each source sheet is preserved in character/marsh-{run,carry}-match-v1/sources.
The explicit column bounds avoid treating stray generated edge pixels as limbs.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SPECS = {
    ("run", "south"): ("run-south-sheet-01.png", 362, [(111, 249), (474, 608), (836, 972), (1200, 1336), (1559, 1691), (1924, 2056)]),
    ("run", "north"): ("run-north-sheet-02.png", 0, [(81, 299), (446, 662), (809, 1030), (1173, 1390), (1531, 1748), (1879, 2092)]),
    ("run", "east"): ("run-east-sheet-01.png", 362, [(49, 290), (433, 609), (796, 979), (1152, 1365), (1502, 1731), (1888, 2079)]),
    ("run", "west"): ("run-west-sheet-01.png", 362, [(99, 310), (457, 662), (787, 1046), (1174, 1382), (1538, 1754), (1919, 2130)]),
    ("carry", "south"): ("carry-south-sheet-01.png", 443, [(142, 307), (595, 761), (1048, 1216), (1504, 1670)]),
    ("carry", "north"): ("carry-north-sheet-02.png", 0, [(172, 378), (709, 915), (1250, 1457), (1787, 1995)]),
    ("carry", "east"): ("carry-east-sheet-01.png", 443, [(133, 316), (610, 756), (1050, 1206), (1523, 1657)]),
    ("carry", "west"): ("carry-west-sheet-01.png", 443, [(113, 323), (580, 727), (1023, 1186), (1467, 1627)]),
}


def build(action: str, direction: str) -> dict:
    name, row, bands = SPECS[action, direction]
    base = ROOT / f"character/marsh-{action}-match-v1"
    source = Image.open(base / "sources" / name).convert("RGBA")
    source_alpha = np.asarray(source.getchannel("A"))
    boxes = []
    for x0, x1 in bands:
        ys = np.where(source_alpha[row:, x0 : x1 + 1] > 32)[0]
        if len(ys) == 0:
            raise ValueError(f"Empty {action}-{direction} source band {x0}:{x1}")
        boxes.append((x0, x1, int(ys.min()), int(ys.max())))
    heights = [box[3] - box[2] + 1 for box in boxes]
    scale = 148.0 / float(np.median(heights))
    foot = max(box[3] for box in boxes)
    out = base / "review" / direction
    out.mkdir(parents=True, exist_ok=True)
    contact = Image.new("RGB", (184 * len(bands), 210), (33, 39, 44))
    pen = ImageDraw.Draw(contact)
    results = []
    loop_frames = []
    for i, (x0, x1, _, _) in enumerate(boxes):
        crop = source.crop((x0, row, x1 + 1, source.height))
        size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
        sprite = crop.resize(size, Image.Resampling.LANCZOS)
        frame = Image.new("RGBA", (184, 184))
        x = 92 - size[0] // 2
        y = round(172 - foot * scale)
        frame.alpha_composite(sprite, (x, y))
        data = np.array(frame)
        data[:, :, 3] = np.where(data[:, :, 3] >= 80, 255, 0).astype(np.uint8)
        frame = Image.fromarray(data, "RGBA")
        bbox = frame.getchannel("A").getbbox()
        if bbox is None or min(bbox[0], bbox[1], 184 - bbox[2], 184 - bbox[3]) < 2:
            raise ValueError(f"Clipped frame: {action}-{direction}/{i:03}")
        frame.save(out / f"{i:03}.png")
        contact.paste(frame, (184 * i, 0), frame)
        backdrop = Image.new("RGB", (184, 184), (33, 39, 44))
        backdrop.paste(frame, (0, 0), frame)
        loop_frames.append(backdrop)
        pen.text((184 * i + 4, 188), f"{action}-{direction} {i}", fill="white")
        results.append({"frame": i, "bbox": bbox})
    contact.save(out / "contact.png")
    loop_frames[0].save(out / "loop.gif", save_all=True, append_images=loop_frames[1:],
                        duration=100 if action == "run" else 180, loop=0, disposal=2)
    record = {"action": action, "direction": direction, "source": name, "row": row, "bands": bands, "scale": scale, "footSourceY": foot, "frames": results, "status": "candidate_not_installed"}
    (out / "registration.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


if __name__ == "__main__":
    for action, direction in SPECS:
        result = build(action, direction)
        print(f"{action}-{direction}: {len(result['frames'])} frames, scale {result['scale']:.4f}")
