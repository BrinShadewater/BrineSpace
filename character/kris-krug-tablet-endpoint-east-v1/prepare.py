from pathlib import Path
import hashlib,json
from PIL import Image

ROOT=Path(__file__).resolve().parent
master=ROOT.parent/'kris-krug-masters-v1/rotations/east.png'
held=ROOT.parent/'kris-krug-tablet-east-v1/key-poses/03.png'
for path,name in [(master,'first.png'),(held,'last.png')]:
    sprite=Image.open(path).convert('RGBA').resize((736,736),Image.Resampling.NEAREST)
    bg=Image.new('RGB',(736,736),'#ff00ff');bg.paste(sprite,(0,0),sprite);bg.save(ROOT/name)
prompt='Fixed camera, exact same man in right-facing EAST profile for entire clip. Smooth continuous transition from supplied relaxed standing FIRST pose into supplied tablet-consultation LAST pose. His FAR/anatomical LEFT glove takes rugged tablet from LEFT hip holster, draws it forward and raises it gently below chest; near RIGHT glove approaches and makes one deliberate tap, finishing exactly in supplied consultation pose. Right-hip FLAT WAFER POUCH stays fixed and untouched, never becomes tablet. Both complete boots remain planted on identical ground line, no step, slide, turn, spin or body translation. Long beard, glasses, tied-back hair, face, receding hairline, graphite wrap suit, collar, harness, boots and pouch retain exact form/stature/material; no hat or new equipment. Only coherent arms/gloves move and minimal head downward glance. Preserve neutral charcoal grey cloth with no teal, green or purple color shift. Tablet dark grey, tiny restrained cyan display; no bright white/green screen. Solid uniform magenta chroma background, no shadows, floor, zoom or camera movement. No floating tablet, duplicated limbs or hidden jump. Complete natural draw-and-raise action, small relaxed motion, settle in exact end pose.'
(ROOT/'prompt.txt').write_text(prompt,encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(ROOT/'input-contract.json').write_text(json.dumps({'first_reference':str(master),'first_reference_sha256':sha(master),
 'last_reference':str(held),'last_reference_sha256':sha(held),'input_size':[736,736],'scale_up':4,
 'canvas':[184,184],'pivot':[92,172],'chroma':'magenta','scope':'Single endpoint-conditioned draw/raise source attempt; reverse return only if visually credible',
 'estimated_usd':.28,'previous_estimated_total':.95,'cumulative_estimated_total':1.23,'verified_billing':None},indent=2),encoding='utf-8')
print('Frozen original standing and consultation endpoints at equal registration; no submission yet.')
