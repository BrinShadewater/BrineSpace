"""Separate authored blue storage banks and cooler; preserve raw source."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
p=Path(__file__).resolve().parents[1]/'assets/rooms/cold-store/pack'
raw=p/'equipment-raw.png';im=Image.open(raw).convert('RGBA')
a=np.array(im);rgb=a[:,:,:3].astype(int)
a[(rgb[:,:,0]-rgb[:,:,1]>35)&(rgb[:,:,2]-rgb[:,:,1]>35)]=0
clean=Image.fromarray(a);records=[]
for name,left,right in [('fridge',0,500),('rack',500,920),('cooler',920,1536)]:
    part=clean.crop((left,0,right,im.height));box=part.getbbox();part=part.crop(box)
    for q,turn in enumerate([part,part.transpose(Image.Transpose.ROTATE_270),part.transpose(Image.Transpose.ROTATE_180),part.transpose(Image.Transpose.ROTATE_90)]):turn.save(p/f'{name}-q{q}.png')
    records.append({'id':name,'region':[left,0,right,im.height],'crop':box,'size':part.size})
record={'sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'size':im.size,'key':'R-G>35 and B-G>35','parts':records,'stage':'cleaned, not selected'}
(p/'equipment-review.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
