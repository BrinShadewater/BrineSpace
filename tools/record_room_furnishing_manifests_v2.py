"""Record v2 furnishing dependencies in manifests that own composition profiles."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "rooms/production-ten/manifest.json"
PROFILES = {
    "research_lab": "rooms/production-ten/decor/research-composition-v4.json",
    "command_center": "rooms/production-ten/decor/command-composition-v4.json",
}


def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def main() -> None:
    records = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    by_id = {record["id"]: record for record in records}
    for room, profile_path in PROFILES.items():
        record = by_id[room]
        profile = json.loads((ROOT / profile_path).read_text(encoding="utf-8"))
        declared = {item["path"].replace("\\", "/"): item for item in record.get("component_assets", [])}
        for texture in profile.get("textures", {}).values():
            asset = texture.removeprefix("res://").replace("\\", "/")
            declared[asset] = {"path": asset, "sha256": digest(asset)}
        furnishing = next(item for item in profile["furniture"] if item["id"] in {"research_specimen_island", "command_planning_table"})
        registration = furnishing["registration"].removeprefix("res://")
        declared[registration] = {"path": registration, "sha256": digest(registration)}
        record["component_assets"] = list(declared.values())
        record["composition_profile"] = profile_path
        record["composition_assets"] = [{"path": profile_path, "sha256": digest(profile_path)}]
        record.setdefault("verification", {})["furnishing_v2"] = (
            "Native four-orientation review and route evidence recorded in "
            "assets/room-furnishings-v2/manifest.json; owner acceptance pending."
        )
    MANIFEST.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print("Updated production-ten manifest: 2 furnishing-v2 rooms")


if __name__ == "__main__":
    main()
