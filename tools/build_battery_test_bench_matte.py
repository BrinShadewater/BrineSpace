"""Reduce glossy highlights on the live Battery Array test bench."""
from __future__ import annotations

import colorsys
import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "rooms/production-ten/decor/battery-test-bench-clean-v2.png"
OUTPUT = ROOT / "rooms/production-ten/decor/battery-test-bench-matte-v1.png"
RECORD = ROOT / "rooms/production-ten/decor/battery-test-bench-matte-v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    image = Image.open(SOURCE).convert("RGBA")
    pixels = image.load()
    steel_pixels = 0
    orange_pixels = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            changed = False
            # Flatten broad charcoal/steel work surfaces while leaving the lamp
            # lens and analog meter face readable above the tabletop.
            if 246 <= y <= 856 and s <= 0.22 and 0.48 <= v <= 0.90:
                v = 0.48 + (v - 0.48) * 0.58
                s *= 0.90
                steel_pixels += 1
                changed = True
            # Burnt-orange hardware remains the department cue, but it no longer
            # carries polished, near-emissive peaks.
            if (h <= 0.12 or h >= 0.98) and s >= 0.42 and v >= 0.48:
                v = 0.48 + (v - 0.48) * 0.68
                s *= 0.88
                orange_pixels += 1
                changed = True
            if changed:
                nr, ng, nb = colorsys.hsv_to_rgb(h, s, v)
                pixels[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255), a)
    image.save(OUTPUT)
    RECORD.write_text(
        json.dumps(
            {
                "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
                "source_sha256": sha(SOURCE),
                "output": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"),
                "output_sha256": sha(OUTPUT),
                "operation": "semantic highlight compression; geometry and alpha unchanged",
                "steel_pixels_compressed": steel_pixels,
                "orange_pixels_compressed": orange_pixels,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
