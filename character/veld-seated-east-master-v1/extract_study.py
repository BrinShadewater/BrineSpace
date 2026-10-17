"""Whole-source extraction for a competing raw study; not runtime selection."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
rawpath=P/'raw-v1.png';raw=np.array(Image.open(rawpath).convert('RGBA'))
labs,_=label(raw[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
parts=sorted(np.argsort(sizes)[-6:],key=lambda k:(np.where(labs==k)[0].mean()//512,np.where(labs==k)[1].mean()//512))
assert min(sizes[parts])>25000
y,x=np.where(labs==parts[0]);height=int(y.max()-y.min()+1);scale=148/height
records=[];frames=[]
for index,k in enumerate(parts):
    y,x=np.where(labs==k);box=[max(0,int(x.min())-3),max(0,int(y.min())-3),min(1536,int(x.max())+4),min(1024,int(y.max())+4)]
    floor=int(y.max());fx=float(x[y>=floor-7].mean())
    mask=binary_dilation(labs==k,iterations=3);a=raw.copy();a[~mask]=0
    size=[round((box[2]-box[0])*scale),round((box[3]-box[1])*scale)]
    position=[round(128-(fx-box[0])*scale),round(223-(floor-box[1])*scale)]
    crop=Image.fromarray(a).crop(box).resize(size,Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(256,256));out.alpha_composite(crop,position)
    path=P/f'study-frames/{index:03}.png';path.parent.mkdir(exist_ok=True);out.save(path);frames.append(out)
    records.append({'pose':index,'rawBox':box,'size':size,'position':position,'floor':floor,'footX':fx,'componentPixels':int(sizes[k]),'sourceHeight':int(y.max()-y.min()+1)})
board=Image.new('RGB',(1792,820),'#202a30');draw=ImageDraw.Draw(board)
master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png'),(36,52))
for row in range(3):board.paste(master,(0,row*272+16),master);draw.text((5,row*272+3),'Selected master',fill='white')
for i in range(6):
    old=Image.open(R/f'character/dr-veld-v2/frames/bare/sit-down-east/{i:03}.png').convert('RGBA')
    previous=Image.open(R/f'character/veld-seated-east-coherent-v1/frames/bare/sit-down-east/{i:03}.png').convert('RGBA')
    for row,(im,title) in enumerate([(old,'Current selected'),(previous,'Earlier staged'),(frames[i],'New ungraded study')]):
        board.paste(im,((i+1)*256,row*272+16),im);draw.text(((i+1)*256+4,row*272+3),title+' '+str(i),fill='white')
board.save(P/'competing-source-review.png')
(P/'study-registration.json').write_text(json.dumps({'fixedRuler':scale,'standingOpaqueHeight':height,'sourceSha256':hashlib.sha256(rawpath.read_bytes()).hexdigest(),'poses':records,'scope':'Ungraded raw study, connected alpha>180 body components plus3pixel edge; background haze excluded. Single ruler from standing source. Source0 is generated comparison only; canonical entrance will be original master. Competing against existing staged East candidate; no normal/manifests/controller admission.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'studyPoses':6,'fixedRuler':scale,'heights':[r['sourceHeight'] for r in records],'normalSelection':False}))
