"""Bring Listening Post floor equipment into the Deepwater navy/brass palette."""
from __future__ import annotations

import colorsys
import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/rooms/radio-lab/source/radio-equipment-v2.png"
OUTPUT = ROOT / "assets/rooms/listening-post/source/listening-equipment.png"


def main() -> None:
    image = Image.open(SOURCE).convert("RGBA")
    pixels = image.load()
    changed = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if a and (h < 0.055 or h > 0.96) and s > 0.30 and v > 0.12:
                # Preserve value/shading while changing the radio pack's red trim
                # to the restrained ochre/brass used by the Deepwater wall banks.
                nr, ng, nb = colorsys.hsv_to_rgb(0.105, min(s * 0.72, 0.72), v * 0.88)
                pixels[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255), a)
                changed += 1
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT)
    provenance = {
        "room": "listening_post",
        "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "output": str(OUTPUT.relative_to(ROOT)).replace("\\", "/"),
        "output_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "changed_pixels": changed,
        "operation": "HSV material-mask recolor from saturated red trim to muted ochre/brass; geometry and luminance retained",
    }
    (OUTPUT.parent / "equipment-palette-repair.json").write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
