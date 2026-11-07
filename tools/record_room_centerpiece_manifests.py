"""Record selected centerpiece profiles and raster hashes in owning room manifests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPDATES = {
    "battery_array": (
        "rooms/production-ten/manifest.json",
        "rooms/production-ten/decor/battery-composition-v5.json",
        ["battery-charge-equalizer", "battery-capacitor-dolly"],
    ),
    "maintenance_bay": (
        "rooms/production-ten/manifest.json",
        "rooms/production-ten/decor/maintenance-composition-v4.json",
        ["maintenance-repair-gantry"],
    ),
    "storage_bay": (
        "rooms/production-ten/manifest.json",
        "rooms/production-ten/decor/storage-composition-v5.json",
        ["storage-cargo-carousel"],
    ),
    "radio_lab": (
        "rooms/underwater/acoustic-comms/manifest.json",
        "rooms/underwater/acoustic-comms/radio-composition-v4.json",
        ["radio-signal-console"],
    ),
    "shield_generator": (
        "rooms/underwater/hull-integrity/manifest.json",
        "rooms/underwater/hull-integrity/hull-composition-v4.json",
        ["shield-emitter-bench"],
    ),
    "solar_array": (
        "rooms/underwater/thermal-control/manifest.json",
        "rooms/underwater/thermal-control/thermal-composition-v3.json",
        ["solar-conversion-island", "solar-junction-cart"],
    ),
}


def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def main() -> None:
    grouped: dict[str, list[tuple[str, str, list[str]]]] = {}
    for room, (manifest, profile, assets) in UPDATES.items():
        grouped.setdefault(manifest, []).append((room, profile, assets))
    for manifest, changes in grouped.items():
        path = ROOT / manifest
        records = json.loads(path.read_text(encoding="utf-8-sig"))
        by_id = {record["id"]: record for record in records}
        for room, profile, names in changes:
            record = by_id[room]
            record["composition_profile"] = profile
            record["composition_assets"] = [{"path": profile, "sha256": digest(profile)}]
            declared = {item["path"].replace("\\", "/"): item for item in record.get("component_assets", [])}
            selected = json.loads((ROOT / profile).read_text(encoding="utf-8"))
            for texture in selected.get("textures", {}).values():
                asset = texture.removeprefix("res://").replace("\\", "/")
                declared[asset] = {"path": asset, "sha256": digest(asset)}
            for name in names:
                registration = f"assets/room-centerpieces-v1/{name}-registration.json"
                declared[registration] = {"path": registration, "sha256": digest(registration)}
            record["component_assets"] = list(declared.values())
            record.setdefault("verification", {})["centerpiece_asset_pass"] = (
                "Native four-orientation review and route evidence recorded in "
                "docs/ROOM_CENTERPIECE_ASSET_PASS_2026-09-12.md; owner acceptance pending."
            )
        path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
        print(f"Updated {manifest}: {len(changes)} room records")


if __name__ == "__main__":
    main()
