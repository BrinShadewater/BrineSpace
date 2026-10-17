"""Registered south-facing Salvage pilot using generated source pixels."""
from pathlib import Path
import hashlib, json, math
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageChops

R=Path(__file__).resolve().parent
SIZE=512; FPS=30
def save(im,path):
    path.parent.mkdir(parents=True,exist_ok=True);im.save(path,compress_level=3)
    return path.relative_to(R).as_posix()
def clean(path):
    a=np.array(Image.open(path).convert('RGBA'));labels,_=ndimage.label(a[:,:,3]>128)
    counts=np.bincount(labels.ravel());counts[0]=0
    keep=ndimage.binary_dilation(labels==counts.argmax(),iterations=2)
    a[:,:,3]=np.where(keep,a[:,:,3],0)
    return Image.fromarray(a)
raw=clean(R/'sources/south-v1.png');bounds=raw.getbbox()
scale=354/(bounds[2]-bounds[0]);offset=np.rint(np.array([256,246])-np.array([627,650])*scale).astype(int)
def point(p):return tuple(np.array(p)*scale+offset)
base=Image.new('RGBA',(SIZE,SIZE));small=raw.convert('RGBa').resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS).convert('RGBA');base.alpha_composite(small,tuple(offset))
save(base,R/'poses/south.png')
jaws=[];fixed=base.copy()
for polygon,pivot,sign in [([(550,930),(607,930),(619,1000),(614,1165),(493,1165),(493,1007)],(574,960),1), ([(647,930),(704,930),(758,1007),(758,1165),(638,1165),(634,1000)],(678,960),-1)]:
    mask=Image.new('L',(SIZE,SIZE));ImageDraw.Draw(mask).polygon([point(p) for p in polygon],fill=255)
    part=base.copy();part.putalpha(ImageChops.multiply(base.getchannel('A'),mask));jaws.append((part,point(pivot),sign))
    fixed.putalpha(ImageChops.multiply(fixed.getchannel('A'),ImageChops.invert(mask)))
fans=[]
for cx,cy,rx,ry in [(181,607,54,38),(1070,607,54,38),(357,776,21,13),(895,776,21,13)]:
    x,y=point((cx,cy));rx*=scale;ry*=scale
    box=(round(x-rx),round(y-ry),round(x+rx+1),round(y+ry+1));patch=base.crop(box)
    mask=Image.new('L',patch.size);ImageDraw.Draw(mask).ellipse((1,1,patch.width-2,patch.height-2),fill=255)
    fans.append((box,patch,mask))
scrap=clean(R/'sources/scrap-v1.png');scrap=scrap.crop(scrap.getbbox());scrap=scrap.resize((34,round(scrap.height*34/scrap.width)),Image.Resampling.LANCZOS);save(scrap,R/'layers/scrap.png')
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def render(n,state):
    close=0
    if state=='retrieve':close=smooth((n-30)/44)
    if state in ['carry','release']:close=1 if state=='carry' else 1-smooth(n/44)
    out=fixed.copy()
    for part,pivot,sign in jaws:
        out.alpha_composite(part.rotate(sign*16*close,resample=Image.Resampling.BICUBIC,center=pivot))
    silhouette=out.getchannel('A')
    for box,patch,mask in fans:
        angle=n*(24 if state in ['swim','carry'] else 6)
        normalized=patch.resize((64,64),Image.Resampling.BICUBIC)
        rotor=normalized.rotate(angle,resample=Image.Resampling.BICUBIC).resize(patch.size,Image.Resampling.LANCZOS)
        out.paste(Image.composite(rotor,patch,mask),box[:2])
    out.putalpha(silhouette)
    cargo=Image.new('RGBA',(SIZE,SIZE))
    if state in ['retrieve','carry','release']:
        # The target starts between open jaws; contact closes around it, then holds.
        px,py=point((627,1093))
        if state=='release':py+=26*smooth((n-44)/45)
        cargo.alpha_composite(scrap,(round(px-scrap.width/2),round(py-scrap.height/2)))
    return out,cargo
states=[];checks=[]
for state,count in [('idle',60),('swim',60),('retrieve',120),('carry',60),('release',120)]:
    atlas=Image.new('RGBA',(SIZE*6,SIZE*math.ceil(count/6)));ca=Image.new('RGBA',atlas.size);paths=[];cp=[];phases=[]
    for n in range(count):
        body,cargo=render(n,state);box=body.getbbox();assert box and min(box[:2])>0 and max(box[2:])<SIZE
        paths.append(save(body,R/'frames'/state/f'{n:03}.png'));cp.append(save(cargo,R/'cargo'/state/f'{n:03}.png'))
        atlas.paste(body,(n%6*SIZE,n//6*SIZE));ca.paste(cargo,(n%6*SIZE,n//6*SIZE))
        phases.append('Approach / align' if state=='retrieve' and n<30 else 'Grip' if state=='retrieve' and n<75 else 'Hold recovered scrap' if state in ['retrieve','carry'] else 'Open claw' if state=='release' and n<45 else 'Release' if state=='release' else state)
    states.append({'id':state+'-south','state':state,'heading':'south','frameCount':count,'fps':FPS,'loop':state in ['idle','swim','carry'],'holdFrame':count-1,'frameFiles':paths,'cargoFiles':cp,'phases':phases,'atlas':{'path':save(atlas,R/'atlases'/f'{state}.png'),'columns':6},'cargoAtlas':{'path':save(ca,R/'atlases'/f'{state}-cargo.png'),'columns':6}})
    checks.append({'state':state,'frames':count,'clipping':'pass'});print(state,'complete',flush=True)
manifest={'id':'salvage-drone-v1-pilot','frameWidth':SIZE,'frameHeight':SIZE,'pivot':[256,246],'fps':FPS,'worldUnitsPerPixel':.34,'nominalWidthWorld':120.36,'headings':{'south':{'pose':'poses/south.png','lamp':list(point((627,285))),'sourceScale':scale,'sourceOffset':offset.tolist()}},'states':states,'lamp':{'periodSeconds':.85,'colors':{'operational':'#69b9ed','stopped':'#ef6464','charging':'#efcb62'}},'scope':'South-facing motion pilot only. No other headings or Godot gameplay integration. Native footprint is a review proposal.','sourceFiles':[{'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (R/'sources').glob('*.png')]}
(R/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(R/'review/build-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
board=Image.new('RGBA',(1050,520),'#17272e');draw=ImageDraw.Draw(board)
for i,(label,path) in enumerate([('Construction',R.parent/'drone-motion-v2-2026-09-26/polish/poses/south.png'),('Mining',R.parent/'mining-rover-v1-2026-09-26/poses/south.png'),('Salvage pilot',R/'poses/south.png')]):
    im=Image.open(path).convert('RGBA');im=im.resize((round(im.width*.34),round(im.height*.34)),Image.Resampling.LANCZOS);x=175+i*350
    board.alpha_composite(im,(x-im.width//2,160-im.height//2));draw.text((x-60,270),label+' / 0.34x',fill='white')
    draw.rectangle((i*350,320,i*350+349,519),fill='#c2c5bd');board.alpha_composite(im,(x-im.width//2,420-im.height//2))
save(board,R/'review/fleet-scale.png')
contact=Image.new('RGBA',(SIZE*3,SIZE*2),'#17272e');dr=ImageDraw.Draw(contact)
for i,(state,n) in enumerate([('idle',0),('swim',15),('retrieve',30),('retrieve',74),('carry',0),('release',119)]):
    body,cargo=render(n,state);x=i%3*SIZE;y=i//3*SIZE;contact.alpha_composite(cargo,(x,y));contact.alpha_composite(body,(x,y));dr.text((x+10,y+10),f'{state} / {n}',fill='white')
save(contact,R/'review/pilot-contact.png')
print('PILOT: five south-facing clips, 420 frames; no directional expansion',flush=True)
