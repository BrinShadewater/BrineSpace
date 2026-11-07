"""Create the five reviewed centerpiece composition profiles from prior revisions."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CENTER = ROOT / "assets/room-centerpieces-v1"
ALL_QUARTERS = [[0, 35], [0, 35], [0, 35], [0, 35]]

SPECS = {
    "maintenance_bay": {
        "source": ROOT / "rooms/production-ten/decor/maintenance-composition-v3.json",
        "output": ROOT / "rooms/production-ten/decor/maintenance-composition-v4.json",
        "id": "maintenance_repair_gantry",
        "texture": "centerpiece",
        "asset": "res://assets/rooms/maintenance-bay/furnishings/repair-gantry.png",
        "registration": "res://assets/room-centerpieces-v1/maintenance-repair-gantry-registration.json",
        "footprint": [-60, 11, 120, 48],
        "ground_width": 1187,
        "centers": ALL_QUARTERS,
    },
    "data_archive": {
        "source": ROOT / "rooms/underwater/batch-two/archive-composition-v2.json",
        "output": ROOT / "rooms/underwater/batch-two/archive-composition-v3.json",
        "id": "archive_index_island",
        "texture": "centerpiece",
        "asset": "res://assets/rooms/data-archive/furnishings/index-island.png",
        "registration": "res://assets/room-centerpieces-v1/archive-index-island-registration.json",
        "footprint": [-58, 9, 116, 38],
        "ground_width": 1160,
        "centers": [[0, 28], [0, 28], [0, 28], [0, 28]],
    },
    "radio_lab": {
        "source": ROOT / "rooms/underwater/acoustic-comms/radio-composition-v3.json",
        "output": ROOT / "rooms/underwater/acoustic-comms/radio-composition-v4.json",
        "id": "radio_signal_console",
        "texture": "centerpiece",
        "asset": "res://assets/rooms/radio-lab/furnishings/signal-console.png",
        "registration": "res://assets/room-centerpieces-v1/radio-signal-console-registration.json",
        "footprint": [-55, 12, 110, 36],
        "ground_width": 1222,
        "centers": [[0, 30], [0, 30], [0, 30], [0, 30]],
    },
    "listening_post": {
        "source": ROOT / "rooms/underwater/rare-dead-ends/listening-composition-v1.json",
        "output": ROOT / "rooms/underwater/rare-dead-ends/listening-composition-v2.json",
        "id": "listening_hydrophone_table",
        "texture": "centerpiece",
        "asset": "res://assets/rooms/listening-post/furnishings/hydrophone-table.png",
        "registration": "res://assets/room-centerpieces-v1/listening-hydrophone-table-registration.json",
        "footprint": [-59, 13, 118, 38],
        "ground_width": 1231,
        "centers": [[0, 32], [0, 32], [0, 32], [0, 32]],
        "remove": ["acoustic_electronics_bench"],
    },
    "storage_bay": {
        "source": ROOT / "rooms/production-ten/decor/storage-composition-v4.json",
        "output": ROOT / "rooms/production-ten/decor/storage-composition-v5.json",
        "id": "storage_cargo_carousel",
        "texture": "centerpiece",
        "asset": "res://assets/rooms/storage-bay/furnishings/cargo-carousel.png",
        "registration": "res://assets/room-centerpieces-v1/storage-cargo-carousel-registration.json",
        "footprint": [-60, 20, 120, 44],
        "ground_width": 1103,
        "centers": [[0, 42], [0, 42], [-100, 55], [0, 42]],
    },
}

SUPPLEMENTAL = {
    "battery_array": {
        "source": ROOT / "rooms/production-ten/decor/battery-composition-v4.json",
        "output": ROOT / "rooms/production-ten/decor/battery-composition-v5.json",
        "items": [
            {"id": "battery_charge_equalizer", "asset": "battery-charge-equalizer", "footprint": [-55, 13, 110, 44], "ground_width": 1135, "centers_by_quarter": [[0, 35], [0, 35], [95, 50], [0, 35]], "centerpiece": True},
            {"id": "battery_capacitor_dolly", "asset": "battery-capacitor-dolly", "footprint": [-156, -81, 72, 28], "ground_width": 942, "centers_by_quarter": [[-120, -67], [-115, 120], [-120, 25], [-115, 120]], "authored_anchor": True},
        ],
    },
    "solar_array": {
        "source": ROOT / "rooms/underwater/thermal-control/thermal-composition-v2.json",
        "output": ROOT / "rooms/underwater/thermal-control/thermal-composition-v3.json",
        "items": [
            {"id": "solar_conversion_island", "asset": "solar-conversion-island", "footprint": [-62, 11, 124, 42], "ground_width": 1201, "centers_by_quarter": [[0, 32]] * 4, "centerpiece": True},
            {"id": "solar_junction_cart", "asset": "solar-junction-cart", "footprint": [-150, 78, 74, 26], "ground_width": 1145, "centers_by_quarter": [[-113, 91], [-91, -113], [113, -91], [91, 113]], "authored_anchor": True},
        ],
    },
    "shield_generator": {
        "source": ROOT / "rooms/underwater/hull-integrity/hull-composition-v3.json",
        "output": ROOT / "rooms/underwater/hull-integrity/hull-composition-v4.json",
        "items": [{"id": "shield_emitter_bench", "asset": "shield-emitter-bench", "footprint": [-41, 37, 82, 26], "ground_width": 1178, "centers_by_quarter": [[-10, 50], [0, 10], [0, 10], [0, 50]], "authored_anchor": True}],
    },
    "life_support": {
        "source": ROOT / "rooms/whole-room/life-support-composition-v3.json",
        "output": ROOT / "rooms/whole-room/life-support-composition-v4.json",
        "items": [{"id": "life_scrubber_trolley", "asset": "life-support-scrubber-trolley", "footprint": [60, 58, 70, 26], "ground_width": 886, "centers_by_quarter": [[95, 71], [-90, 15], [-97, 59], [90, 15]], "authored_anchor": True}],
    },
    "holographic_core": {
        "source": ROOT / "rooms/underwater/batch-two/holo-composition-v3.json",
        "output": ROOT / "rooms/underwater/batch-two/holo-composition-v4.json",
        "items": [{"id": "holo_calibration_block", "asset": "holo-calibration-block", "footprint": [-36, -13, 72, 26], "ground_width": 1018, "centers_by_quarter": [[0, 0], [-90, 95], [-96, 59], [90, 0]], "authored_anchor": True}],
    },
}


def build() -> None:
    manifest = {
        "version": 1,
        "prompt_record": "assets/room-centerpieces-v1/prompts.md",
        "native_evidence": "output/room-centerpieces-v1/native-v6/runtime.json",
        "native_contact_sheet": "output/room-centerpieces-v1/native-v6-contact-sheet.jpg",
        "card_contact_sheet": "output/room-centerpieces-v1/cards-sheet.png",
        "verification": {
            "native_rooms": 10,
            "native_orientations": 40,
            "selected_assets": 12,
            "large_assets": 7,
            "medium_assets": 5,
            "square_or_rectangular_assets": 10,
            "route_evidence": "output/test-runs/20260912-234904-headless",
        },
        "rooms": [],
        "rejected": [
            {"asset": "assets/room-centerpieces-v1/rejected-shield-coil-round.png", "reason": "Round coil silhouette conflicts with the requested square/rectangular shape language."},
            {"asset": "assets/room-centerpieces-v1/rejected-holo-triangular.png", "reason": "Triangular plinth silhouette conflicts with the requested square/rectangular shape language."},
        ],
    }
    for room, spec in SPECS.items():
        profile = json.loads(spec["source"].read_text(encoding="utf-8"))
        profile["textures"][spec["texture"]] = spec["asset"]
        remove = set(spec.get("remove", []))
        profile["furniture"] = [item for item in profile.get("furniture", []) if item["id"] not in remove]
        profile["furniture"].append({
            "id": spec["id"],
            "texture": spec["texture"],
            "registration": spec["registration"],
            "footprint": spec["footprint"],
            "ground_width": spec["ground_width"],
            "centers_by_quarter": spec["centers"],
            "live_furniture": True,
            "centerpiece": True,
        })
        spec["output"].write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
        asset_path = ROOT / spec["asset"].removeprefix("res://")
        registration_path = ROOT / spec["registration"].removeprefix("res://")
        manifest["rooms"].append({
            "room": room,
            "centerpiece": spec["id"],
            "size_class": "large",
            "shape": {"maintenance_bay": "rectangular-open-frame", "data_archive": "rectangle", "radio_lab": "octagonal", "listening_post": "oval", "storage_bay": "square-turntable"}[room],
            "source_profile": spec["source"].relative_to(ROOT).as_posix(),
            "selected_profile": spec["output"].relative_to(ROOT).as_posix(),
            "asset": asset_path.relative_to(ROOT).as_posix(),
            "asset_sha256": hashlib.sha256(asset_path.read_bytes()).hexdigest(),
            "registration": registration_path.relative_to(ROOT).as_posix(),
            "registration_sha256": hashlib.sha256(registration_path.read_bytes()).hexdigest(),
            "centers_by_quarter": spec["centers"],
            "footprint": spec["footprint"],
            "agent_visual_review": "native-reviewed-40-views",
            "owner_acceptance": False,
        })
    for room, bundle in SUPPLEMENTAL.items():
        profile = json.loads(bundle["source"].read_text(encoding="utf-8"))
        for item_spec in bundle["items"]:
            name = item_spec["asset"]
            texture_key = "centerpiece_" + name.replace("-", "_")
            asset = f"res://assets/room-centerpieces-v1/{name}.png"
            registration = f"res://assets/room-centerpieces-v1/{name}-registration.json"
            profile["textures"][texture_key] = asset
            item = {
                "id": item_spec["id"],
                "texture": texture_key,
                "registration": registration,
                "footprint": item_spec["footprint"],
                "ground_width": item_spec["ground_width"],
                "live_furniture": True,
            }
            if item_spec.get("centers_by_quarter"):
                item["centers_by_quarter"] = item_spec["centers_by_quarter"]
            if item_spec.get("centerpiece"):
                item["centerpiece"] = True
            if item_spec.get("authored_anchor"):
                item["authored_anchor"] = True
            profile["furniture"].append(item)
            asset_path = ROOT / asset.removeprefix("res://")
            registration_path = ROOT / registration.removeprefix("res://")
            manifest["rooms"].append({
                "room": room,
                "centerpiece": item_spec["id"],
                "size_class": "large" if item_spec.get("centerpiece") else "medium",
                "shape": "square" if name in ["battery-charge-equalizer", "holo-calibration-block"] else "rectangle",
                "source_profile": bundle["source"].relative_to(ROOT).as_posix(),
                "selected_profile": bundle["output"].relative_to(ROOT).as_posix(),
                "asset": asset_path.relative_to(ROOT).as_posix(),
                "asset_sha256": hashlib.sha256(asset_path.read_bytes()).hexdigest(),
                "registration": registration_path.relative_to(ROOT).as_posix(),
                "registration_sha256": hashlib.sha256(registration_path.read_bytes()).hexdigest(),
                "footprint": item_spec["footprint"],
                "agent_visual_review": "native-reviewed-40-views",
                "owner_acceptance": False,
            })
        bundle["output"].write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    (CENTER / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(SPECS) + len(SUPPLEMENTAL)} room profiles with {len(manifest['rooms'])} assets")


if __name__ == "__main__":
    build()
