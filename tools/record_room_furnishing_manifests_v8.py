"""Record v8 dependencies in the owning room manifests."""

from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPDATES = {
    "maintenance_bay": ("rooms/production-ten/manifest.json", "rooms/production-ten/decor/maintenance-composition-v5.json"),
    "storage_bay": ("rooms/production-ten/manifest.json", "rooms/production-ten/decor/storage-composition-v6.json"),
    "data_archive": ("rooms/underwater/batch-two/export-manifest.json", "rooms/underwater/batch-two/archive-composition-v4.json"),
}

def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()

def main() -> None:
    grouped: dict[str, list[tuple[str, str]]] = {}
    for room, (manifest, profile) in UPDATES.items(): grouped.setdefault(manifest, []).append((room, profile))
    for manifest_path, changes in grouped.items():
        path = ROOT / manifest_path; records = json.loads(path.read_text(encoding="utf-8-sig")); by_id = {r["id"]: r for r in records}
        for room, profile_path in changes:
            record = by_id[room]; profile = json.loads((ROOT / profile_path).read_text(encoding="utf-8"))
            declared = {x["path"].removeprefix("res://").replace("\\", "/"): x for x in record.get("component_assets", [])}
            for texture in profile.get("textures", {}).values():
                relative = texture.removeprefix("res://").replace("\\", "/"); declared[relative] = {"path": relative, "sha256": digest(relative)}
            for item in profile.get("furniture", []):
                registration = item.get("registration", "").removeprefix("res://").replace("\\", "/")
                if registration: declared[registration] = {"path": registration, "sha256": digest(registration)}
            record["component_assets"] = list(declared.values()); record["composition_profile"] = profile_path; record["composition_assets"] = [{"path": profile_path, "sha256": digest(profile_path)}]
            card = f"assets/room-furnishings-v8/cards/{room}.png"; record.setdefault("integration", {})["card"] = card; record["card"] = {"path": card, "sha256": digest(card)}
            record.setdefault("verification", {})["furnishing_v8"] = "Native four-orientation review and route evidence recorded in assets/room-furnishings-v8/manifest.json; owner acceptance pending."
        path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8"); print(f"Updated {manifest_path}: {len(changes)} room records")

if __name__ == "__main__": main()
