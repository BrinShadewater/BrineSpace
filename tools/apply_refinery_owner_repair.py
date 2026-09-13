"""Mute refinery paint and remove exterior-connected white registration leaks."""
import colorsys
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

from register_alpha_silhouette import open_holes, polygons


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAP = {
    "assets/refinery-directional-v1/refinery-north.png": "assets/refinery-directional-v2/refinery-north.png",
    "assets/refinery-directional-v1/refinery-sides.png": "assets/refinery-directional-v2/refinery-sides.png",
    "assets/refinery-directional-v1/refinery-south.png": "assets/refinery-directional-v2/refinery-south.png",
}
EXPECTED_SOURCE_SHA256 = {
    "assets/refinery-directional-v1/refinery-north.png": "c887e52690279460bda2575948df64d9911c91bfccea5d525bb0b27ec0e7109f",
    "assets/refinery-directional-v1/refinery-sides.png": "d6332983c7e681b23818275fcaef0de16576bbff75eea0e8409af9047846d5da",
    "assets/refinery-directional-v1/refinery-south.png": "fc1254c4fd9331ff5ea118eb4877f821963bfe4c6cc8f2ef718bee6219adcb3d",
}
REGISTRATIONS = [
    "rooms/full-wall-v1/registrations/ore-refinery-wall.json",
    "rooms/full-wall-v1/registrations/side-ore-refinery-wall-east.json",
    "rooms/full-wall-v1/registrations/side-ore-refinery-wall-west.json",
    "rooms/full-wall-v1/registrations/side-ore-refinery-wall-south.json",
]


def mute_orange(source: Path, destination: Path) -> dict:
    expected = EXPECTED_SOURCE_SHA256[source.relative_to(ROOT).as_posix()]
    if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
        raise ValueError(f"Refusing to reapply the one-shot palette repair to changed source: {source}")
    image = Image.open(source).convert("RGB")
    rgb = np.asarray(image).astype(np.float32) / 255.0
    flat = rgb.reshape(-1, 3)
    hsv = np.array([colorsys.rgb_to_hsv(*pixel) for pixel in flat], dtype=np.float32)
    # Orange-painted housings move toward the room's burnt-orange engineering palette.
    # Yellow logistics markings remain separate; low-saturation copper and ore retain material identity.
    selected = (
        (hsv[:, 0] >= 0.015)
        & (hsv[:, 0] < 0.095)
        & (hsv[:, 1] >= 0.48)
        & (hsv[:, 2] >= 0.34)
    )
    hsv[selected, 0] *= 0.93
    hsv[selected, 1] *= 0.78
    hsv[selected, 2] *= 0.76
    revised = np.array([colorsys.hsv_to_rgb(*pixel) for pixel in hsv], dtype=np.float32)
    revised = np.clip(np.round(revised.reshape(rgb.shape) * 255.0), 0, 255).astype(np.uint8)
    alpha = np.where(exterior_neutral(image), 0, 255).astype(np.uint8)
    destination.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.dstack([revised, alpha]), "RGBA").save(destination)
    return {
        "source": source.relative_to(ROOT).as_posix(),
        "output": destination.relative_to(ROOT).as_posix(),
        "changed_pixels": int(selected.sum()),
        "transparent_exterior_pixels": int((alpha == 0).sum()),
        "total_pixels": int(selected.size),
        "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
    }


def exterior_neutral(image: Image.Image) -> np.ndarray:
    rgb = np.asarray(image.convert("RGB")).astype(np.int16)
    neutral = (rgb.min(2) >= 228) & ((rgb.max(2) - rgb.min(2)) <= 22)
    flood = Image.fromarray(np.where(neutral, 255, 0).astype("uint8")).copy()
    for x in range(image.width):
        if flood.getpixel((x, 0)) == 255:
            ImageDraw.floodfill(flood, (x, 0), 128)
        if flood.getpixel((x, image.height - 1)) == 255:
            ImageDraw.floodfill(flood, (x, image.height - 1), 128)
    for y in range(image.height):
        if flood.getpixel((0, y)) == 255:
            ImageDraw.floodfill(flood, (0, y), 128)
        if flood.getpixel((image.width - 1, y)) == 255:
            ImageDraw.floodfill(flood, (image.width - 1, y), 128)
    return np.asarray(flood) == 128


def pixel_geometry(mask: np.ndarray):
    spans = []
    for y, row in enumerate(mask):
        changes = np.flatnonzero(np.diff(np.pad(row.astype(np.int8), (1, 1))))
        spans.extend(box(int(left), y, int(right), y + 1) for left, right in zip(changes[::2], changes[1::2]))
    return unary_union(spans)


def repair_registration(path: Path, source_map: dict[str, dict]) -> dict:
    data = json.loads(path.read_text())
    old_source = data["source"].removeprefix("res://")
    new_source = SOURCE_MAP.get(old_source, old_source)
    if new_source not in SOURCE_MAP.values():
        raise ValueError(f"Unexpected refinery source: {old_source}")
    destination = ROOT / new_source
    shape = unary_union([Polygon(piece) for piece in data["pieces"]])
    repaired = shape.difference(pixel_geometry(exterior_neutral(Image.open(destination)))).simplify(1.0, preserve_topology=True)
    if repaired.is_empty:
        raise ValueError(f"Registration emptied: {path}")
    removed_area = float(shape.area - repaired.area)
    data["source"] = "res://" + new_source
    data["sha256"] = source_map[new_source]["sha256"]
    data["method"] = "Exterior-neutral registration repair; raster palette reduced, enclosed pale machine details retained"
    data["pieces"] = [
        [[round(x, 3), round(y, 3)] for x, y in list(piece.exterior.coords)[:-1]]
        for component in polygons(repaired)
        for piece in open_holes(component)
    ]
    data["owner_repair"] = {
        "registration_area_delta_after_1px_simplify": round(-removed_area, 3),
        "rule": "Only bright-neutral pixels connected to a raster edge were excluded; enclosed trim and gauges were retained.",
    }
    path.write_text(json.dumps(data, separators=(",", ":")) + "\n")
    return {"registration": path.relative_to(ROOT).as_posix(), "registration_area_delta": -removed_area, "pieces": len(data["pieces"])}


def main() -> None:
    sources = [mute_orange(ROOT / old, ROOT / new) for old, new in SOURCE_MAP.items()]
    source_map = {record["output"]: record for record in sources}
    registrations = [repair_registration(ROOT / item, source_map) for item in REGISTRATIONS]
    provenance = {
        "operation": "Ore Refinery owner repair",
        "palette_rule": "Mute saturated orange paint toward burnt orange; retain yellow logistics markings and lower-saturation copper/ore materials.",
        "cutout_rule": "Make exterior-connected bright-neutral source background transparent, then exclude any overlap from registered geometry.",
        "sources": sources,
        "registrations": registrations,
    }
    destination = ROOT / "assets/refinery-directional-v2/owner-repair.json"
    destination.write_text(json.dumps(provenance, indent=2) + "\n")
    print(json.dumps(provenance, indent=2))


if __name__ == "__main__":
    main()
