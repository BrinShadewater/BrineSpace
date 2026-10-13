"""Register Marsh's controller poses and derive the connected maintenance chain."""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from prepare_marsh_carry_chain import palette_module
from prepare_marsh_salvage_match import components


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "character/marsh-maintenance-match-v1"
BARE = ROOT / "character/marsh-v2/frames/bare"
DIRECTIONS = ("south", "north", "east", "west")


def foot_center(image):
    alpha = np.asarray(image.getchannel("A")) > 40
    ys, _ = np.where(alpha)
    bottom = int(ys.max()) + 1
    _, xs = np.where(alpha[max(0, bottom - max(2, round((bottom - ys.min()) * .06))):bottom])
    return (int(xs.min()) + int(xs.max()) + 1) / 2, bottom


def save_review(direction, rows):
    review = BASE / "review" / direction
    review.mkdir(parents=True, exist_ok=True)
    row = rows[f"interact-{direction}"]
    contact = Image.new("RGB", (184 * 6, 205), "#21272c")
    draw = ImageDraw.Draw(contact)
    frames = []
    for i, image in enumerate(row):
        contact.paste(image, (184 * i, 0), image)
        draw.text((184 * i + 4, 187), str(i), fill="white")
        canvas = Image.new("RGB", (240, 210), "#21272c")
        canvas.paste(image, (28, 12), image)
        frames.append(canvas)
    contact.save(review / "contact.png")
    frames[0].save(review / "interact.gif", save_all=True, append_images=frames[1:],
                   duration=[150] * 5 + [450], loop=0)
    chain = []
    for sample in range(180):
        t = sample / 30
        action = "kneel" if t < 1 else "repair" if t < 5 else "stand"
        elapsed = t if t < 1 else t - 1 if t < 5 else t - 5
        phase = min(5, int((elapsed % .9) / .15)) if action == "repair" else min(2, int(elapsed / .2))
        canvas = Image.new("RGB", (240, 210), "#21272c")
        image = rows[f"{action}-{direction}"][phase]
        canvas.paste(image, (28, 12), image)
        chain.append(canvas)
    chain[0].save(review / "maintenance.gif", save_all=True, append_images=chain[1:], duration=33, loop=0)


def make(direction, palette):
    revision = "02" if direction == "north" else "01"
    source_path = BASE / "sources" / f"{direction}-sheet-{revision}.png"
    source = Image.open(source_path).convert("RGBA")
    parts, labels = components(source)
    idle_path = BARE / f"idle-{direction}/000.png"
    idle = Image.open(idle_path).convert("RGBA")
    idle_box = idle.getchannel("A").getbbox()
    first = parts[0][1]
    scale = (idle_box[3] - idle_box[1]) / (first[3] - first[1])
    anchor_x, bottom = foot_center(idle)
    folder = BASE / "frames" / f"interact-{direction}"
    review = BASE / "review" / direction
    folder.mkdir(parents=True, exist_ok=True)
    review.mkdir(parents=True, exist_ok=True)
    for phase in (0, 5):
        (folder / f"{phase:03}.png").write_bytes(idle_path.read_bytes())
    records = []
    for phase in range(1, 5):
        component, box = parts[phase]
        x0, y0, x1, y1 = box
        data = np.asarray(source.crop(box)).copy()
        data[labels[y0:y1, x0:x1] != component] = 0
        sprite = Image.fromarray(data, "RGBA")
        source_anchor, _ = foot_center(sprite)
        size = (round(sprite.width * scale), round(sprite.height * scale))
        sprite = sprite.resize(size, Image.Resampling.LANCZOS)
        position = (round(anchor_x - source_anchor * scale), bottom - size[1])
        image = Image.new("RGBA", (184, 184))
        image.alpha_composite(sprite, position)
        data = np.asarray(image).copy()
        data[:, :, 3] = np.where(data[:, :, 3] >= 80, 255, 0).astype(np.uint8)
        image = Image.fromarray(data, "RGBA")
        bounds = image.getchannel("A").getbbox()
        if min(bounds[0], bounds[1], 184 - bounds[2], 184 - bounds[3]) < 2:
            raise ValueError(f"Clipped {direction} phase {phase}: {bounds}")
        unmapped = review / f"{phase:03}-unmapped.png"
        target = folder / f"{phase:03}.png"
        image.save(unmapped)
        if target.exists():
            target.unlink()
        palette.map_file("marsh", unmapped, target)
        records.append({"phase": phase, "component": component, "sourceBox": box,
                        "scale": scale, "sourceFootCenter": source_anchor,
                        "idleFootCenter": anchor_x, "position": position, "bounds": bounds})
    interact = [Image.open(folder / f"{i:03}.png").convert("RGBA") for i in range(6)]
    work_order = [2, 1, 2, 3, 2, 2] if direction == "east" else [2, 3, 2, 1, 2, 2]
    rows = {f"interact-{direction}": interact,
            f"kneel-{direction}": [interact[0], interact[4], interact[2]],
            f"repair-{direction}": [interact[i] for i in work_order],
            f"stand-{direction}": [interact[2], interact[4], interact[0]]}
    for key, row in rows.items():
        out = BASE / "frames" / key
        out.mkdir(parents=True, exist_ok=True)
        for phase, image in enumerate(row):
            if key.startswith("interact-"):
                continue
            image.save(out / f"{phase:03}.png")
    save_review(direction, rows)
    record = {"direction": direction, "source": source_path.relative_to(ROOT).as_posix(),
              "sourceSha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
              "poses": records, "scale": scale, "registration": "Planted boot center and bottom; fixed scale across row",
              "draw": ["exact idle", 4, 2], "work": work_order, "stow": [2, 4, "exact idle"],
              "rejectedSource": "north-sheet-01.png" if direction == "north" else None}
    (review / "registration.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


if __name__ == "__main__":
    palette = palette_module()
    records = [make(direction, palette) for direction in DIRECTIONS]
    (BASE / "registration.json").write_text(json.dumps(records, indent=2) + "\n")
    print("Registered 72 action frames across four directions; exact shared joins")
