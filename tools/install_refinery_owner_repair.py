"""Install reviewed refinery v2 pixels on existing imported runtime paths."""
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COPIES = {
    "assets/refinery-directional-v2/refinery-north.png": "assets/refinery-directional-v1/refinery-north.png",
    "assets/refinery-directional-v2/refinery-sides.png": "assets/refinery-directional-v1/refinery-sides.png",
    "assets/refinery-directional-v2/refinery-south.png": "assets/refinery-directional-v1/refinery-south.png",
}
REGISTRATIONS = {
    "rooms/full-wall-v1/registrations/ore-refinery-wall.json": "assets/refinery-directional-v1/refinery-north.png",
    "rooms/full-wall-v1/registrations/side-ore-refinery-wall-east.json": "assets/refinery-directional-v1/refinery-sides.png",
    "rooms/full-wall-v1/registrations/side-ore-refinery-wall-west.json": "assets/refinery-directional-v1/refinery-sides.png",
    "rooms/full-wall-v1/registrations/side-ore-refinery-wall-south.json": "assets/refinery-directional-v1/refinery-south.png",
}

for source, destination in COPIES.items():
    shutil.copyfile(ROOT / source, ROOT / destination)

for registration, source in REGISTRATIONS.items():
    path = ROOT / registration
    data = json.loads(path.read_text())
    data["source"] = "res://" + source
    data["sha256"] = hashlib.sha256((ROOT / source).read_bytes()).hexdigest()
    old_area = data["owner_repair"].pop("exterior_neutral_area_removed", None)
    if old_area is not None:
        data["owner_repair"]["registration_area_delta_after_1px_simplify"] = round(-float(old_area), 3)
    data["owner_repair"]["runtime_install"] = "Repaired v2 pixels installed on the existing imported v1 texture path."
    path.write_text(json.dumps(data, separators=(",", ":")) + "\n")

provenance_path = ROOT / "assets/refinery-directional-v2/owner-repair.json"
provenance = json.loads(provenance_path.read_text())
provenance["runtime_install"] = {destination: source for source, destination in COPIES.items()}
for record in provenance["registrations"]:
    data = json.loads((ROOT / record["registration"]).read_text())
    record.pop("removed_area", None)
    record["registration_area_delta"] = data["owner_repair"]["registration_area_delta_after_1px_simplify"]
provenance_path.write_text(json.dumps(provenance, indent=2) + "\n")
print("Installed refinery owner repair on three existing runtime texture paths")
