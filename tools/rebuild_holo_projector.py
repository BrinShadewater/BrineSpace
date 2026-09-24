"""Normalize the preserved generated housing; never modify the bought atlas."""
from pathlib import Path
from PIL import Image
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/holo-projector-v1"


def rebuild():
    source = ASSETS / "source.png"
    image = Image.open(source).convert("RGBA")
    # Discard near-transparent generation residue, retaining real edge alpha.
    alpha = image.getchannel("A").point(lambda value: 0 if value < 8 else value)
    image.putalpha(alpha)
    crop = alpha.getbbox()
    housing = image.crop(crop)
    housing.thumbnail((256, 128), Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", (256, 240))
    canvas.alpha_composite(housing, ((256 - housing.width) // 2, 96))
    canvas.save(ASSETS / "projector.png")
    record = {
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "source_size": list(image.size), "alpha_crop": list(crop),
        "housing_size": list(housing.size), "canvas_size": [256, 240],
        "normalization": "alpha below 8 removed; nearest fit 256x128; housing at y96",
        "purpose": "Transparent upper region reserves runtime projection bounds; housing is static.",
    }
    (ASSETS / "provenance.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record))


if __name__ == "__main__":
    rebuild()
