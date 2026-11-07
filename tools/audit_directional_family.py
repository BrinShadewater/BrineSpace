"""Audit standalone directional metadata; never grants visual or runtime acceptance."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile

OPPOSITE = {'north': 'south', 'south': 'north', 'west': 'east', 'east': 'west'}
BACKING = {'north': 'top', 'south': 'bottom', 'west': 'left', 'east': 'right'}
REPORT_KIND = 'brinespace.directional-family-audit.v1'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(root, family):
    root = Path(root).resolve()
    def local(value):
        if not isinstance(value, str) or not value:
            raise ValueError('Required local path missing')
        p = (root/value.removeprefix('res://')).resolve()
        if not p.is_relative_to(root) or not p.is_file():
            raise ValueError(f'Missing or external file: {value}')
        return p
    def read(value):
        return json.loads(local(value).read_text(encoding='utf-8'))
    def require(condition, message):
        if not condition:
            raise ValueError(message)
    require(not ('directions' in family and 'orientations' in family), 'Ambiguous direction maps')
    views = family.get('directions', family.get('orientations'))
    require(isinstance(views, dict) and bool(views), 'Nonempty direction map required')
    require(set(views) <= set(OPPOSITE), 'Unknown wall direction')
    missing = sorted(set(OPPOSITE)-set(views))
    if 'missing_directions' in family:
        declared = family['missing_directions']
        require(isinstance(declared, list) and len(declared)==len(set(declared)) and sorted(declared)==missing,
                'Declared missing directions disagree with coverage')
    seen = set()
    results = []
    for side, entry in views.items():
        require(isinstance(entry, dict), 'Invalid direction entry')
        require(entry.get('inward')==OPPOSITE[side], f'{side}: wrong inward metadata')
        if 'backing_edge' in entry:
            require(entry['backing_edge']==BACKING[side], f'{side}: wrong backing metadata')
        export = local(entry.get('export'))
        require(export not in seen, 'Duplicate directional export')
        seen.add(export)
        actual = digest(export)
        require(actual==entry.get('sha256'), f'{side}: stale export hash')
        registration = read(entry.get('registration'))
        require(digest(local(registration.get('source')))==registration.get('sha256'), f'{side}: stale source hash')
        review = read(entry.get('review'))
        registration_verified = False
        if 'registration_path' in review or 'registration_sha256' in review:
            registration_path = local(entry.get('registration'))
            require(local(review.get('registration_path')) == registration_path,
                    f'{side}: review registration path mismatch')
            require(review.get('registration_sha256') == digest(registration_path),
                    f'{side}: stale review registration hash')
            registration_verified = True
        require(local(review.get('export_path'))==export and review.get('export_sha256')==actual,
                f'{side}: review export mismatch')
        review_checks = review.get('review', {})
        evidence = review_checks.get('native_evidence') or review_checks.get('native_scale', {}).get('evidence')
        local(evidence)
        axis = 'width' if side in ('north', 'south') else 'height'
        size = entry.get(f'world_{axis}', entry.get('long_axis_world'))
        recorded = review.get(f'proposed_display_{axis}_world')
        require(all(isinstance(n, (int, float)) and not isinstance(n, bool) and math.isfinite(n) and n>0
                    for n in (size, recorded)), f'{side}: positive finite long-axis dimensions required')
        require(math.isclose(size, recorded, rel_tol=1e-6), f'{side}: review scale mismatch')
        results.append({'wall': side, 'inward': entry['inward'], 'long_axis_world': size,
                        'native_evidence': evidence,
                        'review_registration_hash_verified': registration_verified})
    return {'metadata': 'pass', 'complete_directional_coverage': not missing,
            'missing_directions': missing, 'directions': results,
            'scope': 'Paths, hashes, declared facing and scale only; no visual or runtime acceptance'}


def run_report(root, family_path, output_path):
    root = Path(root).resolve()
    family_path, output_path = Path(family_path).resolve(), Path(output_path).resolve()
    if output_path.suffix.lower() != '.json' or not output_path.is_relative_to(root/'output'):
        raise ValueError('Audit reports must be JSON files under project output/')
    # Follow only files named by the family and its records, not the asset tree.
    protected = set()
    def protect_file(path):
        if path in protected or not path.is_file():
            return
        protected.add(path)
        if path.suffix.lower() == '.json':
            try:
                protect_values(json.loads(path.read_text(encoding='utf-8')))
            except (ValueError, UnicodeError):
                pass
    def protect_values(value):
        if isinstance(value, dict):
            for child in value.values(): protect_values(child)
        elif isinstance(value, list):
            for child in value: protect_values(child)
        elif isinstance(value, str):
            candidate = (root/value.removeprefix('res://')).resolve()
            if candidate.is_relative_to(root): protect_file(candidate)
    protect_file(family_path)
    if output_path in protected:
        raise ValueError('Report would overwrite a family dependency')
    if output_path.exists():
        existing = json.loads(output_path.read_text(encoding='utf-8'))
        if not isinstance(existing, dict) or existing.get('report_kind') != REPORT_KIND:
            raise ValueError('Refusing to replace an unrecognized report file')
    try:
        result = audit(root, json.loads(family_path.read_text(encoding='utf-8')))
    except (ValueError, OSError, TypeError, KeyError) as error:
        result = {'metadata': 'fail', 'error': str(error), 'complete_directional_coverage': False}
    result.update(report_kind=REPORT_KIND, family_path=str(family_path),
                  family_sha256=digest(family_path) if family_path.is_file() else None)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=output_path.parent, delete=False) as temp:
        temp.write(json.dumps(result, indent=2)+'\n')
    os.replace(temp.name, output_path)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('family', type=Path)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run_report(args.root, args.family, args.output)
    if result['metadata'] != 'pass':
        print(f"Family audit failed: {result['error']}")
        raise SystemExit(1)
    print(f"{len(result['directions'])} directions checked; missing: {result['missing_directions']}; metadata only")


if __name__ == '__main__':
    main()
