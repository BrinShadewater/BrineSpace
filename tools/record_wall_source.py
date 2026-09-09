"""Preserve one generated wall source and append immutable provenance to the rollout.

Copies bytes only; never edits pixels or implies visual/runtime acceptance.
"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

def record(args):
    ledger_path = ROOT / 'assets/wall-room-rollout-v1/rollout.json'
    ledger = json.loads(ledger_path.read_text())
    row = next(r for r in ledger['rooms'] if r['id'] == args.room)
    target = ROOT / 'assets/wall-room-rollout-v1' / args.name
    if target.parent != ledger_path.parent or target.suffix != '.png':
        raise ValueError('Use a plain PNG filename within the rollout directory')
    if target.exists():
        raise ValueError('Preserve revisions at new paths')
    prompt = target.with_suffix('.prompt.txt')
    if not prompt.exists() or not prompt.read_text(encoding='utf-8').strip():
        raise ValueError('Save the exact prompt beside the source before recording')
    data = args.source.read_bytes()
    if data.startswith(b'version https://git-lfs.github.com/spec/'):
        raise ValueError('Source is an LFS pointer')
    with Image.open(args.source) as image:
        dimensions, mode = list(image.size), image.mode
        image.verify()
    shutil.copy2(args.source, target)
    item = {'view': args.view, 'source': target.relative_to(ROOT).as_posix(),
            'sha256': hashlib.sha256(data).hexdigest(), 'dimensions': dimensions,
            'mode': mode, 'prompt': prompt.relative_to(ROOT).as_posix(),
            'references': args.reference, 'stage': 'generated',
            'review': args.review, 'selected': False}
    row['sources'].append(item)
    ledger_path.write_text(json.dumps(ledger, indent=2)+'\n')
    print(args.room, args.view, dimensions, 'preserved; selection and runtime pending')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--room', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--view', required=True)
    parser.add_argument('--reference', action='append', default=[])
    parser.add_argument('--review', default='Pending native review')
    record(parser.parse_args())
