"""Prepare directional retained gestures as a single row at shared source scale."""
from pathlib import Path
import argparse
import hashlib
import json
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-retained-gesture-material-v1'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('direction', choices=['east', 'west', 'north'])
    args = parser.parse_args()
    d = args.direction
    inv = json.loads((ROOT / 'character/marsh-full-family-audit-2026-10-03/inventory.json').read_text())
    idle = inv['states']['idle-'+d]
    old = inv['states']['remove-helmet-'+d]
    assert [f['sha256'] for f in old['frames']] == [f['sha256'] for f in inv['states']['equip-helmet-'+d]['frames']]
    assert idle['pivot'] == [92,172] and old['pivot'] == [92,172]
    entries = old['frames'][1:5] + [idle['frames'][0]]
    board = Image.new('RGBA', (2560,640))
    for i, record in enumerate(entries):
        source = ROOT / record['path']
        assert sha(source) == record['sha256']
        im = Image.open(source).convert('RGBA')
        assert im.size == (184,184)
        board.alpha_composite(im.resize((552,552), Image.Resampling.NEAREST), (i*512-20,44))
    target = BASE / f'inputs/{d}-gesture-target-single-row-01.png'
    board.save(target)
    primary = BASE / f'inputs/{d}-own-idle-3x.png'
    im = Image.open(ROOT / idle['frames'][0]['path']).convert('RGBA')
    im.resize((552,552), Image.Resampling.NEAREST).save(primary)
    master = ROOT / f'character/marsh-motion-polish-v1/sources/{d}-standing-identity-01.png'
    description = {'east': 'exact East profile facing viewer RIGHT; left temple is near viewer and is BARE, RIGHT implant stays on far side',
                   'west': 'exact West profile facing viewer LEFT; RIGHT temple is near viewer and retains the small metal implant',
                   'north': 'exact North rear view facing AWAY from viewer; show back of blond head, backpack/rear straps, no face or front chest panel'}[d]
    height = idle['frames'][0]['occupiedSize'][1]
    width = idle['frames'][0]['occupiedSize'][0]
    prompt = f'''Edit the THIRD image. Return exactly FIVE complete connected Marsh figures in ONE HORIZONTAL ROW on a genuinely transparent background. This is a whole-body identity/material repair of four existing generic hand gestures plus a fifth neutral ruler, not a helmet action. FIRST image is exact own {d} idle enlarged3x and controls proportions, silhouette, camera and muted matte material grade. SECOND is supporting original directional identity master. THIRD is target hand-gesture layout. All FIVE figures must preserve {description}, with the same elevated station camera as FIRST, same planted boots baseline and ONE shared whole-body scale. Neutral body is{width}px wide by{height}px high in the runtime reference, enlarged3x in inputs; roughly{height*3}px tall if output2560x640. ALL five figures must have the SAME occupied height and head/torso/leg proportions; arm gestures can extend width without expanding body. Correct broad/coarse older bodies in the first four cells to match FIRST and fifth neutral. Preserve the four target subtle broad-glove movements at chest/waist; fifth neutral has both arms down and follows FIRST exactly. Whole connected gloves, wrists, arms, legs, boots. Bare blond head, muted ivory ceramic shell, subdued sage shoulder pads, charcoal undersuit/gloves/collar, exact waist pouches/knee rings and directional straps/panel/backpack visible in FIRST. Fine crisp pixel-like source detail, flat matte muted colours, no plastic shine, harsh new lighting or head inflation. No helmet, newly invented equipment/prop/action, detached parts, labels, grid, background, shadows, checkerboard, sixth figure or second row. Keep all full bodies uncropped and distinctly separated at the same scale. Do not mirror another view or add the far temple implant to the near bare temple. Preserve FIRST's perspective and identity in each of the five WHOLE bodies.'''
    paths = [primary,master,target]
    request = {'prompt': prompt, 'transparent_background': True, 'referenced_image_paths': [str(p) for p in paths],
               'references': [{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in paths],
               'sourcePoses': entries, 'selectedStateMetadata': {k:inv['states'][k] for k in ['idle-'+d,'equip-helmet-'+d,'remove-helmet-'+d]},
               'scope': 'Unselected retained generic gesture repair, no actual helmet transition or enabled controller.'}
    requestpath = BASE / f'sources/{d}-gesture-01.request.json'
    assert not requestpath.exists(), 'Preserve previously recorded request; use a new version for new work.'
    requestpath.write_text(json.dumps(request,indent=2)+'\n')
    (BASE / f'sources/{d}-gesture-01.prompt.txt').write_text(prompt)
    print(d,'five whole figures prepared at uniform3x, own occupied ruler',width,height)

if __name__ == '__main__':main()
