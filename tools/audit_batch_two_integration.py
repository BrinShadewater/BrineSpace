"""Read-only batch-two provenance/consumer audit; does not certify art or gameplay."""
import hashlib
import json
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'rooms/underwater/batch-two'
IDS = {'cryo_chamber', 'clone_lab', 'data_archive', 'biodome', 'xeno_lab',
       'anomaly_lab', 'bio_lab', 'holographic_core', 'med_center', 'med_office'}


def project_path(value):
    path = (ROOT / value.removeprefix('res://')).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('Path outside project: ' + value)
    return path


def png_info(path):
    raw = path.read_bytes()
    if raw.startswith(b'version https://git-lfs.github.com/spec/'):
        raise ValueError('Unfetched LFS asset: ' + str(path))
    with Image.open(path) as image:
        image.load()
        return hashlib.sha256(raw).hexdigest(), list(image.size)


def audit():
    rows = json.loads((PACK / 'source-review.json').read_text(encoding='utf-8'))['rooms']
    identities = [row['id'] for row in rows]
    if len(identities) != len(IDS) or set(identities) != IDS:
        raise ValueError('Batch identity set is incomplete or duplicated')
    mappings = []
    for file in ['scripts/grid_canvas.gd', 'scripts/room_card_art.gd']:
        source = (ROOT / file).read_text(encoding='utf-8')
        mappings.append(dict(re.findall(r'"([a-z_]+)"\s*:\s*"(res://[^"\n]+\.png)"', source)))
    result = []
    for row in rows:
        identity = row['id']
        digest, size = png_info(project_path(row['source']))
        if digest != row['sha256'] or size != row['native_size']:
            raise ValueError('Source provenance drift: ' + identity)
        if not row['registered'] or not row['integrated'] or not row['stage'].startswith('registered'):
            raise ValueError('Stale integration stage: ' + identity)
        selected = mappings[0].get(identity)
        if not selected or selected != mappings[1].get(identity):
            raise ValueError('Station/card mappings disagree: ' + identity)
        card_hash, card_size = png_info(project_path(selected))
        if card_size != [512, 512]:
            raise ValueError('Unexpected native card size: ' + identity)
        for path in [PACK / (identity + '_view.gd'), PACK / (identity + '_view.gd.uid'),
                     PACK / row['integration_record']]:
            if not path.is_file():
                raise ValueError('Missing registered dependency: ' + str(path))
        result.append({'id': identity, 'source_hash_verified': True,
                       'matching_card': selected, 'card_sha256': card_hash,
                       'visual_acceptance': 'not evaluated', 'package': 'not evaluated'})
    return result


def audit_export_manifest():
    verified = {row['id']: row for row in audit()}
    sources = {row['id']: row for row in json.loads(
        (PACK / 'source-review.json').read_text(encoding='utf-8'))['rooms']}
    exported = json.loads((PACK / 'export-manifest.json').read_text(encoding='utf-8'))
    if len(exported) != len(IDS) or {row['id'] for row in exported} != IDS:
        raise ValueError('Export identity set is incomplete or duplicated')
    for row in exported:
        identity = row['id']
        if (row['source'] != sources[identity]['source'] or
                row['sha256'] != sources[identity]['sha256'] or
                'res://' + row['integration']['card'] != verified[identity]['matching_card'] or
                row['integration']['view'] != f'rooms/underwater/batch-two/{identity}_view.gd'):
            raise ValueError('Export manifest drift: ' + identity)
    return exported


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
    audit_export_manifest()
    print('BATCH TWO ASSET AUDIT PASS: 10 identities; sources, cards and records agree. Not runtime acceptance.')
