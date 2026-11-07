"""Build the eighth themed/universal furnishing batch for service and logistics rooms."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/room-furnishings-v8"
ROOMS = {
    "maintenance_bay": {
        "source": "rooms/production-ten/decor/maintenance-composition-v4.json",
        "output": "rooms/production-ten/decor/maintenance-composition-v5.json",
        "remove": ["repair_table", "repair_task_light", "parts_trolley", "maintenance_repair_gantry"],
        "items": [
            {"id": "maintenance_component_rebuild_cradle", "asset": "maintenance-component-rebuild-cradle", "scope": "themed", "size_class": "large", "footprint": [-55, -18, 110, 36], "ground_width": 1210, "centers": [[0, 30], [-30, 0], [0, -30], [30, 0]], "centerpiece": True},
            {"id": "universal_fastener_drawer_chest", "asset": "universal-fastener-drawer-chest", "scope": "universal", "size_class": "medium", "footprint": [-30, -13, 60, 26], "ground_width": 1190, "centers": [[-115, 105], [100, 75], [110, -90], [110, 95]], "authored_anchor": True},
        ],
    },
    "storage_bay": {
        "source": "rooms/production-ten/decor/storage-composition-v5.json",
        "output": "rooms/production-ten/decor/storage-composition-v6.json",
        "remove": ["storage_packing_bench", "storage_waiting_case", "storage_task_light", "storage_staging_pallet", "storage_cargo_carousel"],
        "items": [
            {"id": "storage_cargo_sorting_island", "asset": "storage-cargo-sorting-island", "scope": "themed", "size_class": "large", "footprint": [-55, -18, 110, 36], "ground_width": 1210, "centers": [[0, 28], [-28, 0], [0, -28], [28, 0]], "centerpiece": True},
            {"id": "universal_folded_handling_dolly", "asset": "universal-folded-handling-dolly", "scope": "universal", "size_class": "medium", "footprint": [-29, -13, 58, 26], "ground_width": 1190, "centers": [[110, -60], [60, 110], [-110, 60], [-60, -110]], "authored_anchor": True},
        ],
    },
    "data_archive": {
        "source": "rooms/underwater/batch-two/archive-composition-v3.json",
        "output": "rooms/underwater/batch-two/archive-composition-v4.json",
        "remove": ["archive_service_cart", "archive_task_lamp", "archive_index_island"],
        "items": [
            {"id": "archive_media_restoration_table", "asset": "data-archive-media-restoration-table", "scope": "themed", "size_class": "large", "footprint": [-54, -17, 108, 34], "ground_width": 1210, "centers": [[0, 30], [-30, 0], [0, -30], [30, 0]], "centerpiece": True},
            {"id": "universal_sealed_media_transit_case", "asset": "universal-sealed-media-transit-case", "scope": "universal", "size_class": "medium", "footprint": [-30, -13, 60, 26], "ground_width": 1185, "centers": [[110, -45], [45, 110], [-110, 45], [-45, -110]], "authored_anchor": True},
        ],
    },
}
GENERATED = {
    "maintenance-component-rebuild-cradle": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-7c277fa6-360d-4552-8d20-77a76525590b.png",
    "storage-cargo-sorting-island": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-19c8c84c-9fca-43a5-aea8-d8a533df94a9.png",
    "data-archive-media-restoration-table": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-4acae88c-0f71-46c6-8d07-0c8a97a3fb7f.png",
    "universal-fastener-drawer-chest": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-3a73ea7a-f7ba-47f6-b2ab-c2eb00fbeb63.png",
    "universal-folded-handling-dolly": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-4ce5d6d8-f7d0-48c4-a567-9b8e00f9ab32.png",
    "universal-sealed-media-transit-case": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-454e93ce-4bea-42e9-8bf5-75b25ac3f46b.png",
}

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    manifest = {"version": 8, "prompt_record": "assets/room-furnishings-v8/prompts.md", "status": "integrated-native-reviewed-owner-acceptance-pending", "native_evidence": "output/room-furnishings-v8/native-v4/runtime.json", "native_contact_sheet": "output/room-furnishings-v8/native-v4-contact-sheet.jpg", "card_contact_sheet": "output/room-furnishings-v8/cards-sheet.jpg", "route_evidence": "output/test-runs/20260913-021608-headless", "assets": []}
    for room, spec in ROOMS.items():
        profile = json.loads((ROOT / spec["source"]).read_text(encoding="utf-8"))
        removed = set(spec["remove"])
        profile["furniture"] = [item for item in profile.get("furniture", []) if item["id"] not in removed]
        profile["mats"] = [item for item in profile.get("mats", []) if item.get("host") not in removed]
        profile["routes"] = [item for item in profile.get("routes", []) if item.get("from", {}).get("host") not in removed and item.get("to", {}).get("host") not in removed]
        for item_spec in spec["items"]:
            asset = ASSETS / f"{item_spec['asset']}.png"
            registration = ASSETS / f"{item_spec['asset']}-registration.json"
            profile.setdefault("textures", {})[item_spec["id"]] = f"res://{asset.relative_to(ROOT).as_posix()}"
            item = {"id": item_spec["id"], "texture": item_spec["id"], "registration": f"res://{registration.relative_to(ROOT).as_posix()}", "footprint": item_spec["footprint"], "ground_width": item_spec["ground_width"], "centers_by_quarter": item_spec["centers"], "live_furniture": True}
            if item_spec.get("centerpiece"): item["centerpiece"] = True
            if item_spec.get("authored_anchor"): item["authored_anchor"] = True
            profile["furniture"].append(item)
            card = ASSETS / "cards" / f"{room}.png"
            manifest["assets"].append({"room": room, "id": item_spec["id"], "scope": item_spec["scope"], "size_class": item_spec["size_class"], "shape": "rectangle", "source_profile": spec["source"], "selected_profile": spec["output"], "asset": asset.relative_to(ROOT).as_posix(), "asset_sha256": digest(asset), "registration": registration.relative_to(ROOT).as_posix(), "registration_sha256": digest(registration), "generated_source": GENERATED[item_spec["asset"]], "centers_by_quarter": item_spec["centers"], "footprint": item_spec["footprint"], "card": f"assets/room-furnishings-v8/cards/{room}.png", "card_sha256": digest(card) if card.exists() else "", "agent_visual_review": "native-reviewed-12-views", "owner_acceptance": False})
        (ROOT / spec["output"]).write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Built 6 furnishing v8 assets across Maintenance Bay, Storage Bay, and Data Archive")

if __name__ == "__main__":
    main()
