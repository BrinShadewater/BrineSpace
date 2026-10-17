"""Original standing master at fixed source density; identical endpoints."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2]
assert not (P/'generation.json').exists(),'Exclusive paid ledger already exists'
sourcepath=R/'character/veld-east-held-original-master-v1/raw-held-v1.png';raw=Image.open(sourcepath).convert('RGBA')
source=raw.resize((round(raw.width*757/raw.height),757),Image.Resampling.LANCZOS)
source.save(P/'whole-source-reference.png');plate=Image.new('RGBA',(768,1024));plate.alpha_composite(source,(190,130))
white=Image.new('RGBA',plate.size,'white');white.alpha_composite(plate);white.convert('RGB').save(P/'master-input.png')
y,x=np.where(np.array(plate)[:,:,3]>200);estimated=round(1024*148/(y.max()-y.min()+1))
for delta in [0,1,-1,2,-2,3,-3]:
 h=estimated+delta;scale=h/1024;im=plate.resize((round(768*scale),h),Image.Resampling.LANCZOS);a=np.array(im);y,x=np.where(a[:,:,3]>200)
 if y.max()-y.min()+1==148:break
else:raise AssertionError('Reference global148ruler unavailable')
top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];assert 26<=hx.max()-hx.min()+1<=27,'Original head ruler drift before submission';offset=(round(123.5-(hx.min()+hx.max())/2),223-int(y.max()));native=Image.new('RGBA',(256,256));native.alpha_composite(im,offset);native.save(P/'registered-reference.png')
board=Image.new('RGB',(640,310),(32,43,49));d=ImageDraw.Draw(board)
for i,(p,label) in enumerate([(P/'registered-reference.png','Fixed plate reference'),(R/'character/veld-east-held-original-master-v1/frames/bare/000.png','Original held master')]):
 image=Image.open(p).convert('RGBA');board.paste(image,(i*320+32,30),image);d.text((i*320+20,10),label,fill='white')
board.save(P/'input-master-review.png')
record={'source':sourcepath.relative_to(R).as_posix(),'sourceSha256':hashlib.sha256(sourcepath.read_bytes()).hexdigest(),'plateSize':[768,1024],'sourceOffset':[190,130],'nativeSize':list(im.size),'sourceScale':scale,'fixedOffset':list(offset),'referenceHeight':148,'referenceHeadWidth':int(hx.max()-hx.min()+1),'endpointIdentical':True,'inputSha256':hashlib.sha256((P/'master-input.png').read_bytes()).hexdigest(),'modelIntent':'Scoped MiniMax-Hailuo-02 first/last conditioning, same original standing image both ends,6s768P estimatedUSD0.28, verified published rate Oct3; actual billing unverified.','purpose':'Dense initial step and return-to-standing with original-only identity and fixed neutral white plate, after sparse chain held-to-lift planted boot jump. No advance guide or regenerated appearance source.','scope':'Whole-source composition/global reference ruler only. No RGB/body/limb edit, no per-video-frame normalization, no paid retry, no completed animation/physical contact/native/controller acceptance.'}
(P/'input-record.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps(record))
