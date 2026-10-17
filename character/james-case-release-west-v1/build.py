"""Independent West release body/case at one fixed source ruler; staged only."""
from pathlib import Path
import sys,os,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent
SCALE=.1
HEAD=np.array([1010,225])
TARGET=np.array([114.48698058428597,117.85696788241698])
CASE_AT=[54,130]
a=np.array(Image.open(P/'source.png').convert('RGBA'));labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
ids=np.argsort(counts)[-2:][::-1];parts=[];tracking=[]
for i,k in enumerate(ids):
    y,x=np.where(labs==k);box=[int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4]
    cut=a[box[1]:box[3],box[0]:box[2]].copy();cut[~binary_dilation(labs[box[1]:box[3],box[0]:box[2]]==k,iterations=2)]=0
    raw=Image.fromarray(cut);raw.save(P/('source-body.png' if i==0 else 'source-case.png'))
    parts.append(raw.resize((round(raw.width*SCALE),round(raw.height*SCALE)),Image.Resampling.LANCZOS));tracking.append({'box':box,'fixedScale':SCALE})
at=np.rint(TARGET-(HEAD-np.array(tracking[0]['box'][:2]))*SCALE).astype(int).tolist()
body=Image.new('RGBA',(256,276));body.alpha_composite(parts[0],at)
v=np.array(body);ref=np.array(Image.open(P.parent/'james-water-cargo-west-v1/frames/bare/swim-pickup/001.png').convert('RGBA'));yy,xx=np.indices(v.shape[:2]);head=((xx-TARGET[0])/15)**2+((yy-TARGET[1])/16)**2<=1
def neutral(im):
    rgb=im[:,:,:3].astype(float)
    return (im[:,:,3]>180)&(np.ptp(rgb,axis=2)<25)&(rgb[:,:,0]>20)&(rgb[:,:,0]<150)
def gold(im):
    r,g,b=im[:,:,:3].astype(float).transpose(2,0,1)
    return (im[:,:,3]>180)&(r-b>35)&(g-b>20)&~head
def skin(im):
    r,g,b=im[:,:,:3].astype(float).transpose(2,0,1)
    return head&(im[:,:,3]>180)&(r-g>14)&(g-b>12)
gain=float(np.median(ref[:,:,:3][neutral(ref)&~head])/np.median(v[:,:,:3][neutral(v)&~head]));gg=np.median(ref[:,:,:3][gold(ref)],axis=0)/np.median(v[:,:,:3][gold(v)],axis=0)
fg=np.median(ref[:,:,:3][skin(ref)],axis=0)/np.median(v[:,:,:3][skin(v)],axis=0)
hair=np.zeros(head.shape,bool);hair[104:116,100:128]=True;hg=np.median(ref[:,:,:3][hair&neutral(ref)],axis=0)/np.median(v[:,:,:3][hair&neutral(v)],axis=0)
assert all(np.isfinite(g).all() for g in [gain,gg,fg,hg])
rgb=v[:,:,:3].astype(float);rgb[(v[:,:,3]>0)&~head&~gold(v)]*=gain;rgb[gold(v)]*=gg;rgb[skin(v)]*=fg;rgb[hair&neutral(v)]*=hg
v[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');body=Image.fromarray(v);body.save(P/'body-bare.png')
c=np.array(parts[1]);case_ref=ref[130:163,54:81];cg=np.median(case_ref[:,:,:3][neutral(case_ref)],axis=0)/np.median(c[:,:,:3][neutral(c)],axis=0);assert np.isfinite(cg).all()
c[:,:,:3]=np.rint(c[:,:,:3].astype(float)*cg).clip(0,255).astype('uint8');case=Image.fromarray(c);case.save(P/'case.png')
sys.path.insert(0,str(P.parent/'james-water-family-v1'));from extract_sources import extract
w=P.parent/'james-water-west-v1';hr=json.loads((w/'helmet-registration.json').read_text());patch=extract(w/'source-helmet.png',6,6)[4][0]
pa=np.array(patch);r,g,b=pa[:,:,:3].astype(float).transpose(2,0,1);gray=(pa[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17);pa[gray,:3]=np.rint(pa[gray,:3]*.9).astype('uint8')
patch=Image.fromarray(pa).resize((round(patch.width*hr['fixedHeadScale']),round(patch.height*hr['fixedHeadScale'])),Image.Resampling.LANCZOS)
pos=np.rint(TARGET+hr['centerOffset']-[patch.width/2,patch.height/2]).astype(int).tolist();ha=np.array(body);erase=((xx-TARGET[0])/15)**2+((yy-(TARGET[1]-1))/15)**2<=1;ha[erase]=0
helmet=Image.fromarray(ha);helmet.alpha_composite(patch,pos);helmet.save(P/'body-helmet.png')
reg={'status':'selected_runtime_west_case_release','sourceSha256':hashlib.sha256((P/'source.png').read_bytes()).hexdigest(),'generatedOriginal':'C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-64b70555-d179-4953-b424-22de6f547ca0.png','prompt':'tool-prompt-v3.txt','fixedScale':SCALE,'tracking':tracking,'sourceHead':HEAD.tolist(),'headTarget':TARGET.tolist(),'bodyPosition':at,'casePosition':CASE_AT,'caseSize':list(case.size),'neutralGain':gain,'goldGain':gg.tolist(),'faceGain':fg.tolist(),'hairGain':hg.tolist(),'caseGain':cg.tolist(),'helmetPosition':pos,'helmetPatchSize':list(patch.size),'headEraseRadii':[15,15],'scope':'Complete newly authored West release body/case, common .1 physical ruler, native West shell. Case cannot reuse selected whole component because glove touches it; new case is not exact selected-case pixels. Current runtime selection/evidence in selection.json.'}
(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n')
for gear in ['bare','helmet']:
    cargo=P.parent/'james-water-cargo-west-v1';cm=json.loads((cargo/f'{gear}-manifest.json').read_text());source=next(s for s in cm['states'] if s['id']=='swim-pickup-west')
    stow=P.parent/'james-water-torch-stow-west-v1';sm=json.loads((stow/f'{gear}-manifest.json').read_text())['states'][0];states=[]
    for index in range(1,6):
        files=[cargo/source['frameFiles'][i] for i in range(index,0,-1)]+[P/f'body-{gear}.png']+[stow/f for f in sm['frameFiles'][1:]]
        durations=[50]*index+[80]+sm['frameDurationsMs'][1:]
        states.append({'id':f'swim-cancel-release-pickup-{index}-west','frameFiles':[Path(os.path.relpath(f,P)).as_posix() for f in files],'frameDurationsMs':durations,'loop':False,'waterPoses':[True]*len(files),'waterKinds':['swim']*len(files),'facings':['west']*len(files),'depthOffsets':[0.0]*len(files),'caseReleaseMs':50*index})
    manifest={'name':'James West indexed release candidate '+gear,'frameWidth':256,'frameHeight':276,'pivot':[128,128],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':reg['status'],'states':states}
    (P/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
board=Image.new('RGB',(768,320),'#303b40');d=ImageDraw.Draw(board)
for i,(name,im) in enumerate([('selected West pickup1',Image.open(P.parent/'james-water-cargo-west-v1/frames/helmet/swim-pickup/001.png').convert('RGBA')),('West authored bare release',body),('West paired native helmet',helmet)]):
    im=im.copy()
    if i:im.alpha_composite(case,tuple(CASE_AT))
    board.paste(im,(i*256,35),im);d.text((i*256+8,8),name,fill='white')
board.save(P/'contact.png');print(json.dumps({'parts':len(parts),'scale':SCALE,'caseSize':case.size,'neutralGain':gain,'bodyBounds':body.getbbox(),'helmetBounds':helmet.getbbox()}))
import runpy
runpy.run_path(str(P/'build_followthrough.py'))
