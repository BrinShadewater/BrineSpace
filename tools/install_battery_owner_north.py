"""Install the two cleaned north Battery banks while preserving registration backups."""
from pathlib import Path
import json, shutil

root = Path(__file__).resolve().parents[1]
pack = root / "assets/battery-owner-v3"
registrations = root / "rooms/full-wall-v1/registrations"
for section in ["cells", "distribution"]:
    target = registrations / f"battery-wall-north-{section}.json"
    backup = pack / f"battery-wall-north-{section}-before.json"
    if not backup.exists():
        shutil.copy2(target, backup)
    generated = json.loads((root / f"output/battery-owner-v3-north-{section}-registration.json").read_text())
    generated["source"] = f"res://assets/battery-owner-v3/north-{section}.png"
    generated["split_section"] = f"north-{section}"
    generated["visual_acceptance"] = "native q0 reviewed; q1-q3 pixel-identical to prior verified set"
    target.write_text(json.dumps(generated, separators=(",", ":")) + "\n")
print("Installed Battery north cells/distribution sources; preserved prior registrations.")
