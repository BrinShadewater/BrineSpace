"""Audit room furnishings v2 sources, profiles, cards, and final native evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets/room-furnishings-v2/manifest.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    runtime = {row["id"]: row for row in json.loads((ROOT / data["native_evidence"]).read_text(encoding="utf-8"))}
    errors: list[str] = []
    for item in data["assets"]:
        for key, hash_key in (("asset", "asset_sha256"), ("registration", "registration_sha256"), ("card", "card_sha256")):
            path = ROOT / item[key]
            if not path.is_file() or digest(path) != item[hash_key]:
                errors.append(f"{item['id']}: missing or stale {key}")
        with Image.open(ROOT / item["asset"]) as image:
            if image.mode != "RGBA" or image.size != (1254, 1254) or image.getchannel("A").getextrema() != (0, 255):
                errors.append(f"{item['id']}: invalid source dimensions/mode/alpha")
        profile = json.loads((ROOT / item["selected_profile"]).read_text(encoding="utf-8"))
        if not any(prop["id"] == item["id"] for prop in profile.get("furniture", [])):
            errors.append(f"{item['id']}: missing from selected profile")
        room = runtime.get(item["room"])
        if room is None or len(room.get("views", [])) != 4:
            errors.append(f"{item['id']}: missing four-view native record")
        else:
            for view in room["views"]:
                if item["id"] not in {prop["id"] for prop in view.get("props", [])}:
                    errors.append(f"{item['id']}: absent from quarter {view.get('quarter')}")
    report = {
        "assets": len(data["assets"]),
        "themed": sum(item["scope"] == "themed" for item in data["assets"]),
        "universal": sum(item["scope"] == "universal" for item in data["assets"]),
        "large": sum(item["size_class"] == "large" for item in data["assets"]),
        "medium": sum(item["size_class"] == "medium" for item in data["assets"]),
        "rooms": len({item["room"] for item in data["assets"]}),
        "native_orientations": sum(len(row.get("views", [])) for row in runtime.values()),
        "errors": errors,
    }
    print(json.dumps(report, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
