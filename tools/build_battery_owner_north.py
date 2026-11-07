"""Separate and key the owner-directed low overhead Battery north banks."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image

root = Path(__file__).resolve().parents[1]
pack = root / "assets/battery-owner-v3"
raw = pack / "north-raw.png"
image = Image.open(raw).convert("RGBA")
pixels = np.array(image)
rgb = pixels[:, :, :3].astype(int)
pixels[(rgb[:, :, 0] - rgb[:, :, 1] > 35) & (rgb[:, :, 2] - rgb[:, :, 1] > 35)] = 0
clean = Image.fromarray(pixels)
records = []
for name, region in [("cells", (0, 0, 1010, image.height)), ("distribution", (1010, 0, image.width, image.height))]:
    part = clean.crop(region)
    crop = part.getbbox()
    part = part.crop(crop)
    part.save(pack / f"north-{name}.png")
    records.append({"id": name, "region": region, "crop": crop, "size": part.size})
review = {
    "source_sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
    "source_size": image.size,
    "key": "R-G>35 and B-G>35",
    "inventory": {"cells": 4, "distribution_units": 3, "gauges": 3},
    "facing": "north wall; controls face down/inward",
    "parts": records,
    "stage": "cleaned candidate; native fit and integration pending"
}
(pack / "north-review.json").write_text(json.dumps(review, indent=2) + "\n")
print(json.dumps(review))
