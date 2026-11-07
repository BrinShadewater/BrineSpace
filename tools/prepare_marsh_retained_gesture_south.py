"""Prepare whole-source retained gesture repair; no raster anatomy edits."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-retained-gesture-material-v1'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    (BASE / 'inputs').mkdir(parents=True, exist_ok=True)
    (BASE / 'sources').mkdir(exist_ok=True)
    inv = json.loads((ROOT / 'character/marsh-full-family-audit-2026-10-03/inventory.json').read_text())
    idle = inv['states']['idle-south']['frames'][0]
    targets = inv['states']['remove-helmet-south']['frames']
    other = inv['states']['equip-helmet-south']['frames']
    assert [f['sha256'] for f in targets] == [f['sha256'] for f in other]
    entries = [targets[i] for i in range(1, 5)] + [idle]
    board = Image.new('RGBA', (1536, 1280))
    refs = []
    for i, record in enumerate(entries):
        path = ROOT / record['path']
        assert sha(path) == record['sha256']
        im = Image.open(path).convert('RGBA')
        # Every source is enlarged with the SAME factor3; no per-pose fit.
        whole = im.resize((im.width * 3, im.height * 3), Image.Resampling.NEAREST)
        x, y = (i % 3) * 512 + 256 - 92 * 3, (i // 3) * 640 + 560 - 172 * 3
        board.alpha_composite(whole, (x, y))
        refs.append(dict(record, cell=i, operation='Whole source uniform3x; common pivot at cell(256,560).'))
    target = BASE / 'inputs/south-gesture-target-01.png'
    board.save(target)
    primary = BASE / 'inputs/south-own-idle-3x.png'
    own = Image.open(ROOT / idle['path']).convert('RGBA')
    own.resize((552, 552), Image.Resampling.NEAREST).save(primary)
    master = ROOT / 'character/marsh-motion-polish-v1/sources/south-standing-identity-01.png'
    prompt = '''Edit the THIRD image, a transparent sprite sheet, using the FIRST image as the exact primary identity/proportion/material ruler and SECOND image as high-detail supporting Marsh identity master. Return one transparent1536x1280 sheet,3columns x2rows of512x640cells. There are exactly FIVE full figures: cells0,1,2 across top, cells3,4 across bottom, cell5 stays EMPTY. Preserve whole connected anatomy and the target hand gestures in cells0..3. Cell4 is the same neutral standing Marsh as FIRST reference, unchanged in design/proportions. All figures face exactly South toward viewer, the existing elevated station camera; same head angle, foot baseline and body scale. This is a whole-body material/identity correction, not a helmet action. Bare blond head in every cell; no helmet, new equipment or new gesture. Match FIRST image's slender58px-wide neutral body at147px occupied height, shown3x in references; each full figure about441pixels tall in output. Fixed planted boots on cell row560; do not widen torso, inflate head or shorten legs. Ivory ceramic/android shell, subdued sage shoulder pads, charcoal undersuit/collar, paired small chest fasteners, exact waist pouches/knee rings/boots and pale face/hair matching FIRST. Marsh has RIGHT temple implant, visible on viewer LEFT, with the other temple bare. Hands/gloves remain connected to wrists. Retain target gentle broad-glove movements at chest/waist, with no detached objects. Flat muted matte material and fine crisp pixel-like source detail matching FIRST; no shine, bloom, gradients/background, glow, labels, grid, shadows, checkerboard or sixth figure. Keep all five WHOLE bodies distinct, uncropped and in their cells at one consistent scale. Do not copy the obsolete broad torso/coarse head from target; FIRST reference controls identity and proportions.'''
    (BASE / 'sources/south-gesture-01.prompt.txt').write_text(prompt, encoding='utf-8')
    paths = [primary, master, target]
    request = {'prompt': prompt, 'transparent_background': True,
               'referenced_image_paths': [str(p) for p in paths],
               'references': [{'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p)} for p in paths],
               'sourcePoses': refs, 'selectedStateMetadata': {k: inv['states'][k] for k in ['idle-south', 'remove-helmet-south', 'equip-helmet-south']},
               'scope': 'Unselected retained generic-gesture material repair. Both helmet actions disabled in Marsh controller; no actual helmet/change capability claim.'}
    (BASE / 'sources/south-gesture-01.request.json').write_text(json.dumps(request, indent=2) + '\n')
    print('Five whole figures prepared at common3x source scale; two legacy state banks share exact sources.')

if __name__ == '__main__':
    main()
