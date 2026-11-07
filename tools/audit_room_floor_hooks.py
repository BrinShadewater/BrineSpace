"""Static floor-hook audit for room dressing; not proof of runtime drawing or aesthetics."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def floor_bodies(path, seen=None):
    seen = set() if seen is None else seen
    if path in seen:
        return []
    seen.add(path)
    source = path.read_text(encoding='utf-8-sig')
    parent = re.search(r'^extends "res://([^\"]+)"', source, re.M)
    body = re.search(r'^func draw_room_floor\([^\n]+\n(.*?)(?=^func |\Z)', source, re.M | re.S)
    result = [(path, body.group(1))] if body else []
    if parent and (not body or 'super.draw_room_floor(' in body.group(1)):
        result += floor_bodies(ROOT / parent.group(1), seen)
    return result


def audit():
    records, errors = [], []
    for path in sorted((ROOT / 'rooms').rglob('*view.gd')):
        source = path.read_text(encoding='utf-8-sig')
        registrations = re.findall(r'(\w+)\s*=\s*\w*Dressing\.new\(self,"res://([^\"]+)"\)', source)
        for variable, profile in registrations:
            data = json.loads((ROOT / profile).read_text(encoding='utf-8-sig'))
            count = sum(len(data.get(key, [])) for key in ('mats', 'routes', 'surface_routes', 'decals'))
            hooks = [str(p.relative_to(ROOT)) for p, body in floor_bodies(path)
                     if re.search(r'\b' + re.escape(variable) + r'\.floor\(\)', body)]
            record = {'view': str(path.relative_to(ROOT)), 'profile': profile,
                      'floor_details': count, 'hook_owners': hooks}
            records.append(record)
            if count and len(hooks) != 1:
                record['problem'] = 'missing floor hook' if not hooks else 'duplicate inherited floor hooks'
                errors.append(record)
    return {'scope': 'Static selected-profile floor hook reachability; conditions, pixels and runtime hosts require separate review',
            'profiles': len(records), 'records': records, 'errors': errors}


if __name__ == '__main__':
    result = audit()
    print(json.dumps(result, indent=2))
    sys.exit(bool(result['errors']))
