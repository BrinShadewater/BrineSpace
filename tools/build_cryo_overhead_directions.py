"""Build and register four coherent Cryo wall directions from one reviewed overhead source."""
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

from register_alpha_silhouette import register


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/cryo-directional-v2/north-overhead-v1.png"
EXPECTED_SOURCE_SHA256 = "44ff7986f6c2b3d95da72734c7df27ace71e2ac7e2c4b3500da5375fd797b33b"
DIRECTIONS = {
    "north": (0, "rooms/full-wall-v1/registrations/cryo-support-wall.json"),
    "east": (-90, "rooms/full-wall-v1/registrations/side-cryo-support-wall-east.json"),
    "south": (180, "rooms/full-wall-v1/registrations/side-cryo-support-wall-south.json"),
    "west": (90, "rooms/full-wall-v1/registrations/side-cryo-support-wall-west.json"),
}


def main() -> None:
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    expected = EXPECTED_SOURCE_SHA256 or source_hash
    if source_hash != expected:
        raise ValueError("Reviewed Cryo overhead source hash changed")
    image = Image.open(SOURCE).convert("RGBA")
    backup_dir = ROOT / "assets/cryo-directional-v2/original-registrations"
    registration_dir = ROOT / "assets/cryo-directional-v2/registrations"
    backup_dir.mkdir(parents=True, exist_ok=True)
    registration_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for direction, (degrees, live_registration) in DIRECTIONS.items():
        output = ROOT / f"assets/cryo-directional-v2/cryo-{direction}.png"
        oriented = image.rotate(degrees, expand=True)
        oriented.save(output, optimize=True)
        live_path = ROOT / live_registration
        backup = backup_dir / live_path.name
        if not backup.exists():
            shutil.copyfile(live_path, backup)
        data = register(output.relative_to(ROOT), threshold=8, min_area=1000, simplify=1.0)
        data["source"] = "res://" + output.relative_to(ROOT).as_posix()
        data["direction"] = direction
        data["wall_contact"] = {
            "side": direction,
            "purpose": "Fixed manifold backing outward; service controls and releases face inward.",
        }
        data["owner_revision"] = "cryo-directional-v2 strict overhead"
        candidate = registration_dir / live_path.name
        candidate.write_text(json.dumps(data, separators=(",", ":")) + "\n")
        shutil.copyfile(candidate, live_path)
        records.append({
            "direction": direction,
            "rotation_degrees": degrees,
            "source": data["source"],
            "sha256": data["sha256"],
            "registration": live_registration,
            "region": data["region"],
            "pieces": len(data["pieces"]),
        })
    provenance = {
        "source": SOURCE.relative_to(ROOT).as_posix(),
        "source_sha256": source_hash,
        "camera": "strict orthographic overhead",
        "facing_rule": "North source controls face south; exact 90/180 degree rotations move that working edge inward on every wall without perspective drift.",
        "directions": records,
    }
    (ROOT / "assets/cryo-directional-v2/directional-build.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(json.dumps(provenance, indent=2))


if __name__ == "__main__":
    main()
