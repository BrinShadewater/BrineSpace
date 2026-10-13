"""Register Marsh's loaded-swim pickup to the active swim endpoint."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label

from prepare_marsh_carry_chain import palette_module


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "character/marsh-swim-pickup-match-v1"
RUNTIME = ROOT / "character/marsh-v2/supplemental"


def segments(source: Image.Image):
    labels, _ = label(np.asarray(source.getchannel("A")) > 40)
    sizes = np.bincount(labels.ravel())
    parts = []
    for component in range(1, len(sizes)):
        if sizes[component] < 10000:
            continue
        ys, xs = np.where(labels == component)
        parts.append((component, (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)))
    parts.sort(key=lambda row: row[1][0])
    if len(parts) != 6:
        raise ValueError(f"Expected six figures, got {len(parts)}")
    return parts, labels


def make(direction, palette):
    source_path = BASE / "sources" / f"{direction}-sheet-01.png"
    source = Image.open(source_path).convert("RGBA")
    parts, labels = segments(source)
    old = []
    for phase in range(6):
        relative = f"character/marsh-v2/supplemental/loaded-swim-{direction}/swim-pickup-{direction}-{phase:03}.png"
        saved = BASE / "installation-backup" / relative
        old.append(Image.open(saved if saved.exists() else ROOT / relative).convert("RGBA"))
    old_boxes = [frame.getchannel("A").getbbox() for frame in old]
    first_height = old_boxes[0][3] - old_boxes[0][1]
    source_first_height = parts[0][1][3] - parts[0][1][1]
    scale = first_height / source_first_height
    frames = BASE / "frames" / f"swim-pickup-{direction}"
    review = BASE / "review" / direction
    frames.mkdir(parents=True, exist_ok=True)
    review.mkdir(parents=True, exist_ok=True)
    records = []
    selected_salvage_start = ROOT / "character/marsh-salvage-match-v1/frames" / f"salvage-{direction}" / "000.png"
    if not selected_salvage_start.exists():
        raise FileNotFoundError(selected_salvage_start)
    salvage = Image.new("RGBA", (224, 208))
    salvage.alpha_composite(Image.open(selected_salvage_start).convert("RGBA"), (20, 0))
    salvage.save(frames / "000.png")
    for phase in range(1, 5):
        component, (x0, y0, x1, y1) = parts[phase]
        patch = np.asarray(source.crop((x0, y0, x1, y1))).copy()
        patch[np.asarray(labels[y0:y1, x0:x1]) != component] = 0
        sprite = Image.fromarray(patch, "RGBA")
        size = (round(sprite.width * scale), round(sprite.height * scale))
        sprite = sprite.resize(size, Image.Resampling.LANCZOS)
        old_box = old_boxes[phase]
        center_x = round((old_box[0] + old_box[2]) / 2)
        bottom = old_box[3]
        frame = Image.new("RGBA", (224, 208))
        frame.alpha_composite(sprite, (center_x - size[0] // 2, bottom - size[1]))
        data = np.asarray(frame).copy()
        data[:, :, 3] = np.where(data[:, :, 3] >= 80, 255, 0).astype(np.uint8)
        frame = Image.fromarray(data, "RGBA")
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
                        "component": component, "scale": scale,
                        "centerX": center_x, "bottom": bottom, "registeredBox": box})
    endpoint = RUNTIME / f"loaded-swim-{direction}/swim-carry-{direction}-000.png"
    (frames / "005.png").write_bytes(endpoint.read_bytes())
    row = [Image.open(frames / f"{i:03}.png").convert("RGBA") for i in range(6)]
    contact = Image.new("RGB", (6 * 224, 230), "#21272c")
    pen = ImageDraw.Draw(contact)
    for i, frame in enumerate(row):
        contact.paste(frame, (224 * i, 0), frame)
        pen.text((224 * i + 5, 211), str(i), fill="white")
    contact.save(review / "contact.png")
    preview = []
    for frame in row:
        canvas = Image.new("RGB", (280, 244), "#21272c")
        canvas.paste(frame, (28, 12), frame)
        preview.append(canvas)
    preview[0].save(review / "motion.gif", save_all=True, append_images=preview[1:],
                    duration=[180, 180, 180, 180, 180, 700], loop=0)
    record = {"direction": direction, "source": source_path.relative_to(ROOT).as_posix(),
              "sourceSha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
              "scaleFromStandingHeight": scale, "poses": records,
              "endpoints": "exact active salvage frame zero and swim-carry frame zero",
              "rejectedFirstPose": f"review/{direction}/000-generated-not-installed.png",
              "status": "candidate_not_installed"}
    (review / "registration.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


if __name__ == "__main__":
    palette = palette_module()
    records = [make(direction, palette) for direction in ("south", "north", "east", "west")]
    (BASE / "registration.json").write_text(json.dumps(records, indent=2) + "\n")
    print("Registered", len(records), "underwater pickup directions")
