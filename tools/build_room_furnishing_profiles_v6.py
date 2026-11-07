"""Build the sixth themed/universal furnishing batch for utility and science rooms."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/room-furnishings-v6"
ROOMS = {
    "tidal_condenser": {
        "source": "rooms/underwater/tidal-condenser/tidal-composition-v2.json",
        "output": "rooms/underwater/tidal-condenser/tidal-composition-v3.json",
        "remove": ["tidal_sampling_bench"],
        "items": [
            {"id": "tidal_analysis_island", "asset": "tidal-analysis-island", "scope": "themed", "size_class": "large", "footprint": [-48, -14, 96, 28], "ground_width": 1213, "centers": [[0, -92], [92, 0], [0, 92], [-92, 0]], "centerpiece": True},
            {"id": "universal_valve_locker", "asset": "universal-valve-locker", "scope": "universal", "size_class": "medium", "footprint": [-29, -11, 58, 22], "ground_width": 1210, "centers": [[112, 65], [-65, 112], [-112, -65], [65, -112]], "authored_anchor": True},
        ],
    },
    "gravity_loom": {
        "source": "rooms/underwater/gravity-loom/loom-composition-v2.json",
        "output": "rooms/underwater/gravity-loom/loom-composition-v3.json",
        "remove": ["loom_calibration_bench", "loom_task_light"],
        "items": [
            {"id": "gravity_tensor_console", "asset": "gravity-tensor-console", "scope": "themed", "size_class": "large", "footprint": [-43, -13, 86, 26], "ground_width": 1215, "centers": [[-110, 130], [-130, -110], [110, -130], [130, 110]], "centerpiece": True},
            {"id": "universal_diagnostic_rack", "asset": "universal-diagnostic-rack", "scope": "universal", "size_class": "medium", "footprint": [-28, -10, 56, 20], "ground_width": 1190, "centers": [[110, 130], [-130, 110], [-110, -130], [130, -110]], "authored_anchor": True},
        ],
    },
    "xeno_lab": {
        "source": "rooms/underwater/batch-two/xeno-composition-v2.json",
        "output": "rooms/underwater/batch-two/xeno-composition-v3.json",
        "remove": ["xeno_service_cart"],
        "items": [
            {"id": "xeno_assay_table", "asset": "xeno-assay-table", "scope": "themed", "size_class": "large", "footprint": [-46, -14, 92, 28], "ground_width": 1230, "centers": [[-92, -44], [-70, 0], [90, 35], [45, -85]], "centerpiece": True},
            {"id": "universal_decon_caddy", "asset": "universal-decon-caddy", "scope": "universal", "size_class": "medium", "footprint": [-15, -22, 30, 44], "ground_width": 776, "centers": [[118, 105], [-112, 105], [-112, -95], [118, 105]], "authored_anchor": True},
        ],
    },
}

GENERATED = {
    "tidal-analysis-island": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-80bdcb8b-3926-4b42-8286-4754607f465c.png",
    "gravity-tensor-console": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-bcfeec7d-0758-42bd-b890-ae6629b2490c.png",
    "xeno-assay-table": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-2ebfefd1-9b2c-481c-a8cb-4ca02c70b395.png",
    "universal-valve-locker": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-50678e54-fd32-414e-8ddf-6b4b34743498.png",
    "universal-diagnostic-rack": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-395343d1-cbbc-4110-87cb-e9af250edf09.png",
    "universal-decon-caddy": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-2c198526-74c0-499e-94fe-fc34fe7d30de.png",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = {"version": 6, "prompt_record": "assets/room-furnishings-v6/prompts.md", "status": "integrated-native-reviewed-owner-acceptance-pending", "native_evidence": "output/room-furnishings-v6/native-v1/runtime.json", "native_contact_sheet": "output/room-furnishings-v6/native-v1-contact-sheet.jpg", "card_contact_sheet": "output/room-furnishings-v6/cards-sheet.jpg", "route_evidence": "output/test-runs/20260913-013058-headless", "assets": []}
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
            manifest["assets"].append({"room": room, "id": item_spec["id"], "scope": item_spec["scope"], "size_class": item_spec["size_class"], "shape": "portrait-rectangle" if item_spec["id"] == "universal_decon_caddy" else "rectangle", "source_profile": spec["source"], "selected_profile": spec["output"], "asset": asset.relative_to(ROOT).as_posix(), "asset_sha256": digest(asset), "registration": registration.relative_to(ROOT).as_posix(), "registration_sha256": digest(registration), "generated_source": GENERATED[item_spec["asset"]], "centers_by_quarter": item_spec["centers"], "footprint": item_spec["footprint"], "card": f"assets/room-furnishings-v6/cards/{room}.png", "card_sha256": digest(ASSETS / "cards" / f"{room}.png"), "agent_visual_review": "native-reviewed-12-views", "owner_acceptance": False})
        (ROOT / spec["output"]).write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Built 6 furnishing v6 assets across Tidal Condenser, Gravity Loom, and Xeno Lab")


if __name__ == "__main__":
    main()
