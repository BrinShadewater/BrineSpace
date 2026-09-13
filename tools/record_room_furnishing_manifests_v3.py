"""Record v3 furnishing dependencies in manifests that own composition profiles."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPDATES = {
    "ore_refinery": ("rooms/production-ten/manifest.json", "rooms/production-ten/decor/refinery-composition-v4.json", "refinery_sorting_bench"),
    "quarantine_cell": ("rooms/production-ten/manifest.json", "rooms/production-ten/decor/quarantine-composition-v4.json", "universal_parts_chest"),
    "cryo_chamber": ("rooms/underwater/batch-two/export-manifest.json", "rooms/underwater/batch-two/cryo-composition-v3.json", "cryo_thaw_cart"),
    "pressure_control": ("rooms/underwater/rare-dead-ends/pressure-manifest.json", "rooms/underwater/rare-dead-ends/pressure-composition-v2.json", "universal_equipment_plinth"),
    "isolation_vault": ("rooms/underwater/rare-dead-ends/isolation-manifest.json", "rooms/underwater/rare-dead-ends/isolation-composition-v2.json", "universal_task_table"),
}


def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def main() -> None:
    grouped: dict[str, list[tuple[str, str, str]]] = {}
    for room, (manifest, profile, asset_id) in UPDATES.items(): grouped.setdefault(manifest, []).append((room, profile, asset_id))
    for manifest, changes in grouped.items():
        path = ROOT / manifest
        records = json.loads(path.read_text(encoding="utf-8-sig"))
        by_id = {record["id"]: record for record in records}
        for room, profile_path, asset_id in changes:
            record = by_id[room]
            profile = json.loads((ROOT / profile_path).read_text(encoding="utf-8"))
            declared = {item["path"].replace("\\", "/"): item for item in record.get("component_assets", [])}
            for texture in profile.get("textures", {}).values():
                asset = texture.removeprefix("res://").replace("\\", "/")
                declared[asset] = {"path": asset, "sha256": digest(asset)}
            furnishing = next(item for item in profile["furniture"] if item["id"] == asset_id)
            registration = furnishing["registration"].removeprefix("res://")
            declared[registration] = {"path": registration, "sha256": digest(registration)}
            record["component_assets"] = list(declared.values())
            record["composition_profile"] = profile_path
            record["composition_assets"] = [{"path": profile_path, "sha256": digest(profile_path)}]
            record.setdefault("verification", {})["furnishing_v3"] = (
                "Native four-orientation review and route evidence recorded in assets/room-furnishings-v3/manifest.json; owner acceptance pending."
            )
        path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
        print(f"Updated {manifest}: {len(changes)} room records")


if __name__ == "__main__":
    main()
