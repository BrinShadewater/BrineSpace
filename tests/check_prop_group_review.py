"""Run graphical Godot group-review positive and rejection checks.

Usage: python tests/check_prop_group_review.py --godot PATH
Writes fixtures, logs and the valid capture under output/prop-group-checks.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--godot', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    out = root/'output/prop-group-checks'
    out.mkdir(parents=True, exist_ok=True)
    base = json.loads((root/'assets/operator-stool-v1/group.json').read_text())
    cases = [('valid', base, None)]
    for name, field, value, error in [
        ('outside_source', 'region', [0, 0, 99999, 100], 'exceeds export canvas'),
        ('outside_panel', 'at', [480, 0], 'exceeds review panels'),
        ('negative_position', 'at', [-1, 0], 'exceeds review panels'),
        ('invalid_number', 'width', '328', 'require finite numbers'),
        ('stale_hash', 'sha256', '0'*64, 'hash mismatch'),
    ]:
        data = copy.deepcopy(base)
        data['entries'][0][field] = value
        cases.append((name, data, error))
    cases.append(('empty', {'entries': []}, 'nonempty entries array'))
    cases.append(('overwrite', base, 'must not overwrite'))
    protected = root/base['entries'][0]['export'].removeprefix('res://')
    before = hashlib.sha256(protected.read_bytes()).hexdigest()
    for name, data, error in cases:
        fixture = out/f'{name}.json'
        fixture.write_text(json.dumps(data))
        capture = protected if name == 'overwrite' else out/f'{name}.png'
        # Reject cases must never produce a capture, including repeated runs.
        if error and capture != protected and capture.exists():
            capture.unlink()
        with (out/f'{name}.log').open('w') as log:
            result = subprocess.run([
                args.godot, '--path', str(root), '--script',
                'tools/review_prop_group.gd', '--',
                f'--group={fixture.as_posix()}', f'--review={capture.as_posix()}'
            ], stdout=log, stderr=subprocess.STDOUT, timeout=30)
        text = (out/f'{name}.log').read_text()
        assert 'SCRIPT ERROR' not in text, (name, text)
        if error:
            assert result.returncode == 1 and error in text, (name, text)
            assert capture == protected or not capture.exists(), name
        else:
            assert result.returncode == 0 and 'PROP GROUP PASS' in text and capture.exists(), text
    assert hashlib.sha256(protected.read_bytes()).hexdigest() == before
    print(f'{len(cases)} group checks passed; protected export unchanged; logs: {out}')


if __name__ == '__main__':
    main()
