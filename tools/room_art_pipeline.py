"""Non-destructive room PNG cleanup. Pillow required; no generation/API calls.

Only neutral light pixels connected to the exterior or explicitly reviewed gap
seeds are removed. Unselected interior lamps are preserved. Always inspect the
result: this is not semantic segmentation.
"""
import argparse
from collections import deque
import json
from pathlib import Path
from PIL import Image


def clear_exterior(source, gap_seeds=()):
    image = source.convert('RGBA').copy()
    width, height = image.size
    pixels = image.load()
    seen = bytearray(width * height)
    queue = deque()
    for x, y in gap_seeds:
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError('Gap seed is outside the source canvas')
        r, g, b, a = pixels[x, y]
        if a and not (min(r, g, b) >= 190 and max(r, g, b) - min(r, g, b) <= 24):
            raise ValueError('Gap seed must select light neutral background')
        queue.append((x, y))
    for x in range(width):
        queue.extend(((x, 0), (x, height - 1)))
    for y in range(height):
        queue.extend(((0, y), (width - 1, y)))
    while queue:
        x, y = queue.popleft()
        index = y * width + x
        if seen[index]:
            continue
        seen[index] = 1
        r, g, b, a = pixels[x, y]
        if a > 0 and not (min(r, g, b) >= 190 and max(r, g, b) - min(r, g, b) <= 24):
            continue
        pixels[x, y] = (0, 0, 0, 0)
        for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            if 0 <= nx < width and 0 <= ny < height and not seen[ny * width + nx]:
                queue.append((nx, ny))
    return image


def normalize(source, size=1280, margin=8):
    if size <= 0 or margin < 0 or margin * 2 >= size:
        raise ValueError('Invalid canvas size or margin')
    source = source.convert('RGBA')
    bounds = source.getchannel('A').getbbox()
    if bounds is None:
        raise ValueError('Room has no visible pixels')
    cropped = source.crop(bounds)
    scale = (size - margin * 2) / max(cropped.size)
    dimensions = tuple(max(1, round(n * scale)) for n in cropped.size)
    cropped = cropped.resize(dimensions, Image.Resampling.NEAREST)
    output = Image.new('RGBA', (size, size))
    output.alpha_composite(cropped, ((size-dimensions[0])//2, (size-dimensions[1])//2))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--size', type=int, default=1280)
    parser.add_argument('--margin', type=int, default=8)
    parser.add_argument('--clear-gap', type=int, nargs=2, action='append', default=[],
                        metavar=('X', 'Y'), help='Reviewed enclosed background seed; repeat per gap')
    parser.add_argument('--keep-canvas', action='store_true', help='Preserve source pixel coordinates')
    args = parser.parse_args()
    if args.destination.exists():
        parser.error('Destination exists; use a new filename to preserve prior work')
    with Image.open(args.source) as original:
        output = clear_exterior(original, args.clear_gap)
        if not args.keep_canvas:
            output = normalize(output, args.size, args.margin)
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    output.save(args.destination)
    print(json.dumps({'source': str(args.source), 'output': str(args.destination),
                      'size': output.size, 'alpha_bounds': output.getbbox()}))


if __name__ == '__main__':
    main()
