"""Whole-source extraction/registration only; never paints replacement anatomy."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
source = Image.open(ROOT / 'source-atlas.png').convert('RGBA')
alpha = np.array(source.getchannel('A'))
assert alpha.min() == 0 and alpha.max() == 255
cuts = [0, 500, 850, 1378, source.width]
names = ['south', 'east', 'north', 'west']
crops = []
for name, left, right in zip(names, cuts, cuts[1:]):
    region = source.crop((left, 0, right, source.height))
    substantial = Image.fromarray((np.array(region.getchannel('A')) > 32).astype('uint8') * 255)
    body_bounds = substantial.getbbox()
    assert body_bounds and body_bounds[0] > 3 and body_bounds[2] < region.width - 3
    bounds = (body_bounds[0] - 3, max(0, body_bounds[1] - 3), body_bounds[2] + 3, min(region.height, body_bounds[3] + 3))
    crop = region.crop(bounds)
    opaque = np.array(crop.getchannel('A')) > 180
    yy, xx = np.where(opaque)
    crops.append((name, (left + bounds[0], bounds[1], left + bounds[2], bounds[3]), crop, int(yy.max()), int(yy.min())))

front = crops[0]
scale = 148 / (front[3] - front[4] + 1)
(ROOT / 'rotations').mkdir(exist_ok=True)
records = []
sprites = []
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
for name, bounds, crop, bottom, top in crops:
    sprite = crop.resize((round(crop.width * scale), round(crop.height * scale)), Image.Resampling.NEAREST)
    opaque = np.array(sprite.getchannel('A')) > 180
    yy, xx = np.where(opaque)
    x = 92 - sprite.width // 2
    y = 172 - int(yy.max())
    canvas = Image.new('RGBA', (184, 184))
    assert x >= 0 and y >= 0 and x + sprite.width <= 184 and y + sprite.height <= 184
    canvas.paste(sprite, (x, y))
    path = ROOT / 'rotations' / (name + '.png')
    canvas.save(path)
    assert canvas.getpixel((0, 0))[3] == 0
    records.append({'direction': name, 'path': 'res://character/kris-krug-masters-v1/rotations/' + name + '.png',
                    'source_bounds': bounds, 'registration': [x, y], 'opaque_height': int(yy.max() - yy.min() + 1),
                    'alpha_bounds': canvas.getbbox(), 'sha256': sha(path)})
    sprites.append(canvas)

manifest = {'name': 'Kris Krüg', 'title': 'Cognitive Concordance Specialist',
            'speciality': 'Intent Harmonisation', 'department': 'AI & Robotics',
            'scope': 'unselected static standing candidates; no animation', 'canvas': [184, 184],
            'pivot': [92, 172], 'common_source_scale': scale, 'front_standing_ruler': 148,
            'alpha_threshold_for_registration': 180, 'crop_threshold': 32, 'crop_margin': 3,
            'crop_note': 'Generator has near-transparent gutter speckles. Bounds use alpha>32 plus 3px; RGBA inside whole crop preserved.',
            'resampling': 'nearest', 'views': records}
(ROOT / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
provenance = {'tool': 'built-in image_gen', 'source_atlas_sha256': sha(ROOT / 'source-atlas.png'),
              'generated_source': 'C:/Users/Alex/.codex/generated_images/01a10108-0cea-7ee1-8d89-586acd3a735c/exec-bfea9830-d707-4f20-9026-78713a74bb10.png',
              'prompt': 'prompt.txt', 'references': [{'path': str(p.relative_to(REPO)), 'sha256': sha(p)} for p in [
                  REPO / 'character/kris-krug-concept-v1/concept-03-concordance-specialist.png',
                  REPO / 'character/major-bill-v3/rotations/south.png']],
              'processing': 'Whole figure crops, one standing-derived scale, translation registration. No RGB edits, limb patches or generated motion.'}
(ROOT / 'provenance.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')

board = Image.new('RGB', (1100, 1030), '#262a2e')
draw = ImageDraw.Draw(board)
draw.text((24, 16), 'KRIS KRUG - FOUR CARDINAL STANDING CANDIDATES', fill='white')
draw.text((24, 38), 'Common front-derived scale; 184px canvas / pivot 92,172. No animation or runtime selection.', fill='#bac5ca')
for i, (name, sprite) in enumerate(zip(names, sprites)):
    x = 30 + i * 270
    board.paste(sprite, (x, 65), sprite)
    draw.text((x + 60, 255), name.upper(), fill='white')
    enlarged = sprite.resize((368, 368), Image.Resampling.NEAREST)
    body = enlarged.crop((65, 0, 303, 368))
    board.paste(body, (x, 290), body)
draw.text((24, 690), 'Same standing ruler: selected Bill / earlier Kris concept / new Kris south', fill='white')
bill = Image.open(REPO / 'character/major-bill-v3/rotations/south.png').convert('RGBA')
board.paste(bill, (40, 735), bill)
concept = Image.open(REPO / 'character/kris-krug-concept-v1/concept-03-concordance-specialist.png').convert('RGB')
concept = concept.crop((545, 266, 803, 831)).resize((68, 148), Image.Resampling.NEAREST)
board.paste(concept, (265, 759))
board.paste(sprites[0], (390, 735), sprites[0])
room = Image.open(REPO / 'character/dr-veld-v1/qa/native/crew-together-crop.png').convert('RGB')
room = room.crop((120, 110, 380, 345))
small = sprites[0].resize((92, 92), Image.Resampling.NEAREST)
room.paste(small, (175, 83), small)
board.paste(room, (640, 735))
draw.text((620, 985), 'Historical room + static inset; no engine evidence.', fill='#bac5ca')
board.save(ROOT / 'review.png')
print(json.dumps({'views': 4, 'source_size': source.size, 'genuine_alpha': True,
                  'standing_heights': [r['opaque_height'] for r in records], 'common_scale': scale,
                  'clipping_failures': 0}))
