"""Record the second furnishing batch in the organic-room rollout ledger."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/ORGANIC_ROOM_ROLLOUT.json"
ROOMS = {
    "research_lab": "research_specimen_island",
    "command_center": "command_planning_table",
    "med_center": "medical_instrument_trolley",
    "crew_hab": "universal_storage_bench",
    "anomaly_lab": "universal_utility_cart",
    "med_office": "universal_workbench",
}


def main() -> None:
    data = json.loads(LEDGER.read_text(encoding="utf-8-sig"))
    records = {record["id"]: record for record in data["rooms"]}
    evidence = [
        "assets/room-furnishings-v2/manifest.json",
        "output/room-furnishings-v2/native-v3/runtime.json",
        "output/room-furnishings-v2/verification.json",
        "output/test-runs/20260913-001455-headless",
    ]
    note = "Themed/universal furnishing v2 is selected and reviewed in four native orientations; owner aesthetic acceptance and a new export remain pending."
    for room, asset in ROOMS.items():
        record = records[room]
        current = record.setdefault("evidence", [])
        for path in evidence:
            if path not in current:
                current.append(path)
        furnishing_assets = record.setdefault("furnishing_assets", [])
        if asset not in furnishing_assets:
            furnishing_assets.append(asset)
        record["composition_phase"] = "themed_universal_furnishing_v2_native_verified"
        record["status"] = "integrated_native_reviewed_owner_acceptance_pending"
        limitations = record.get("limitations", "")
        if isinstance(limitations, list):
            if note not in limitations:
                limitations.append(note)
        elif note not in limitations:
            record["limitations"] = (limitations.rstrip() + " " + note).strip()
    data["room_furnishings_v2"] = {
        "handoff": "docs/ROOM_FURNISHINGS_V2_2026-09-13.md",
        "manifest": "assets/room-furnishings-v2/manifest.json",
        "assets": 6,
        "themed": 3,
        "universal": 3,
        "large": 3,
        "medium": 3,
        "rooms": 6,
        "native_orientations": 24,
        "owner_acceptance": False,
    }
    LEDGER.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Recorded room furnishings v2 in six rollout records")


if __name__ == "__main__":
    main()
