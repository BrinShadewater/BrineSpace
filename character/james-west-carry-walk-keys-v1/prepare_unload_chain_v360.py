import hashlib
import json
from pathlib import Path

from PIL import Image

root = Path.cwd()
bank = root / 'character/james-west-carry-walk-keys-v1'
output = bank / 'north-unload-chain-v360'
output.mkdir(exist_ok=True)
first = root / 'character/james-cargo-half-turns-v1/frames/bare/carry-turn-north-south/000.png'
last = root / 'character/james-cargo-north-v1/frames/bare/pickup-north/000.png'
middle = bank / 'north-unload-pose-v359/source.png'
alignment = json.loads((bank / 'north-unload-pose-v359/review.json').read_text())
background = (48, 59, 64)

# Authoring controls use one uniform canvas ruler and rigid ground registration.
# No per-pose body fitting, repainting, warping or material correction.
for source, name in [(first, 'carry.png'), (last, 'standing.png')]:
    image = Image.open(source).convert('RGBA')
    assert image.size == (256, 256)
    plate = Image.new('RGB', image.size, background)
    plate.paste(image, (0, 0), image)
    plate.resize((768, 768), Image.Resampling.NEAREST).save(output / name)
image = Image.open(middle).convert('RGBA')
assert image.size == (1254, 1254)
image = image.resize((768, 768), Image.Resampling.LANCZOS)
plate = Image.new('RGB', (768, 768), background)
plate.paste(image, (0, round(alignment['floorTranslationAt256px'] * 3)), image)
plate.save(output / 'crouch.png')
prompts = {
    'bend': 'Fixed-camera rear-view game sprite. The same engineer begins in the exact first standing carry pose, gently bends his hips and knees and lowers the cargo case in front of him, ending in the exact final supported crouch pose. Both boots stay planted on the ground at hip width; knees bend directly above the boots and never spread sideways. The load stays in front of his body, mostly occluded from this rear view. Both hands lower the case together, shoulders and elbows remain connected. Keep his grey hair, head proportions, compact backpack, muted yellow hardware, matte graphite suit and worn warm metal consistent. The wrench stays hanging on the right side of his belt throughout, never in his hands. No steps, rotation, extra limbs, body clipping, camera movement, lighting changes or glossy/magenta flash. One smooth lowering action and a short settled hold; preserve scale, flat dark background and ground contact.',
    'rise': 'Fixed-camera rear-view game sprite. The same engineer begins in the exact first supported crouch, having lowered the cargo case onto the floor in front of him. He releases the load and rises smoothly to the exact final empty-handed standing pose. Both boots remain planted at hip width on the same ground line; knees straighten without spreading sideways. Arms return naturally to his sides, keeping shoulders and elbows connected. Cargo stays on the floor in front, not attached to his hands, belt or calves. Keep his grey hair, head proportions, compact backpack, muted yellow hardware, matte graphite suit and worn warm metal consistent. The wrench stays hanging on the right side of his belt throughout, never in his hands. No extra gesture, steps, rotation, extra limbs, body clipping, camera movement, lighting change or glossy/magenta flash. One smooth rise and a short settled hold; preserve scale, flat dark background and ground contact.'
}
for part, prompt in prompts.items():
    directory = output / part
    directory.mkdir(exist_ok=True)
    (directory / 'prompt.txt').write_text(prompt, encoding='utf8')
data = {'version': 360, 'method': 'Two controlled Hailuo02 first/last source clips, shared crouch control', 'selected': False, 'normalChanged': False, 'estimatedUSD': .56, 'billingVerified': False, 'sources': {name: {'path': str(path.relative_to(root)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for name, path in [('carry', first), ('crouch', middle), ('standing', last)]}, 'controls': {name: hashlib.sha256((output / (name + '.png')).read_bytes()).hexdigest() for name in ['carry', 'crouch', 'standing']}, 'registration': {'canvas': [768, 768], 'sourceCanvas': [256, 256], 'ruler': 3, 'crouchSourceRuler': 768 / 1254, 'crouchTranslationY': round(alignment['floorTranslationAt256px'] * 3), 'background': list(background)}, 'limits': 'Crouch is unselected and changes some identity/material detail. These controls do not establish coherent accepted animation.'}
(output / 'inputs.json').write_text(json.dumps(data, indent=2) + '\n')
print('Prepared shared crouch with accepted carry/standing endpoint controls; no runtime change.')
