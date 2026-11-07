"""Record v7 profile, card, and component dependencies in owning manifests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPDATES = {
    "life_support": ("rooms/whole-room/export-manifest.json", "rooms/whole-room/life-support-composition-v5.json"),
    "med_bay": ("rooms/whole-room/export-manifest.json", "rooms/whole-room/med-bay-composition-v3.json"),
    "bio_lab": ("rooms/underwater/batch-two/export-manifest.json", "rooms/underwater/batch-two/bio-composition-v3.json"),
}

def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()

def main() -> None:
    grouped: dict[str, list[tuple[str, str]]] = {}
    for room, (manifest, profile) in UPDATES.items():
        grouped.setdefault(manifest, []).append((room, profile))
    for manifest_path, changes in grouped.items():
        path = ROOT / manifest_path
        records = json.loads(path.read_text(encoding="utf-8-sig"))
        by_id = {record["id"]: record for record in records}
        for room, profile_path in changes:
            record = by_id[room]
            profile = json.loads((ROOT / profile_path).read_text(encoding="utf-8"))
            declared = {item["path"].removeprefix("res://").replace("\\", "/"): item for item in record.get("component_assets", [])}
            for texture in profile.get("textures", {}).values():
                relative = texture.removeprefix("res://").replace("\\", "/")
                declared[relative] = {"path": relative, "sha256": digest(relative)}
            for item in profile.get("furniture", []):
                registration = item.get("registration", "").removeprefix("res://").replace("\\", "/")
                if registration:
                    declared[registration] = {"path": registration, "sha256": digest(registration)}
            record["component_assets"] = list(declared.values())
            record["composition_profile"] = profile_path
            record["composition_assets"] = [{"path": profile_path, "sha256": digest(profile_path)}]
            card = f"assets/room-furnishings-v7/cards/{room}.png"
            if isinstance(record.get("integration"), dict):
                record["integration"]["card"] = card
            record["card"] = {"path": card, "sha256": digest(card)}
            record.setdefault("verification", {})["furnishing_v7"] = "Native four-orientation review and route evidence recorded in assets/room-furnishings-v7/manifest.json; owner acceptance pending."
        path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
        print(f"Updated {manifest_path}: {len(changes)} room records")

if __name__ == "__main__":
    main()
