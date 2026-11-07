"""Read source alpha and emit vector registration; never modify/write raster art.

Pillow reads alpha, Shapely unions pixel runs and opens holes into separate polygons.
The result still requires native review: alpha is not a semantic object mask.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image
from shapely.geometry import Polygon, box
from shapely.ops import unary_union


def polygons(geometry):
    if geometry.geom_type == "Polygon":
        yield geometry
    elif hasattr(geometry, "geoms"):
        for child in geometry.geoms:
            yield from polygons(child)


def open_holes(polygon):
    """Cut through one hole per step; draw_polygon cannot encode interior rings."""
    if not polygon.interiors:
        yield polygon
        return
    hole = Polygon(polygon.interiors[0])
    cut = hole.representative_point().y
    left, top, right, bottom = polygon.bounds
    for band in [box(left-1, top-1, right+1, cut), box(left-1, cut, right+1, bottom+1)]:
        for part in polygons(polygon.intersection(band)):
            yield from open_holes(part)


def register(source, threshold=128, min_area=16, simplify=1.0):
    with Image.open(source) as image:
        if "A" not in image.getbands():
            raise ValueError("Source has no alpha channel; RGB backgrounds are not silhouettes")
        mask = np.asarray(image.getchannel("A")) >= threshold
        size = list(image.size)
    if mask.all():
        raise ValueError("No exterior alpha below threshold; channel presence is not transparency")
    spans = []
    for y, row in enumerate(mask):
        changes = np.flatnonzero(np.diff(np.pad(row.astype(np.int8), (1, 1))))
        spans.extend(box(int(a), y, int(b), y+1) for a, b in zip(changes[::2], changes[1::2]))
    if not spans:
        raise ValueError("No source pixels meet the alpha threshold")
    components = [p.simplify(simplify, preserve_topology=True) for p in polygons(unary_union(spans)) if p.area >= min_area]
    if not components:
        raise ValueError("No silhouette component meets the minimum area")
    bounds = unary_union(components).bounds
    pieces = [list(p.exterior.coords)[:-1] for component in components for p in open_holes(component)]
    return {
        "source": source.as_posix(),
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "native_size": size,
        "method": "Read-only alpha to vector registration; raster unchanged",
        "threshold": threshold,
        "minimum_component_area": min_area,
        "simplify_source_pixels": simplify,
        "components": len(components),
        "region": [bounds[0], bounds[1], bounds[2]-bounds[0], bounds[3]-bounds[1]],
        "pieces": [[[round(x, 3), round(y, 3)] for x, y in piece] for piece in pieces],
        "visual_acceptance": "pending native review",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--threshold", type=int, default=128)
    parser.add_argument("--min-area", type=float, default=16)
    parser.add_argument("--simplify", type=float, default=1.0)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output already exists; choose a new registration revision")
    if not 1 <= args.threshold <= 255 or args.min_area < 0 or args.simplify < 0:
        parser.error("Invalid threshold, area or simplification")
    result = register(args.source, args.threshold, args.min_area, args.simplify)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as output:
        json.dump(result, output, indent=2)
        output.write("\n")
    print(f"Registered {result['components']} components as {len(result['pieces'])} polygons; source unchanged")


if __name__ == "__main__":
    main()
