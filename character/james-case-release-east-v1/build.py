from pathlib import Path
import sys,json,hashlib,os
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation,distance_transform_edt
P=Path(__file__).resolve().parent
SCALE=.1
POINT=np.array([141.5378198256979,118.2267791396747])
SOURCE_HEAD=np.array([957,245])
a=np.array(Image.open(P/'source.png').convert('RGBA'));labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;ids=sorted(np.argsort(counts)[-2:],key=lambda k:np.where(labs==k)[1].mean());parts=[];records=[]
for k in ids:
 y,x=np.where(labs==k);box=[int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4];v=a[box[1]:box[3],box[0]:box[2]].copy();v[~binary_dilation(labs[box[1]:box[3],box[0]:box[2]]==k,iterations=2)]=0;im=Image.fromarray(v);im.save(P/('source-body.png' if not parts else 'source-case.png'));small=im.resize((round(im.width*SCALE),round(im.height*SCALE)),Image.Resampling.LANCZOS);parts.append(small);records.append({'box':box,'fixedScale':SCALE})
at=np.rint(POINT-(SOURCE_HEAD-np.array(records[0]['box'][:2]))*SCALE).astype(int).tolist();body=Image.new('RGBA',(256,276));body.alpha_composite(parts[0],at)
ref=np.array(Image.open(P.parent/'james-water-cargo-east-v1/frames/bare/swim-pickup/001.png').convert('RGBA'));v=np.array(body);yy,xx=np.indices(v.shape[:2]);head=((xx-POINT[0])/14)**2+((yy-POINT[1])/15)**2<=1
r,g,b=v[:,:,:3].astype(float).transpose(2,0,1);rr,rg,rb=ref[:,:,:3].astype(float).transpose(2,0,1)
neutral=lambda im:(im[:,:,3]>180)&(np.max(im[:,:,:3],axis=2)-np.min(im[:,:,:3],axis=2)<25)&(im[:,:,0]>20)&(im[:,:,0]<150)
gold=(v[:,:,3]>180)&(r-b>35)&(g-b>20)&~head;refgold=(ref[:,:,3]>180)&(rr-rb>35)&(rg-rb>20)&~head
gain=float(np.median(ref[:,:,:3][neutral(ref)&~head])/np.median(v[:,:,:3][neutral(v)&~head]));gg=np.median(ref[:,:,:3][refgold],axis=0)/np.median(v[:,:,:3][gold],axis=0)
rgb=v[:,:,:3].astype(float);rgb[(v[:,:,3]>0)&~head&~gold]*=gain;rgb[gold]*=gg
skin=head&(v[:,:,3]>180)&(r-g>14)&(g-b>12);rskin=head&(ref[:,:,3]>180)&(rr-rg>14)&(rg-rb>12);fg=np.median(ref[:,:,:3][rskin],axis=0)/np.median(v[:,:,:3][skin],axis=0);rgb[skin]*=fg
hair=np.zeros(head.shape,bool);hair[108:116,133:150]=True;hm=hair&(v[:,:,3]>180)&~skin;rhm=hair&(ref[:,:,3]>180)&~rskin;hg=np.median(ref[:,:,:3][rhm],axis=0)/np.median(v[:,:,:3][hm],axis=0);rgb[hm]*=hg
assert all(np.all(np.isfinite(x)) for x in [gain,gg,fg,hg]);v[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');body=Image.fromarray(v);body.save(P/'body-bare.png')
parts[1].save(P/'rejected-generated-case.png')
# Reuse the complete selected case, including its owned antialias fringe.
# Nearest-component ownership excludes any glove fringe; no missing pixels filled.
rl,rn=label(ref[:,:,3]>180);case_id=int(rl[140,200]);body_id=int(rl[140,100]);assert case_id and body_id and case_id!=body_id
dc=distance_transform_edt(rl!=case_id);db=distance_transform_edt(rl!=body_id)
owned=(dc<=3)&(dc<db);cv=ref.copy();cv[~owned]=0
box=Image.fromarray(cv).getbbox();case=Image.fromarray(cv).crop(box);case.save(P/'case.png');case_at=list(box[:2]);cg=np.ones(3)
sys.path.insert(0,str(P.parent/'james-water-family-v1'));from extract_sources import extract
w=P.parent/'james-water-east-v1';hr=json.loads((w/'helmet-registration.json').read_text());patch=extract(w/'source-helmet.png',6,6)[4][0];pa=np.array(patch);r,g,b=pa[:,:,:3].astype(float).transpose(2,0,1);mask=(pa[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17);pa[mask,:3]=np.rint(pa[mask,:3]*.9).astype('uint8');patch=Image.fromarray(pa).resize((round(patch.width*hr['fixedHeadScale']),round(patch.height*hr['fixedHeadScale'])),Image.Resampling.LANCZOS);pos=np.rint(POINT+hr['centerOffset']-[patch.width/2,patch.height/2]).astype(int).tolist();ha=np.array(body);erase=((xx-POINT[0])/14)**2+((yy-(POINT[1]-1))/14)**2<=1;ha[erase]=0;helmet=Image.fromarray(ha);helmet.alpha_composite(patch,pos);helmet.save(P/'body-helmet.png')
reg={'status':'staged_release_layer_candidate_not_installed','sourceSha256':hashlib.sha256((P/'source.png').read_bytes()).hexdigest(),'generatedOriginal':'C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-4cae0f77-5c5b-428e-821e-8040e74ff49d.png','prompt':'tool-prompt.txt','fixedScale':SCALE,'tracking':records,'sourceHead':SOURCE_HEAD.tolist(),'headTarget':POINT.tolist(),'bodyPosition':at,'casePosition':[181,130],'neutralGain':gain,'goldGain':gg.tolist(),'faceGain':fg.tolist(),'hairGain':hg.tolist(),'caseGain':cg.tolist(),'helmetPosition':pos,'scope':'New authored complete release body and detached case at one physical ruler; native shell reuse. Candidate only, not installed or exact old-pose reconstruction.'};(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n')
reg['helmetPatchSize']=list(patch.size);reg['casePosition']=case_at;reg['caseProvenance']={'source':'../james-water-cargo-east-v1/frames/bare/swim-pickup/001.png','sha256':hashlib.sha256((P.parent/'james-water-cargo-east-v1/frames/bare/swim-pickup/001.png').read_bytes()).hexdigest(),'nativeScale':1.0,'crop':list(box),'ownership':'selected opaque component plus at most3px fringe nearest case rather than body','opaqueCoreSize':[40,33],'rejectedGeneratedSize':list(parts[1].size)};reg['scope']='New authored complete release body at fixed .1 source ruler plus exact selected complete case at native scale1. Native shell reuse. Candidate only, not installed; generated smaller case retained as rejected.';reg['runtimeSelection']='selection.json';reg['scope']='Authored complete release body at fixed .1 source ruler plus exact selected complete case at native scale1 and native East shell. Body/case are selected by indexed East cancellation runtime; source extraction provenance remains here, selection/evidence scope in selection.json. Generated smaller case retained as rejected.';(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n')
board=Image.new('RGB',(768,320),'#303b40');d=ImageDraw.Draw(board)
for i,(name,im) in enumerate([('selected floor pickup',Image.open(P.parent/'james-water-cargo-east-v1/frames/helmet/swim-pickup/001.png').convert('RGBA')),('candidate bare',body),('candidate helmet',helmet)]):
 layer=im.copy()
 if i:layer.alpha_composite(case,tuple(case_at))
 board.paste(layer,(i*256,35),layer);d.text((i*256+8,8),name,fill='white')
board.save(P/'contact.png');print(json.dumps({'parts':len(parts),'fixedScale':SCALE,'caseSize':case.size,'neutralGain':gain,'helmetPosition':pos}))
# Stage the separated floor entrance and release-to-empty join for native review.
for gear in ['bare','helmet']:
 donor=P.parent/f'james-water-cargo-east-v1/frames/{gear}/swim-pickup/001.png';entry=np.array(Image.open(donor).convert('RGBA'));entry[owned]=0
 folder=P/'frames'/gear;folder.mkdir(parents=True,exist_ok=True);Image.fromarray(entry).save(folder/'000.png');Image.open(P/f'body-{gear}.png').save(folder/'001.png')
 stow=P.parent/'james-water-torch-stow-east-v1'/('frames/bare' if gear=='bare' else 'frames')
 files=[folder/'000.png',folder/'001.png']+[stow/f'{i:03d}.png' for i in range(1,6)]
 state={'id':'swim-case-release-east','frameFiles':[Path(os.path.relpath(f,P)).as_posix() for f in files],'frameDurationsMs':[50,80,60,80,80,70,60],'loop':False,'waterPoses':[True]*7,'waterKinds':['swim']*7,'facings':['east']*7,'depthOffsets':[0.0]*7}
 manifest={'name':'James East separated case release candidate '+gear,'frameWidth':256,'frameHeight':276,'pivot':[128,128],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_native_layer_review_not_installed','caseLayer':{'frameFile':'case.png','position':case_at,'worldAnchorRequired':True},'states':[state]}
 (P/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
