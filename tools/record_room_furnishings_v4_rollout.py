"""Record the power-room furnishing batch in the organic-room rollout ledger."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/ORGANIC_ROOM_ROLLOUT.json"
ROOMS = {
    "current_turbine": ["current_flow_governor", "universal_instrument_cabinet"],
    "biomass_digester": ["biomass_feedstock_island", "universal_maintenance_trestle"],
    "heat_recovery": ["heat_exchanger_manifold", "universal_cable_caddy"],
}


def main() -> None:
    data = json.loads(LEDGER.read_text(encoding="utf-8-sig"))
    records = {record["id"]: record for record in data["rooms"]}
    evidence = [
        "assets/room-furnishings-v4/manifest.json",
        "output/room-furnishings-v4/native-v1/runtime.json",
        "output/room-furnishings-v4/verification.json",
        "output/test-runs/20260913-010049-headless",
    ]
    note = "Power-room furnishing v4 is selected and reviewed in four native orientations; owner aesthetic acceptance and a new export remain pending."
    for room, assets in ROOMS.items():
        record = records[room]
        current = record.setdefault("evidence", [])
        for path in evidence:
            if path not in current:
                current.append(path)
        furnishing_assets = record.setdefault("furnishing_assets", [])
        for asset in assets:
            if asset not in furnishing_assets:
                furnishing_assets.append(asset)
        record["composition_phase"] = "power_room_furnishing_v4_native_verified"
        record["status"] = "integrated_native_reviewed_owner_acceptance_pending"
        limitations = record.get("limitations", "")
        if isinstance(limitations, list):
            if note not in limitations:
                limitations.append(note)
        elif note not in limitations:
            record["limitations"] = (limitations.rstrip() + " " + note).strip()
    data["room_furnishings_v4"] = {
        "handoff": "docs/ROOM_FURNISHINGS_V4_2026-09-13.md",
        "manifest": "assets/room-furnishings-v4/manifest.json",
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
    print("Recorded room furnishings v4 in three rollout records")


if __name__ == "__main__":
    main()
