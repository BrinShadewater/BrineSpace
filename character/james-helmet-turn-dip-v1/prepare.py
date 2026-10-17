from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
audit=json.loads((r/'character/james-selected-turn-master-audit-v1/review.json').read_bytes())
s=audit['states']['helmet/carry-turn-south-west'];b=audit['states']['bare/carry-turn-south-west']
box=(96,56,160,120);hashes={};sources={}
board=Image.new('RGB',(6*384,384),'#303b40');d=ImageDraw.Draw(board)
for i,(hp,bp) in enumerate(zip(s['frames'],b['frames'])):
    helm=Image.open(r/hp).convert('RGBA');bare=Image.open(r/bp).convert('RGBA')
    assert helm.size==bare.size==(256,256)
    hashes[hp]=hashlib.sha256((r/hp).read_bytes()).hexdigest();hashes[bp]=hashlib.sha256((r/bp).read_bytes()).hexdigest()
    crop=helm.crop(box);bg=Image.new('RGBA',(64,64),'#303b40');bg.alpha_composite(crop)
    board.paste(bg.convert('RGB').resize((384,384),Image.Resampling.NEAREST),(i*384,0))
    d.text((i*384+4,4),f'{i} shell/collar fixed window',fill='white')
    if i in [1,2,3]:
        name={1:'previous',2:'target',3:'next'}[i];crop.resize((512,512),Image.Resampling.NEAREST).save(p/f'{name}.png');sources[name]=hp
    diff=np.any(np.asarray(helm)!=np.asarray(bare),axis=2);yy,xx=np.where(diff)
    sources[f'difference{i}']={'bounds':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]}
board.save(p/'shell-collar-before.png')
prompt='''Edit the FIRST image only: James helmeted head/collar crop. The SECOND and THIRD images are the neighboring turn angles for identity, physical scale and shell fit. Preserve exactly the target's three-quarter-left camera angle and mature face, visor, eyes, moustache, earpiece, helmet material, neutral white lamp and dark matte steel shell. The target shell is slightly undersized vertically: its crown sits two original sprite pixels lower than neighbors while the collar seating stays put. Enlarge only the TOP curvature of the helmet crown upward by TWO original sprite pixels (16 pixels in this512x512 reference), maintaining the same center, face/visor position and collar ring/contact. Original crown y14 in this64-square crop should become y12, collar bottom stays around53. Do not translate the whole helmet or face. Keep the same shell width, asymmetry and perspective; no rotation, bob, face redesign, colour flash, gloss, wide new rim, changes to yellow shoulder badge or torso. Retain all lower collar/shoulder pixels unchanged. This is a narrow equipment silhouette correction, not a new head or character. Transparent background with clean alpha and no white halo. Return one crop with the identical full64-square framing scaled uniformly into output, not cropped tightly.'''
(p/'prompt.txt').write_text(prompt+'\n');hashes[(p/'prompt.txt').relative_to(r).as_posix()]=hashlib.sha256((p/'prompt.txt').read_bytes()).hexdigest()
(p/'inputs.json').write_text(json.dumps({'crop':box,'sources':sources,'preCallSha256':hashes,'normalSelectionChanged':False},indent=2)+'\n')
print('Six enlarged registered shell/collar views; source-difference bounds and pre-call hashes saved.')
