"""Package generated case; preserve native actor pixels in staged registered previews."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
raw=np.array(Image.open(P/'sources/case-v4.png').convert('RGBA'))
labels,_=label(raw[:,:,3]>80);counts=np.bincount(labels.ravel());counts[0]=0
region=labels==counts.argmax();ys,xs=np.where(region)
box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
clean=raw.copy();keep=binary_dilation(region,iterations=2)&(raw[:,:,3]>0);clean[~keep]=0
crop=Image.fromarray(clean).crop(tuple(box))
scale=23/crop.width
case=crop.resize((23,round(crop.height*scale)),Image.Resampling.LANCZOS)
pos=[128-case.width//2,220-case.height]
floor=Image.new('RGBA',(256,256));floor.alpha_composite(case,tuple(pos));floor.save(P/'floor-case-north.png')
board=Image.new('RGBA',(1024,840),'#22343e');draw=ImageDraw.Draw(board);checks=0
hashes={};metrics={}
for row,gear in enumerate(['bare','helmet']):
 idle_path=R/f'character/bill-carry-start-south-v2/short-route-captures/rot0-{gear}-completed-north-source.png'
 unload_path=R/f'character/bill-unload-north-rise-v1/frames/{gear}/unload-north/013.png'
 idle=Image.open(idle_path).convert('RGBA');assert idle.size==(184,184)
 standing=Image.new('RGBA',(256,256));standing.alpha_composite(idle,(36,52))
 preview=floor.copy();preview.alpha_composite(standing)
 preview.save(P/f'{gear}-idle-with-floor-case.png')
 a=np.array(standing);b=np.array(preview);opaque=a[:,:,3]==255
 assert np.array_equal(a[opaque],b[opaque]);checks+=int(opaque.sum())
 floor_pixels=np.array(floor);empty=a[:,:,3]==0
 assert np.array_equal(b[empty],floor_pixels[empty]);checks+=int(empty.sum())
 # Every pixel outside the new prop's support remains original RGBA.
 outside=floor_pixels[:,:,3]==0
 assert np.array_equal(a[outside],b[outside]);checks+=int(outside.sum())
 for col,(name,im) in enumerate([('original unload',Image.open(unload_path)),('selected idle',standing),('staged floor case',preview),('separate prop',floor)]):
  board.alpha_composite(im,(col*256,row*420))
  small=im.resize((round(256*82/148),)*2,Image.Resampling.LANCZOS)
  board.alpha_composite(small,(col*256+55,row*420+260))
  draw.text((col*256+8,row*420+405),gear+' / '+name,fill='white')
 for path in [idle_path,unload_path]:hashes[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
 metrics[gear]={'opaqueBodyPixelsPreserved':int(opaque.sum()),'outsidePropPixelsPreserved':int(outside.sum())}
board.convert('RGB').save(P/'registered-case-review.png')
registration={'source':'sources/case-v4.png','sourceBox':box,'scale':scale,'nativeCaseSize':list(case.size),'position':pos,'pivot':[128,224],'standingHeight':148,'alphaExtraction':'Largest alpha>80 component, associated two-pixel fringe only; original raw alpha retained in sources. No painted pixels.','grade':'No recoloring applied; generated material reviewed separately.','sourceSha256':hashlib.sha256((P/'sources/case-v4.png').read_bytes()).hexdigest(),'protectedInputs':hashes,'metrics':metrics,'status':'staged source/prop study; no normal loader, ownership, lifetime, depth, persistence or Continue behavior selected'}
(P/'registration.json').write_text(json.dumps(registration,indent=2)+'\n',encoding='utf-8')
(P/'validation.json').write_text(json.dumps({'passed':True,'pixelComparisons':checks,'mechanicalScope':'Exact native opaque body and outside-prop RGBA retained; case behind body, same floor location both gears. Not native lifecycle or visual acceptance.'},indent=2)+'\n',encoding='utf-8')
print('Case box',box,'native',case.size,'position',pos,'protected comparisons',checks)
