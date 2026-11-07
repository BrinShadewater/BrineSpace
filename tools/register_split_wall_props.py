"""Register separate sprite-sheet cells without cutting continuous machinery.

Writes vector registrations only; rejects silhouettes touching a cell divider.
Native door, facing and scale review remains required.
"""
import argparse
import json
from pathlib import Path
from PIL import Image
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from register_full_wall_props import ROOT, register
from register_alpha_silhouette import register as register_alpha, polygons, open_holes

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--columns', type=int, default=2)
    parser.add_argument('--rows', type=int, default=1)
    parser.add_argument('--row-cuts', help='Optional comma-separated native Y coordinates of reviewed white gutters')
    parser.add_argument('--labels', required=True, help='Comma-separated, row-major file labels')
    args = parser.parse_args()
    labels = args.labels.split(',')
    if args.columns < 1 or args.rows < 1 or len(labels) != args.columns * args.rows:
        parser.error('Positive dimensions and one label per cell required')
    if len(set(labels)) != len(labels) or any(not label.replace('-', '').replace('_', '').isalnum() for label in labels):
        parser.error('Labels must be unique simple filenames')
    source = args.source.resolve()
    relative = source.relative_to(ROOT).as_posix()
    if args.output.exists():
        parser.error('Output already exists; preserve prior registrations')
    with Image.open(source) as image:
        width, height = image.size
        alpha = 'A' in image.getbands() and image.getchannel('A').getextrema()[0] < 128
    cuts = [float(value) for value in args.row_cuts.split(',')] if args.row_cuts else [height * i / args.rows for i in range(1, args.rows)]
    if len(cuts) != args.rows - 1 or any(not 0 < cut < height for cut in cuts) or cuts != sorted(set(cuts)):
        parser.error('Row cuts must be strictly increasing inside the image, one per row boundary')
    boundaries = [0, *cuts, height]
    data = register_alpha(source) if alpha else register(source)
    data['source'] = 'res://' + relative
    shape = unary_union([Polygon(piece) for piece in data['pieces']])
    results = []
    for index, label in enumerate(labels):
        col, row = index % args.columns, index // args.columns
        left, top = col * width / args.columns, boundaries[row]
        right, bottom = (col + 1) * width / args.columns, boundaries[row + 1]
        part = shape.intersection(box(left, top, right, bottom))
        if part.is_empty:
            raise ValueError('Empty sprite cell: ' + label)
        x, y, x2, y2 = part.bounds
        if not (x > left + 1 and x2 < right - 1 and y > top + 1 and y2 < bottom - 1):
            raise ValueError('Sprite touches sheet edge or divider: ' + label)
        result = dict(data, region=[x, y, x2-x, y2-y], split_section=label)
        result['sheet_cell'] = [left, top, right, bottom]
        result['pieces'] = [[[round(px, 3), round(py, 3)] for px, py in list(p.exterior.coords)[:-1]] for poly in polygons(part) for p in open_holes(poly)]
        results.append((label, result))
    args.output.mkdir(parents=True)
    for label, result in results:
        (args.output / (label + '.json')).write_text(json.dumps(result, separators=(',', ':')) + '\n')
        print(label, result['region'])

if __name__ == '__main__':
    main()
