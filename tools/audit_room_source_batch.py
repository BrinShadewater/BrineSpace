"""Audit saved room-source provenance and assemble a review sheet; never approve art.

Paths in manifests are repository-relative. Sources and manifest are read-only.
Use a new output directory for each audit to preserve earlier evidence.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw


def audit(manifest, output, root):
    rows = json.loads(manifest.read_text(encoding='utf-8'))
    ids = [row['id'] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate identities in manifest')
    if output.exists():
        raise ValueError('Use a new output directory; audit evidence is immutable')
    records, previews = [], []
    for row in rows:
        versions = [{'source': row['source'], 'sha256': row['sha256']}] + row.get('revisions', [])
        for version in versions:
            source = (root / version['source']).resolve()
            if not source.is_relative_to(root.resolve()):
                raise ValueError('Source outside project: ' + str(source))
            data = source.read_bytes()
            if data.startswith(b'version https://git-lfs.github.com/spec/'):
                raise ValueError('Fetch LFS source before audit: ' + str(source))
            digest = hashlib.sha256(data).hexdigest()
            if digest != version['sha256']:
                raise ValueError('Source hash mismatch: ' + str(source))
            with Image.open(source) as original:
                rgba = original.convert('RGBA')
                histogram = rgba.getchannel('A').histogram()
                pixels = original.width * original.height
                record = {'id': row['id'], 'source': version['source'],
                          'sha256': digest, 'native_size': list(original.size),
                          'mode': original.mode, 'transparent_pixels': histogram[0],
                          'partial_alpha_pixels': sum(histogram[1:255]),
                          'opaque_fraction': histogram[255] / pixels,
                          'geometry_verdict': 'not evaluated',
                          'runtime_verdict': 'not evaluated'}
                records.append(record)
                if version['source'] == row.get('selected_source', row['source']):
                    previews.append((row['id'], rgba.copy(), row['stage']))
    if len(previews) != len(rows):
        raise ValueError('Every selected source must identify a recorded version')
    output.mkdir(parents=True)
    # Identical full-canvas scale; no independent tight cropping of room silhouettes.
    cell, title = 320, 54
    sheet = Image.new('RGB', (cell * 5, (cell + title) * ((len(rows)+4)//5)), '#142027')
    draw = ImageDraw.Draw(sheet)
    for index, (identity, rgba, stage) in enumerate(previews):
        x, y = (index % 5)*cell, (index // 5)*(cell+title)
        rgba.thumbnail((cell-12, cell-12), Image.Resampling.NEAREST)
        sheet.paste(rgba, (x+(cell-rgba.width)//2, y+6), rgba)
        draw.text((x+9, y+cell+3), identity.replace('_', ' ').upper(), fill='#eef3f3')
        draw.text((x+9, y+cell+19), stage + ' / NOT RUNTIME-VERIFIED', fill='#f1b878')
    sheet.save(output / 'source-contact-sheet.png')
    (output / 'audit.json').write_text(json.dumps(records, indent=2)+'\n', encoding='utf-8')
    print(f'{len(rows)} identities, {len(records)} source versions verified; no art acceptance inferred.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    audit(args.manifest, args.output, Path(__file__).resolve().parents[1])
