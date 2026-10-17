from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;D=P.parent/'bill-seated-helmet-east-coherent-v1/sources/canonical-head.png';S=P/'sources/closed-eye-v1.png'
original=Image.open(D).convert('RGBA');source=Image.open(S).convert('RGBA');a=np.array(original);out=a.copy()
skin=np.array(source.crop((745,620,850,690)))[:,:,:3].astype(float)
ref=a[19:22,23:27,:3].astype(float);gain=np.median(ref.reshape(-1,3),axis=0)/np.median(skin.reshape(-1,3),axis=0)
source_box=[806,557,921,611];target=[26,16,29,19]
eye=np.array(source.crop(source_box).resize((3,3),Image.Resampling.LANCZOS));out[16:19,26:29,:3]=np.clip(eye[:,:,:3]*gain,0,255).astype('uint8')
result=P/'sources/canonical-closed-eye.png';Image.fromarray(out).save(result)
change=np.any(out!=a,axis=2);mask=np.zeros(a.shape[:2],bool);mask[16:19,26:29]=True
assert np.array_equal(out[:,:,3],a[:,:,3]) and not np.any(change&~mask)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
record={'generation':'exec-43de739f-b7d9-495b-b277-72833aa65c4b','canonicalSha256':sha(D),'donorSha256':sha(S),'resultSha256':sha(result),'sourceBox':source_box,'targetBox':target,'skinGain':gain.tolist(),'changedPixels':int(change.sum()),'alphaExact':True,'scope':'9 RGB pixels; every shell/visor/collar/face-outline pixel outside the eye mask unchanged'}
(P/'closed-eye-registration.json').write_text(json.dumps(record,indent=2)+'\n')
review=Image.new('RGB',(700,380),(34,52,62))
for i,im in enumerate([original,Image.fromarray(out)]):large=im.resize((350,380),Image.Resampling.NEAREST);review.paste(large,(350*i,0),large)
review.save(P/'closed-eye-review.png');print('Authored eyelid fitted:9 RGB pixels changed; canonical alpha/hardware exact')
