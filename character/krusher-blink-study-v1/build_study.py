from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;R=P.parent.parent
head_source=R/'character/krusher-bill-base-test-v2/sources/south-head-native.png';body_source=R/'character/krusher-runtime-candidate-v1/frames/bare/idle-south/000.png'
original=Image.open(head_source).convert('RGBA');registered=Image.open(P/'registered-blink.png').convert('RGBA');a=np.array(original);b=np.array(registered)
mask=np.zeros(a.shape[:2],bool)
for box in [(8,14,13,17),(16,14,21,17)]:
    x0,y0,x1,y1=box;mask[y0:y1,x0:x1]=True
closed=a.copy();closed[mask,:3]=b[mask,:3]
closed_head=Image.fromarray(closed);closed_head.save(P/'south-head-closed.png');Image.fromarray(mask.astype('uint8')*255).save(P/'eye-mask.png')
base=Image.open(body_source).convert('RGBA');body=np.array(base);head_xy=(81,23);x,y=head_xy;head_region=body[y:y+28,x:x+23].copy();head_region[mask,:3]=closed[mask,:3];body[y:y+28,x:x+23]=head_region
closed_body=Image.fromarray(body);closed_body.save(P/'south-idle-closed.png')
base.save(P/'blink-preview.png',save_all=True,append_images=[closed_body,base],duration=[1700,100,900],loop=0,disposal=1,blend=0)
board=Image.new('RGBA',(960,640),'#272b2e');d=ImageDraw.Draw(board);font=lambda n:ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),n)
d.text((24,15),'KRUSHER DOM / SOUTH BLINK SOURCE STUDY',font=font(30),fill='white')
for i,head in enumerate([original,closed_head]):
    board.alpha_composite(head.resize((184,224),Image.Resampling.NEAREST),(30+i*220,85))
    d.text((30+i*220,325),'OPEN / ORIGINAL' if i==0 else 'CLOSED / EYES ONLY',font=font(23),fill='white')
for i,im in enumerate([base,closed_body]):
    board.alpha_composite(im,(510+i*210,100));d.text((510+i*210,325),'OPEN' if i==0 else 'CLOSED',font=font(23),fill='white')
    small=im.resize((92,92),Image.Resampling.LANCZOS);board.alpha_composite(small,(545+i*210,375))
d.text((24,500),'Authored edit: eye regions only. Head outline, alpha, hair, beard and body remain exact.',font=font(23),fill='#bdcdd0')
d.text((24,540),'One closed-eye source; no half-close inbetween or runtime selection.',font=font(22),fill='#bdcdd0')
d.text((24,575),'Preview: open 1700 / closed 100 / open 900 ms. Small views are 92 px display references.',font=font(22),fill='#bdcdd0')
board.convert('RGB').save(P/'blink-reference-sheet.png')
fullmask=np.zeros(body.shape[:2],bool);fullmask[y:y+28,x:x+23]=mask
report={'eyeRects':[[8,14,13,17],[16,14,21,17]],'headPaste':list(head_xy),'headAlphaExact':bool(np.array_equal(a[:,:,3],closed[:,:,3])),'headOutsideEyeMaskExact':bool(np.array_equal(a[~mask],closed[~mask])),'bodyOutsideEyeMaskExact':bool(np.array_equal(np.array(base)[~fullmask],body[~fullmask])),'changedPixels':int(np.any(a!=closed,axis=2).sum()),'sourceHashes':{str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [head_source,body_source]},'timingMs':[1700,100,900],'scope':'south bare facial source study; not a new breathing body clip, helmet coverage or final motion acceptance'}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['headAlphaExact','headOutsideEyeMaskExact','bodyOutsideEyeMaskExact','changedPixels']}));assert all(report[k] for k in ['headAlphaExact','headOutsideEyeMaskExact','bodyOutsideEyeMaskExact'])
