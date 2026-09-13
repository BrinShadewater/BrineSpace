"""Report 4-connected visible-alpha components in one or more PNGs."""
import argparse
import json
from collections import deque
from pathlib import Path

from PIL import Image


def audit(path: Path) -> dict:
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    seen = bytearray(image.width * image.height)
    components = []
    for y in range(image.height):
        for x in range(image.width):
            index = y * image.width + x
            if seen[index] or alpha.getpixel((x, y)) == 0:
                continue
            queue = deque([(x, y)])
            seen[index] = 1
            count = 0
            bounds = [x, y, x, y]
            while queue:
                px, py = queue.popleft()
                count += 1
                bounds = [min(bounds[0], px), min(bounds[1], py), max(bounds[2], px), max(bounds[3], py)]
                for nx, ny in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                    if not (0 <= nx < image.width and 0 <= ny < image.height):
                        continue
                    neighbor = ny * image.width + nx
                    if seen[neighbor] or alpha.getpixel((nx, ny)) == 0:
                        continue
                    seen[neighbor] = 1
                    queue.append((nx, ny))
            components.append({"pixels": count, "bounds": bounds})
    components.sort(key=lambda item: item["pixels"], reverse=True)
    return {"path": path.as_posix(), "size": image.size, "components": components}


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("png", type=Path, nargs="+")
args = parser.parse_args()
print(json.dumps([audit(path) for path in args.png], indent=2))
