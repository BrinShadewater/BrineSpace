"""Record the clinical/biology furnishing batch in the organic-room rollout ledger."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/ORGANIC_ROOM_ROLLOUT.json"
ROOMS = {
    "life_support": ["life_atmosphere_analysis_island", "universal_filter_cassette_chest"],
    "med_bay": ["med_sterile_triage_island", "universal_enclosed_equipment_cart"],
    "bio_lab": ["bio_culture_preparation_island", "universal_specimen_transit_case"],
}

def main() -> None:
    data = json.loads(LEDGER.read_text(encoding="utf-8-sig"))
    records = {record["id"]: record for record in data["rooms"]}
    evidence = ["assets/room-furnishings-v7/manifest.json", "output/room-furnishings-v7/native-v2/runtime.json", "output/room-furnishings-v7/verification.json", "output/test-runs/20260913-014953-headless"]
    note = "Clinical/biology furnishing v7 is selected and reviewed in four native orientations; owner aesthetic acceptance and a new export remain pending."
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
        record["composition_phase"] = "clinical_biology_furnishing_v7_native_verified"
        record["status"] = "integrated_native_reviewed_owner_acceptance_pending"
        limitations = record.get("limitations", "")
        if isinstance(limitations, list):
            if note not in limitations:
                limitations.append(note)
        elif note not in limitations:
            record["limitations"] = (limitations.rstrip() + " " + note).strip()
    data["room_furnishings_v7"] = {"handoff": "docs/ROOM_FURNISHINGS_V7_2026-09-13.md", "manifest": "assets/room-furnishings-v7/manifest.json", "assets": 6, "themed": 3, "universal": 3, "large": 3, "medium": 3, "rooms": 3, "native_orientations": 12, "owner_acceptance": False}
    LEDGER.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Recorded room furnishings v7 in three rollout records")

if __name__ == "__main__":
    main()
