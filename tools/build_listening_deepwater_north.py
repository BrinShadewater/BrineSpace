"""Build the Listening Post north wall from the accepted south Deepwater bank."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/rooms/listening-post/walls/south.png"
SOURCE_REG = ROOT / "rooms/full-wall-v1/registrations/side-deepwater-listening-wall-south.json"
OUTPUT = ROOT / "assets/rooms/listening-post/walls/north.png"
OUTPUT_REG = ROOT / "rooms/full-wall-v1/registrations/deepwater-listening-wall.json"


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCE) as image:
        width, height = image.size
        image.rotate(180).save(OUTPUT)

    data = json.loads(SOURCE_REG.read_text(encoding="utf-8"))
    x, y, w, h = data["region"]
    data["source"] = "res://assets/rooms/listening-post/walls/north.png"
    data["sha256"] = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    data["method"] = "Exact 180-degree rotation of accepted south Deepwater bank; exterior-neutral vector registration rotated with raster"
    data["region"] = [width - x - w, height - y - h, w, h]
    data["pieces"] = [
        [[width - px, height - py] for px, py in polygon]
        for polygon in data["pieces"]
    ]
    data["direction"] = "north"
    data["wall_contact"] = {
        "side": "north",
        "purpose": "Rear pipe rail flush north; keyboard spacebar and cup handles inward",
    }
    OUTPUT_REG.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    provenance = {
        "room": "listening_post",
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "output": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"),
        "output_sha256": data["sha256"],
        "operation": "exact 180-degree rotation",
        "reason": "Match the accepted Side Deepwater Listening Walls family with an inward-facing north bank.",
    }
    (OUTPUT.parent / "directional-build.json").write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
