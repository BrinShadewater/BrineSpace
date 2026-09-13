"""Build one coherent Clone Growth wall family from the owner-approved east bank."""
from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/clone-directional-v1/clone-sides.png"
PACK = ROOT / "assets/clone-directional-v2"
REG_DIR = ROOT / "rooms/full-wall-v1/registrations"
# Accepted east bank recorded by side-clone-growth-wall-east.json.
EAST_CROP = (910, 17, 1227, 975)


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
        "method": "Accepted east Clone Growth bank extraction; border-connected neutral cleanup; exact quarter turns",
        "region": [left, top, right - left, bottom - top],
        "pieces": [[[left, top], [right, top], [right, bottom], [left, bottom]]],
        "direction": direction,
        "wall_contact": {
            "side": direction,
            "purpose": "Outer service rail against wall; growth chamber, microscope and controls face inward",
        },
    }


def main() -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    cleaned, removed = remove_exterior_neutral(Image.open(SOURCE))
    east = cleaned.crop(EAST_CROP)
    if east.getchannel("A").getbbox() != (0, 0, east.width, east.height):
        east = east.crop(east.getchannel("A").getbbox())
    directions = {
        "east": east,
        "north": east.transpose(Image.Transpose.ROTATE_90),
        "south": east.transpose(Image.Transpose.ROTATE_270),
        "west": east.transpose(Image.Transpose.ROTATE_180),
    }
    targets = {
        "north": "clone-growth-wall.json",
        "east": "side-clone-growth-wall-east.json",
        "south": "side-clone-growth-wall-south.json",
        "west": "side-clone-growth-wall-west.json",
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
        "room": "clone_lab",
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": sha(SOURCE),
        "accepted_source_direction": "east",
        "accepted_source_crop": list(EAST_CROP),
        "border_neutral_pixels_removed_before_crop": removed,
        "operation": "owner-approved east bank extraction plus exact quarter turns",
        "directions": {
            d: {"path": str(p.relative_to(ROOT)).replace("\\", "/"), "sha256": sha(p)}
            for d, p in paths.items()
        },
    }
    (PACK / "directional-build.json").write_text(json.dumps(build, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
