"""Derive exact four-direction families from the owner-preferred south banks."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
REGISTRATIONS = ROOT / "rooms/full-wall-v1/registrations"
PACK = ROOT / "assets/owner-strict-overhead-v1"
FAMILIES = {
    "medical-treatment-wall": "side-medical-treatment-wall-south.json",
    "mycelium-cultivation-wall": "side-mycelium-cultivation-wall-south.json",
    "crew-lounge-built-in": "side-crew-lounge-built-in-south.json",
    "drone-service-wall": "side-drone-service-wall-south.json",
    "research-analysis-wall": "side-research-analysis-wall-south.json",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def turn_point(point: list[float], operation: str, size: tuple[int, int]) -> list[float]:
    x, y = point
    width, height = size
    if operation == "south":
        return [x, y]
    if operation == "north":
        return [width - x, height - y]
    if operation == "east":  # counter-clockwise: rear edge moves from south to east
        return [y, width - x]
    if operation == "west":  # clockwise: rear edge moves from south to west
        return [height - y, x]
    raise ValueError(operation)


def turn_image(image: Image.Image, operation: str) -> Image.Image:
    if operation == "south":
        return image.copy()
    if operation == "north":
        return image.transpose(Image.Transpose.ROTATE_180)
    if operation == "east":
        return image.transpose(Image.Transpose.ROTATE_90)
    if operation == "west":
        return image.transpose(Image.Transpose.ROTATE_270)
    raise ValueError(operation)


def transformed_registration(
    canonical: dict, source: Path, direction: str, source_size: tuple[int, int], backup: Path
) -> dict:
    pieces = [
        [turn_point(point, direction, source_size) for point in polygon]
        for polygon in canonical["pieces"]
    ]
    all_points = [point for polygon in pieces for point in polygon]
    left = min(point[0] for point in all_points)
    top = min(point[1] for point in all_points)
    right = max(point[0] for point in all_points)
    bottom = max(point[1] for point in all_points)
    return {
        "source": "res://" + source.relative_to(ROOT).as_posix(),
        "sha256": digest(source),
        "method": "Exact raster and registration quarter-turn from owner-preferred south overhead bank",
        "native_size": list(Image.open(source).size),
        "region": [left, top, right - left, bottom - top],
        "pieces": pieces,
        "direction": direction,
        "wall_contact": {
            "side": direction,
            "purpose": "Rear edge against wall; controls, access and seating face inward",
        },
        "previous_registration": "res://" + backup.relative_to(ROOT).as_posix(),
    }


def target_names(family: str) -> dict[str, str]:
    return {
        "north": f"{family}.json",
        "east": f"side-{family}-east.json",
        "south": f"side-{family}-south.json",
        "west": f"side-{family}-west.json",
    }


def main() -> None:
    manifest = {
        "operation": "Exact north/east/south/west turns from each current owner-preferred south overhead source",
        "families": {},
    }
    for family, canonical_name in FAMILIES.items():
        family_pack = PACK / family
        backup_dir = family_pack / "registrations-before"
        backup_dir.mkdir(parents=True, exist_ok=True)
        canonical_path = REGISTRATIONS / canonical_name
        canonical_backup = backup_dir / f"{canonical_name}.original"
        canonical_record = canonical_backup if canonical_backup.exists() else canonical_path
        canonical = json.loads(canonical_record.read_text(encoding="utf-8"))
        source_path = ROOT / canonical["source"].removeprefix("res://")
        source_image = Image.open(source_path).convert("RGB")
        source_size = source_image.size
        family_record = {
            "canonical_registration": f"rooms/full-wall-v1/registrations/{canonical_name}",
            "canonical_source": canonical["source"].removeprefix("res://"),
            "canonical_source_sha256": digest(source_path),
            "source_size": list(source_size),
            "directions": {},
        }
        targets = target_names(family)
        for direction, target_name in targets.items():
            target = REGISTRATIONS / target_name
            backup = backup_dir / f"{target_name}.original"
            if not backup.exists():
                shutil.copyfile(target, backup)
            output = family_pack / f"{direction}.png"
            turn_image(source_image, direction).save(output, optimize=True)
            registration = transformed_registration(canonical, output, direction, source_size, backup)
            target.write_text(json.dumps(registration, indent=2) + "\n", encoding="utf-8")
            family_record["directions"][direction] = {
                "source": output.relative_to(ROOT).as_posix(),
                "sha256": digest(output),
                "registration": target.relative_to(ROOT).as_posix(),
            }
        manifest["families"][family] = family_record
    PACK.mkdir(parents=True, exist_ok=True)
    (PACK / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"PASS derived {len(FAMILIES)} strict-overhead families and {len(FAMILIES) * 4} directions")


if __name__ == "__main__":
    main()
