from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
import numpy as np
P=Path(__file__).resolve().parent
original=np.asarray(Image.open(P/'registered-reference.png').convert('RGBA'));control=np.asarray(Image.open(P/'input-alpha-control.png').convert('RGBA'))
# Original-only fixed spatial cloth mask below arms and belt; never edits artwork.
region=np.zeros((256,256),bool);region[150:175,110:135]=True
rgb=original[:,:,:3].astype(int)
mask=region&(original[:,:,3]>200)&(np.ptp(rgb,axis=2)<25)&(rgb[:, :,0]<110)&(rgb.mean(2)>20)
def sample(a):
 m=mask&(a[:,:,3]>200);return dict(pixels=int(m.sum()),median=np.median(a[:,:,:3][m],axis=0).tolist(),mean=np.mean(a[:,:,:3][m],axis=0).tolist(),originalCommonMAE=float(np.abs(a[:,:,:3].astype(float)[m]-rgb[m]).mean()))
rows=[];bindings={}
for n,file in enumerate(sorted((P/'full-clip-frames-v2').glob('*.png'))):
 a=np.asarray(Image.open(file).convert('RGBA'));rows.append(dict(frame=n,**sample(a)));bindings[str(file.relative_to(P))]=hashlib.sha256(file.read_bytes()).hexdigest()
indices=[0,18,30,60,90,112,130,141];board=Image.new('RGB',(1600,450),'#202a30');draw=ImageDraw.Draw(board)
for col,n in enumerate(indices):
 im=Image.open(P/'full-clip-frames-v2'/f'{n:03}.png').convert('RGBA');crop=im.crop((100,143,146,183)).resize((184,160),Image.Resampling.NEAREST)
 board.paste(crop,(col*200,45),crop);draw.text((col*200+3,5),f'{n}: '+str(rows[n]['median']),fill='white')
 ref=Image.fromarray(original).crop((100,143,146,183)).resize((184,160),Image.Resampling.NEAREST);board.paste(ref,(col*200,250),ref);draw.text((col*200+3,222),'Original same fixed region',fill='white')
board.save(P/'stationary-trouser-grade-review.png')
report=dict(reference=sample(original),inputAlphaControl=sample(control),maskDefinition='Fixed original cloth-only opaque pixels in x110:135,y150:175; below arm action. Candidates only restricted to common opaque pixels; not a matched anatomical landmark proof.',rows=rows,bindings=bindings,rangeMedianPerChannel=[[min(row['median'][i] for row in rows),max(row['median'][i] for row in rows)] for i in range(3)],visualReview='pending',scope='Stationary cloth grade diagnostic only; does not certify full materials/physics. Source RGB unchanged.')
(P/'stationary-grade-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(reference=report['reference'],control=report['inputAlphaControl'],range=report['rangeMedianPerChannel'],samples=[rows[n] for n in [0,71,141]])))
