from pathlib import Path
import json,hashlib
import sys
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
version=sys.argv[1] if len(sys.argv)>1 else 'v1'
rawName='raw-key-'+version+'.png';nativeName='key-native-'+version+'.png'
raw=Image.open(P/rawName).convert('RGBA');assert raw.width==raw.height
native=raw.resize((256,256),Image.Resampling.LANCZOS);native.save(P/nativeName)
images=[Image.open(P/'master-native.png').convert('RGBA'),Image.open(P/'motion-native.png').convert('RGBA'),native]
board=Image.new('RGB',(2304,820),'#202a30');draw=ImageDraw.Draw(board);metrics=[]
for i,(im,label) in enumerate(zip(images,['Original West appearance','Old action: motion only','New whole interaction key'])):
 board.paste(im.resize((768,768),Image.Resampling.NEAREST),(i*768,40),im.resize((768,768),Image.Resampling.NEAREST));draw.text((i*768+12,10),label,fill='white')
 a=np.asarray(im);ys,xs=np.where(a[:,:,3]>200);top=int(ys.min());floor=int(ys.max())
 head=a[top:top+20,:,3]>200;hy,hx=np.where(head)
 # Head band includes bun and forehead; not an anatomical skull measurement.
 cloth=a[150:175,110:135];mask=(cloth[:,:,3]>200)&(cloth[:,:,0]<110)&(np.max(cloth[:,:,:3],axis=2)-np.min(cloth[:,:,:3],axis=2)<25)
 med=np.median(cloth[:,:,:3][mask],axis=0).tolist() if mask.any() else None
 metrics.append(dict(label=label,opaqueHeight=floor-top+1,headTop=top,bootFloor=floor,top20AlphaWidth=int(hx.max()-hx.min()+1),top20Axis=float((hx.max()+hx.min())/2),fixedTrouserPatchMedian=med,patchPixelCount=int(mask.sum())))
board.save(P/('master-key-comparison-'+version+'.png'))
bindings={}
for name in [rawName,nativeName,'master-native.png','motion-native.png','prompt.txt','master-input.png','motion-input.png']:bindings[name]=hashlib.sha256((P/name).read_bytes()).hexdigest()
if version=='v3':
 for name in ['high-source-prompt.txt','original-high-source-input.png','HIGH_SOURCE_INPUT.json']:bindings[name]=hashlib.sha256((P/name).read_bytes()).hexdigest()
for role,row in json.loads((P/'INPUTS.json').read_bytes()).items():assert hashlib.sha256((R/row['source']).read_bytes()).hexdigest()==row['SHA256'],role
(P/('AUDIT-'+version+'.json')).write_text(json.dumps(dict(rawSize=raw.size,fixedWholeScale=256/raw.width,fixedWholeOffset=[0,0],metrics=metrics,bindings=bindings,visualReview='pending',scope='One key source appearance; no sequence, contact, helmet/native/normal adoption. Fixed trouser patch is a diagnostic, not whole material proof.'),indent=2)+'\n')
print(json.dumps(metrics))
