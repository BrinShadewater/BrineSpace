"""Register new Marsh salvage motion between exact active idle endpoints."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label

from prepare_marsh_carry_chain import palette_module


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "character/marsh-salvage-match-v1"
RUNTIME = ROOT / "character/marsh-v2/frames/bare"
DIRECTIONS = ("south", "north", "east", "west")


def components(source):
    labels, _ = label(np.asarray(source.getchannel("A")) > 40)
    sizes = np.bincount(labels.ravel())
    parts = []
    for component in range(1, len(sizes)):
        if sizes[component] < 10000:
            continue
        ys, xs = np.where(labels == component)
        parts.append((component, (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)))
    parts.sort(key=lambda item: item[1][0])
    if len(parts) != 6:
        raise ValueError(f"Expected six isolated poses, got {len(parts)}")
    return parts, labels


def make(direction, palette):
    source_path = BASE / "sources" / f"{direction}-sheet-01.png"
    source = Image.open(source_path).convert("RGBA")
    parts, labels = components(source)
    idle_path = RUNTIME / f"idle-{direction}/000.png"
    idle = Image.open(idle_path).convert("RGBA")
    idle_box = idle.getchannel("A").getbbox()
    source_box = parts[0][1]
    scale = (idle_box[3] - idle_box[1]) / (source_box[3] - source_box[1])
    old = []
    for phase in range(6):
        relative = f"character/marsh-v2/frames/bare/salvage-{direction}/{phase:03}.png"
        saved = BASE / "installation-backup" / relative
        old.append(Image.open(saved if saved.exists() else ROOT / relative).convert("RGBA"))
    frames = BASE / "frames" / f"salvage-{direction}"
    review = BASE / "review" / direction
    frames.mkdir(parents=True, exist_ok=True)
    review.mkdir(parents=True, exist_ok=True)
    for phase in (0, 5):
        (frames / f"{phase:03}.png").write_bytes(idle_path.read_bytes())
    records = []
    for phase in range(1, 5):
        component, (x0, y0, x1, y1) = parts[phase]
        patch = np.asarray(source.crop((x0, y0, x1, y1))).copy()
        patch[np.asarray(labels[y0:y1, x0:x1]) != component] = 0
        sprite = Image.fromarray(patch, "RGBA")
        size = (round(sprite.width * scale), round(sprite.height * scale))
        sprite = sprite.resize(size, Image.Resampling.LANCZOS)
        old_box = old[phase].getchannel("A").getbbox()
        center_x = round((old_box[0] + old_box[2]) / 2)
        bottom = old_box[3]
        frame = Image.new("RGBA", (184, 184))
        frame.alpha_composite(sprite, (center_x - size[0] // 2, bottom - size[1]))
        data = np.asarray(frame).copy()
        data[:, :, 3] = np.where(data[:, :, 3] >= 80, 255, 0).astype(np.uint8)
        frame = Image.fromarray(data, "RGBA")
        box = frame.getchannel("A").getbbox()
        if box is None or min(box[0], box[1], 184 - box[2], 184 - box[3]) < 2:
            raise ValueError(f"Clipped {direction} phase {phase}: {box}")
        unmapped = review / f"{phase:03}-unmapped.png"
        frame.save(unmapped)
        target = frames / f"{phase:03}.png"
        if target.exists():
            target.unlink()
        palette.map_file("marsh", unmapped, target)
        records.append({"phase": phase, "sourceBox": [x0, y0, x1, y1],
                        "component": component, "scale": scale,
                        "centerX": center_x, "bottom": bottom, "registeredBox": box})
    row = [Image.open(frames / f"{phase:03}.png").convert("RGBA") for phase in range(6)]
    contact = Image.new("RGB", (184 * 6, 205), "#21272c")
    pen = ImageDraw.Draw(contact)
    for phase, frame in enumerate(row):
        contact.paste(frame, (184 * phase, 0), frame)
        pen.text((184 * phase + 5, 187), str(phase), fill="white")
    contact.save(review / "contact.png")
    preview = []
    for frame in row:
        canvas = Image.new("RGB", (240, 210), "#21272c")
        canvas.paste(frame, (28, 12), frame)
        preview.append(canvas)
    preview[0].save(review / "motion.gif", save_all=True, append_images=preview[1:],
                    duration=[180, 180, 180, 180, 180, 700], loop=0)
    record = {"direction": direction, "source": source_path.relative_to(ROOT).as_posix(),
              "sourceSha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
              "scaleFromStandingHeight": scale, "poses": records,
              "endpoints": "Exact active bare idle frame zero at phases zero and five",
              "status": "candidate_not_installed"}
    (review / "registration.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


if __name__ == "__main__":
    palette = palette_module()
    records = [make(direction, palette) for direction in DIRECTIONS]
    (BASE / "registration.json").write_text(json.dumps(records, indent=2) + "\n")
    print("Registered", len(records), "salvage directions")
