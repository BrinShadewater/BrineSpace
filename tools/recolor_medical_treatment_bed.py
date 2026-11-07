"""Recolor the selected Med Bay south treatment upholstery without repainting art."""

from __future__ import annotations

import colorsys
import hashlib
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/room-facing-repair-v3/medical-treatment-wall-south.png"
OUTPUT = ROOT / "assets/med-bay-directional-v1/treatment-south-blue-v1.png"
ROI = (560, 205, 1435, 485)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if OUTPUT.exists():
        raise SystemExit(f"Refusing to overwrite {OUTPUT}")

    source = Image.open(SOURCE).convert("RGB")
    result = source.copy()
    changed = 0

    for y in range(ROI[1], ROI[3]):
        for x in range(ROI[0], ROI[2]):
            red, green, blue = source.getpixel((x, y))
            hue, saturation, value = colorsys.rgb_to_hsv(
                red / 255.0, green / 255.0, blue / 255.0
            )
            if not (0.025 <= hue <= 0.125 and saturation >= 0.24 and value >= 0.16):
                continue

            # Keep the source shading and edge texture while moving warm upholstery
            # into the established muted medical cyan family.
            target_saturation = min(0.55, max(0.32, saturation * 0.74))
            target_value = min(1.0, value * 0.72)
            recolored = colorsys.hsv_to_rgb(0.523, target_saturation, target_value)
            result.putpixel((x, y), tuple(round(channel * 255) for channel in recolored))
            changed += 1

    if result.size != source.size:
        raise AssertionError("Canvas dimensions changed")
    for y in range(source.height):
        for x in range(source.width):
            if ROI[0] <= x < ROI[2] and ROI[1] <= y < ROI[3]:
                continue
            if result.getpixel((x, y)) != source.getpixel((x, y)):
                raise AssertionError(f"Pixel outside upholstery ROI changed at {(x, y)}")
    if changed < 150_000:
        raise AssertionError(f"Unexpectedly small upholstery mask: {changed} pixels")

    result.save(OUTPUT, optimize=True)
    print(f"PASS changed={changed} size={result.size} sha256={digest(OUTPUT)}")


if __name__ == "__main__":
    main()
