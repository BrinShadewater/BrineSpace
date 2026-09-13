"""Record the reviewed room-centerpiece pass in the organic composition ledger."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/ORGANIC_ROOM_ROLLOUT.json"
ROOMS = {
    "maintenance_bay": ["maintenance_repair_gantry"],
    "data_archive": ["archive_index_island"],
    "radio_lab": ["radio_signal_console"],
    "listening_post": ["listening_hydrophone_table"],
    "storage_bay": ["storage_cargo_carousel"],
    "battery_array": ["battery_charge_equalizer", "battery_capacitor_dolly"],
    "solar_array": ["solar_conversion_island", "solar_junction_cart"],
    "shield_generator": ["shield_emitter_bench"],
    "life_support": ["life_scrubber_trolley"],
    "holographic_core": ["holo_calibration_block"],
}


def main() -> None:
    data = json.loads(LEDGER.read_text(encoding="utf-8-sig"))
    records = {record["id"]: record for record in data["rooms"]}
    evidence = [
        "assets/room-centerpieces-v1/manifest.json",
        "output/room-centerpieces-v1/native-v6/runtime.json",
        "output/room-centerpieces-v1/verification.json",
        "output/test-runs/20260912-234904-headless",
    ]
    for room, assets in ROOMS.items():
        record = records[room]
        existing = record.setdefault("evidence", [])
        for item in evidence:
            if item not in existing:
                existing.append(item)
        record["centerpiece_assets"] = assets
        record["composition_phase"] = "large_medium_asset_pass_native_verified"
        record["status"] = "integrated_native_reviewed_owner_acceptance_pending"
        note = "Large/medium furnishing pass is selected and reviewed in four native orientations; owner aesthetic acceptance and a new export remain pending."
        limitations = record.get("limitations", "")
        if isinstance(limitations, list):
            if note not in limitations:
                limitations.append(note)
        elif note not in limitations:
            record["limitations"] = (limitations.rstrip() + " " + note).strip()
    data["centerpiece_asset_pass"] = {
        "handoff": "docs/ROOM_CENTERPIECE_ASSET_PASS_2026-09-12.md",
        "manifest": "assets/room-centerpieces-v1/manifest.json",
        "selected_assets": 12,
        "large_assets": 7,
        "medium_assets": 5,
        "square_or_rectangular_assets": 10,
        "rooms": 10,
        "native_orientations": 40,
        "owner_acceptance": False,
    }
    LEDGER.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {LEDGER.relative_to(ROOT)}: {len(ROOMS)} rooms")


if __name__ == "__main__":
    main()
