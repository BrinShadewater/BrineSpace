"""Build the ninth themed/universal furnishing batch for communications rooms."""

from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/room-furnishings-v9"
ROOMS = {
    "radio_lab": {
        "source": "rooms/underwater/acoustic-comms/radio-composition-v4.json",
        "output": "rooms/underwater/acoustic-comms/radio-composition-v5.json",
        "remove": ["acoustic_electronics_bench", "acoustic_operator_chair", "radio_signal_console"],
        "items": [
            {"id": "radio_signal_routing_console", "asset": "radio-signal-routing-console", "scope": "themed", "size_class": "large", "footprint": [-55, -18, 110, 36], "ground_width": 1215, "centers": [[0, 34], [-34, 0], [0, -34], [34, 0]], "centerpiece": True},
            {"id": "universal_patch_cable_organizer", "asset": "universal-patch-cable-organizer-chest", "scope": "universal", "size_class": "medium", "footprint": [-30, -13, 60, 26], "ground_width": 1195, "centers": [[-112, 110], [-110, -112], [-115, 62], [110, 112]], "authored_anchor": True},
        ],
    },
    "listening_post": {
        "source": "rooms/underwater/rare-dead-ends/listening-composition-v2.json",
        "output": "rooms/underwater/rare-dead-ends/listening-composition-v3.json",
        "remove": ["listening_operator_chair", "listening_hydrophone_table"],
        "items": [
            {"id": "listening_hydrophone_analysis_table", "asset": "listening-hydrophone-analysis-table", "scope": "themed", "size_class": "large", "footprint": [-55, -18, 110, 36], "ground_width": 1215, "centers": [[0, 38], [-38, 0], [0, -38], [38, 0]], "centerpiece": True},
            {"id": "universal_rugged_power_conditioner", "asset": "universal-rugged-power-conditioner", "scope": "universal", "size_class": "medium", "footprint": [-30, -13, 60, 26], "ground_width": 1190, "centers": [[112, 110], [55, -55], [-112, -110], [130, -105]], "authored_anchor": True},
        ],
    },
    "holographic_core": {
        "source": "rooms/underwater/batch-two/holo-composition-v4.json",
        "output": "rooms/underwater/batch-two/holo-composition-v5.json",
        "remove": ["holo_calibration_cart", "holo_calibration_block"],
        "items": [
            {"id": "holo_projection_alignment_deck", "asset": "holographic-core-projection-alignment-deck", "scope": "themed", "size_class": "large", "footprint": [-54, -18, 108, 36], "ground_width": 1210, "centers": [[0, 25], [-25, 0], [0, -25], [25, 0]], "centerpiece": True},
            {"id": "universal_instrument_calibration_case", "asset": "universal-instrument-calibration-case", "scope": "universal", "size_class": "medium", "footprint": [-30, -13, 60, 26], "ground_width": 1185, "centers": [[-112, 108], [-108, -112], [112, -108], [108, 112]], "authored_anchor": True},
        ],
    },
}
GENERATED = {
    "radio-signal-routing-console": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-6d3ae48b-4ec6-4e75-ba2e-6a57f1c97826.png",
    "listening-hydrophone-analysis-table": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-f600d043-3341-40e8-9009-a00ff1bcd728.png",
    "holographic-core-projection-alignment-deck": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-e7273e71-6167-44bd-94b8-58b957207c5e.png",
    "universal-patch-cable-organizer-chest": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-f5ea125d-8dbb-4a69-a087-1320a1f37cc8.png",
    "universal-rugged-power-conditioner": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-8990d407-672c-452a-939d-884b7e13018a.png",
    "universal-instrument-calibration-case": "C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-02d5b51d-e5d8-485f-a178-ce3e0ddfa7d1.png",
}

def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    manifest = {"version": 9, "prompt_record": "assets/room-furnishings-v9/prompts.md", "status": "integrated-native-reviewed-owner-acceptance-pending", "native_evidence": "output/room-furnishings-v9/native-v5/runtime.json", "native_contact_sheet": "output/room-furnishings-v9/native-v5-contact-sheet.jpg", "card_contact_sheet": "output/room-furnishings-v9/cards-sheet.jpg", "route_evidence": "output/test-runs/20260913-024217-headless", "assets": []}
    for room, spec in ROOMS.items():
        profile = json.loads((ROOT / spec["source"]).read_text(encoding="utf-8")); removed = set(spec["remove"])
        profile["furniture"] = [x for x in profile.get("furniture", []) if x["id"] not in removed]
        profile["mats"] = [x for x in profile.get("mats", []) if x.get("host") not in removed]
        profile["routes"] = [x for x in profile.get("routes", []) if x.get("from", {}).get("host") not in removed and x.get("to", {}).get("host") not in removed]
        for item_spec in spec["items"]:
            asset = ASSETS / f"{item_spec['asset']}.png"; registration = ASSETS / f"{item_spec['asset']}-registration.json"
            profile.setdefault("textures", {})[item_spec["id"]] = f"res://{asset.relative_to(ROOT).as_posix()}"
            item = {"id": item_spec["id"], "texture": item_spec["id"], "registration": f"res://{registration.relative_to(ROOT).as_posix()}", "footprint": item_spec["footprint"], "ground_width": item_spec["ground_width"], "centers_by_quarter": item_spec["centers"], "live_furniture": True}
            if item_spec.get("centerpiece"): item["centerpiece"] = True
            if item_spec.get("authored_anchor"): item["authored_anchor"] = True
            profile["furniture"].append(item); card = ASSETS / "cards" / f"{room}.png"
            manifest["assets"].append({"room": room, "id": item_spec["id"], "scope": item_spec["scope"], "size_class": item_spec["size_class"], "shape": "rectangle", "source_profile": spec["source"], "selected_profile": spec["output"], "asset": asset.relative_to(ROOT).as_posix(), "asset_sha256": digest(asset), "registration": registration.relative_to(ROOT).as_posix(), "registration_sha256": digest(registration), "generated_source": GENERATED[item_spec["asset"]], "centers_by_quarter": item_spec["centers"], "footprint": item_spec["footprint"], "card": f"assets/room-furnishings-v9/cards/{room}.png", "card_sha256": digest(card) if card.exists() else "", "agent_visual_review": "native-reviewed-12-views", "owner_acceptance": False})
        (ROOT / spec["output"]).write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Built 6 furnishing v9 assets across Radio Lab, Listening Post, and Holographic Core")

if __name__ == "__main__": main()
