"""Fixed-ruler sofa source extraction, pooled master grade and native helmet fit."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
HEADS=[(306,122),(765,184),(1238,223),(255,680),(637,756),(1090,875)]
NECKS=[(306,174),(765,235),(1238,271),(279,724),(677,791),(1146,882)]
CONTACTS=[(306,550),(767,547),(1239,546),(351,969),(805,922),(1350,951)]
DURATIONS=[180,180,200,220,240,500]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def regions(a,head):
    v=a[:,:,:3].astype(float);solid=a[:,:,3]>200;luma=v.mean(2)
    warm=(v[:,:,0]>v[:,:,1]*1.12)&(v[:,:,1]>v[:,:,2]*1.20)
    skin=solid&head&warm&(luma>=80)
    hair=solid&head&~skin&((warm&(luma<80))|(luma>115))
    blue=solid&~head&(v[:,:,2]>v[:,:,0]*1.30)&(v[:,:,2]>v[:,:,1]*1.10)
    return {'skin':skin,'hair':hair,'science':blue,'neutral':solid&~head&~blue&(np.ptp(v,axis=2)<45)}
rawpath=P/'sources/fall-v1.png';raw=np.array(Image.open(rawpath).convert('RGBA'))
labs,n=label(raw[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
ids=sorted(np.argsort(sizes)[-6:],key=lambda k:(np.where(labs==k)[0].mean()//512,np.where(labs==k)[1].mean()))
assert len(ids)==6 and min(sizes[ids])>40000
y,x=np.where(labs==ids[0]);height=int(y.max()-y.min()+1);assert height==474
scale=148/height
masterpath=R/'character/crew-runtime-matte-v1/veld/frames/idle-south-breathing-v1/000.png'
master=Image.new('RGBA',(256,272));master.alpha_composite(Image.open(masterpath).convert('RGBA'),(36,52));ref=np.array(master)
yy,xx=np.indices(raw.shape[:2]);head=np.zeros(raw.shape[:2],bool)
for hx,hy in HEADS:head|=((xx-hx)/49)**2+((yy-hy)/49)**2<1
ry,rx=np.indices(ref.shape[:2]);rh=(rx>=117)&(rx<144)&(ry>=76)&(ry<104)
sm=regions(raw,head);rm=regions(ref,rh);graded=raw.copy();curves={};quantiles=[0,15,35,55,75,90,100]
for material,mask in sm.items():
    assert mask.sum()>30 and rm[material].sum()>5
    intensity=raw[:,:,:3][mask].mean(1);knots=np.percentile(intensity,quantiles);target=np.percentile(ref[:,:,:3][rm[material]],quantiles,axis=0)
    for c in range(3):graded[mask,c]=np.interp(intensity,knots,target[:,c]).clip(0,255).astype('uint8')
    curves[material]={'knots':knots.tolist(),'targets':target.tolist(),'sourcePixels':int(mask.sum()),'masterPixels':int(rm[material].sum())}
frames={};records=[];bindings={rawpath.relative_to(R).as_posix():sha(rawpath),masterpath.relative_to(R).as_posix():sha(masterpath)}
checks=0
def pad(image):
    canvas=Image.new('RGBA',(256,272));canvas.alpha_composite(image);return canvas
for gear in ['bare','helmet']:
    entry=R/f'character/veld-read-seated-south-coherent-v1/frames/{gear}/read-seated-south/003.png'
    bindings[entry.relative_to(R).as_posix()]=sha(entry);frames[gear]=[pad(Image.open(entry).convert('RGBA'))]
    for i in [2,3,4]:
        k=ids[i];y,x=np.where(labs==k);box=[int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4]
        keep=binary_dilation(labs==k,iterations=3)&(raw[:,:,3]>0)
        pixels=graded.copy();pixels[~keep]=0
        size=[round((box[2]-box[0])*scale),round((box[3]-box[1])*scale)]
        cut=Image.fromarray(pixels).crop(box).resize(size,Image.Resampling.LANCZOS)
        position=[round(128-(CONTACTS[i][0]-box[0])*scale),round(223-(CONTACTS[i][1]-box[1])*scale)]
        out=Image.new('RGBA',(256,272));out.alpha_composite(cut,position)
        center=[position[j]+(HEADS[i][j]-box[j])*scale for j in range(2)]
        neck=[position[j]+(NECKS[i][j]-box[j])*scale for j in range(2)]
        fit=None
        if gear=='helmet':
            componentpath=R/'character/veld-death-ground-south-coherent-v1/sources/fitted-pitch-02.png'
            bindings[componentpath.relative_to(R).as_posix()]=sha(componentpath)
            component=Image.open(componentpath).convert('RGBA');angle={2:0,3:25,4:50}[i];anchor=[18,35]
            b=np.array(out);cy,cx=np.indices(b.shape[:2]);local=((cx-center[0])/18)**2+((cy-center[1])/18)**2<1
            v=b[:,:,:3].astype(float);warm=(v[:,:,0]>v[:,:,1]*1.12)&(v[:,:,1]>v[:,:,2]*1.14)
            erase=local&(warm|((cy<neck[1]-5)&(b[:,:,3]>0)))
            rotated=component.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
            rad=math.radians(angle);dx=anchor[0]-component.width/2;dy=anchor[1]-component.height/2
            ra=[rotated.width/2+math.cos(rad)*dx+math.sin(rad)*dy,rotated.height/2-math.sin(rad)*dx+math.cos(rad)*dy]
            pos=[round(neck[j]-ra[j]) for j in range(2)]
            protected=erase.copy();protected[pos[1]:pos[1]+rotated.height,pos[0]:pos[0]+rotated.width]=True
            original=b.copy();b[erase]=0;out=Image.fromarray(b);out.alpha_composite(rotated,pos)
            assert np.array_equal(np.array(out)[~protected],original[~protected]);checks+=1
            fit={'component':componentpath.relative_to(R).as_posix(),'nativeScale':1,'forwardPitchDegrees':25,'screenTiltCCW':angle,'position':pos,'size':list(rotated.size),'eraseRadius':18}
        a=np.array(out);a[a[:,:,3]<8]=0;out=Image.fromarray(a);frames[gear].append(out)
        records.append({'gear':gear,'sourcePose':i,'box':box,'size':size,'position':position,'sourceContact':CONTACTS[i],'headCenter':center,'neck':neck,'helmet':fit})
    for index in [4,5]:
        terminal=R/f'character/veld-death-ground-south-coherent-v1/frames/{gear}/death-ground-south/{index:03}.png'
        bindings[terminal.relative_to(R).as_posix()]=sha(terminal);frames[gear].append(pad(Image.open(terminal).convert('RGBA')))
    files=[]
    for index,frame in enumerate(frames[gear]):
        file=P/f'frames/{gear}/death-sofa-read-south/{index:03}.png';file.parent.mkdir(parents=True,exist_ok=True);frame.save(file);files.append('res://'+file.relative_to(R).as_posix())
        box=frame.getbbox();assert box[0]>0 and box[1]>0 and box[2]<256 and box[3]<272;checks+=1
    assert frames[gear][0].crop((0,0,256,256)).tobytes()==Image.open(entry).convert('RGBA').tobytes();checks+=1
    state={'id':'death-sofa-read-south','frameFiles':files,'frameDurationsMs':DURATIONS,'loop':False,'terminalFrame':5,'facings':['south']*6,'depthOffsets':[0]*6}
    manifest={'name':'Veld South sofa reading supported floor fall '+gear,'equipment':'diving-helmet' if gear=='helmet' else '', 'frameWidth':256,'frameHeight':272,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'staged_candidate','sofaFallDeathMode':'reader-south-v1','states':[state]}
    (P/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(P/'material-grade.json').write_text(json.dumps(curves,indent=2)+'\n',encoding='utf-8')
(P/'registration.json').write_text(json.dumps({'sourceHeight':height,'fixedRuler':scale,'nativeStandingHeight':148,'pivot':[128,224],'poses':records,'bindings':bindings,'checks':checks,'alphaPolicy':'opaque>180 body component, dilate3 source pixels, drop alpha<8 after fixed resampling; backdrop excluded','scope':'authored staged South reader-supported fall. No normal loader/controller/world acceptance yet'},indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1536,880),'#202a30');d=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
    for index,frame in enumerate(frames[gear]):board.paste(frame,(index*256,row*292+20),frame);d.text((index*256+5,row*292+3),gear+' sofa fall '+str(index),fill='white')
for index in range(6):board.paste(master,(index*256,604),master);d.text((index*256+5,588),'Standing master / H148',fill='white')
board.save(P/'paired-source-review.png')
print(json.dumps({'checks':checks,'failures':0,'pairedFrames':12,'fixedRuler':scale,'normalSelection':False}))
