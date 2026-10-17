"""Registered endpoint references; authored master pixels only."""
from pathlib import Path
from PIL import Image
import numpy as np, json
P=Path(__file__).resolve().parent
specs=[('bare','veld-side-foundation-v1/side-master-01.png',(389,48,644,962),.78),('helmet','veld-helmet-side-v1/side-master-01.png',(372,16,658,984),.78*763/778)]
records=[]
for name,source,box,scale in specs:
 im=Image.open(P.parent/source).convert('RGBA').crop(box)
 a=np.array(im);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);im=Image.fromarray(a)
 im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
 pos=(512-im.width//2,940-im.height)
 out=Image.new('RGB',(1024,1024),(48,190,72));out.paste(im,pos,im);out.save(P/f'{name}-input.png')
 records.append(dict(name=name,source=source,crop=box,scale=scale,placement=pos,soleY=940))
(P/'inputs.json').write_text(json.dumps(records,indent=2)+'\n')
