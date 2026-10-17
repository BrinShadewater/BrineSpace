from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parents[2];src=Image.open(P/'source.png').convert('RGBA');a=np.array(src);mask=a[:,:,3]>8;lab,n=label(mask);counts=np.bincount(lab.ravel());keep=counts>=20;keep[0]=False;a[~keep[lab]]=0
opaque=a[:,:,3]>128;yy,xx=np.where(opaque);scale=148/(yy.max()-yy.min()+1);floor=int(yy.max())
# One fixed authored-key calibration and whole-body registration, not per-frame clip correction.
scaled=Image.fromarray(a).resize((round(src.width*scale),round(src.height*scale)),Image.Resampling.LANCZOS);offset=(4,224-round((floor+1)*scale));im=Image.new('RGBA',(256,256));im.alpha_composite(scaled,offset);im.save(P/'native.png')
master=Image.open(P.parent/'west-sample-family-v3/master-native.png').convert('RGBA');old=Image.open(R/'character/veld-unload-west-consistent-v1/frames/bare/000.png').convert('RGBA')
board=Image.new('RGB',(768,620),'#202a30');d=ImageDraw.Draw(board)
for i,(name,img) in enumerate([('Original standing',master),('Installed cargo hold',old),('New cargo key trial',im)]):
 board.paste(img,(i*256,30),img);d.text((i*256+5,5),name,fill='white');d.line((i*256,254,i*256+255,254),fill='#466570');crop=img.crop((90,60,170,150)).resize((160,180),Image.Resampling.NEAREST);board.paste(crop,(i*256+40,320),crop)
board.save(P/'comparison.png')
metrics={}
for name,img in [('master',master),('candidate',im)]:
 aa=np.array(img);mask=aa[:,:,3]>128;y,x=np.where(mask);head=mask.copy();head[100:]=False;hy,hx=np.where(head)
 metrics[name]={'opaqueHeight':int(y.max()-y.min()+1),'floor':int(y.max()),'headTop':int(hy.min()),'headWidthAboveY100':int(hx.max()-hx.min()+1),'headLeft':int(hx.min())}
(P/'BUILD_REVIEW.json').write_text(json.dumps({'sourceSha256':hashlib.sha256((P/'source.png').read_bytes()).hexdigest(),'sourceSize':src.size,'uniformScale':scale,'wholeKeyOffset':offset,'alphaThreshold':8,'componentMinPixels':20,'calibration':'148px opaque standing height at one fixed whole-key scale; floor224 boundary. No per-part/RGB edits. Not a motion source.','metrics':metrics},indent=2)+'\n');print(metrics)
