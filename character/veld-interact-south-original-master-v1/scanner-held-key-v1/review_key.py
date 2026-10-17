from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[2]
ref=Image.open(R/'character/veld-cargo-turns-master-family-v1/original-south-identity-reference.png').convert('RGBA')
raw=Image.open(P/'raw-source.png').convert('RGBA')
authority=json.loads((R/'character/veld-idle-south-original-master-v1/master-reference.json').read_bytes())
# Uniform source-canvas mapping only; never normalize a generated body to its own bounds.
canvas_ratio=ref.width/raw.width
scale=authority['scale']*canvas_ratio
resized=raw.resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS)
key=Image.new('RGBA',(256,256));key.alpha_composite(resized,tuple(authority['wholeImageOffset']));key.save(P/'native-held-key.png')
master=Image.open(R/'character/veld-idle-south-original-master-v1/original-idle-master.png').convert('RGBA')
def metrics(im):
    a=np.asarray(im);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1]
    return dict(height=int(y.max()-y.min()+1),top=top,floor=int(y.max()),left=int(x.min()),right=int(x.max()),headWidth=int(hx.max()-hx.min()+1),headAxis=float((hx.max()+hx.min())/2))
board=Image.new('RGB',(768,550),'#202a30');d=ImageDraw.Draw(board)
for i,im in enumerate([master,key,master]):
    board.paste(im,(i*256,24),im);d.text((i*256+3,4),['Original rest','Whole held key','Original return'][i],fill='white')
    crop=im.crop((94,65,174,145)).resize((256,256),Image.Resampling.NEAREST);board.paste(crop,(i*256,288),crop)
board.save(P/'master-held-comparison.png')
record=dict(referenceSize=ref.size,rawSize=raw.size,rawSHA256=hashlib.sha256((P/'raw-source.png').read_bytes()).hexdigest(),canvasAspectRelativeError=abs((raw.width/raw.height)/(ref.width/ref.height)-1),registration=dict(scale=scale,offset=authority['wholeImageOffset'],method='Uniform mapping from reference canvas width, unchanged original placement; no body-bound scaling or per-region edit.'),master=metrics(master),key=metrics(key),scope='Single authored whole-source key diagnostic; visual proportions/material/prop proof required before animation.')
(P/'KEY_REVIEW.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record))
