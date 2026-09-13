"""Build four exact Xeno containment directions from one reviewed overhead source."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets/xeno-directional-v2"
CANONICAL = PACK / "north-overhead.png"
REG_DIR = ROOT / "rooms/full-wall-v1/registrations"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def registration(path: Path, direction: str) -> dict:
    with Image.open(path) as image:
        bbox = image.getchannel("A").getbbox()
    assert bbox is not None
    left, top, right, bottom = bbox
    return {
        "source": "res://" + str(path.relative_to(ROOT)).replace("\\", "/"),
        "sha256": sha(path),
        "method": "Transparent alpha registration from one strict-overhead canonical source; exact quarter-turn raster",
        "region": [left, top, right - left, bottom - top],
        "pieces": [[[left, top], [right, top], [right, bottom], [left, bottom]]],
        "direction": direction,
        "wall_contact": {
            "side": direction,
            "purpose": "Rear service rail against wall; glove ports, controls and access edge inward",
        },
    }


def main() -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    image = Image.open(CANONICAL).convert("RGBA")
    directions = {
        "north": image,
        "east": image.transpose(Image.Transpose.ROTATE_270),
        "south": image.transpose(Image.Transpose.ROTATE_180),
        "west": image.transpose(Image.Transpose.ROTATE_90),
    }
    paths = {}
    for direction, output in directions.items():
        path = PACK / f"{direction}-overhead.png"
        output.save(path)
        paths[direction] = path

    targets = {
        "north": REG_DIR / "xeno-containment-wall.json",
        "east": REG_DIR / "side-xeno-containment-wall-east.json",
        "south": REG_DIR / "side-xeno-containment-wall-south.json",
        "west": REG_DIR / "side-xeno-containment-wall-west.json",
    }
    for direction, target in targets.items():
        target.write_text(json.dumps(registration(paths[direction], direction), indent=2) + "\n", encoding="utf-8")

    build = {
        "room": "xeno_lab",
        "canonical": "assets/xeno-directional-v2/north-overhead.png",
        "canonical_sha256": sha(CANONICAL),
        "operation": "exact clockwise quarter turns from one strict-overhead north source",
        "directions": {d: {"path": str(p.relative_to(ROOT)).replace("\\", "/"), "sha256": sha(p)} for d, p in paths.items()},
    }
    (PACK / "directional-build.json").write_text(json.dumps(build, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
