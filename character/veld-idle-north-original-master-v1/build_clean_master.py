from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];source=P/'raw-clean-master-v1.png'
im=Image.open(source).convert('RGBA');a=np.array(im);y,x=np.where(a[:,:,3]>200);height=int(y.max()-y.min()+1);scale=148/height
for adjustment in [0,1,-1,2,-2]:
    resized_height=round(im.height*scale)+adjustment
    scaled=im.resize((round(im.width*resized_height/im.height),resized_height),Image.Resampling.LANCZOS);s=np.array(scaled);sy,sx=np.where(s[:,:,3]>200)
    if sy.max()-sy.min()+1==148:break
else:raise AssertionError('No exact opaque standing ruler within two quantized source pixels')
scale=resized_height/im.height;top=int(sy.min());_,hx=np.where(s[top:top+16,:,3]>128);pos=(round(128-(hx.min()+hx.max())/2),224-int(sy.max()));body=Image.new('RGBA',(256,256));body.alpha_composite(scaled,pos);body.save(P/'clean-idle-master.png');b=np.array(body);by,bx=np.where(b[:,:,3]>200)
assert by.max()==224 and by.max()-by.min()+1==148
original=Image.open(P/'original-idle-master.png').convert('RGBA');old=Image.open(R/'character/veld-cargo-north-master-family-v1/frames/bare/unload-north/005.png').convert('RGBA')
board=Image.new('RGB',(768,480),'#202a30');d=ImageDraw.Draw(board)
for col,(name,f) in enumerate([('Original keyed diagnostic',original),('Prepared original candidate',body),('Prior cargo endpoint',old)]):
 xx=col*256;d.text((xx+4,5),name,fill='white');board.paste(f,(xx,25),f);detail=f.crop((96,70,160,130)).resize((192,180),Image.Resampling.NEAREST);board.paste(detail,(xx+32,290),detail)
board.save(P/'prepared-master-comparison.png')
(P/'clean-master-reference.json').write_text(json.dumps({'source':source.name,'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'preparation':'Built-in faithful background/edge cleanup, not pixel-exact original. Compare to original before admission.','opaqueThreshold':200,'originalOpaqueHeight':height,'oneStandingRuler':148,'scale':scale,'wholeImageOffset':list(pos),'nativeOpaqueHeight':148,'nativeOpaqueWidth':int(bx.max()-bx.min()+1),'nativeBootFloor':224,'postGenerationColourChanged':False},indent=2)+'\n')
print(f'Prepared North cutout148px; width{bx.max()-bx.min()+1}; native colour unchanged after generation.')
