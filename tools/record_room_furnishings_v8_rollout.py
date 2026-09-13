"""Record the service/logistics furnishing batch in the organic-room rollout ledger."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/ORGANIC_ROOM_ROLLOUT.json"
ROOMS = {
    "maintenance_bay": ["maintenance_component_rebuild_cradle", "universal_fastener_drawer_chest"],
    "storage_bay": ["storage_cargo_sorting_island", "universal_folded_handling_dolly"],
    "data_archive": ["archive_media_restoration_table", "universal_sealed_media_transit_case"],
}

def main() -> None:
    data = json.loads(LEDGER.read_text(encoding="utf-8-sig")); records = {r["id"]: r for r in data["rooms"]}
    evidence = ["assets/room-furnishings-v8/manifest.json", "output/room-furnishings-v8/native-v4/runtime.json", "output/room-furnishings-v8/verification.json", "output/test-runs/20260913-021608-headless"]
    note = "Service/logistics furnishing v8 is selected and reviewed in four native orientations; owner aesthetic acceptance and a new export remain pending."
    for room, assets in ROOMS.items():
        record = records[room]; current = record.setdefault("evidence", [])
        for path in evidence:
            if path not in current: current.append(path)
        furnishing_assets = record.setdefault("furnishing_assets", [])
        for asset in assets:
            if asset not in furnishing_assets: furnishing_assets.append(asset)
        record["composition_phase"] = "service_logistics_furnishing_v8_native_verified"; record["status"] = "integrated_native_reviewed_owner_acceptance_pending"
        limitations = record.get("limitations", "")
        if isinstance(limitations, list):
            if note not in limitations: limitations.append(note)
        elif note not in limitations: record["limitations"] = (limitations.rstrip() + " " + note).strip()
    data["room_furnishings_v8"] = {"handoff": "docs/ROOM_FURNISHINGS_V8_2026-09-13.md", "manifest": "assets/room-furnishings-v8/manifest.json", "assets": 6, "themed": 3, "universal": 3, "large": 3, "medium": 3, "rooms": 3, "native_orientations": 12, "owner_acceptance": False}
    LEDGER.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8"); print("Recorded room furnishings v8 in three rollout records")

if __name__ == "__main__": main()
