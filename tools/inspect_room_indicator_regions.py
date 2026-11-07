"""Read-only colour-cluster suggestions, NOT an automatic emissive-mask generator.

Printed source-pixel bounds need review: coloured paint/specimens can match LEDs.
Never modifies source images or changes asset acceptance status.
"""
import argparse
import json
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('source')
parser.add_argument('--colour', choices=['violet', 'cyan'], default='violet')
parser.add_argument('--minimum-pixels', type=int, default=3)
args = parser.parse_args()
image = Image.open(args.source).convert('RGBA')
pixels = image.load()
selected = set()
for y in range(image.height):
    for x in range(image.width):
        r, g, b, a = pixels[x, y]
        match = r - g >= 16 and b - g >= 26 and b >= 72 if args.colour == 'violet' else min(g, b) - r >= 26 and g >= 69
        if a >= 128 and match:
            selected.add((x, y))
components = []
while selected:
    seed = min(selected, key=lambda p: (p[1], p[0]))
    selected.remove(seed)
    pending, cluster = [seed], []
    while pending:
        x, y = pending.pop()
        cluster.append((x, y))
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                point = x + dx, y + dy
                if point in selected:
                    selected.remove(point)
                    pending.append(point)
    if len(cluster) < args.minimum_pixels:
        continue
    left, top = min(p[0] for p in cluster), min(p[1] for p in cluster)
    right, bottom = max(p[0] for p in cluster), max(p[1] for p in cluster)
    components.append({'pixels': len(cluster), 'rect': [left, top, right-left+1, bottom-top+1]})
print(json.dumps({'source': args.source, 'size': image.size, 'colour': args.colour, 'minimum_pixels': args.minimum_pixels, 'suggestions_only': components}, indent=2))
