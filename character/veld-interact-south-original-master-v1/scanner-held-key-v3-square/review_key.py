from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[2]
raw=Image.open(P/'raw-source.png').convert('RGBA');assert raw.width==raw.height
key=raw.resize((256,256),Image.Resampling.LANCZOS);key.save(P/'native-held-key.png')
master=Image.open(R/'character/veld-idle-south-original-master-v1/original-idle-master.png').convert('RGBA')
control=Image.open(P/'original-square-reference.png').convert('RGBA').resize((256,256),Image.Resampling.LANCZOS);control.save(P/'input-control.png')
def metrics(im):
    a=np.asarray(im);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1]
    return dict(height=int(y.max()-y.min()+1),top=top,floor=int(y.max()),left=int(x.min()),right=int(x.max()),headWidth=int(hx.max()-hx.min()+1),headAxis=float((hx.max()+hx.min())/2))
board=Image.new('RGB',(1024,550),'#202a30');d=ImageDraw.Draw(board)
for i,im in enumerate([master,control,key,master]):
    board.paste(im,(i*256,24),im);d.text((i*256+3,4),['Original rest','Input control','Whole held key','Original return'][i],fill='white')
    crop=im.crop((94,65,174,145)).resize((256,256),Image.Resampling.NEAREST);board.paste(crop,(i*256,288),crop)
board.save(P/'master-held-comparison.png')
record=dict(rawSize=raw.size,rawSHA256=hashlib.sha256((P/'raw-source.png').read_bytes()).hexdigest(),registration=dict(scale=256/raw.width,offset=[0,0],method='Uniform square-canvas mapping only; no body-bound scale/recenter/refloor or per-region change.'),master=metrics(master),control=metrics(control),key=metrics(key),scope='Whole authored source key comparison, not animated/native controller acceptance.')
(P/'KEY_REVIEW.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps(record))
