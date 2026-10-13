"""Prepare four coherent half-settled poses with matched whole figure references."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-walk-joins-v1';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
idle_source=R/'character/bill-east-idle-master-motion-v1/frames/idle-east/000.png'
idle=Image.new('RGBA',(1024,1024));idle.alpha_composite(Image.open(idle_source).convert('RGBA').resize((736,736),Image.Resampling.LANCZOS),(144,208));idle.save(D/'idle-reference.png')
master=R/'character/bill-east-walk-master-pilot-v1/original-master.png'
for slot in [0,12,24,36]:
 S=D/f'settle-{slot:03}';S.mkdir()
 target=R/f'character/bill-east-walk-master-full-v1/frames/{slot:03}.png';Image.open(target).resize((1024,1024),Image.Resampling.NEAREST).save(S/'edit-target.png')
 refs=[{'path':str(p),'sha256':sha(p),'source':str(src),'sourceSha256':sha(src),'role':role} for p,src,role in [(S/'edit-target.png',target,'Starting whole walking pose and exact placement'),(D/'idle-reference.png',idle_source,'Destination standing pose, source-density identity/detail reference'),(master,master,'Original master identity and matte materials')]]
 prompt=f'''Edit image1 into ONE complete coherent intermediate settling pose for Bill, between image1 walking phase{slot} and the standing destination image2. Transparent RGBA sprite; one whole person only. Move each foot HALF of the way horizontally from its image1 location toward its corresponding image2 standing location. Ease the knee bends and arm swing HALF toward the destination. Keep anatomical length and narrow build; pelvis, shoulders, crown and head size remain registered to the same physical figure profile, pivot at(512,896) on all supplied1024square canvases. A natural weight transfer with soft knees, heel/toe contact, no crouch, no wide shoulders. Head/face match the same angular brown-haired bearded Bill with warm readable skin; avoid head/collar re-design. Preserve original-master matte grey quilted suit detail, red worn shoulder badge and chest patch, silver straps, belt, gloves and boots. No shine, brighter grading, extra hands, extra feet, duplicate limbs, painted shadows/background, halos, text, montage or motion blur. This is a single authored whole pose, not a composited head/body. Retain precise overall height and common sole level from the references. Source physical alignment and worn material detail matter more than embellishment.'''
 (S/'prompt.txt').write_text(prompt,encoding='utf-8');(S/'references.json').write_text(json.dumps(refs,indent=2)+'\n',encoding='utf-8')
print('Prepared four matched1024 whole settling pose edits; current walk untouched.')
