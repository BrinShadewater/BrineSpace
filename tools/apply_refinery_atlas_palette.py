"""Create the Ore Refinery machinery atlas with restrained burnt-orange paint."""
import colorsys
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "rooms/production-ten/ore_refinery-source-v1.png"
OUTPUT = ROOT / "rooms/production-ten/ore_refinery-source-v2.png"
EXPECTED_SHA256 = "f6b88ce8fe1d69e290da77c8863a78f796b27cf52cefc4dcc65a0c39a371edd8"


def main() -> None:
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != EXPECTED_SHA256:
        raise ValueError("Refinery atlas changed; review the new source before applying the recorded palette mask")
    image = Image.open(SOURCE).convert("RGB")
    rgb = np.asarray(image).astype(np.float32) / 255.0
    hsv = np.array([colorsys.rgb_to_hsv(*pixel) for pixel in rgb.reshape(-1, 3)], dtype=np.float32)
    selected = (
        (hsv[:, 0] >= 0.015)
        & (hsv[:, 0] < 0.095)
        & (hsv[:, 1] >= 0.48)
        & (hsv[:, 2] >= 0.34)
    )
    hsv[selected, 0] *= 0.93
    hsv[selected, 1] *= 0.78
    hsv[selected, 2] *= 0.76
    revised = np.array([colorsys.hsv_to_rgb(*pixel) for pixel in hsv], dtype=np.float32)
    revised = np.clip(np.round(revised.reshape(rgb.shape) * 255.0), 0, 255).astype(np.uint8)
    Image.fromarray(revised, "RGB").save(OUTPUT)
    record = {
        "source": SOURCE.relative_to(ROOT).as_posix(),
        "source_sha256": EXPECTED_SHA256,
        "output": OUTPUT.relative_to(ROOT).as_posix(),
        "output_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "changed_pixels": int(selected.sum()),
        "total_pixels": int(selected.size),
        "rule": "Match the directional wall bank: mute saturated orange paint toward burnt orange while retaining yellow logistics marks and lower-saturation ore/copper materials.",
    }
    record_path = ROOT / "assets/refinery-directional-v2/atlas-palette-repair.json"
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
