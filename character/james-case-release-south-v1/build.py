"""Deterministic South source extraction/registration; no anatomy edits."""
from pathlib import Path
import json, os, sys, hashlib
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation
P=Path(__file__).resolve().parent
SCALE=.25
HEADS=[[282,270],[770,270],[1260,278],[280,774],[770,775]]
CORRECTED_HEADS={0:[282,270],3:[280,781],4:[770,785]}
TARGET=np.array([128.1706284400895,142.98699570555857])
a=np.array(Image.open(P/'source.png').convert('RGBA'))
labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
ids=sorted(np.argsort(counts)[-6:],key=lambda k:np.where(labs==k)[0].mean()//500*2000+np.where(labs==k)[1].mean())
ca=np.array(Image.open(P/'source-v2.png').convert('RGBA'));cl,cn=label(ca[:,:,3]>180);cc=np.bincount(cl.ravel());cc[0]=0
cids=sorted(np.argsort(cc)[-6:],key=lambda k:np.where(cl==k)[0].mean()//500*2000+np.where(cl==k)[1].mean())
rows=[];tracking=[]
for i,k in enumerate(ids):
    pixels,labels,component,point=(ca,cl,cids[i],CORRECTED_HEADS[i]) if i in CORRECTED_HEADS else (a,labs,k,HEADS[i] if i<5 else None)
    y,x=np.where(labels==component);box=[int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4]
    v=pixels[box[1]:box[3],box[0]:box[2]].copy()
    v[~binary_dilation(labels[box[1]:box[3],box[0]:box[2]]==component,iterations=2)]=0
    raw=Image.fromarray(v);(P/'source-crops').mkdir(exist_ok=True);raw.save(P/'source-crops'/f'{i:03d}.png')
    small=raw.resize((round(raw.width*SCALE),round(raw.height*SCALE)),Image.Resampling.LANCZOS)
    if i==5:
        case=small;continue
    at=np.rint(TARGET-(np.array(point)-box[:2])*SCALE).astype(int).tolist()
    out=Image.new('RGBA',(256,276));out.alpha_composite(small,at);rows.append(np.array(out))
    tracking.append({'sourcePose':i,'source':'source-v2.png' if i in CORRECTED_HEADS else 'source.png','box':box,'sourceHead':point,'fixedScale':SCALE,'position':at})
cargo=P.parent/'james-water-cargo-south-v1';water=P.parent/'james-water-south-v1'
ref=np.array(Image.open(cargo/'frames/bare/swim-pickup/001.png').convert('RGBA'));yy,xx=np.indices(ref.shape[:2])
head=((xx-TARGET[0])/14)**2+((yy-TARGET[1])/16)**2<=1
def neutral(v):
    rgb=v[:,:,:3].astype(float);return (v[:,:,3]>180)&(np.ptp(rgb,axis=2)<25)&(rgb[:,:,0]>20)&(rgb[:,:,0]<150)
def gold(v):
    r,g,b=v[:,:,:3].astype(float).transpose(2,0,1);return (v[:,:,3]>180)&(r-b>35)&(g-b>20)&~head
def skin(v):
    r,g,b=v[:,:,:3].astype(float).transpose(2,0,1);return (v[:,:,3]>180)&head&(r-g>12)&(g-b>5)&(r<210)
grades={}
for source in ['source.png','source-v2.png']:
    cohort=[v for v,t in zip(rows,tracking) if t['source']==source]
    pooled=lambda mask:np.concatenate([v[:,:,:3][mask(v)] for v in cohort])
    grades[source]={'neutral':float(np.median(ref[:,:,:3][neutral(ref)&~head&(yy<185)])/np.median(pooled(lambda v:neutral(v)&~head))), 'gold':(np.median(ref[:,:,:3][gold(ref)],axis=0)/np.median(pooled(gold),axis=0)).tolist(), 'skin':(np.median(ref[:,:,:3][skin(ref)],axis=0)/np.median(pooled(skin),axis=0)).tolist()}
    assert all(np.isfinite(g).all() for g in grades[source].values())
sys.path.insert(0,str(P.parent/'james-water-family-v1'));from extract_sources import extract
hr=json.loads((water/'helmet-registration.json').read_text());patch=extract(water/'source-helmet.png',6,6)[4][0]
pa=np.array(patch);r,g,b=pa[:,:,:3].astype(float).transpose(2,0,1);gray=(pa[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17)
pa[gray,:3]=np.rint(pa[gray,:3]*.9).astype('uint8')
patch=Image.fromarray(pa).resize((round(patch.width*hr['fixedHeadScale']),round(patch.height*hr['fixedHeadScale'])),Image.Resampling.LANCZOS)
pos=np.rint(TARGET+hr['centerOffset']-[patch.width/2,patch.height/2]).astype(int).tolist()
erase=((xx-TARGET[0])/14)**2+((yy-(TARGET[1]-1))/14)**2<=1
for i,v in enumerate(rows):
    rgb=v[:,:,:3].astype(float);gm=gold(v);sm=skin(v)
    gain=grades[tracking[i]['source']]
    rgb[(v[:,:,3]>0)&~head&~gm]*=gain['neutral'];rgb[gm]*=gain['gold'];rgb[sm]*=gain['skin']
    v[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');bare=Image.fromarray(v)
    hv=v.copy();hv[erase]=0;helmet=Image.fromarray(hv);helmet.alpha_composite(patch,pos);hv=np.array(helmet)
    allowed=erase.copy();allowed[pos[1]:pos[1]+patch.height,pos[0]:pos[0]+patch.width]=True
    assert np.array_equal(v[~allowed],hv[~allowed])
    for gear,image in [('bare',bare),('helmet',helmet)]:
        folder=P/'frames'/gear;folder.mkdir(parents=True,exist_ok=True);image.save(folder/f'{i:03d}.png')
    tracking[i]['bodyBounds']=list(bare.getbbox())
cv=np.array(case);rgb=cv[:,:,:3].astype(float);rgb[cv[:,:,3]>0]*=grades['source.png']['neutral']
cv[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');case=Image.fromarray(cv);case.save(P/'case.png');case_at=[111,187]
reg={'status':'selected_runtime_south_empty_case_release','sourceSha256':hashlib.sha256((P/'source.png').read_bytes()).hexdigest(),'generatedOriginal':'C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-5b32c764-bf58-4335-9ed1-8361077eac70.png','prompt':'tool-prompt.txt','fixedScale':SCALE,'headTarget':TARGET.tolist(),'tracking':tracking,'helmetPosition':pos,'helmetPatchSize':list(patch.size),'casePosition':case_at,'caseSize':list(case.size),'caseProvenance':'Complete independently authored case, same .25 ruler as five whole bodies; no glove cutout.'}
reg['correction']={'source':'source-v2.png','sha256':hashlib.sha256((P/'source-v2.png').read_bytes()).hexdigest(),'original':'C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-6411b2bc-b089-4159-a1d5-f84a2335d28e.png','prompt':'tool-prompt-v2.txt','selectedWholeCells':[0,3,4],'reason':'Source-authored glove clearance and longer final trailing-leg projection; original whole cells1,2 and case preserved.'}
reg['sourceGrade']=grades
for obsolete in ['neutralGain','goldGain','skinGain']:reg.pop(obsolete,None)
(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n')
for gear in ['bare','helmet']:
    cm=json.loads((cargo/f'{gear}-manifest.json').read_text());source=next(s for s in cm['states'] if s['id']=='swim-pickup-south');states=[]
    end=water/('frames/swim/000.png' if gear=='bare' else 'frames/helmet/swim/000.png')
    for index in range(1,6):
        files=[cargo/source['frameFiles'][i] for i in range(index,0,-1)]+[P/f'frames/{gear}/{i:03d}.png' for i in range(5)]+[end]
        states.append({'id':f'swim-cancel-release-pickup-{index}-south','frameFiles':[Path(os.path.relpath(f,P)).as_posix() for f in files],'frameDurationsMs':[50]*index+[80,60,80,80,70,60],'loop':False,'waterPoses':[True]*len(files),'waterKinds':['swim']*len(files),'facings':['south']*len(files),'depthOffsets':[0.0]*len(files),'caseReleaseMs':50*index,'provenance':{'interiors':'Five independently authored South empty-handed full bodies; no work torch stow','endpoint':'exact selected empty swim0'}})
    m={'name':'James South indexed empty case release '+gear,'frameWidth':256,'frameHeight':276,'pivot':[128,128],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':reg['status'],'states':states};(P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
contact=Image.new('RGB',(7*180,440),'#303b40');draw=ImageDraw.Draw(contact)
for slot in range(7):
    for row,gear in enumerate(['bare','helmet']):
        m=json.loads((P/f'{gear}-manifest.json').read_text());im=Image.open(P/m['states'][0]['frameFiles'][slot]).convert('RGBA');layer=im.copy()
        if slot:layer.alpha_composite(case,tuple(case_at))
        crop=layer.crop((80,65,175,225));contact.paste(crop,(slot*180+35,row*220+35),crop)
        draw.text((slot*180+12,row*220+12),gear+' '+str(slot),fill='white')
contact.save(P/'join-contact.png')
print(json.dumps({'poses':len(rows),'scale':SCALE,'caseSize':case.size,'casePosition':case_at,'sourceGrade':grades,'helmetPosition':pos}))
