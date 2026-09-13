"""Build four Emergency Isolation wall directions from the accepted south bank."""
from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/isolation-directional-v1/isolation-south.png"
PACK = ROOT / "assets/isolation-directional-v2"
REG_DIR = ROOT / "rooms/full-wall-v1/registrations"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remove_exterior_neutral(source: Image.Image) -> tuple[Image.Image, int]:
    image = source.convert("RGBA")
    px = image.load()
    queue = deque()
    seen = set()
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


def registration(path: Path, direction: str) -> dict:
    image = Image.open(path).convert("RGBA")
    left, top, right, bottom = image.getchannel("A").getbbox()
    return {
        "source": "res://" + str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": sha(path),
        "method": "Accepted south Emergency Isolation bank; border-connected neutral cleanup; exact quarter turns",
        "region": [left, top, right - left, bottom - top],
        "pieces": [[[left, top], [right, top], [right, bottom], [left, bottom]]],
        "direction": direction,
        "wall_contact": {
            "side": direction,
            "purpose": "Closed chamber hinges and supply backs against wall; catches and pickup access face inward",
        },
    }


def main() -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    south, removed = remove_exterior_neutral(Image.open(SOURCE))
    bbox = south.getchannel("A").getbbox()
    south = south.crop(bbox)
    directions = {
        "south": south,
        "north": south.transpose(Image.Transpose.ROTATE_180),
        "east": south.transpose(Image.Transpose.ROTATE_90),
        "west": south.transpose(Image.Transpose.ROTATE_270),
    }
    targets = {
        "north": "emergency-isolation-wall.json",
        "east": "side-emergency-isolation-wall-east.json",
        "south": "side-emergency-isolation-wall-south.json",
        "west": "side-emergency-isolation-wall-west.json",
    }
    paths = {}
    for direction, output in directions.items():
        path = PACK / f"{direction}-overhead.png"
        output.save(path)
        paths[direction] = path
        (REG_DIR / targets[direction]).write_text(
            json.dumps(registration(path, direction), indent=2) + "\n", encoding="utf-8"
        )
    build = {
        "room": "isolation_vault",
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": sha(SOURCE),
        "accepted_source_direction": "south",
        "source_alpha_bbox": list(bbox),
        "border_neutral_pixels_removed": removed,
        "operation": "owner-approved south Emergency Isolation bank plus exact quarter turns",
        "directions": {
            d: {"path": str(p.relative_to(ROOT)).replace("\\", "/"), "sha256": sha(p)}
            for d, p in paths.items()
        },
    }
    (PACK / "directional-build.json").write_text(json.dumps(build, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
