from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
canonical=P/'sources/canonical-head.png';source=P/'sources/closed-eyes-v1.png'
original=Image.open(canonical).convert('RGBA');raw=Image.open(source).convert('RGBA')
out=np.array(original);ref=out[:,:,:3].astype(float)
src=np.array(raw.crop((460,450,850,580)));rgb=src[:,:,:3].astype(float)
mask=(src[:,:,3]>180)&(rgb[:,:,0]>1.15*rgb[:,:,1])&(rgb.mean(2)>100)
yy,xx=np.indices(out.shape[:2]);authority=(out[:,:,3]>180)&(xx>=12)&(xx<24)&(yy>=20)&(yy<24)&(ref[:,:,0]>1.15*ref[:,:,1])&(ref.mean(2)>65)
gain=np.median(ref[authority],axis=0)/np.median(rgb[mask],axis=0)
regions=[{'source':[494,478,609,529],'target':[13,18,17,21]},{'source':[696,478,811,529],'target':[19,18,23,21]}]
for region in regions:
 x0,y0,x1,y1=region['target'];eye=np.array(raw.crop(region['source']).resize((x1-x0,y1-y0),Image.Resampling.LANCZOS))
 out[y0:y1,x0:x1,:3]=np.clip(eye[:,:,:3]*gain,0,255).astype('uint8')
Image.fromarray(out).save(P/'sources/canonical-closed-eyes.png')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
changed=np.any(out!=np.array(original),axis=2)
record={'generation':'exec-0b1ad8c7-6822-4afb-816d-f4980cb3c9fe','sourceSha256':sha(source),'canonicalSha256':sha(canonical),'resultSha256':sha(P/'sources/canonical-closed-eyes.png'),'regions':regions,'gain':gain.tolist(),'changedPixels':int(changed.sum()),'alphaExact':bool(np.array_equal(out[:,:,3],np.array(original)[:,:,3])),'scope':'authored eyelid donor sampled into24 RGB pixels only; exact shell/visor/collar/face outline and alpha preserved'}
(P/'closed-eye-registration.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
preview=Image.new('RGB',(720,420),(34,52,62));preview.paste(original.resize((360,420),Image.Resampling.NEAREST),(0,0),original.resize((360,420),Image.Resampling.NEAREST));preview.paste(Image.fromarray(out).resize((360,420),Image.Resampling.NEAREST),(360,0),Image.fromarray(out).resize((360,420),Image.Resampling.NEAREST));preview.save(P/'closed-eye-review.png')
print(json.dumps({'changedPixels':record['changedPixels'],'alphaExact':record['alphaExact']}))
