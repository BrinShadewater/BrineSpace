from pathlib import Path
import json,runpy,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
layout=json.loads((P/'input-evidence.json').read_text());raw=Image.open(P/'source.png').convert('RGBA');a=np.array(raw)
fixed_scale=.4152542372881356*layout['templateSize'][0]/raw.width
labels,_=ndimage.label(a[:,:,3]>180);counts=np.bincount(labels.ravel());counts[0]=0
ids=sorted(np.argsort(counts)[-6:],key=lambda k:np.where(labels==k)[0].mean())
ids=[k for row in [ids[:3],ids[3:]] for k in sorted(row,key=lambda k:np.where(labels==k)[1].mean())]
helpers=runpy.run_path(str(R/'character/james-lying-family-v1/build.py'));foot,head=helpers['foot'],helpers['head']
reference=Image.open(R/'character/james-rest-south-identity-v2/frames/lie-down/005.png').convert('RGBA');target=foot(reference)
frames=[];records=[];(P/'frames').mkdir(exist_ok=True)
for i,k in enumerate(ids):
    y,x=np.where(labels==k);box=[int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4]
    cell=a[box[1]:box[3],box[0]:box[2]].copy();cell[~ndimage.binary_dilation(labels[box[1]:box[3],box[0]:box[2]]==k,iterations=2)]=0
    im=Image.fromarray(cell);at=np.rint(target-foot(im)*fixed_scale).astype(int)
    out=Image.new('RGBA',(256,256));out.alpha_composite(im.resize((round(im.width*fixed_scale),round(im.height*fixed_scale)),Image.Resampling.LANCZOS),tuple(at))
    out.save(P/'frames'/f'{i:03}.png');frames.append(out);arr=np.array(out);yy,xx=np.where(arr[:,:,3]>192);point,hb=head(out,'south',5)
    records.append({'index':i,'sourceBox':box,'translation':at.tolist(),'headAnchor':point.tolist(),'headBox':hb,'widthAlpha192':int(xx.max()-xx.min()+1),'heightAlpha192':int(yy.max()-yy.min()+1),'crown':int(yy.min()),'sole':int(yy.max()),'sha256':hashlib.sha256((P/'frames'/f'{i:03}.png').read_bytes()).hexdigest()})
board=Image.new('RGB',(7*300,300),'#303b40');d=ImageDraw.Draw(board)
for i,(label,im) in enumerate([('exact reference neutral',reference),*[(f'authored source {j}',im) for j,im in enumerate(frames)]]):
    crop=im.crop((60,115,195,235)).resize((270,240),Image.Resampling.NEAREST);board.paste(crop,(i*300,30),crop);d.text((i*300+4,4),label,fill='white')
board.save(P/'fixed-ruler-review.png')
e={'fixedScale':fixed_scale,'ruler':'Original.415254 source anatomical ruler times template-width/output-width, shared across all6 complete figures. Source-cell translations place fixed supported sole pivot; no per-pose resizing. Unmodified authored heads/limbs at this source-review stage.','templateSize':layout['templateSize'],'sourceSize':list(raw.size),'runtimeInstalled':False,'records':records,'uniqueAuthoredRasterReferences':len({r['sha256'] for r in records})}
(P/'fixed-ruler-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
print(json.dumps({'fixedScale':fixed_scale,'sourceSize':list(raw.size),'referenceRuler':layout['templateSize'],'references':len(records),'uniqueRasterReferences':e['uniqueAuthoredRasterReferences'],'widths':[r['widthAlpha192'] for r in records],'heights':[r['heightAlpha192'] for r in records],'crowns':[r['crown'] for r in records],'soles':[r['sole'] for r in records]}))
