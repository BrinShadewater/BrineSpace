"""Initialize verified asset metadata; never infer visual or owner acceptance.

Example: python tools/init_material_scale_review.py --registration assets/.../registration.json
 --export assets/.../asset.png --prompt assets/.../source.prompt.txt
 --asset-id example --width 328 --output output/example-review.json
Use --height instead for side-wall banks. Existing outputs are never overwritten.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_path(root, value):
    value = str(value).removeprefix('res://')
    path = Path(value)
    path = (root / path).resolve() if not path.is_absolute() else path.resolve()
    path.relative_to(root)  # Runtime source/export evidence belongs to this checkout.
    if not path.is_file():
        raise ValueError(f'Missing file: {path}')
    return path


def initialize(root, registration, export, prompt, asset_id, *, width=None, height=None,
               references=()):
    root = root.resolve()
    if (width is None) == (height is None):
        raise ValueError('Specify exactly one intended width or height.')
    size = width if width is not None else height
    if not math.isfinite(size) or size <= 0:
        raise ValueError('Intended scale must be finite and positive.')
    if not asset_id.strip():
        raise ValueError('Asset id must not be blank.')
    reg_path = local_path(root, registration)
    export_path = local_path(root, export)
    prompt_path = local_path(root, prompt)
    data = json.loads(reg_path.read_text(encoding='utf-8'))
    source_path = local_path(root, data['source'])
    if source_path == export_path:
        raise ValueError('Source and export must be separate preserved files.')
    if digest(source_path) != data['sha256']:
        raise ValueError('Registration source hash mismatch.')
    with Image.open(source_path) as source:
        canvas = source.size
        source_mode = source.mode
    region = data['region']
    if len(region) != 4 or not all(isinstance(n, (float, int)) and math.isfinite(n) for n in region):
        raise ValueError('Registration region requires four finite numbers.')
    x, y, w, h = region
    if x < 0 or y < 0 or w <= 0 or h <= 0 or x+w > canvas[0] or y+h > canvas[1]:
        raise ValueError('Registration region is outside the native canvas or empty.')
    with Image.open(export_path) as image:
        if image.size != canvas:
            raise ValueError('Export must preserve registered source canvas dimensions.')
        if 'A' not in image.getbands():
            raise ValueError('Export has no alpha channel.')
        alpha = image.getchannel('A').getextrema()
        if alpha[0] != 0 or alpha[1] == 0:
            raise ValueError('Export must contain transparent and visible pixels.')
    template = root/'skills/brinespace-room-pipeline/templates/material-scale-review.json'
    record = json.loads(template.read_text(encoding='utf-8'))
    rel = lambda path: path.relative_to(root).as_posix()
    record.update(asset_id=asset_id, source_path=rel(source_path),
                  source_sha256=digest(source_path), export_path=rel(export_path),
                  export_sha256=digest(export_path), native_canvas_px=list(canvas),
                  proposed_display_width_world=width if width is not None else height*w/h,
                  proposed_display_height_world=height if height is not None else width*h/w,
                  registration_path=rel(reg_path), registration_sha256=digest(reg_path),
                  prompt_path=rel(prompt_path), prompt_sha256=digest(prompt_path))
    record['metadata_checks'] = {'source_mode': source_mode,
                                 'export_alpha_extrema': list(alpha),
                                 'scope': 'provenance and dimensions only; visual review pending'}
    for path, role in references:
        reference = Path(path)
        if not reference.is_absolute():
            reference = root/reference
        reference = reference.resolve()
        if not reference.is_file() or not role.strip():
            raise ValueError('Each reference needs an existing file and an explicit role.')
        record['references'].append({'path': reference.as_posix(),
                                     'sha256': digest(reference), 'role': role})
    # Template defaults cannot accidentally promote this metadata initializer.
    for gate in ('materials', 'native_scale', 'alpha'):
        record['review'][gate]['verdict'] = None
    record['owner_acceptance'] = None
    record['review']['integration'] = {'stage': 'not_installed', 'evidence': None}
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('registration', 'export', 'prompt', 'asset-id', 'output'):
        parser.add_argument('--'+name, required=True)
    scale = parser.add_mutually_exclusive_group(required=True)
    scale.add_argument('--width', type=float)
    scale.add_argument('--height', type=float)
    parser.add_argument('--reference', nargs=2, action='append', default=[], metavar=('PATH', 'ROLE'))
    args = parser.parse_args()
    try:
        output = Path(args.output).resolve()
        output.relative_to(ROOT)
        if output.exists():
            raise ValueError('Output exists; preserve the reviewed record and choose a new path.')
        record = initialize(ROOT, args.registration, args.export, args.prompt, args.asset_id,
                            width=args.width, height=args.height, references=args.reference)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('x', encoding='utf-8') as stream:
            json.dump(record, stream, indent=2)
            stream.write('\n')
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.error(str(error))
    print(f'Initialized {output.relative_to(ROOT)}; visual review and owner acceptance pending.')


if __name__ == '__main__':
    main()
