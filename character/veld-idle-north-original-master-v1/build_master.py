from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];source=R/'character/veld-cargo-turns-master-family-v1/original-north-identity-reference.png'
a=np.array(Image.open(source).convert('RGBA'));key=(a[:,:,0]>220)&(a[:,:,1]<60)&(a[:,:,2]>220)
assert key[0].all() and key[-1].all() and key[:,0].all() and key[:,-1].all()
clean=a.copy();clean[key]=0;y,x=np.where(clean[:,:,3]>200);height=int(y.max()-y.min()+1);scale=148/height
im=Image.fromarray(clean);im.save(P/'original-alpha-reference.png');scaled=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);s=np.array(scaled);sy,sx=np.where(s[:,:,3]>200);top=int(sy.min());_,hx=np.where(s[top:top+16,:,3]>128);pos=(round(128-(hx.min()+hx.max())/2),224-int(sy.max()));body=Image.new('RGBA',(256,256));body.alpha_composite(scaled,pos);body.save(P/'original-idle-master.png');b=np.array(body);by,bx=np.where(b[:,:,3]>200)
assert by.max()==224 and by.max()-by.min()+1==148
old=Image.open(R/'character/veld-cargo-north-master-family-v1/frames/bare/unload-north/005.png').convert('RGBA');board=Image.new('RGB',(768,420),'#202a30');d=ImageDraw.Draw(board)
for col,(name,f) in enumerate([('Original authored master',body),('Prior cargo endpoint',old),('Original head detail',body)]):
 x=col*256;d.text((x+4,5),name,fill='white');board.paste(f,(x,25),f)
 detail=f.crop((96,70,160,130)).resize((192,180),Image.Resampling.NEAREST);board.paste(detail,(x+32,240),detail)
board.save(P/'master-endpoint-comparison.png')
(P/'master-reference.json').write_text(json.dumps({'source':source.relative_to(R).as_posix(),'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'legacyMagentaKey':{'redGreaterThan':220,'greenLessThan':60,'blueGreaterThan':220,'removedPixels':int(key.sum()),'scope':'Background removal only; remaining source RGB unchanged.'},'originalOpaqueHeight':height,'oneStandingRuler':148,'scale':scale,'wholeImageOffset':list(pos),'nativeOpaqueHeight':148,'nativeOpaqueWidth':int(bx.max()-bx.min()+1),'nativeBootFloor':224,'colourChanged':False},indent=2)+'\n')
print(f'Original North master registered at148px; width{bx.max()-bx.min()+1}; source RGB unchanged outside legacy background key.')
