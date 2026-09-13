"""Build the fifth themed/universal furnishing batch for three departments."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/room-furnishings-v5"
ROOMS = {
    "reactor": {
        "source": "rooms/whole-room/reactor-composition-v2.json",
        "output": "rooms/whole-room/reactor-composition-v3.json",
        "remove": ["reactor_service_table", "reactor_task_lamp"],
        "items": [
            {"id": "reactor_control_rod_bench", "asset": "reactor-control-rod-bench", "scope": "themed", "size_class": "large", "footprint": [-50, -14, 100, 28], "ground_width": 1217, "centers": [[-105, 120], [-120, -105], [105, -120], [120, 105]], "centerpiece": True},
            {"id": "universal_tool_chest", "asset": "universal-tool-chest", "scope": "universal", "size_class": "medium", "footprint": [-29, -12, 58, 24], "ground_width": 1093, "centers": [[112, -95], [95, 112], [-112, 95], [-95, -112]], "authored_anchor": True},
        ],
    },
    "clone_lab": {
        "source": "rooms/underwater/batch-two/clone-composition-v2.json",
        "output": "rooms/underwater/batch-two/clone-composition-v3.json",
        "remove": ["clone_preparation"],
        "items": [
            {"id": "clone_genome_island", "asset": "clone-genome-island", "scope": "themed", "size_class": "large", "footprint": [-48, -15, 96, 30], "ground_width": 1220, "centers": [[-20, -91], [126, 4], [0, 130], [-126, -2]], "centerpiece": True},
            {"id": "universal_sample_trolley", "asset": "universal-sample-trolley", "scope": "universal", "size_class": "medium", "footprint": [-27, -11, 54, 22], "ground_width": 974, "centers": [[0, 30], [-30, 0], [0, -30], [30, 0]], "authored_anchor": True},
        ],
    },
    "biodome": {
        "source": "rooms/underwater/batch-two/biodome-composition-v2.json",
        "output": "rooms/underwater/batch-two/biodome-composition-v3.json",
        "remove": ["biodome_cultivation_cart", "biodome_propagation_shelf"],
        "items": [
            {"id": "biodome_potting_island", "asset": "biodome-potting-island", "scope": "themed", "size_class": "large", "footprint": [-48, -15, 96, 30], "ground_width": 1236, "centers": [[-124, 25], [-25, -124], [124, -9], [-95, 30]], "centerpiece": True},
            {"id": "universal_supply_pallet", "asset": "universal-supply-pallet", "scope": "universal", "size_class": "medium", "footprint": [-30, -11, 60, 22], "ground_width": 1152, "centers": [[116, 24], [-24, 116], [-116, -24], [105, 30]], "authored_anchor": True},
        ],
    },
}

GENERATED = {
    "reactor-control-rod-bench": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-5818162e-1ec4-4e78-951d-701a3e472bbb.png",
    "clone-genome-island": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-3ce9aca4-1d25-48e9-b0af-5effce1058c3.png",
    "biodome-potting-island": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-fe7a6dd6-b13a-4f7e-ad44-8bef7f53cc88.png",
    "universal-tool-chest": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-c115acda-e2f5-4bd7-8345-3c4c7013d91b.png",
    "universal-sample-trolley": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-cd3e54ea-0d2e-4faa-acaa-f217b5121913.png",
    "universal-supply-pallet": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-0b197d03-a0ba-4392-afe4-a7d691beccad.png",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = {
        "version": 5,
        "prompt_record": "assets/room-furnishings-v5/prompts.md",
        "status": "integrated-native-reviewed-owner-acceptance-pending",
        "native_evidence": "output/room-furnishings-v5/native-v1/runtime.json",
        "native_contact_sheet": "output/room-furnishings-v5/native-v1-contact-sheet.jpg",
        "card_contact_sheet": "output/room-furnishings-v5/cards-sheet.jpg",
        "route_evidence": "output/test-runs/20260913-011605-headless",
        "assets": [],
    }
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
            item = {
                "id": item_spec["id"], "texture": item_spec["id"],
                "registration": f"res://{registration.relative_to(ROOT).as_posix()}",
                "footprint": item_spec["footprint"], "ground_width": item_spec["ground_width"],
                "centers_by_quarter": item_spec["centers"], "live_furniture": True,
            }
            if item_spec.get("centerpiece"): item["centerpiece"] = True
            if item_spec.get("authored_anchor"): item["authored_anchor"] = True
            profile["furniture"].append(item)
            manifest["assets"].append({
                "room": room, "id": item_spec["id"], "scope": item_spec["scope"],
                "size_class": item_spec["size_class"], "shape": "rectangle",
                "source_profile": spec["source"], "selected_profile": spec["output"],
                "asset": asset.relative_to(ROOT).as_posix(), "asset_sha256": digest(asset),
                "registration": registration.relative_to(ROOT).as_posix(), "registration_sha256": digest(registration),
                "generated_source": GENERATED[item_spec["asset"]],
                "centers_by_quarter": item_spec["centers"], "footprint": item_spec["footprint"],
                "card": f"assets/room-furnishings-v5/cards/{room}.png",
                "card_sha256": digest(ASSETS / "cards" / f"{room}.png"),
                "agent_visual_review": "native-reviewed-12-views", "owner_acceptance": False,
            })
        (ROOT / spec["output"]).write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Built 6 furnishing v5 assets across Reactor, Clone Lab, and Biodome")


if __name__ == "__main__":
    main()
