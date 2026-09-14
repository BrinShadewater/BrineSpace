"""Mute painted orange across the selected Battery Array wall family."""

from __future__ import annotations

import argparse
import colorsys
import hashlib
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "battery-north-muted-v1.png": ROOT
    / "assets/rooms/battery-array/walls/split-north.png",
    "battery-sides-muted-v1.png": ROOT
    / "assets/battery-directional-v1/side-overhead.png",
    "battery-south-muted-v1.png": ROOT
    / "assets/battery-directional-v1/battery-south.png",
}
DEFAULT_OUTPUT_DIR = ROOT / "assets/battery-directional-v2"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def recolor(source_path: Path, output_path: Path, value_scale: float) -> int:
    source = Image.open(source_path).convert("RGBA")
    result = source.copy()
    changed = 0

    for y in range(source.height):
        for x in range(source.width):
            red, green, blue, alpha = source.getpixel((x, y))
            if alpha < 10:
                continue
            hue, saturation, value = colorsys.rgb_to_hsv(
                red / 255.0, green / 255.0, blue / 255.0
            )
            if not (0.015 <= hue <= 0.13 and saturation >= 0.35 and value >= 0.18):
                continue

            # Retain the source hue, wear and lighting while lowering painted
            # orange beneath the graphite battery lids. Preserve small yellow
            # indicator pixels so functional readouts remain distinct.
            if hue >= 0.095 and saturation >= 0.62 and value >= 0.68:
                continue
            recolored = colorsys.hsv_to_rgb(
                hue,
                max(0.0, min(1.0, saturation * 0.78)),
                max(0.0, min(1.0, value * value_scale)),
            )
            result.putpixel(
                (x, y),
                (*tuple(round(channel * 255) for channel in recolored), alpha),
            )
            changed += 1

    if result.size != source.size:
        raise AssertionError("Canvas dimensions changed")
    if changed < 100_000:
        raise AssertionError(f"Unexpectedly small orange mask: {changed} pixels")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        raise SystemExit(f"Refusing to overwrite {output_path}")
    result.save(output_path, optimize=True)
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--value-scale", type=float, default=0.68)
    args = parser.parse_args()
    if not 0.1 <= args.value_scale <= 1.0:
        raise SystemExit("--value-scale must be between 0.1 and 1.0")

    for output_name, source_path in SOURCES.items():
        output_path = args.output_dir / output_name
        changed = recolor(source_path, output_path, args.value_scale)
        with Image.open(output_path) as output:
            size = output.size
        print(
            f"PASS {output_name} changed={changed} size={size} "
            f"sha256={digest(output_path)}"
        )


if __name__ == "__main__":
    main()
