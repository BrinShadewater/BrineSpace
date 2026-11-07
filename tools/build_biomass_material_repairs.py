"""Rebalance Biomass wall colors and repair its service-bench source matte."""
from __future__ import annotations

import colorsys
import hashlib
import json
from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "assets/biomass-material-v2"
REG_DIR = ROOT / "rooms/full-wall-v1/registrations"
WALL_SOURCES = {
    "north": ROOT / "assets/room-consistency-v1/biomass-north.png",
    "sides": ROOT / "assets/room-consistency-v1/biomass-sides.png",
    "south": ROOT / "assets/room-consistency-v1/biomass-south.png",
}
SUPPORT_SOURCE = ROOT / "assets/material-polish-v4/maintenance-support.png"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remove_exterior_neutral(source: Image.Image) -> tuple[Image.Image, int]:
    image = source.convert("RGBA")
    px = image.load()
    queue = deque()
    seen = set()
    for x in range(image.width):
        queue.extend(((x, 0), (x, image.height - 1)))
    for y in range(image.height):
        queue.extend(((0, y), (image.width - 1, y)))
    removed = 0
    while queue:
        x, y = queue.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        r, g, b, a = px[x, y]
        if a == 0 or min(r, g, b) < 210 or max(r, g, b) - min(r, g, b) > 24:
            continue
        px[x, y] = (r, g, b, 0)
        removed += 1
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < image.width and 0 <= ny < image.height:
                queue.append((nx, ny))
    return image, removed


def recolor_wall(source: Path, output: Path) -> dict:
    image, removed = remove_exterior_neutral(Image.open(source))
    px = image.load()
    recolored = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            if 0.035 <= h <= 0.115 and s >= 0.46 and v >= 0.30:
                # Match the olive/moss feedstock windows without making hardware
                # luminous or erasing its value separation from charcoal steel.
                h = 0.205
                s = 0.42 + min(0.14, (s - 0.46) * 0.30)
                v = min(0.58, 0.28 + (v - 0.30) * 0.50)
                nr, ng, nb = colorsys.hsv_to_rgb(h, s, v)
                px[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255), a)
                recolored += 1
    image.save(output)
    return {"source": str(source.relative_to(ROOT)).replace("\\", "/"), "source_sha256": sha(source), "output_sha256": sha(output), "exterior_pixels_removed": removed, "orange_pixels_recolored": recolored}


def build_support(output: Path) -> dict:
    image, removed = remove_exterior_neutral(Image.open(SUPPORT_SOURCE))
    px = image.load()
    lifted = 0
    # Biomass uses the upper-left bench registration only.
    for y in range(148, 572):
        for x in range(135, 639):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            if s <= 0.30 and 0.10 <= v <= 0.50:
                v = min(0.56, v * 1.16 + 0.025)
                s *= 0.92
                nr, ng, nb = colorsys.hsv_to_rgb(h, s, v)
                px[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255), a)
                lifted += 1
    image.save(output)
    return {"source": str(SUPPORT_SOURCE.relative_to(ROOT)).replace("\\", "/"), "source_sha256": sha(SUPPORT_SOURCE), "output_sha256": sha(output), "exterior_pixels_removed": removed, "bench_midtones_lifted": lifted}


def update_registration(name: str, source: Path) -> None:
    path = REG_DIR / name
    data = json.loads(path.read_text(encoding="utf-8"))
    data["source"] = "res://" + str(source.relative_to(ROOT)).replace("\\", "/")
    data["sha256"] = sha(source)
    data["method"] = "Existing reviewed geometry retained; border-connected neutral cleanup and semantic orange-to-moss material correction"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    PACK.mkdir(parents=True, exist_ok=True)
    wall_records = {}
    for direction, source in WALL_SOURCES.items():
        output = PACK / f"biomass-{direction}-moss-v1.png"
        wall_records[direction] = recolor_wall(source, output)
    support = PACK / "biomass-service-support-matte-v1.png"
    support_record = build_support(support)
    update_registration("biomass-processing-wall.json", PACK / "biomass-north-moss-v1.png")
    update_registration("side-biomass-processing-wall-east.json", PACK / "biomass-sides-moss-v1.png")
    update_registration("side-biomass-processing-wall-west.json", PACK / "biomass-sides-moss-v1.png")
    update_registration("side-biomass-processing-wall-south.json", PACK / "biomass-south-moss-v1.png")
    record = {
        "room": "biomass_digester",
        "operation": "moss material alignment, true-alpha service support and bench midtone lift",
        "walls": wall_records,
        "service_support": support_record,
    }
    (PACK / "material-build.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
