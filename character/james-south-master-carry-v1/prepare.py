from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];p.mkdir(exist_ok=True)
manifest=r/'character/crew-runtime-matte-v1/branforth/manifest.json';m=json.loads(manifest.read_bytes());s=next(s for s in m['states'] if s['id']=='idle-south');source=manifest.parent/s['frameFiles'][0]
base=Image.new('RGBA',(256,256));base.alpha_composite(Image.open(source).convert('RGBA'),(128-round(m['pivot'][0]),224-round(m['pivot'][1])));base.save(p/'original.png')
base.crop((80,96,176,192)).resize((768,768),Image.Resampling.LANCZOS).save(p/'target.png')
case=r/'character/james-west-master-carry-v1/local-case-reference.png';Image.open(case).save(p/'case-reference.png')
detail=r/'character/branforth-video-south-v1/master-source.png'
prompt='''Edit IMAGE 1 ONLY: a fixed96-square native crop of James SOUTH-facing torso/arms/belt, enlarged8x. This is NOT a complete figure. Preserve exact square crop framing, original shoulder/collar/torso/belt/hip locations and margins. Do not extend to invent a head, legs or full-body pose. IMAGE 2 gives the dark grey equipment case/hardware only. IMAGE 3 gives original finely painted South-facing equipment/style detail ONLY; do not copy brighter exposure or reframe the target.

Raise BOTH forearms from hanging arms into a natural two-handed carrying grip on one compact HORIZONTAL dark grey case in front at WAIST level. South-facing front view, symmetrical case alignment, four subdued worn silver corner fittings, same compact case scale as the reference. Fingers visibly hold both case sides; elbows bent, shoulders attached naturally. Erase old hanging hands and show coherent original trouser/hip material there. No duplicated hands, elbow/body/backpack clipping or stretched forearms. Keep the master torso/head-facing orientation; no twisting. The anatomical-RIGHT belt wrench stays on his RIGHT hip (viewer LEFT), anatomical-LEFT meter stays at LEFT hip (viewer RIGHT). Do NOT relocate, duplicate or hold belt equipment. New arms/case may naturally occlude parts of belt tools without moving them aside. Exactly one wrench and one meter remain at their original anatomical belt locations, not in hands.

Use image1's subdued neutral MATTE graphite fabric, muted engineering ochre, restrained worn neutral silver and dark gloves. Fine painted sprite details matching master, same gear symbols. No purple/magenta, orange/bright yellow, glossy finish, exposure lift, black shadow expansion, white halo or blur. Preserve genuine TRANSPARENCY and antialiasing. Keep target composition and empty margins exactly; no zoom/recenter/new badge/goggles/text/checkerboard. Return ONE complete original square cropped torso/arms/belt pose, not whole character.'''
(p/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=[manifest,source,case,detail,p/'original.png',p/'target.png',p/'case-reference.png',p/'prompt.txt']
(p/'inputs.json').write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'source':source.relative_to(r).as_posix(),'crop':[80,96,176,192],'admissionRegion':[80,104,174,165],'selected':False,'detailReferenceStatus':'Preserved reference-derived candidate,not replacement locked master; actual selected native South remains geometry/material authority.'},indent=2)+'\n',encoding='utf-8')
print('Current selected South idle frozen; native96 crop8x, original head/lower body protected outside admitted torso region.')
