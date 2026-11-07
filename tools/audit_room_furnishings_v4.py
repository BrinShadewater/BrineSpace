"""Audit the six v4 furnishing sources, registrations, cards, profiles, and native views."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets/room-furnishings-v4/manifest.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    native_path = ROOT / data["native_evidence"]
    native = json.loads(native_path.read_text(encoding="utf-8")) if native_path.exists() else []
    views = {row["id"]: row.get("views", []) for row in native}
    for record in data["assets"]:
        for key, hash_key in (("asset", "asset_sha256"), ("registration", "registration_sha256"), ("card", "card_sha256")):
            path = ROOT / record[key]
            if not path.exists():
                errors.append(f"{record['id']}: missing {key} {record[key]}")
            elif digest(path) != record[hash_key]:
                errors.append(f"{record['id']}: stale {key} hash")
        image = Image.open(ROOT / record["asset"])
        if image.size != (1254, 1254) or image.mode != "RGBA" or image.getchannel("A").getextrema() != (0, 255):
            errors.append(f"{record['id']}: expected 1254-square true-alpha RGBA source")
        profile = json.loads((ROOT / record["selected_profile"]).read_text(encoding="utf-8"))
        if record["id"] not in {item["id"] for item in profile.get("furniture", [])}:
            errors.append(f"{record['id']}: absent from selected profile")
        room_views = views.get(record["room"], [])
        if len(room_views) != 4:
            errors.append(f"{record['room']}: expected four native views")
        elif any(record["id"] not in {prop["id"] for prop in view["props"]} for view in room_views):
            errors.append(f"{record['id']}: absent from a native view")
    summary = {
        "assets": len(data["assets"]),
        "themed": sum(item["scope"] == "themed" for item in data["assets"]),
        "universal": sum(item["scope"] == "universal" for item in data["assets"]),
        "large": sum(item["size_class"] == "large" for item in data["assets"]),
        "medium": sum(item["size_class"] == "medium" for item in data["assets"]),
        "rooms": len({item["room"] for item in data["assets"]}),
        "native_orientations": sum(len(value) for value in views.values()),
        "errors": errors,
    }
    print(json.dumps(summary, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
