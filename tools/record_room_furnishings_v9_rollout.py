"""Record the communications furnishing batch in the organic-room rollout ledger."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/ORGANIC_ROOM_ROLLOUT.json"
ROOMS = {
    "radio_lab": ["radio_signal_routing_console", "universal_patch_cable_organizer"],
    "listening_post": ["listening_hydrophone_analysis_table", "universal_rugged_power_conditioner"],
    "holographic_core": ["holo_projection_alignment_deck", "universal_instrument_calibration_case"],
}


def main() -> None:
    data = json.loads(LEDGER.read_text(encoding="utf-8-sig"))
    records = {record["id"]: record for record in data["rooms"]}
    evidence = [
        "assets/room-furnishings-v9/manifest.json",
        "output/room-furnishings-v9/native-v5/runtime.json",
        "output/room-furnishings-v9/verification.json",
        "output/test-runs/20260913-024217-headless",
    ]
    note = "Communications furnishing v9 is selected and reviewed in four native orientations; owner aesthetic acceptance and a new export remain pending."
    for room, assets in ROOMS.items():
        record = records[room]
        current = record.setdefault("evidence", [])
        for superseded in ("output/room-furnishings-v9/native-v3/runtime.json", "output/test-runs/20260913-023559-headless"):
            if superseded in current:
                current.remove(superseded)
        for path in evidence:
            if path not in current:
                current.append(path)
        furnishing_assets = record.setdefault("furnishing_assets", [])
        for asset in assets:
            if asset not in furnishing_assets:
                furnishing_assets.append(asset)
        record["composition_phase"] = "communications_furnishing_v9_native_verified"
        record["status"] = "integrated_native_reviewed_owner_acceptance_pending"
        limitations = record.get("limitations", "")
        if isinstance(limitations, list):
            if note not in limitations:
                limitations.append(note)
        elif note not in limitations:
            record["limitations"] = (limitations.rstrip() + " " + note).strip()
    data["room_furnishings_v9"] = {
        "handoff": "docs/ROOM_FURNISHINGS_V9_2026-09-13.md",
        "manifest": "assets/room-furnishings-v9/manifest.json",
        "assets": 6,
        "themed": 3,
        "universal": 3,
        "large": 3,
        "medium": 3,
        "rooms": 3,
        "native_orientations": 12,
        "owner_acceptance": False,
    }
    LEDGER.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Recorded room furnishings v9 in three rollout records")


if __name__ == "__main__":
    main()
