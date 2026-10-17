from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
from scipy import ndimage
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
inputs=json.loads((p/'inputs.json').read_bytes());grade=json.loads((p/'grade-inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
assert all(hashlib.sha256((p/k).read_bytes()).hexdigest()==v for k,v in grade['preCallSha256'].items())
raw=Image.open(p/'grade-raw.png').convert('RGB');assert raw.size==(1254,1254)
m=json.loads((r/'character/james-cargo-return-bridges-v1/bare-joined-manifest-v9.json').read_bytes());state=m['states'][0]
paths=[r/f[6:] if f.startswith('res://') else r/'character/james-cargo-return-bridges-v1'/f for f in state['frameFiles']]
original=[Image.open(f).convert('RGBA') for f in paths];poses=[original[0]];out=p/'frames';out.mkdir(exist_ok=True)
for j in range(4):
    rgb=np.asarray(raw.crop(((j%2)*627,(j//2)*627,(j%2+1)*627,(j//2+1)*627))).astype(float)
    white=np.min(rgb,axis=2)>=240;seed=np.zeros(white.shape,bool);seed[0,:]=white[0,:];seed[-1,:]=white[-1,:];seed[:,0]=white[:,0];seed[:,-1]=white[:,-1]
    bg=ndimage.binary_propagation(seed,mask=white);fringe=ndimage.binary_dilation(bg,iterations=1)&~bg
    alpha=np.ones(white.shape);alpha[bg]=0;alpha[fringe]=np.clip((255-np.min(rgb[fringe],axis=1))/35,0,1)
    edge=fringe&(alpha>0);rgb[edge]=np.clip((rgb[edge]-255*(1-alpha[edge,None]))/alpha[edge,None],0,255)
    crop=Image.fromarray(np.dstack((rgb,alpha*255)).round().astype('uint8')).resize((80,80),Image.Resampling.LANCZOS)
    im=original[j+1].copy();im.paste(crop.crop((8,8,66,78)),(104,64))
    assert all(im.getpixel((x,y))==original[j+1].getpixel((x,y)) for y in range(256) for x in range(256) if not(104<=x<162 and 64<=y<134))
    im.save(out/('%03d.png'%j));poses.append(im)
poses.append(original[-1]);board=Image.new('RGB',(1920,640),'#303b40');draw=ImageDraw.Draw(board)
for j,im in enumerate(poses):
    draw.text((j*320+8,8),str(j),fill='white');board.paste(im,(j*320+32,30),im)
    crop=im.crop((96,56,176,136)).resize((320,320),Image.Resampling.NEAREST);board.paste(crop,(j*320,290),crop)
board.save(p/'whole-grade-review.png')
comparison=Image.new('RGB',(1920,550),'#303b40');cd=ImageDraw.Draw(comparison)
for j,(old,new) in enumerate(zip(original,poses)):
    cd.text((j*320+8,8),str(j)+' original above / trial below',fill='white')
    comparison.paste(old,(j*320+32,25),old);comparison.paste(new,(j*320+32,280),new)
comparison.save(p/'original-comparison.png')
native=Image.new('RGB',(1200,250),'#303b40')
for j,im in enumerate(poses):
    for h,y in [(82,25),(54,125),(27,195)]:
        small=im.resize((round(256*h/148),)*2,Image.Resampling.LANCZOS);native.paste(small,(j*200+80-small.width//2,y),small)
native.save(p/'station-scale.png')
report={'selected':False,'visualReviewPending':True,'videoFrames':142,'sampleIndices':grade['indices'],'newUpperPoses':4,'protectedPixelsEach':61476,'scale':80/627,'origin':[96,56],'outsideRect':[104,64,162,134],'exactFirstLast':True,'sourceSha256':hashlib.sha256((p/'grade-raw.png').read_bytes()).hexdigest(),'scope':'Source trial only. Four real video phases edited jointly for colour and assembled on originalV9body intermediates. No normal admission or helmet/native acceptance.','alphaRecipe':'Border-connected minRGB>=240 key,one-pixel soft fringe/white unmix before fixed627->80 reduction,no interior recolouring or pose fit.'}
(p/'grade-review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['newUpperPoses','protectedPixelsEach','scale','exactFirstLast']}))
