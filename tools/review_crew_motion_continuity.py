"""Make pivot-aligned selected-frame comparisons; no automatic visual verdict."""
from pathlib import Path
import argparse
import hashlib
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PACKS = {'veld': 'dr-veld-v2', 'branforth': 'chief-engineer-branforth-v2', 'marsh': 'marsh-v2'}

def review(actor, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    base = ROOT / 'character' / PACKS[actor]
    catalog = json.loads((base / 'catalog.json').read_text())
    rows = {}
    for relative in catalog['body']:
        manifest = base / relative
        data = json.loads(manifest.read_text())
        for state in data['states']:
            rows[state['id']] = (manifest, data, state)
    probes = [('idle', -1), ('walk', 0), ('walk', 3), ('kneel', 0), ('run', 0), ('carry', 0)]
    sheet = Image.new('RGB', (1200, 880), '#293b40')
    draw = ImageDraw.Draw(sheet)
    evidence = []
    for y, direction in enumerate(['east', 'west', 'north', 'south']):
        for x, (action, index) in enumerate(probes):
            key = action + '-' + direction
            draw.text((x*200+5, y*220+3), key + ' ' + str(index), fill='white')
            if key not in rows:
                draw.text((x*200+5, y*220+30), 'MISSING', fill='orange')
                continue
            manifest, data, state = rows[key]
            source = manifest.parent / state['frameFiles'][index]
            im = Image.open(source).convert('RGBA')
            scale = 148 / data.get('standingHeight', 74)
            pivot = data['pivot']
            im = im.resize((round(im.width*scale), round(im.height*scale)), Image.Resampling.NEAREST)
            left = x*200+100-round(pivot[0]*scale)
            top = y*220+200-round(pivot[1]*scale)
            sheet.paste(im, (left, top), im)
            draw.line((x*200+5,y*220+201,x*200+195,y*220+201), fill='#53676c')
            evidence.append({'state':key,'frameIndex':index,'source':source.relative_to(ROOT).as_posix(),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pivot':pivot,'scale':scale,'bounds':im.getbbox()})
    sheet.save(output/'continuity-contact.png')
    (output/'review.json').write_text(json.dumps({'actor':actor,'status':'comparison_only_not_acceptance','probes':evidence,'limits':['Selected pose comparisons do not prove live transitions or animation quality.','Carry poses include cargo; action poses may intentionally change height.']},indent=2)+'\n')
    print(f'{actor}: {len(evidence)} selected pose comparisons')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('actor', choices=PACKS)
    parser.add_argument('output')
    args = parser.parse_args()
    review(args.actor, args.output)
