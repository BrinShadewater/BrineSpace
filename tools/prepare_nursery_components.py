"""Register the three component trial assets without rescaling native canvases."""
import hashlib
import json
from pathlib import Path
from PIL import Image
from room_art_pipeline import clear_exterior

root = Path(__file__).resolve().parents[1] / "rooms/modular/components-01"
manifest = root / "registration.json"
if manifest.exists():
    raise FileExistsError(manifest)
assets = {}
for name in ["growth", "reservoir", "microscope"]:
    raw = root / (name + "-raw.png")
    destination = root / (name + ".png")
    if destination.exists():
        raise FileExistsError(destination)
    with Image.open(raw) as source:
        native_alpha = source.mode == "RGBA" and source.getchannel("A").getextrema()[0] == 0
        result = source.copy() if native_alpha else clear_exterior(source)
        # Near-invisible alpha specks must not displace the ground anchor.
        bounds = result.getchannel("A").point(lambda a: 255 if a >= 128 else 0).getbbox() if native_alpha else result.getchannel("A").getbbox()
        if not bounds:
            raise ValueError(name)
        if native_alpha:
            bounds = (max(0, bounds[0]-2), max(0, bounds[1]-2), min(result.width, bounds[2]+2), min(result.height, bounds[3]+2))
        result.save(destination)
        assets[name] = {
            "file": destination.name, "bounds": list(bounds), "native_size": list(result.size),
            "enabled_in_pilot": True,
            "processing": "native alpha preserved" if native_alpha else "edge-connected light neutral removal; native canvas preserved",
            "raw_sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
            "clean_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
            "registration": "native-alpha assets: alpha>=128 bounds +2px margin, ignoring faint exterior specks; aspect-preserving contain fit, bottom-center anchor; never rotate texture",
            "directions": [0] if name == "microscope" else [0, 1, 2, 3]
        }
manifest.write_text(json.dumps({"assets": assets}, indent=2) + "\n", encoding="utf-8")
print(json.dumps(assets, indent=2))
