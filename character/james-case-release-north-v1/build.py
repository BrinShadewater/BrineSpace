"""Independent rear-prone empty release; complete selected North case reused."""
from pathlib import Path
import sys,json,os,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation,distance_transform_edt
P=Path(__file__).resolve().parent
SCALE=.23
HEADS=[[279,124],[768,124],[1270,124],[280,628],[768,629],[1270,628]]
TARGET=np.array([127.81442786069653,109.75945273631841])
a=np.array(Image.open(P/'source.png').convert('RGBA'));labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
ids=sorted(np.argsort(counts)[-6:],key=lambda k:np.where(labs==k)[0].mean()//500*2000+np.where(labs==k)[1].mean());rows=[];tracking=[]
for i,k in enumerate(ids):
    y,x=np.where(labs==k);box=[int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4];v=a[box[1]:box[3],box[0]:box[2]].copy();v[~binary_dilation(labs[box[1]:box[3],box[0]:box[2]]==k,iterations=2)]=0
    raw=Image.fromarray(v);(P/'source-crops').mkdir(exist_ok=True);raw.save(P/'source-crops'/f'{i:03d}.png');small=raw.resize((round(raw.width*SCALE),round(raw.height*SCALE)),Image.Resampling.LANCZOS);at=np.rint(TARGET-(np.array(HEADS[i])-box[:2])*SCALE).astype(int).tolist();out=Image.new('RGBA',(256,276));out.alpha_composite(small,at);rows.append(np.array(out));tracking.append({'sourcePose':i,'box':box,'sourceHead':HEADS[i],'fixedScale':SCALE,'position':at})
ref_path=P.parent/'james-water-cargo-north-v1/frames/bare/swim-pickup/001.png';ref=np.array(Image.open(ref_path).convert('RGBA'));yy,xx=np.indices(ref.shape[:2]);head=((xx-TARGET[0])/14)**2+((yy-TARGET[1])/14)**2<=1
def neutral(v):
    rgb=v[:,:,:3].astype(float);return (v[:,:,3]>180)&(np.ptp(rgb,axis=2)<25)&(rgb[:,:,0]>20)&(rgb[:,:,0]<150)
def gold(v):
    r,g,b=v[:,:,:3].astype(float).transpose(2,0,1);return (v[:,:,3]>180)&(r-b>35)&(g-b>20)&~head
hair=((xx-TARGET[0])/11)**2+((yy-TARGET[1])/8)**2<=1
pool=lambda mask:np.concatenate([v[:,:,:3][mask(v)] for v in rows[:5]])
ng=float(np.median(ref[:,:,:3][neutral(ref)&~head&(yy>=91)])/np.median(pool(lambda v:neutral(v)&~head)))
gg=np.median(ref[:,:,:3][gold(ref)],axis=0)/np.median(pool(gold),axis=0)
hg=np.median(ref[:,:,:3][hair&(ref[:,:,3]>180)],axis=0)/np.median(pool(lambda v:hair&(v[:,:,3]>180)),axis=0)
assert all(np.isfinite(g).all() for g in [ng,gg,hg])
sys.path.insert(0,str(P.parent/'james-water-family-v1'));from extract_sources import extract
w=P.parent/'james-water-north-v1';hr=json.loads((w/'helmet-registration.json').read_text());patch=extract(w/'source-helmet.png',6,6)[4][0];pa=np.array(patch);r,g,b=pa[:,:,:3].astype(float).transpose(2,0,1);gray=(pa[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17);pa[gray,:3]=np.rint(pa[gray,:3]*.9).astype('uint8');patch=Image.fromarray(pa).resize((round(patch.width*hr['fixedHeadScale']),round(patch.height*hr['fixedHeadScale'])),Image.Resampling.LANCZOS);pos=np.rint(TARGET+hr['centerOffset']-[patch.width/2,patch.height/2]).astype(int).tolist();erase=((xx-TARGET[0])/14)**2+((yy-(TARGET[1]-1))/14)**2<=1
for i,v in enumerate(rows):
    rgb=v[:,:,:3].astype(float);rgb[(v[:,:,3]>0)&~head&~gold(v)]*=ng;rgb[gold(v)]*=gg;rgb[hair&(v[:,:,3]>0)]*=hg;v[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');bare=Image.fromarray(v);ha=v.copy();ha[erase]=0;helmet=Image.fromarray(ha);helmet.alpha_composite(patch,pos);hv=np.array(helmet)
    foreground=(yy<TARGET[1]-12)&(v[:,:,3]>0);hv[foreground]=v[foreground];helmet=Image.fromarray(hv)
    for gear,image in [('bare',bare),('helmet',helmet)]:
        folder=P/'frames'/gear;folder.mkdir(parents=True,exist_ok=True);image.save(folder/f'{i:03d}.png')
    allowed=erase.copy();allowed[pos[1]:pos[1]+patch.height,pos[0]:pos[0]+patch.width]=True;assert np.array_equal(v[~allowed],hv[~allowed]);tracking[i].update(bodyBounds=bare.getbbox(),foreground='original gloves above cranial ownership')
rl,rn=label(ref[:,:,3]>180);ci=int(rl[75,128]);bi=int(rl[145,128]);assert ci and bi and ci!=bi
dc=distance_transform_edt(rl!=ci);db=distance_transform_edt(rl!=bi);owned=(dc<=3)&(dc<db);cv=ref.copy();cv[~owned]=0;box=Image.fromarray(cv).getbbox();case=Image.fromarray(cv).crop(box);case.save(P/'case.png');case_at=list(box[:2])
reg={'status':'selected_runtime_north_empty_case_release','sourceSha256':hashlib.sha256((P/'source.png').read_bytes()).hexdigest(),'generatedOriginal':'C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-f0d6dbdb-4887-45c0-b469-630c33ca6665.png','prompt':'tool-prompt-v2.txt','fixedScale':SCALE,'headTarget':TARGET.tolist(),'tracking':tracking,'neutralGain':ng,'goldGain':gg.tolist(),'hairGain':hg.tolist(),'helmetPosition':pos,'helmetPatchSize':list(patch.size),'casePosition':case_at,'caseSize':list(case.size),'caseProvenance':{'source':str(ref_path.relative_to(P.parent)),'sha256':hashlib.sha256(ref_path.read_bytes()).hexdigest(),'nativeScale':1.0,'crop':list(box),'opaqueCoreSize':[41,22],'opaqueCoreCount':860,'ownership':'selected complete case plus3pxnearest-owned fringe, excludes gloves'},'scope':'North independent complete rear-prone bodies, fixed.23ruler and pooled matte grade, canonical rear shell and true glove foreground. Exact complete selected case at native scale1. Pose5 is source study only; runtime uses1release/0,2,3,4empty interiors and exact selected swim0.'}
(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n')
for gear in ['bare','helmet']:
    cargo=P.parent/'james-water-cargo-north-v1';cm=json.loads((cargo/f'{gear}-manifest.json').read_text());source=next(s for s in cm['states'] if s['id']=='swim-pickup-north');states=[]
    end=w/('frames/swim/000.png' if gear=='bare' else 'frames/helmet/swim/000.png')
    for index in range(1,6):
        files=[cargo/source['frameFiles'][i] for i in range(index,0,-1)]+[P/f'frames/{gear}/{i:03d}.png' for i in [1,0,2,3,4]]+[end];durations=[50]*index+[80,60,80,80,70,60]
        states.append({'id':f'swim-cancel-release-pickup-{index}-north','frameFiles':[Path(os.path.relpath(f,P)).as_posix() for f in files],'frameDurationsMs':durations,'loop':False,'waterPoses':[True]*len(files),'waterKinds':['swim']*len(files),'facings':['north']*len(files),'depthOffsets':[0.0]*len(files),'caseReleaseMs':50*index,'provenance':{'entrance':'exact selected pickup'+str(index),'interiors':'complete newly authored empty-handed North bodies1,0,2,3,4; no work torch stow','endpoint':'exact selected empty swim0'}})
    manifest={'name':'James North indexed empty case release '+gear,'frameWidth':256,'frameHeight':276,'pivot':[128,128],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':reg['status'],'states':states};(P/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
contact=Image.new('RGB',(7*220,450),'#303b40');draw=ImageDraw.Draw(contact);review=[]
for slot in range(7):
    frame=Image.new('RGB',(850,520),'#303b40');d=ImageDraw.Draw(frame);d.text((12,8),'James North empty case release / staged / native148 +82 ruler',fill='white')
    for row,gear in enumerate(['bare','helmet']):
        m=json.loads((P/f'{gear}-manifest.json').read_text());im=Image.open(P/m['states'][0]['frameFiles'][slot]).convert('RGBA');layer=im.copy()
        if slot:layer.alpha_composite(case,tuple(case_at))
        crop=layer.crop((80,55,175,210));contact.paste(crop,(slot*220+25,row*220+35),crop);draw.text((slot*220+12,row*220+12),gear+' '+str(slot),fill='white');frame.paste(layer,(30,row*230+20),layer)
        small=layer.resize((round(256*82/148),round(276*82/148)),Image.Resampling.LANCZOS);frame.paste(small,(430,row*230+45),small)
    review.append(frame)
contact.save(P/'join-contact.png');review[0].save(P/'review.gif',save_all=True,append_images=review[1:],duration=[400,80,60,80,80,70,600],loop=0,disposal=2)
print(json.dumps({'poses':len(rows),'scale':SCALE,'caseSize':case.size,'casePosition':case_at,'pooledNeutralGain':ng,'helmetPosition':pos}))
