"""Read-only composition dependency audit; does not establish visual acceptance."""
import argparse
import hashlib
import json
from pathlib import Path


def resource_path(value):
    return value.removeprefix("res://").replace("\\", "/")


def audit(root, manifests):
    errors, profiles = [], 0
    for manifest in manifests:
        for room in json.loads((root / manifest).read_text(encoding="utf-8-sig")):
            declared = {resource_path(a["path"]): a for a in room.get("component_assets", [])}
            declared[resource_path(room["source"])] = room
            for asset in room.get("composition_assets", []):
                profiles += 1
                path = root / resource_path(asset["path"])
                if not path.is_file():
                    errors.append(f"{room['id']}: missing profile {path}")
                    continue
                if hashlib.sha256(path.read_bytes()).hexdigest() != asset["sha256"]:
                    errors.append(f"{room['id']}: stale profile hash {path}")
                profile = json.loads(path.read_text(encoding="utf-8-sig"))
                for texture in profile.get("textures", {}).values():
                    relative = resource_path(texture)
                    image = root / relative
                    if relative not in declared:
                        errors.append(f"{room['id']}: undeclared texture {relative}")
                    elif not image.is_file():
                        errors.append(f"{room['id']}: missing texture {relative}")
                    elif hashlib.sha256(image.read_bytes()).hexdigest() != declared[relative]["sha256"]:
                        errors.append(f"{room['id']}: stale texture hash {relative}")
    return profiles, errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifests", nargs="+", type=Path)
    args = parser.parse_args()
    count, errors = audit(Path(__file__).resolve().parents[1], args.manifests)
    print(json.dumps({"profiles": count, "errors": errors}, indent=2))
    raise SystemExit(bool(errors))
