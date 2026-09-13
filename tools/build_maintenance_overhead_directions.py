"""Build four muted overhead Maintenance wall directions from the accepted south bank."""
from __future__ import annotations

import colorsys
import hashlib
import json
from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/room-facing-repair-v2/maintenance-repair-wall-south.png"
PACK = ROOT / "assets/maintenance-directional-v2"
REG_DIR = ROOT / "rooms/full-wall-v1/registrations"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exterior_neutral_to_alpha(image: Image.Image) -> tuple[Image.Image, int]:
    image = image.convert("RGBA")
    px = image.load()
    seen = set()
    queue = deque()
    for x in range(image.width):
        queue.extend(((x, 0), (x, image.height - 1)))
    for y in range(image.height):
        queue.extend(((0, y), (image.width - 1, y)))
    removed = 0
    while queue:
        x, y = queue.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        r, g, b, a = px[x, y]
        if a == 0 or min(r, g, b) < 228 or max(r, g, b) - min(r, g, b) > 22:
            continue
        px[x, y] = (r, g, b, 0)
        removed += 1
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < image.width and 0 <= ny < image.height:
                queue.append((nx, ny))
    return image, removed


def mute_orange(image: Image.Image) -> tuple[Image.Image, int]:
    px = image.load()
    changed = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if 0.025 <= h <= 0.125 and s >= 0.38 and v >= 0.18:
                nr, ng, nb = colorsys.hsv_to_rgb(h, s * 0.76, v * 0.70)
                px[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255), a)
                changed += 1
    return image, changed


def registration(path: Path, direction: str) -> dict:
    image = Image.open(path).convert("RGBA")
    left, top, right, bottom = image.getchannel("A").getbbox()
    return {
        "source": "res://" + str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": sha(path),
        "method": "Border-connected neutral cleanup and semantic orange mute; exact quarter-turn transparent raster",
        "region": [left, top, right - left, bottom - top],
        "pieces": [[[left, top], [right, top], [right, bottom], [left, bottom]]],
        "direction": direction,
        "wall_contact": {"side": direction, "purpose": "Backing against wall; tool grips, vise and drawer handles inward"},
    }


def main() -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    image, removed = exterior_neutral_to_alpha(Image.open(SOURCE))
    image, changed = mute_orange(image)
    # Canonical source is south-facing; exact turns preserve every tool and control.
    directions = {
        "south": image,
        "north": image.transpose(Image.Transpose.ROTATE_180),
        "east": image.transpose(Image.Transpose.ROTATE_90),
        "west": image.transpose(Image.Transpose.ROTATE_270),
    }
    targets = {
        "north": "maintenance-repair-wall.json",
        "east": "side-maintenance-repair-wall-east.json",
        "south": "side-maintenance-repair-wall-south.json",
        "west": "side-maintenance-repair-wall-west.json",
    }
    paths = {}
    for direction, output in directions.items():
        path = PACK / f"{direction}-overhead.png"
        output.save(path)
        paths[direction] = path
        (REG_DIR / targets[direction]).write_text(json.dumps(registration(path, direction), indent=2) + "\n", encoding="utf-8")
    build = {
        "room": "maintenance_bay",
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": sha(SOURCE),
        "border_neutral_pixels_removed": removed,
        "orange_pixels_muted": changed,
        "operation": "south exemplar plus exact quarter turns",
        "directions": {d: {"path": str(p.relative_to(ROOT)).replace("\\", "/"), "sha256": sha(p)} for d, p in paths.items()},
    }
    (PACK / "directional-build.json").write_text(json.dumps(build, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
