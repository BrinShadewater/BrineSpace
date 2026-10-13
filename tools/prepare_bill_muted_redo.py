"""Preserve approved south poses; prepare east with the same muted material target."""
from pathlib import Path
import hashlib
import json
import shutil
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'character/bill-south-muted-v1'
E=ROOT/'character/bill-east-direct-v3'
S.mkdir(exist_ok=True);E.mkdir(exist_ok=True)
SATURATION=.90

def mute(rgb):
    # Preserve encoded RGB luma; fixed transform across every pose/direction.
    luma=np.sum(rgb*np.array([.2126,.7152,.0722]),axis=2,keepdims=True)
    return np.clip(np.rint(luma+(rgb-luma)*SATURATION),0,255).astype('uint8')

source=ROOT/'character/bill-south-direct-v2'
source_checks=json.loads((source/'checks.json').read_text())
hashes={};max_luma_delta=0.;images=[]
out=S/'frames/walk-south';out.mkdir(parents=True,exist_ok=True)
for n in range(source_checks['sourceFrames']):
    src=source/f'frames/walk-south/{n:03}.png';a=np.array(Image.open(src).convert('RGBA'));b=a.copy()
    b[:,:,:3]=mute(a[:,:,:3].astype(float))
    b[a[:,:,3]==0]=a[a[:,:,3]==0]
    assert np.array_equal(a[:,:,3],b[:,:,3])
    delta=np.abs(np.sum((b[:,:,:3].astype(float)-a[:,:,:3])*[.2126,.7152,.0722],axis=2))
    max_luma_delta=max(max_luma_delta,float(delta.max()))
    dest=out/f'{n:03}.png';im=Image.fromarray(b);im.save(dest);images.append(im)
    hashes[dest.relative_to(S).as_posix()]=hashlib.sha256(dest.read_bytes()).hexdigest()
sheet=Image.new('RGB',(184*8,210*3),'#303b40');draw=ImageDraw.Draw(sheet)
for j,n in enumerate(np.linspace(0,len(images)-1,24).astype(int)):
    x=j%8*184;y=j//8*210;sheet.paste(images[n],(x,y+20),images[n]);draw.text((x+8,y+3),str(n),fill='white')
sheet.save(S/'contact.png')
checks=source_checks.copy();checks.update(processing='Previous matte south frames with fixed 90% chroma about Rec.709 encoded RGB luma; alpha/poses identical; no second matte pass.',saturation=SATURATION,alphaUnchanged=True,maxEncodedLumaDelta=max_luma_delta,source='bill-south-direct-v2')
checks['neutralMedians']=[]
checks['sourceVideoSha256']=hashlib.sha256((source/'source.mp4').read_bytes()).hexdigest()
checks['sourceFrameHashes']={f'{i:03}':hashlib.sha256((source/f'frames/walk-south/{i:03}.png').read_bytes()).hexdigest() for i in range(source_checks['sourceFrames'])}
for im in images:
    a=np.array(im);rgb=a[:,:,:3].astype(float);v=rgb.mean(2);m=(np.ptp(rgb,axis=2)<24)&(a[:,:,3]>250)&(v>25)&(v<120)
    checks['neutralMedians'].append(np.median(rgb[m],axis=0).tolist())
(S/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(S/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')

def reference(direction):
    return np.array(Image.open(ROOT/f'character/bill-{direction}-direct-v2/master-input.png').convert('RGB')).astype(float)

def foreground(a):
    return ~((a[:,:,1]>a[:,:,0]*1.3)&(a[:,:,1]>a[:,:,2]*1.3)&(a[:,:,1]>90))

def fabric_median(a):
    h,w=a.shape[:2];yy=np.indices((h,w))[0];val=a.mean(2)
    m=foreground(a)&(yy>h*.25)&(yy<h*.85)&(np.ptp(a,axis=2)<32)&(val>30)&(val<150)
    return np.median(a[m],axis=0)

east=reference('east');south=reference('south');gain=fabric_median(south)/fabric_median(east)
h,w=east.shape[:2];yy=np.indices((h,w))[0];val=east.mean(2)
weight=np.clip((32-np.ptp(east,axis=2))/12,0,1)*np.clip((140-val)/35,0,1)*np.clip((yy/h-.22)/.04,0,1)
weight*=foreground(east)
matched=east*(1+weight[:,:,None]*(gain-1))
result=mute(matched);result[~foreground(east)]=east[~foreground(east)].astype('uint8')
Image.fromarray(result).save(E/'master-input.png')
report=dict(saturation=SATURATION,neutralFabricGain=gain.tolist(),source='bill-east-direct-v2/master-input.png',target='bill-south-direct-v2/master-input.png',backgroundUnchanged=True,geometryUnchanged=True,method='One feathered fixed neutral-fabric RGB gain below head, then 90% chroma on foreground. No pose repaint or scaling.')
(E/'reference-treatment.json').write_text(json.dumps(report,indent=2)+'\n')
shutil.copy2(ROOT/'character/bill-east-direct-v2/build.py',E/'build.py')
(E/'prompt.txt').write_text('[Static shot] Side view of the character walking in place facing right. He completes an easy, natural walk cycle with alternating steps and gentle arm movement. His torso stays upright at a constant size and position. Preserve the reference colours, dark matte suit and brown hair. The camera and green background stay fixed.',encoding='utf-8')
print(json.dumps({'southFrames':len(images),'saturation':SATURATION,'maxEncodedLumaDelta':max_luma_delta,'eastFabricGain':gain.tolist()}))
