"""Fixed-ruler source fitting; camera/material authority is selected east idle."""
from pathlib import Path
import math,json,hashlib,copy
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
SOURCE=P/'sources/death-v1.png'
IDLE=R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png'
HELM=R/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png'
HEADS=[[248,127],[824,185],[1377,303],[401,775],[935,852],[1456,859]]
CONTACT_X=[270,760,1340,155,610,1130]
TARGET_X=[143,143,143,112,90,90]
NECKS=[[244,166],[789,218],[1330,333],[367,805],[886,872],[1408,878]]
ANGLES=[0,18,37,50,80,85]
DURATIONS=[180,160,180,180,220,500]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ground(path):
    out=Image.new('RGBA',(256,256));out.alpha_composite(Image.open(path).convert('RGBA'),(36,52));return out
def regions(a,head):
    v=a[:,:,:3].astype(float);solid=a[:,:,3]>200;warm=(v[:,:,0]>1.12*v[:,:,1])&(v[:,:,1]>1.20*v[:,:,2]);luma=v.mean(2)
    blue=solid&(v[:,:,2]>1.30*v[:,:,0])&(v[:,:,2]>1.10*v[:,:,1])
    return {'face':solid&head&warm&(luma>=80),'hair':solid&head&warm&(luma<80),'science':blue,'neutral':solid&~head&~blue&(np.ptp(v,axis=2)<45)}
def main():
    raw=np.array(Image.open(SOURCE).convert('RGBA'));lab,n=label(raw[:,:,3]>180);sizes=np.bincount(lab.ravel());sizes[0]=0
    ids=sorted(np.argsort(sizes)[-6:],key=lambda k:(np.where(lab==k)[0].mean()//512,np.where(lab==k)[1].mean()))
    assert len(ids)==6 and min(sizes[ids])>35000
    y0,x0=np.where(lab==ids[0]);scale=148/(int(y0.max()-y0.min())+1)
    assert .29<scale<.31
    yy,xx=np.indices(raw.shape[:2]);head=np.zeros(raw.shape[:2],bool)
    for hx,hy in HEADS:head|=(xx-hx)**2+(yy-hy)**2<62**2
    ref=np.array(ground(IDLE));ry,rx=np.indices(ref.shape[:2]);rh=(rx>=117)&(rx<155)&(ry>=76)&(ry<105)
    src_masks=regions(raw,head);ref_masks=regions(ref,rh);graded=raw.copy();curves={};q=[0,15,35,55,75,90,100]
    for name,mask in src_masks.items():
        authority=ref_masks[name];assert mask.sum()>30 and authority.sum()>5,(name,int(mask.sum()),int(authority.sum()))
        src=raw[:,:,:3][mask].mean(1);knots=np.percentile(src,q);targets=np.percentile(ref[:,:,:3][authority],q,axis=0)
        for channel in range(3):graded[mask,channel]=np.interp(src,knots,targets[:,channel]).clip(0,255).astype('uint8')
        curves[name]={'knots':knots.tolist(),'targets':targets.tolist(),'sourcePixels':int(mask.sum()),'masterPixels':int(authority.sum())}
    bare=[ground(IDLE)];helmet=[ground(HELM)];records=[]
    native=Image.open(HELM).convert('RGBA').crop((82,17,117,56));native.save(P/'sources/canonical-head.png');anchor=[19,36]
    for i in range(1,6):
        y,x=np.where(lab==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
        keep=binary_dilation(lab==ids[i],iterations=3)&(raw[:,:,3]>0);a=graded.copy();a[~keep]=0
        cut=Image.fromarray(a).crop(box);cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS)
        contact=[CONTACT_X[i],int(y.max())];target=[TARGET_X[i],223];pos=[round(target[j]-(contact[j]-box[j])*scale) for j in range(2)]
        out=Image.new('RGBA',(256,256));out.alpha_composite(cut,pos);bare.append(out)
        neck=[pos[j]+(NECKS[i][j]-box[j])*scale for j in range(2)];center=[pos[j]+(HEADS[i][j]-box[j])*scale for j in range(2)]
        angle=ANGLES[i];rad=math.radians(angle);rot=native.rotate(-angle,resample=Image.Resampling.BICUBIC,expand=True)
        dx,dy=anchor[0]-native.width/2,anchor[1]-native.height/2
        ra=[rot.width/2+math.cos(rad)*dx-math.sin(rad)*dy,rot.height/2+math.sin(rad)*dx+math.cos(rad)*dy];hp=[round(neck[j]-ra[j]) for j in range(2)]
        b=np.array(out);v=b[:,:,:3].astype(float);cy,cx=np.indices(b.shape[:2]);local=(cx-center[0])**2+(cy-center[1])**2<20**2
        warm=(v[:,:,0]>1.12*v[:,:,1])&(v[:,:,1]>1.14*v[:,:,2]);b[local&warm]=0
        fitted=Image.fromarray(b);fitted.alpha_composite(rot,hp);helmet.append(fitted)
        records.append({'pose':i,'box':box,'size':list(cut.size),'position':pos,'sourceContact':contact,'targetContact':target,'neck':neck,'headCenter':center,'helmetPosition':hp,'tiltDegrees':angle,'nativeScale':1,'eraseRadius':20})
    hashes={}
    for gear,frames in [('bare',bare),('helmet',helmet)]:
        files=[]
        for i,im in enumerate(frames):
            f=P/f'frames/{gear}/death-ground-east/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);files.append(f.relative_to(P).as_posix());hashes[files[-1]]=sha(f)
        state={'id':'death-ground-east','frameFiles':files,'frameDurationsMs':DURATIONS,'loop':False,'terminalFrame':5,'facings':['east']*6,'waterPoses':[False]*6,'waterKinds':['death-ground']*6,'depthOffsets':[0]*6}
        m={'name':f'Veld east dry collapse {gear} candidate','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'staged_candidate','states':[state]}
        if gear=='helmet':m['equipment']='diving-helmet'
        (P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
    data={'generation':'exec-341162b9-d481-49a5-bb1f-c39735c3245c','fixedRuler':scale,'heads':HEADS,'necks':NECKS,'sourceSha256':sha(SOURCE),'bareIdle':IDLE.relative_to(R).as_posix(),'bareIdleSha256':sha(IDLE),'helmetIdle':HELM.relative_to(R).as_posix(),'helmetIdleSha256':sha(HELM),'frames':records,'scope':'source fit and canonical native head; expression/contact/pacing/full-family polish remain; no normal selection'}
    for name,d in [('registration.json',data),('material-grade.json',curves),('frame-hashes.json',hashes)]:(P/name).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    board=Image.new('RGB',(1536,768),'#202a30')
    for row,frames in enumerate([bare,helmet,[bare[0]]*6]):
        for i,im in enumerate(frames):board.paste(im,(i*256,row*256),im)
    board.save(P/'contact-sheet.png')
    for gear,frames in [('bare',bare),('helmet',helmet)]:
        gif=[Image.new('RGB',(256,256),'#202a30') for _ in frames]
        for out,im in zip(gif,frames):out.paste(im,(0,0),im)
        gif[0].save(P/f'{gear}-death.gif',save_all=True,append_images=gif[1:],duration=DURATIONS,loop=0,disposal=2)
    print(json.dumps({'frames':12,'fixedRuler':scale,'sourceStandingHeight':int(y0.max()-y0.min())+1}))
if __name__=='__main__':main()
