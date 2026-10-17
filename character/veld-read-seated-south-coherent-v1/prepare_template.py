"""Repeat the exact preserved seated source as an arm-only authoring target."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image
P=Path(__file__).resolve().parent; R=P.parents[1]; base=R/'character/veld-seated-south-coherent-v1'
g=json.loads((base/'source-review.json').read_text()); source=base/g['source']; a=np.array(Image.open(source).convert('RGBA'))
labs,n=label(a[:,:,3]>180); counts=np.bincount(labs.ravel()); counts[0]=0
parts=sorted(np.argsort(counts)[-6:],key=lambda k:(int(np.where(labs==k)[0].mean())//512,int(np.where(labs==k)[1].mean())//512)); record=g['frames'][5]
pixels=a.copy(); pixels[~(binary_dilation(labs==parts[5],iterations=3)&(a[:,:,3]>0))]=0
crop=Image.fromarray(pixels).crop(record['rawBox']); atlas=Image.new('RGBA',(1536,1024)); positions=[]
for row in range(2):
 for col in range(3):
  x=round(col*512+256-(record['sourceFootCenterX']-record['rawBox'][0])); y=round(row*512+499-(record['sourceFloorY']-record['rawBox'][1]))
  atlas.alpha_composite(crop,(x,y));positions.append([x,y])
(P/'sources').mkdir(parents=True,exist_ok=True);atlas.save(P/'sources/arm-template-v1.png')
(P/'sources/template-v1.json').write_text(json.dumps({'source':source.relative_to(R).as_posix(),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceSlot':5,'sourceRawBox':record['rawBox'],'standingRuler':g['fixedRuler'],'scale':1,'positions':positions,'floorPerRow':[499,1011],'scope':'same raw neutral six times; edit forearms/hands/tablet only, preserve body/head/feet'},indent=2)+'\n')
print('Six identical seated source bodies saved; no rescaling or colour changes.')
