"""Build four Crew Hab berth directions from the accepted three-berth south source."""
from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/room-facing-repair-v4/crew-hab-berth-wall-south.png"
PACK = ROOT / "assets/crew-hab-directional-v2"
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
        "method": "Border-connected neutral cleanup; exact quarter-turn transparent raster from accepted south three-berth source",
        "region": [left, top, right - left, bottom - top],
        "pieces": [[[left, top], [right, top], [right, bottom], [left, bottom]]],
        "direction": direction,
        "wall_contact": {"side": direction, "purpose": "Berth backing against wall; mattress and pillow access toward room interior"},
    }


def main() -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    image, removed = remove_exterior_neutral(Image.open(SOURCE))
    directions = {
        "south": image,
        "north": image.transpose(Image.Transpose.ROTATE_180),
        "east": image.transpose(Image.Transpose.ROTATE_90),
        "west": image.transpose(Image.Transpose.ROTATE_270),
    }
    targets = {
        "north": "crew-hab-berth-wall.json",
        "east": "side-crew-hab-berth-wall-east.json",
        "south": "side-crew-hab-berth-wall-south.json",
        "west": "side-crew-hab-berth-wall-west.json",
    }
    paths = {}
    for direction, output in directions.items():
        path = PACK / f"{direction}-overhead.png"
        output.save(path)
        paths[direction] = path
        (REG_DIR / targets[direction]).write_text(json.dumps(registration(path, direction), indent=2) + "\n", encoding="utf-8")
    build = {
        "room": "crew_hab",
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": sha(SOURCE),
        "border_neutral_pixels_removed": removed,
        "operation": "accepted south three-berth source plus exact quarter turns",
        "directions": {d: {"path": str(p.relative_to(ROOT)).replace("\\", "/"), "sha256": sha(p)} for d, p in paths.items()},
    }
    (PACK / "directional-build.json").write_text(json.dumps(build, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
