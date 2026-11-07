"""Build the third themed/universal furnishing profile batch and manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/room-furnishings-v3"
SPECS = {
    "hydroponics_bay": {
        "source": "rooms/whole-room/hydro-composition-v3.json", "output": "rooms/whole-room/hydro-composition-v4.json",
        "id": "hydro_nutrient_island", "asset": "hydroponics-nutrient-island", "scope": "themed", "size_class": "large",
        "footprint": [-52, 24, 104, 32], "ground_width": 1160, "centers": [[-85, 35], [0, 40], [85, -35], [0, 40]], "centerpiece": True,
        "generated_source": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-64020c72-25e3-4794-9df4-9179c456adf3.png",
    },
    "ore_refinery": {
        "source": "rooms/production-ten/decor/refinery-composition-v3.json", "output": "rooms/production-ten/decor/refinery-composition-v4.json",
        "id": "refinery_sorting_bench", "asset": "refinery-assay-bench", "scope": "themed", "size_class": "large",
        "footprint": [47, 85, 96, 30], "ground_width": 1170, "centers": [[95, 100], [-100, 95], [-95, -100], [100, -20]], "centerpiece": True,
        "remove": ["refinery_assay_bench"],
        "generated_source": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-fe86782b-5358-4ab1-86b1-82ac4949b23b.png",
    },
    "cryo_chamber": {
        "source": "rooms/underwater/batch-two/cryo-composition-v2.json", "output": "rooms/underwater/batch-two/cryo-composition-v3.json",
        "id": "cryo_thaw_cart", "asset": "cryo-thaw-cart", "scope": "themed", "size_class": "medium",
        "footprint": [58, 49, 56, 24], "ground_width": 810, "centers": [[86, 61], [-82, 62], [-86, -61], [82, -62]], "authored_anchor": True,
        "generated_source": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-f2fe8a9e-d7ee-409a-b496-abab1ec82df5.png",
    },
    "quarantine_cell": {
        "source": "rooms/production-ten/decor/quarantine-composition-v3.json", "output": "rooms/production-ten/decor/quarantine-composition-v4.json",
        "id": "universal_parts_chest", "asset": "universal-parts-chest", "scope": "universal", "size_class": "medium",
        "footprint": [42, 72, 78, 24], "ground_width": 1110, "centers": [[81, 84], [-84, 81], [-81, -84], [84, -81]], "authored_anchor": True,
        "remove": ["quarantine_sealed_cooler"],
        "generated_source": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-3fef65dc-825b-4014-bb7f-1144fe574fd3.png",
    },
    "pressure_control": {
        "source": "rooms/underwater/rare-dead-ends/pressure-composition-v1.json", "output": "rooms/underwater/rare-dead-ends/pressure-composition-v2.json",
        "id": "universal_equipment_plinth", "asset": "universal-equipment-plinth", "scope": "universal", "size_class": "large",
        "footprint": [-56, 21, 112, 42], "ground_width": 1150, "centers": [[0, 42]] * 4, "centerpiece": True,
        "generated_source": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-919517bd-3c5e-44ee-a6b1-48ee50dbd957.png",
    },
    "isolation_vault": {
        "source": "rooms/underwater/rare-dead-ends/isolation-composition-v1.json", "output": "rooms/underwater/rare-dead-ends/isolation-composition-v2.json",
        "id": "universal_task_table", "asset": "universal-task-table", "scope": "universal", "size_class": "medium",
        "footprint": [-48, 32, 96, 28], "ground_width": 1130, "centers": [[0, 46]] * 4, "authored_anchor": True,
        "remove": ["battery_test_bench", "battery_cable_reel"],
        "generated_source": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-8d88d2bb-880d-4a6d-996d-c2d9962c0b92.png",
    },
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = {"version": 3, "prompt_record": "assets/room-furnishings-v3/prompts.md", "status": "integrated-native-reviewed-owner-acceptance-pending",
        "native_evidence": "output/room-furnishings-v3/native-v2/runtime.json", "native_contact_sheet": "output/room-furnishings-v3/native-v2-contact-sheet.jpg",
        "card_contact_sheet": "output/room-furnishings-v3/cards-sheet.jpg", "route_evidence": "output/test-runs/20260913-003920-headless", "assets": []}
    for room, spec in SPECS.items():
        profile = json.loads((ROOT / spec["source"]).read_text(encoding="utf-8"))
        remove = set(spec.get("remove", []))
        profile["furniture"] = [item for item in profile.get("furniture", []) if item["id"] not in remove]
        asset = ASSETS / f"{spec['asset']}.png"
        registration = ASSETS / f"{spec['asset']}-registration.json"
        profile.setdefault("textures", {})[spec["id"]] = f"res://{asset.relative_to(ROOT).as_posix()}"
        item = {"id": spec["id"], "texture": spec["id"], "registration": f"res://{registration.relative_to(ROOT).as_posix()}",
                "footprint": spec["footprint"], "ground_width": spec["ground_width"], "centers_by_quarter": spec["centers"], "live_furniture": True}
        if spec.get("centerpiece"): item["centerpiece"] = True
        if spec.get("authored_anchor"): item["authored_anchor"] = True
        profile["furniture"].append(item)
        (ROOT / spec["output"]).write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
        manifest["assets"].append({"room": room, "id": spec["id"], "scope": spec["scope"], "size_class": spec["size_class"], "shape": "rectangle",
            "source_profile": spec["source"], "selected_profile": spec["output"], "asset": asset.relative_to(ROOT).as_posix(), "asset_sha256": digest(asset),
            "registration": registration.relative_to(ROOT).as_posix(), "registration_sha256": digest(registration), "generated_source": spec["generated_source"],
            "centers_by_quarter": spec["centers"], "footprint": spec["footprint"], "card": f"assets/room-furnishings-v3/cards/{room}.png",
            "card_sha256": digest(ASSETS / "cards" / f"{room}.png"), "agent_visual_review": "native-reviewed-24-views", "owner_acceptance": False})
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Built 6 furnishing v3 profiles")


if __name__ == "__main__":
    main()
