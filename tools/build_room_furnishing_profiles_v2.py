"""Build the second large/medium furnishing profile batch and source manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets/room-furnishings-v2"
SPECS = {
    "research_lab": {
        "source": "rooms/production-ten/decor/research-composition-v3.json",
        "output": "rooms/production-ten/decor/research-composition-v4.json",
        "id": "research_specimen_island",
        "asset": "research-specimen-island",
        "size_class": "large",
        "scope": "themed",
        "footprint": [-60, 25, 120, 44],
        "ground_width": 1175,
        "centers": [[0, 47], [0, 47], [0, 47], [0, 47]],
        "centerpiece": True,
        "remove": ["preparation_island"],
        "generated_source": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-f011f01f-b781-43dd-bc9d-cf7b6a7175c8.png",
    },
    "command_center": {
        "source": "rooms/production-ten/decor/command-composition-v3.json",
        "output": "rooms/production-ten/decor/command-composition-v4.json",
        "id": "command_planning_table",
        "asset": "command-planning-table",
        "size_class": "large",
        "scope": "themed",
        "footprint": [-62, 18, 124, 46],
        "ground_width": 1180,
        "centers": [[-76, 41], [0, 41], [0, 41], [0, 41]],
        "centerpiece": True,
        "generated_source": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-7d5dbd99-71b5-48e3-b93b-558a2e60d84e.png",
    },
    "med_center": {
        "source": "rooms/underwater/batch-two/med-center-composition-v3.json",
        "output": "rooms/underwater/batch-two/med-center-composition-v4.json",
        "id": "medical_instrument_trolley",
        "asset": "medical-instrument-trolley",
        "size_class": "medium",
        "scope": "themed",
        "footprint": [64, 50, 52, 22],
        "ground_width": 825,
        "centers": [[90, 61], [-82, 62], [-88, -58], [86, -58]],
        "authored_anchor": True,
        "generated_source": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-b06c72ae-089b-40df-bcc5-5c963a0084ea.png",
    },
    "crew_hab": {
        "source": "rooms/whole-room/crew-hab-composition-v3.json",
        "output": "rooms/whole-room/crew-hab-composition-v4.json",
        "id": "universal_storage_bench",
        "asset": "universal-storage-bench",
        "size_class": "medium",
        "scope": "universal",
        "footprint": [-45, 84, 90, 24],
        "ground_width": 1130,
        "centers": [[-96, 70], [-96, 0], [0, -96], [96, 0]],
        "authored_anchor": True,
        "generated_source": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-78d74d7b-8055-4df6-8966-95b87e439b8b.png",
    },
    "anomaly_lab": {
        "source": "rooms/underwater/batch-two/anomaly-composition-v2.json",
        "output": "rooms/underwater/batch-two/anomaly-composition-v3.json",
        "id": "universal_utility_cart",
        "asset": "universal-utility-cart",
        "size_class": "medium",
        "scope": "universal",
        "footprint": [52, 61, 54, 22],
        "ground_width": 780,
        "centers": [[79, 72], [-72, 79], [-79, -72], [72, -79]],
        "authored_anchor": True,
        "generated_source": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-4ef13358-b642-4cc1-afc6-f245763abf83.png",
    },
    "med_office": {
        "source": "rooms/underwater/batch-two/med-office-composition-v2.json",
        "output": "rooms/underwater/batch-two/med-office-composition-v3.json",
        "id": "universal_workbench",
        "asset": "universal-workbench",
        "size_class": "large",
        "scope": "universal",
        "footprint": [-52, 83, 104, 30],
        "ground_width": 1160,
        "centers": [[0, 98], [-98, 0], [0, -98], [98, 0]],
        "authored_anchor": True,
        "generated_source": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-eec6c4af-5d96-42ae-9b1f-18974390e381.png",
    },
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = {
        "version": 2,
        "prompt_record": "assets/room-furnishings-v2/prompts.md",
        "status": "integrated-native-reviewed-owner-acceptance-pending",
        "native_evidence": "output/room-furnishings-v2/native-v3/runtime.json",
        "native_contact_sheet": "output/room-furnishings-v2/native-v3-contact-sheet.jpg",
        "card_contact_sheet": "output/room-furnishings-v2/cards-sheet.jpg",
        "route_evidence": "output/test-runs/20260913-001455-headless",
        "assets": [],
    }
    for room, spec in SPECS.items():
        source = ROOT / spec["source"]
        output = ROOT / spec["output"]
        profile = json.loads(source.read_text(encoding="utf-8"))
        remove = set(spec.get("remove", []))
        profile["furniture"] = [item for item in profile.get("furniture", []) if item["id"] not in remove]
        texture_key = spec["id"]
        asset_path = ASSET_ROOT / f"{spec['asset']}.png"
        registration_path = ASSET_ROOT / f"{spec['asset']}-registration.json"
        profile.setdefault("textures", {})[texture_key] = f"res://{asset_path.relative_to(ROOT).as_posix()}"
        item = {
            "id": spec["id"],
            "texture": texture_key,
            "registration": f"res://{registration_path.relative_to(ROOT).as_posix()}",
            "footprint": spec["footprint"],
            "ground_width": spec["ground_width"],
            "centers_by_quarter": spec["centers"],
            "live_furniture": True,
        }
        if spec.get("centerpiece"):
            item["centerpiece"] = True
        if spec.get("authored_anchor"):
            item["authored_anchor"] = True
        profile["furniture"].append(item)
        output.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
        manifest["assets"].append({
            "room": room,
            "id": spec["id"],
            "scope": spec["scope"],
            "size_class": spec["size_class"],
            "shape": "rectangle",
            "source_profile": spec["source"],
            "selected_profile": spec["output"],
            "asset": asset_path.relative_to(ROOT).as_posix(),
            "generated_source": spec["generated_source"],
            "asset_sha256": digest(asset_path),
            "registration": registration_path.relative_to(ROOT).as_posix(),
            "registration_sha256": digest(registration_path),
            "centers_by_quarter": spec["centers"],
            "footprint": spec["footprint"],
            "card": f"assets/room-furnishings-v2/cards/{room}.png",
            "card_sha256": digest(ASSET_ROOT / "cards" / f"{room}.png"),
            "agent_visual_review": "native-reviewed-24-views",
            "owner_acceptance": False,
        })
    (ASSET_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(SPECS)} furnishing profiles")


if __name__ == "__main__":
    main()
