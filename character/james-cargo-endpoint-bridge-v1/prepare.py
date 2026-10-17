from pathlib import Path
import hashlib,json
from PIL import Image
p=Path(__file__).resolve().parent;r=p.parents[1]
sources={'entry':'character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/010.png','exit':'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png'}
hashes={}
for role,rel in sources.items():
    source=r/rel;im=Image.open(source).convert('RGBA');assert im.size==(256,256)
    im.resize((1024,1024),Image.Resampling.NEAREST).save(p/f'{role}-reference.png')
    hashes[rel]=hashlib.sha256(source.read_bytes()).hexdigest()
prompt='''Create one coherent 2x2 sprite animation atlas with FOUR consecutive intermediate whole-body poses of exactly the man in the attached references. Transparent background. Reference1 is the actual carry entry; reference2 the actual unload-ready exit. These are fixed endpoints, NOT two different characters. Author only the four intermediate poses, ordered top-left, top-right, bottom-left, bottom-right, moving smoothly from entry toward exit. This is a short subtle carry settling transition, not walking, lowering the case to the floor, head nodding, or a full turn.

In every equal square cell preserve the references' full 256-square framing: root ground pivot at (128,224), anatomical standing reference148px, crown around76, soles around224; use one common scale for all cells. Translate these coordinates proportionately into the output cell size. Same planted adjacent boots, ankle and heel placement throughout. No steps, foot sticking out, bent broken legs, global leaning, head bob or scale change. The small orientation change belongs in head/collar/shoulder/torso articulation with coherent anatomy and hand contact on the same case; feet stay planted. Interpolate the ENTIRE upper pose together, including head, neck, collar and shoulders, not independent pasted head patches. Maintain exact mature face, grey hair, goggles on forehead, moustache, yellow shoulder patch emblem, matte charcoal fabric, steel hardware, backpack, wrench visibly on belt and identical black cargo case, two arms/two hands. Match the original subdued neutral grade and source pixel-art detail; no purple/magenta, warm orange skin shift, gloss, bright rims, white halos or redesigned insignia. Four complete separate figures, no overlap, margins matching reference framing, no labels, grid lines or background. Each successive pose should be a small equal advance from the entry reference to the exit reference, with no overshoot. Exact source identity/proportion/perspective is more important than added detail.'''
(p/'prompt.txt').write_text(prompt+'\n')
hashes['character/james-cargo-endpoint-bridge-v1/prompt.txt']=hashlib.sha256((p/'prompt.txt').read_bytes()).hexdigest()
(p/'inputs.json').write_text(json.dumps({'roles':sources,'preGenerationSha256':hashes,'selected':False},indent=2)+'\n')
print('Two whole endpoint references enlarged uniformly4x; exact prompt and pre-call hashes saved.')
