"""Record v4 furnishing profiles, cards, and dependencies in the power-room manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "rooms/power-expansion-v1/manifest.json"
PROFILES = {
    "current_turbine": "rooms/power-expansion-v1/current_turbine-composition-v2.json",
    "biomass_digester": "rooms/power-expansion-v1/biomass_digester-composition-v2.json",
    "heat_recovery": "rooms/power-expansion-v1/heat_recovery-composition-v2.json",
}


def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def main() -> None:
    records = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    by_id = {record["id"]: record for record in records}
    for room, profile_path in PROFILES.items():
        record = by_id[room]
        profile = json.loads((ROOT / profile_path).read_text(encoding="utf-8"))
        declared = {
            item["path"].removeprefix("res://").replace("\\", "/"): item
            for item in record.get("component_assets", [])
        }
        for texture in profile.get("textures", {}).values():
            relative = texture.removeprefix("res://").replace("\\", "/")
            declared[relative] = {"path": f"res://{relative}", "sha256": digest(relative)}
        for item in profile.get("furniture", []):
            registration = item.get("registration", "").removeprefix("res://").replace("\\", "/")
            if registration:
                declared[registration] = {"path": f"res://{registration}", "sha256": digest(registration)}
        record["component_assets"] = list(declared.values())
        record["composition_assets"] = [{"path": f"res://{profile_path}", "sha256": digest(profile_path)}]
        card = f"assets/room-furnishings-v4/cards/{room}.png"
        record["card"] = {"path": f"res://{card}", "sha256": digest(card)}
        record.setdefault("verification", {})["furnishing_v4"] = (
            "Native four-orientation review and route evidence recorded in assets/room-furnishings-v4/manifest.json; owner acceptance pending."
        )
    MANIFEST.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print("Updated three power-room manifest records for furnishing v4")


if __name__ == "__main__":
    main()
