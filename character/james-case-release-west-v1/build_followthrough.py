"""Four authored empty-handed whole poses; never reuse work torch-stow interiors."""
from pathlib import Path
import sys,json,os,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent
SCALE=.16
HEADS=[[265,187],[1175,210],[267,624],[1156,632]]
TARGET=np.array([114.48698058428597,117.85696788241698])
a=np.array(Image.open(P/'source-empty-followthrough.png').convert('RGBA'));labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
ids=sorted(np.argsort(counts)[-4:],key=lambda k:np.where(labs==k)[0].mean()//440*2000+np.where(labs==k)[1].mean())
rows=[];tracking=[]
for i,k in enumerate(ids):
    y,x=np.where(labs==k);box=[int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4];v=a[box[1]:box[3],box[0]:box[2]].copy();v[~binary_dilation(labs[box[1]:box[3],box[0]:box[2]]==k,iterations=2)]=0
    raw=Image.fromarray(v);(P/'followthrough-source-crops').mkdir(exist_ok=True);raw.save(P/'followthrough-source-crops'/f'{i:03d}.png')
    small=raw.resize((round(raw.width*SCALE),round(raw.height*SCALE)),Image.Resampling.LANCZOS);at=np.rint(TARGET-(np.array(HEADS[i])-box[:2])*SCALE).astype(int).tolist();out=Image.new('RGBA',(256,276));out.alpha_composite(small,at);rows.append(np.array(out));tracking.append({'sourcePose':i,'box':box,'sourceHead':HEADS[i],'fixedScale':SCALE,'position':at})
ref=np.array(Image.open(P.parent/'james-water-cargo-west-v1/frames/bare/swim-pickup/001.png').convert('RGBA'));yy,xx=np.indices(ref.shape[:2]);head=((xx-TARGET[0])/15)**2+((yy-TARGET[1])/16)**2<=1
def neutral(v):
    rgb=v[:,:,:3].astype(float);return (v[:,:,3]>180)&(np.ptp(rgb,axis=2)<25)&(rgb[:,:,0]>20)&(rgb[:,:,0]<150)
def gold(v):
    r,g,b=v[:,:,:3].astype(float).transpose(2,0,1);return (v[:,:,3]>180)&(r-b>35)&(g-b>20)&~head
def skin(v):
    r,g,b=v[:,:,:3].astype(float).transpose(2,0,1);return head&(v[:,:,3]>180)&(r-g>14)&(g-b>12)
hair=np.zeros(head.shape,bool);hair[104:116,100:128]=True
pool=lambda mask:np.concatenate([v[:,:,:3][mask(v)] for v in rows])
ng=float(np.median(ref[:,:,:3][neutral(ref)&~head])/np.median(pool(lambda v:neutral(v)&~head)))
gg=np.median(ref[:,:,:3][gold(ref)],axis=0)/np.median(pool(gold),axis=0)
fg=np.median(ref[:,:,:3][skin(ref)],axis=0)/np.median(pool(skin),axis=0)
hg=np.median(ref[:,:,:3][hair&neutral(ref)],axis=0)/np.median(pool(lambda v:hair&neutral(v)),axis=0)
assert all(np.isfinite(g).all() for g in [ng,gg,fg,hg])
sys.path.insert(0,str(P.parent/'james-water-family-v1'));from extract_sources import extract
w=P.parent/'james-water-west-v1';hr=json.loads((w/'helmet-registration.json').read_text());patch=extract(w/'source-helmet.png',6,6)[4][0];pa=np.array(patch);r,g,b=pa[:,:,:3].astype(float).transpose(2,0,1);gray=(pa[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17);pa[gray,:3]=np.rint(pa[gray,:3]*.9).astype('uint8');patch=Image.fromarray(pa).resize((round(patch.width*hr['fixedHeadScale']),round(patch.height*hr['fixedHeadScale'])),Image.Resampling.LANCZOS);pos=np.rint(TARGET+hr['centerOffset']-[patch.width/2,patch.height/2]).astype(int).tolist()
erase=((xx-TARGET[0])/15)**2+((yy-(TARGET[1]-1))/15)**2<=1
for i,v in enumerate(rows):
    rgb=v[:,:,:3].astype(float);rgb[(v[:,:,3]>0)&~head&~gold(v)]*=ng;rgb[gold(v)]*=gg;rgb[skin(v)]*=fg;rgb[hair&neutral(v)]*=hg;v[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');bare=Image.fromarray(v)
    ha=v.copy();ha[erase]=0;helmet=Image.fromarray(ha);helmet.alpha_composite(patch,pos)
    # Authored far glove is genuinely in front of the low helmet edge in pose1.
    foreground=np.zeros(erase.shape,bool)
    if i==0:foreground[129:140,96:110]=True
    hv=np.array(helmet);hv[foreground&(v[:,:,3]>180)]=v[foreground&(v[:,:,3]>180)];helmet=Image.fromarray(hv)
    for gear,image in [('bare',bare),('helmet',helmet)]:
        folder=P/'followthrough'/gear;folder.mkdir(parents=True,exist_ok=True);image.save(folder/f'{i+1:03d}.png')
    allowed=erase.copy();allowed[pos[1]:pos[1]+patch.height,pos[0]:pos[0]+patch.width]=True
    assert np.array_equal(v[~allowed],hv[~allowed])
    tracking[i]['bodyBounds']=bare.getbbox();tracking[i]['foreground']=([96,129,110,140] if i==0 else None)
for gear in ['bare','helmet']:
    file=P/f'{gear}-manifest.json';m=json.loads(file.read_text())
    for state in m['states']:
        index=int(state['id'].split('-')[4]);state['frameFiles'][index+1:index+5]=[f'followthrough/{gear}/{i:03d}.png' for i in range(1,5)]
        state.setdefault('provenance',{})['followthrough']='Four newly authored empty-handed whole-body West poses, torch holstered and wrench fixed. No reused work tool-stow interiors. Exact selected empty swim endpoint.'
    file.write_text(json.dumps(m,indent=2)+'\n')
reg={'sourceSha256':hashlib.sha256((P/'source-empty-followthrough.png').read_bytes()).hexdigest(),'generatedOriginal':'C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-91dbdd40-d908-4e3f-8cbd-0f3bde89792b.png','prompt':'tool-prompt-empty-followthrough.txt','fixedScale':SCALE,'headTarget':TARGET.tolist(),'tracking':tracking,'neutralGain':ng,'goldGain':gg.tolist(),'faceGain':fg.tolist(),'hairGain':hg.tolist(),'helmetPosition':pos,'helmetPatchSize':list(patch.size),'scope':'Four complete independently authored empty-handed interiors, pooled matte grade, fixed ruler and native West shell. Gear body exact outside local head/shell; actual runtime selection/evidence separate.'}
(P/'followthrough-registration.json').write_text(json.dumps(reg,indent=2)+'\n');print(json.dumps({'poses':len(rows),'fixedScale':SCALE,'pooledNeutralGain':ng}))
