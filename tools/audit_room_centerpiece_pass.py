"""Audit the selected room-centerpiece batch and its final native evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets/room-centerpieces-v1/manifest.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    entries = manifest["rooms"]
    runtime_path = ROOT / manifest["native_evidence"]
    runtime = {record["id"]: record for record in json.loads(runtime_path.read_text(encoding="utf-8"))}

    for entry in entries:
        asset = ROOT / entry["asset"]
        registration = ROOT / entry["registration"]
        if not asset.is_file() or sha256(asset) != entry["asset_sha256"]:
            errors.append(f"{entry['centerpiece']}: missing or stale raster")
            continue
        if not registration.is_file() or sha256(registration) != entry["registration_sha256"]:
            errors.append(f"{entry['centerpiece']}: missing or stale registration")
        with Image.open(asset) as image:
            if image.mode != "RGBA" or image.size != (1254, 1254):
                errors.append(f"{entry['centerpiece']}: expected RGBA 1254x1254, got {image.mode} {image.size}")
            elif image.getchannel("A").getextrema() != (0, 255):
                errors.append(f"{entry['centerpiece']}: alpha channel lacks transparent and opaque pixels")
        room = runtime.get(entry["room"])
        if room is None or len(room.get("views", [])) != 4:
            errors.append(f"{entry['centerpiece']}: missing four-view native evidence")
            continue
        for view in room["views"]:
            ids = {prop["id"] for prop in view.get("props", [])}
            if entry["centerpiece"] not in ids:
                errors.append(f"{entry['centerpiece']}: absent from quarter {view.get('quarter')}")
        profile = json.loads((ROOT / entry["selected_profile"]).read_text(encoding="utf-8"))
        selected = next((item for item in profile.get("furniture", []) if item["id"] == entry["centerpiece"]), None)
        if selected is None:
            errors.append(f"{entry['centerpiece']}: absent from selected profile")
        elif selected.get("registration", "").removeprefix("res://") != entry["registration"]:
            errors.append(f"{entry['centerpiece']}: selected profile registration differs")

    rejected_text = "\n".join(
        (ROOT / entry["selected_profile"]).read_text(encoding="utf-8") for entry in entries
    )
    for rejected in manifest["rejected"]:
        if rejected["asset"] in rejected_text or Path(rejected["asset"]).name in rejected_text:
            errors.append(f"rejected candidate is selected: {rejected['asset']}")

    square_rect = sum(
        1 for entry in entries if "square" in entry["shape"] or "rect" in entry["shape"]
    )
    report = {
        "selected_assets": len(entries),
        "large_assets": sum(entry["size_class"] == "large" for entry in entries),
        "medium_assets": sum(entry["size_class"] == "medium" for entry in entries),
        "square_or_rectangular_assets": square_rect,
        "rooms": len({entry["room"] for entry in entries}),
        "native_orientations": sum(len(record.get("views", [])) for record in runtime.values()),
        "rejected_candidates": len(manifest["rejected"]),
        "errors": errors,
    }
    print(json.dumps(report, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
