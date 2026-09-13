"""Record v5 profile, card, and component dependencies in owning room manifests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPDATES = {
    "reactor": ("rooms/whole-room/export-manifest.json", "rooms/whole-room/reactor-composition-v3.json"),
    "clone_lab": ("rooms/underwater/batch-two/export-manifest.json", "rooms/underwater/batch-two/clone-composition-v3.json"),
    "biodome": ("rooms/underwater/batch-two/export-manifest.json", "rooms/underwater/batch-two/biodome-composition-v3.json"),
}


def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def main() -> None:
    grouped: dict[str, list[tuple[str, str]]] = {}
    for room, (manifest, profile) in UPDATES.items():
        grouped.setdefault(manifest, []).append((room, profile))
    for manifest_path, changes in grouped.items():
        path = ROOT / manifest_path
        records = json.loads(path.read_text(encoding="utf-8-sig"))
        by_id = {record["id"]: record for record in records}
        for room, profile_path in changes:
            record = by_id[room]
            profile = json.loads((ROOT / profile_path).read_text(encoding="utf-8"))
            declared = {item["path"].removeprefix("res://").replace("\\", "/"): item for item in record.get("component_assets", [])}
            for texture in profile.get("textures", {}).values():
                relative = texture.removeprefix("res://").replace("\\", "/")
                declared[relative] = {"path": relative, "sha256": digest(relative)}
            for item in profile.get("furniture", []):
                registration = item.get("registration", "").removeprefix("res://").replace("\\", "/")
                if registration:
                    declared[registration] = {"path": registration, "sha256": digest(registration)}
            record["component_assets"] = list(declared.values())
            record["composition_profile"] = profile_path
            record["composition_assets"] = [{"path": profile_path, "sha256": digest(profile_path)}]
            card = f"assets/room-furnishings-v5/cards/{room}.png"
            if isinstance(record.get("selected"), dict): record["selected"]["card"] = card
            record["card"] = {"path": card, "sha256": digest(card)}
            record.setdefault("verification", {})["furnishing_v5"] = (
                "Native four-orientation review and route evidence recorded in assets/room-furnishings-v5/manifest.json; owner acceptance pending."
            )
        path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
        print(f"Updated {manifest_path}: {len(changes)} room records")


if __name__ == "__main__":
    main()
