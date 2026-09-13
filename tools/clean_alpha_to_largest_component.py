"""Keep one reviewed connected sprite silhouette and clear generated alpha specks."""
import argparse
from collections import deque
from pathlib import Path

from PIL import Image


def components(alpha: Image.Image) -> list[list[tuple[int, int]]]:
    seen = bytearray(alpha.width * alpha.height)
    found = []
    for y in range(alpha.height):
        for x in range(alpha.width):
            index = y * alpha.width + x
            if seen[index] or alpha.getpixel((x, y)) == 0:
                continue
            queue = deque([(x, y)])
            seen[index] = 1
            component = []
            while queue:
                px, py = queue.popleft()
                component.append((px, py))
                for nx, ny in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                    if not (0 <= nx < alpha.width and 0 <= ny < alpha.height):
                        continue
                    neighbor = ny * alpha.width + nx
                    if seen[neighbor] or alpha.getpixel((nx, ny)) == 0:
                        continue
                    seen[neighbor] = 1
                    queue.append((nx, ny))
            found.append(component)
    return sorted(found, key=len, reverse=True)


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=Path)
parser.add_argument("destination", type=Path)
parser.add_argument("--min-main-pixels", type=int, required=True)
args = parser.parse_args()
if args.destination.exists():
    parser.error("Destination exists; use a new path to preserve provenance")
image = Image.open(args.source).convert("RGBA")
found = components(image.getchannel("A"))
if not found or len(found[0]) < args.min_main_pixels:
    raise ValueError("No dominant reviewed silhouette at the expected scale")
removed = 0
for component in found[1:]:
    for point in component:
        red, green, blue, _ = image.getpixel(point)
        image.putpixel(point, (red, green, blue, 0))
        removed += 1
args.destination.parent.mkdir(parents=True, exist_ok=True)
image.save(args.destination, optimize=True)
print(f"PASS components={len(found)} main={len(found[0])} removed={removed} alpha_bounds={image.getchannel('A').getbbox()}")
