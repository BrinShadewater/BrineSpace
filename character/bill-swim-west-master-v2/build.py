"""Package representative original-master swim sources without runtime promotion."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib,copy
P=Path(__file__).resolve().parent;R=P.parent
MASTER=R/'crew-side-masters-v1/bill-side-master-01.png'
DONOR=R/'bill-cargo-helmet-west-v1/sources/canonical-head.png'
source=P/'sources/stroke-extend-v1.png'
inputs=[MASTER,DONOR,source,P/'sources/stroke-extend-prompt-v1.txt',R/'bill-land-water-west-v11/sources/prone-legs-v4.png',R/'bill-land-water-west-v11/bare/frames/land-swim-west/005.png',R/'bill-land-water-west-v11/helmet/frames/land-swim-west/005.png',R/'bill-swim-west-coherent-v1/frames/swim-west/000.png',R/'bill-swim-west-coherent-v1/manifest.json']
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
before={f.relative_to(R).as_posix():sha(f) for f in inputs}
raw=Image.open(source).convert('RGBA');assert raw.size==(1536,1024)
a=np.array(raw);lab,_=label(a[:,:,3]>250);counts=np.bincount(lab.ravel());keep=binary_dilation(lab==np.argmax(counts[1:])+1,iterations=3)&(a[:,:,3]>0);a[~keep]=0
density=148/956
small=Image.fromarray(a).resize((round(raw.width*density),round(raw.height*density)),Image.Resampling.LANCZOS)
c=np.array(small);yy,xx=np.indices(c.shape[:2]);op=c[:,:,3]>180;top=int(yy[op].min());crown=int(np.median(xx[op&(yy<top+5)]));shift=(134-crown,200-top)
bare=Image.new('RGBA',(320,320));bare.alpha_composite(small,shift)
assert np.count_nonzero(np.array(bare)[:,:,3])==np.count_nonzero(c[:,:,3])
b=np.array(bare);yy,xx=np.indices(b.shape[:2]);x,y=134,200
head=Image.open(DONOR).convert('RGBA');assert head.size==(40,40)
position=(x-15,y-4);poly=[(x-17,y-3),(x+18,y-3),(x+19,y+23),(x+8,y+33),(x-17,y+33),(x-18,y+22)]
mask=Image.new('L',bare.size);ImageDraw.Draw(mask).polygon(poly,fill=255);erase=np.array(mask)>0
body=b.copy();body[erase]=0;helmet=Image.fromarray(body);helmet.alpha_composite(head,position);h=np.array(helmet)
foreground=(((yy>=y+27)&(xx>=x+7))|((yy>=y+33)&(xx<=x-5))|((yy>=y+18)&(xx<=x-22)))&(b[:,:,3]>0)
h[foreground]=b[foreground]
area=Image.new('L',bare.size);area.paste(head.getchannel('A'),position);allowed=erase|(np.array(area)>0)
assert np.array_equal(h[~allowed],b[~allowed]) and np.array_equal(h[foreground],b[foreground])
assert np.array_equal(h[yy>=position[1]+40],b[yy>=position[1]+40])
helmet=Image.fromarray(h)
for gear,im in [('bare',bare),('helmet',helmet)]:
    dest=P/gear/'frames/swim-west-extend/000.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest)
    manifest=dict(name='Bill West original-master extended stroke source study',frameWidth=320,frameHeight=320,pivot=[160,224],standingHeight=148,textureFilter='linear',precomposed=True,status='source_study_unselected',states=[dict(id='swim-west-extend',frameFiles=['frames/swim-west-extend/000.png'],frameDurationsMs=[160],loop=False,facings=['west'],waterKinds=['swim'],waterPoses=[True],depthOffsets=[0],provenance='Representative single source pose, not a complete swim loop. Original148/956 drawing density and whole-crown registration; no runtime admission.')])
    if gear=='helmet':manifest['equipment']='diving-helmet'
    (P/gear/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
old=Image.open(R/'bill-swim-west-coherent-v1/frames/swim-west/000.png').convert('RGBA');oldpad=Image.new('RGBA',(320,320));oldpad.alpha_composite(old,(74,136))
orig=Image.open(MASTER).convert('RGBA').crop((850,0,1280,1024));orig=orig.resize((round(orig.width*density),round(orig.height*density)),Image.Resampling.LANCZOS);standing=Image.new('RGBA',(320,320));standing.alpha_composite(orig,(125,round(224-977*density)))
board=Image.new('RGB',(1280,720),'#182932');d=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
    poses=[('Original bare master',standing),('Entry near-prone',Image.open(R/f'bill-land-water-west-v11/{gear}/frames/land-swim-west/005.png').convert('RGBA')),('Old bare extended stroke',oldpad),('New extended stroke',bare if gear=='bare' else helmet)]
    for col,(title,im) in enumerate(poses):
        board.paste(im,(col*320,row*360+25),im);d.text((col*320+4,row*360+4),gear+' /'+title,fill='white');d.line((col*320,row*360+249,col*320+319,row*360+249),fill='#6aa39e')
board.save(P/'master-entry-stroke-review.png')
detail=Image.new('RGB',(800,360),'#182932');d=ImageDraw.Draw(detail)
for i,(name,im) in enumerate([('Bare',bare),('Helmet',helmet)]):
    crop=im.crop((89,190,189,265)).resize((400,300),Image.Resampling.NEAREST);detail.paste(crop,(i*400,30),crop);d.text((i*400+5,5),name+' head/collar /same4x',fill='white')
detail.save(P/'neck-review.png')
after={f.relative_to(R).as_posix():sha(f) for f in inputs};assert before==after
report=dict(scope='Representative extended stroke only, not complete loop or native acceptance.',inputSHA256=before,frozenInputsStable=len(before),wholeSourceDensity=density,translation=shift,crown=[134,200],canvas=[320,320],pivot=[160,224],standingHeight=148,sourceGeneration='exec-79355fb1-095a-4315-afd4-f3073442dde0',canonicalHelmetSize=[40,40],canonicalHelmetScale=1,bodyOutsideHeadExact=True,foregroundExact=True,allPaintedSupportPreserved=True,normalSelected=False,nativeAcceptance=False,visualAcceptance='Pending raw/master/entry/stroke/neck inspection')
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(P/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Bill west swim master repair</title><style>body{background:#182932;color:#eee;font:18px sans-serif;margin:24px}img{max-width:1280px;width:100%;display:block;margin:20px 0}</style><h1>Bill — west extended stroke master study</h1><p>One representative source pose, bare and helmeted. Full stroke family, colour, anatomy and native moving joins remain pending.</p><img src="master-entry-stroke-review.png"><img src="neck-review.png">''',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='inputSHA256'}))
