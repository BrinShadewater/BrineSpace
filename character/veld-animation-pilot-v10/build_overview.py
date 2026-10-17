"""Package existing frames for letter-labelled review; no artwork changes."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R=Path(__file__).resolve().parent
old=R.with_name('veld-animation-pilot-v9')
m=json.loads((R/'manifest.json').read_text())
states={s['id']:s for s in m['states']}
order=['idle-south','idle-east','idle-north','idle-west','walk-east','walk-west','interact-east']
labels=['A - Front idle','B - East idle','C - Rear idle','D - West idle','E - East walk','F - West walk','G - Inspection']
out=R/'review-all';out.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
frames={k:[Image.open(R/p).convert('RGBA') for p in states[k]['frameFiles']] for k in order}
for k in order:
    for p in states[k]['frameFiles']:
        assert np.array_equal(np.array(Image.open(R/p))[:,:,3],np.array(Image.open(old/p))[:,:,3])
        if k in ('idle-south','idle-north'):assert (R/p).read_bytes()==(old/p).read_bytes()
rendered=[]
for t in range(0,4320,60):
    im=Image.new('RGB',(840,990),'#202a31');d=ImageDraw.Draw(im)
    for n,k in enumerate(order):
        s=states[k];phase=t%sum(s['frameDurationsMs']);idx=0
        for i,duration in enumerate(s['frameDurationsMs']):
            if phase<duration:idx=i;break
            phase-=duration
        x=(n%3)*280;y=(n//3)*330
        sprite=frames[k][idx].resize((276,276),Image.Resampling.NEAREST)
        im.paste(sprite,(x+2,y+32),sprite)
        d.text((x+12,y+8),labels[n],font=font,fill='white')
        d.text((x+12,y+304),f'Frame {idx+1}/6',font=font,fill='#a8c9d8')
    for y,line in [(710,'Veld v10 candidates'),(748,'A and C unchanged'),(786,'Faces matched to A'),(824,'East silver restored'),(880,'Letter + frame for fixes')]:
        d.text((300,y),line,font=font,fill='white')
    rendered.append(im)
rendered[0].save(out/'all-animations.gif',save_all=True,append_images=rendered[1:],duration=60,loop=0,optimize=False)
rendered[0].save(out/'overview.png')
html='<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Veld v10 review</title><style>body{background:#202a31;color:white;font:18px system-ui;margin:20px}img{max-width:100%;image-rendering:pixelated}.frames{display:flex;overflow:auto}.frames img{width:184px}</style><h1>Veld v10 colour corrections</h1><p>A and C unchanged. B/D/E/F/G faces matched to A; side fabric exposure aligned; B/E/G silver restored independently. Candidates only.</p><img src="all-animations.gif">'
for k,label in zip(order,labels):
    html+=f'<h2>{label}</h2><img width="368" src="../preview/{k}-new.webp"><div class="frames">'+''.join(f'<figure><img src="../{p}"><figcaption>Frame {i+1}</figcaption></figure>' for i,p in enumerate(states[k]['frameFiles']))+'</div>'
(out/'index.html').write_text(html,encoding='utf-8')
(R/'owner-feedback-checks.json').write_text(json.dumps({'alpha_masks_unchanged':42,'A_C_byte_identical':12,'pose_and_timing_changes':False,'owner_visual_acceptance':'pending'},indent=2),encoding='utf-8')
print('Overview rebuilt; 42 alpha masks unchanged; A/C 12 frames byte-identical.')
