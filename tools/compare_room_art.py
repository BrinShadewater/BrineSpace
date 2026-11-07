"""Compare native catalog captures: pixels, prop inventory and placement.

Read-only evidence for directional art revisions. A clean inventory comparison
does not establish facing, style or functional behavior; inspect native images.
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]


def capture_rooms(directory):
    return {room['id']: room for room in json.loads((directory / 'runtime.json').read_text())}


def capture_image(room, quarter):
    suffix = f'-q{quarter}.png'
    source = next(path for path in room['images'] if path.endswith(suffix))
    path = ROOT / source.removeprefix('res://')
    with Image.open(path) as image:
        return image.convert('RGB')


def compare(before, after):
    old, new = capture_rooms(before), capture_rooms(after)
    result = {'removed_rooms': sorted(old.keys() - new.keys()),
              'added_rooms': sorted(new.keys() - old.keys()), 'rooms': {}}
    for room_id in sorted(old.keys() & new.keys()):
        old_views = {v['quarter']: v for v in old[room_id]['views']}
        new_views = {v['quarter']: v for v in new[room_id]['views']}
        room = {'removed_views': sorted(old_views.keys() - new_views.keys()),
                'added_views': sorted(new_views.keys() - old_views.keys()), 'views': {}}
        for quarter in sorted(old_views.keys() & new_views.keys()):
            a = {p['id']: p for p in old_views[quarter]['props']}
            b = {p['id']: p for p in new_views[quarter]['props']}
            first, second = capture_image(old[room_id], quarter), capture_image(new[room_id], quarter)
            same_size = first.size == second.size
            fields = ['rect', 'visual_bounds', 'side_view', 'variant_source', 'wall_mount']
            room['views'][quarter] = {
                'same_image_size': same_size,
                'changed_pixel_bounds': ImageChops.difference(first, second).getbbox() if same_size else None,
                'added_props': sorted(b.keys() - a.keys()),
                'removed_props': sorted(a.keys() - b.keys()),
                'changed_props': {key: {field: {'before': a[key].get(field), 'after': b[key].get(field)}
                                        for field in fields if a[key].get(field) != b[key].get(field)}
                                  for key in sorted(a.keys() & b.keys())
                                  if any(a[key].get(field) != b[key].get(field) for field in fields)},
            }
        result['rooms'][room_id] = room
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path)
    parser.add_argument('after', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    report = compare(args.before, args.after)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    for room_id, room in report['rooms'].items():
        for quarter, view in room['views'].items():
            print(f"{room_id} q{quarter}: pixels={view['changed_pixel_bounds']} "
                  f"added={view['added_props']} removed={view['removed_props']} "
                  f"changed={list(view['changed_props'])}")
    print(f"Report: {args.out}")
