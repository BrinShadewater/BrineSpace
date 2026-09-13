"""Build the seventh themed/universal furnishing batch for clinical and biology rooms."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/room-furnishings-v7"
ROOMS = {
    "life_support": {
        "source": "rooms/whole-room/life-support-composition-v4.json",
        "output": "rooms/whole-room/life-support-composition-v5.json",
        "remove": ["life_filter_bench", "life_scrubber_trolley"],
        "items": [
            {"id": "life_atmosphere_analysis_island", "asset": "life-support-atmosphere-analysis-island", "scope": "themed", "size_class": "large", "footprint": [-52, -16, 104, 32], "ground_width": 1200, "centers": [[-78, 74], [-74, -78], [78, -74], [74, 78]], "centerpiece": True},
            {"id": "universal_filter_cassette_chest", "asset": "universal-sealed-filter-cassette-chest", "scope": "universal", "size_class": "medium", "footprint": [-29, -12, 58, 24], "ground_width": 1205, "centers": [[105, 106], [-106, 105], [-105, -106], [106, -105]], "authored_anchor": True},
        ],
    },
    "med_bay": {
        "source": "rooms/whole-room/med-bay-composition-v2.json",
        "output": "rooms/whole-room/med-bay-composition-v3.json",
        "remove": ["med_preparation"],
        "items": [
            {"id": "med_sterile_triage_island", "asset": "med-bay-sterile-triage-island", "scope": "themed", "size_class": "large", "footprint": [-52, -16, 104, 32], "ground_width": 1210, "centers": [[0, 114], [-112, 105], [0, -114], [105, 80]], "centerpiece": True},
            {"id": "universal_enclosed_equipment_cart", "asset": "universal-enclosed-equipment-cart", "scope": "universal", "size_class": "medium", "footprint": [-27, -12, 54, 24], "ground_width": 1135, "centers": [[-118, -30], [105, 105], [-118, -55], [55, -118]], "authored_anchor": True},
        ],
    },
    "bio_lab": {
        "source": "rooms/underwater/batch-two/bio-composition-v2.json",
        "output": "rooms/underwater/batch-two/bio-composition-v3.json",
        "remove": ["bio_preparation", "bio_sample_cooler"],
        "items": [
            {"id": "bio_culture_preparation_island", "asset": "bio-lab-culture-preparation-island", "scope": "themed", "size_class": "large", "footprint": [-52, -16, 104, 32], "ground_width": 1215, "centers": [[0, 18], [-18, 0], [0, -18], [18, 0]], "centerpiece": True},
            {"id": "universal_specimen_transit_case", "asset": "universal-specimen-transit-case", "scope": "universal", "size_class": "medium", "footprint": [-29, -12, 58, 24], "ground_width": 1185, "centers": [[110, -42], [42, 110], [-110, 42], [-42, -110]], "authored_anchor": True},
        ],
    },
}

GENERATED = {
    "life-support-atmosphere-analysis-island": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-43ab7c11-476d-4e6d-80f9-24195764ea65.png",
    "med-bay-sterile-triage-island": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-b6f8a5de-1bfc-4b78-8dd5-c941cb6ca6df.png",
    "bio-lab-culture-preparation-island": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-da7b5ee2-e861-4678-a848-8610a5355db0.png",
    "universal-sealed-filter-cassette-chest": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-526a35af-eb90-4f03-8cdd-734ff768a718.png",
    "universal-enclosed-equipment-cart": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-10824830-b830-4204-a8af-23fdae56d2a0.png",
    "universal-specimen-transit-case": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-f31be0c8-6f76-4370-935d-2dd1ef7cab2d.png",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = {
        "version": 7,
        "prompt_record": "assets/room-furnishings-v7/prompts.md",
        "status": "integrated-native-reviewed-owner-acceptance-pending",
        "native_evidence": "output/room-furnishings-v7/native-v2/runtime.json",
        "native_contact_sheet": "output/room-furnishings-v7/native-v2-contact-sheet.jpg",
        "card_contact_sheet": "output/room-furnishings-v7/cards-sheet.jpg",
        "route_evidence": "output/test-runs/20260913-014953-headless",
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
            card = ASSETS / "cards" / f"{room}.png"
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
                "card": f"assets/room-furnishings-v7/cards/{room}.png",
                "card_sha256": digest(card) if card.exists() else "",
                "agent_visual_review": "native-reviewed-12-views",
                "owner_acceptance": False,
            })
        (ROOT / spec["output"]).write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Built 6 furnishing v7 assets across Life Support, Med Bay, and Bio Lab")


if __name__ == "__main__":
    main()
