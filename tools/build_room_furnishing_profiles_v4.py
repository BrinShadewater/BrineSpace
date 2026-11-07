"""Build the fourth themed/universal furnishing batch for the power rooms."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/room-furnishings-v4"
ROOMS = {
    "current_turbine": {
        "source": "rooms/power-expansion-v1/current_turbine-composition.json",
        "output": "rooms/power-expansion-v1/current_turbine-composition-v2.json",
        "remove": ["current_turbine_service_bench"],
        "items": [
            {"id": "current_flow_governor", "asset": "current-flow-governor", "scope": "themed", "size_class": "large", "footprint": [-50, -14, 100, 28], "ground_width": 1212, "centers": [[-72, 92], [-91, -62], [-72, -92], [91, -62]], "centerpiece": True},
            {"id": "universal_instrument_cabinet", "asset": "universal-instrument-cabinet", "scope": "universal", "size_class": "medium", "footprint": [-29, -11, 58, 22], "ground_width": 1092, "centers": [[132, 28], [-116, 82], [92, -92], [116, 82]], "authored_anchor": True},
        ],
    },
    "biomass_digester": {
        "source": "rooms/power-expansion-v1/biomass_digester-composition.json",
        "output": "rooms/power-expansion-v1/biomass_digester-composition-v2.json",
        "remove": ["biomass_digester_service_bench"],
        "items": [
            {"id": "biomass_feedstock_island", "asset": "biomass-feedstock-island", "scope": "themed", "size_class": "large", "footprint": [-50, -16, 100, 32], "ground_width": 1237, "centers": [[-70, -92]] * 4, "centerpiece": True},
            {"id": "universal_maintenance_trestle", "asset": "universal-maintenance-trestle", "scope": "universal", "size_class": "medium", "footprint": [-30, -12, 60, 24], "ground_width": 1152, "centers": [[90, -92]] * 4, "authored_anchor": True},
        ],
    },
    "heat_recovery": {
        "source": "rooms/power-expansion-v1/heat_recovery-composition.json",
        "output": "rooms/power-expansion-v1/heat_recovery-composition-v2.json",
        "remove": ["heat_recovery_service_bench"],
        "items": [
            {"id": "heat_exchanger_manifold", "asset": "heat-exchanger-manifold", "scope": "themed", "size_class": "large", "footprint": [-52, -15, 104, 30], "ground_width": 1204, "centers": [[-70, -92]] * 4, "centerpiece": True},
            {"id": "universal_cable_caddy", "asset": "universal-cable-caddy", "scope": "universal", "size_class": "medium", "footprint": [-31, -11, 62, 22], "ground_width": 1203, "centers": [[92, -92]] * 4, "authored_anchor": True},
        ],
    },
}

GENERATED = {
    "current-flow-governor": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-8ca6e5c3-9dbd-451f-8a7c-7e89ffd1abfc.png",
    "biomass-feedstock-island": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-d10f17e9-fbbe-447c-8c93-7641b18fb08e.png",
    "heat-exchanger-manifold": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-c3851a0b-4f18-418a-9f21-090bb9dd0816.png",
    "universal-instrument-cabinet": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-453e0764-9b1b-48b0-92e8-24931bfc5331.png",
    "universal-maintenance-trestle": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-1b178412-0b48-4364-a3ee-13e11cd60ace.png",
    "universal-cable-caddy": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-23cb9e8c-e857-4010-90b9-e83fd659b0f2.png",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = {
        "version": 4,
        "prompt_record": "assets/room-furnishings-v4/prompts.md",
        "status": "integrated-native-reviewed-owner-acceptance-pending",
        "native_evidence": "output/room-furnishings-v4/native-v1/runtime.json",
        "native_contact_sheet": "output/room-furnishings-v4/native-v1-contact-sheet.jpg",
        "card_contact_sheet": "output/room-furnishings-v4/cards-sheet.jpg",
        "route_evidence": "output/test-runs/20260913-010049-headless",
        "assets": [],
    }
    for room, spec in ROOMS.items():
        profile = json.loads((ROOT / spec["source"]).read_text(encoding="utf-8"))
        removed = set(spec["remove"])
        profile["furniture"] = [item for item in profile.get("furniture", []) if item["id"] not in removed]
        profile["mats"] = [item for item in profile.get("mats", []) if item.get("host") not in removed]
        for item_spec in spec["items"]:
            asset = ASSETS / f"{item_spec['asset']}.png"
            registration = ASSETS / f"{item_spec['asset']}-registration.json"
            profile.setdefault("textures", {})[item_spec["id"]] = f"res://{asset.relative_to(ROOT).as_posix()}"
            item = {
                "id": item_spec["id"],
                "texture": item_spec["id"],
                "registration": f"res://{registration.relative_to(ROOT).as_posix()}",
                "footprint": item_spec["footprint"],
                "ground_width": item_spec["ground_width"],
                "centers_by_quarter": item_spec["centers"],
                "live_furniture": True,
            }
            if item_spec.get("centerpiece"):
                item["centerpiece"] = True
            if item_spec.get("authored_anchor"):
                item["authored_anchor"] = True
            profile["furniture"].append(item)
            manifest["assets"].append({
                "room": room,
                "id": item_spec["id"],
                "scope": item_spec["scope"],
                "size_class": item_spec["size_class"],
                "shape": "rectangle",
                "source_profile": spec["source"],
                "selected_profile": spec["output"],
                "asset": asset.relative_to(ROOT).as_posix(),
                "asset_sha256": digest(asset),
                "registration": registration.relative_to(ROOT).as_posix(),
                "registration_sha256": digest(registration),
                "generated_source": GENERATED[item_spec["asset"]],
                "centers_by_quarter": item_spec["centers"],
                "footprint": item_spec["footprint"],
                "card": f"assets/room-furnishings-v4/cards/{room}.png",
                "card_sha256": digest(ASSETS / "cards" / f"{room}.png"),
                "agent_visual_review": "native-reviewed-12-views",
                "owner_acceptance": False,
            })
        (ROOT / spec["output"]).write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Built 6 furnishing v4 assets across 3 power-room profiles")


if __name__ == "__main__":
    main()
