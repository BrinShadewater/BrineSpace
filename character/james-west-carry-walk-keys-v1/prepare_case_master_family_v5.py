from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];crop=[80,96,176,192]
master=r/'character/james-west-master-carry-v1/local-v3-carry-pose.png'
reference=p/'walk00-case-master-v5-reference.png'
pilot=p/'walk00-case-master-v5.png'
Image.open(pilot).convert('RGBA').crop(crop).resize((768,768),Image.Resampling.LANCZOS).save(p/'case-master-family-v5-contact-reference.png')
for i in (8,12,20,28,36,44,48):
    n=f'walk{i:02d}-case-master-v5';source=p/f'walk{i:02d}-belt-anatomy-v4.png'
    Image.open(source).convert('RGBA').crop(crop).resize((768,768),Image.Resampling.LANCZOS).save(p/f'{n}-target.png')
    prompt=(p/'walk00-case-master-v5-prompt.txt').read_text().replace('walk phase0',f'walk phase{i}')
    prompt+='\nImage3 is phase0 contact/waist-placement pilot at same framing, supporting grip continuity ONLY. Image2 actual original master remains authority for box dimensions/latch shape/material, not the pilot. Preserve image1 own original gait/torso lean, adjust both hands/necessary lower forearm for the SAME rigid case and low waist grip; do not copy image2/image3 hips/thighs/legs. Avoid coarse pixel-art re-rendering or boxy square latch redesign: original softer muted detailed matte sprite material, dull silver vertical corner hardware. No new belt tool visibility or alpha hole.\n'
    (p/f'{n}-prompt.txt').write_text(prompt,encoding='utf-8')
    files=[source,master,reference,pilot,p/'case-master-family-v5-contact-reference.png',p/f'{n}-target.png',p/f'{n}-prompt.txt',Path(__file__)]
    (p/f'{n}-inputs.json').write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':crop,'admissionRegion':[88,116,151,161],'baseFile':source.name,'scope':'Actual master-driven rigid-case/grip family correction; pose0 only supporting contact guide. Local material/tool/arm seams provisional.'},indent=2)+'\n',encoding='utf-8')
print('Seven actual master-case/grip edits prepared.')
