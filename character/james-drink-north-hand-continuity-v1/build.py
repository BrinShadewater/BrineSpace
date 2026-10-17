from pathlib import Path
import json,sys,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parents[1]
sys.path.insert(0,str(R/'character/james-meal-family-v1'))
# This script shares a filename with the grading module; load by explicit path.
import importlib.util
spec=importlib.util.spec_from_file_location('meal_grade',R/'character/james-meal-family-v1/build.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
raw=Image.open(P/'source.png').convert('RGBA');a=np.array(raw);labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;keys=sorted(np.argsort(counts)[-6:],key=lambda k:np.where(labs==k)[1].mean());assert all(counts[k]>10000 for k in keys)
centers=[np.where(labs==k)[1].mean() for k in keys];edges=[0]+[round((centers[i]+centers[i+1])/2) for i in range(5)]+[raw.width];cells=[raw.crop((edges[i],0,edges[i+1],raw.height)) for i in range(6)]
neutral=Image.open(R/'character/james-meal-north-v1/frames/drink/000.png').convert('RGBA');na=np.array(neutral);ny,nx=np.where(na[:,:,3]>180)
cy,cx=np.where(np.array(cells[0])[:,:,3]>180);scale=(ny.max()-ny.min()+1)/(cy.max()-cy.min()+1);target=module.feet(neutral);rows=[];records=[]
for i,cell in enumerate(cells):
 anchor=module.feet(cell);at=(round(target[0]-anchor[0]*scale),round(target[1]-anchor[1]*scale));out=Image.new('RGBA',neutral.size);out.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),at);out=module.grade(out,'north');rows.append(out);records.append({'index':i,'scale':scale,'sourceBootAnchor':anchor,'translation':at})
# One rigid raster registration correction from the matching raw neutral pose.
reference_y=int(np.where(np.array(rows[0])[:,:,3]>180)[0].max());sole_delta=int(ny.max())-reference_y
for i,x in enumerate(rows):
 moved=Image.new('RGBA',neutral.size);moved.alpha_composite(x,(0,sole_delta));rows[i]=moved;records[i]['translation']=(records[i]['translation'][0],records[i]['translation'][1]+sole_delta)
# Source-level shared neutral/ochre calibration, excluding warm skin/hair.
def masks(a):
 rgb=a[:,:,:3].astype(float);lum=rgb.mean(2);rr,gg,bb=rgb.transpose(2,0,1);opaque=a[:,:,3]>180
 return rgb,lum,opaque&(rgb.max(2)-rgb.min(2)<25)&(lum>25)&(lum<190),opaque&(gg-bb>20)&(rr>gg)&((gg-bb)>1.2*(rr-gg))
qs=[.1,.25,.5,.75,.9,.97];nr,nl,nn,ng=masks(na);tq=np.quantile(nl[nn],qs);tg=np.median(nr[ng],0);arrays=[np.array(x) for x in rows];nv=[];gv=[]
for x in arrays:
 rgb,lum,n,g=masks(x);nv.append(lum[n]);gv.append(rgb[g])
sq=np.quantile(np.concatenate(nv),qs);goldgain=tg/np.median(np.concatenate(gv),0)
for i,x in enumerate(arrays):
 rgb,lum,n,g=masks(x);mapped=np.interp(lum,np.r_[25,sq,190],np.r_[25,tq,190]);gain=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0);rgb[n]*=gain[n,None];rgb[g]*=goldgain;x[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');rows[i]=Image.fromarray(x)
# A fixed pooled cap-material chroma gain matches the held reference, without
# altering head shape or fitting separate poses to different palettes.
def cap_mask(x):
 rgb=x[:,:,:3].astype(float);rr,gg,bb=rgb.transpose(2,0,1);yy,xx=np.indices(x.shape[:2]);top=int(np.where(x[:,:,3]>180)[0].min())
 return (x[:,:,3]>180)&(yy<top+16)&(xx>=80)&(xx<104)&(rr>=gg)&(gg>=bb)&(rr-bb<50)
cap_target=np.median(na[cap_mask(na),:3],0);cap_source=np.median(np.concatenate([np.array(x)[cap_mask(np.array(x)),:3] for x in rows]),0);cap_gain=cap_target/cap_source
for i,x in enumerate(rows):
 a=np.array(x);rgb=a[:,:,:3].astype(float);mask=cap_mask(a);rgb[mask]*=cap_gain;a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');rows[i]=Image.fromarray(a)
rows[0]=neutral.copy();rows[5]=neutral.copy()
files=[]
for i,x in enumerate(rows):
 dest=P/'frames'/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True);x.save(dest);files.append(dest.relative_to(P).as_posix())
family=json.loads((R/'character/james-meal-family-v1/bare-manifest.json').read_text());base=next(s for s in family['states'] if s['id']=='drink-north');state=json.loads(json.dumps(base));state['frameFiles']=files;states=[state]
hands=json.loads((R/'character/james-cup-pickup-north-v1/handoffs-manifest.json').read_text());deposit=next(s for s in hands['states'] if s['id']=='cup-deposit-north')
for index in range(6):
 prefix=[index] if index in [0,5] else list(range(index,-1,-1));tail=[f if f.startswith('res://') else 'res://character/james-cup-pickup-north-v1/'+f for f in deposit['frameFiles'][1:]]
 states.append({'id':f'meal-return-drink-{index}-north','frameCount':len(prefix)+len(tail),'frameFiles':[files[j] for j in prefix]+tail,'frameDurationsMs':[80]*len(prefix)+deposit['frameDurationsMs'][1:],'loop':False,'facings':['north']*(len(prefix)+len(tail)),'waterPoses':[False]*(len(prefix)+len(tail)),'depthOffsets':[0]*(len(prefix)+len(tail)),'provenance':{'sourceAction':'drink','sourceIndex':index,'derivation':'Exact selected left-cup current pose, reverse whole sip prefix to original held endpoint, unchanged cup deposit tail; no limb splice/mirror.'}})
manifest={'name':'James North left-cup sip continuity','frameWidth':184,'frameHeight':192,'pivot':[92,172],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'selected_production_native_verified_owner_review_pending','states':states}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(P/'registration.json').write_text(json.dumps({'fixedWholeScale':scale,'authority':'Whole raw neutral pose crown/sole versus exact148px held master; one scale across six source figures','poses':records,'wholeSourceSoleCorrection':sole_delta,'capMaterialGain':cap_gain.tolist(),'neutralQuantilesSource':sq.tolist(),'neutralQuantilesMaster':tq.tolist(),'goldGain':goldgain.tolist(),'exactHeldEndpoints':True,'sourceSha256':hashlib.sha256((P/'source.png').read_bytes()).hexdigest(),'generatedOriginal':'C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-ecc050d2-f274-4ef0-8c95-3444aa953176.png','productionInstalled':True,'ownerVisualAcceptance':False},indent=2),encoding='utf-8')
board=Image.new('RGB',(8*184,240),'#303b40');draw=ImageDraw.Draw(board)
for i,im in enumerate([neutral]+rows+[neutral]):board.paste(im,(i*184,30),im);draw.text((i*184+6,8),['held master','exact held','raise','mouth','sip','lower','exact held','held master'][i],fill='white')
board.save(P/'master-review.png')
views=[]
for i,x in enumerate(rows):
 view=Image.new('RGB',(650,280),'#303b40');ImageDraw.Draw(view).text((8,8),'North left-cup sip candidate / '+str(i),fill='white');view.paste(x,(20,50),x);view.paste(neutral,(225,50),neutral)
 for height,left in [(82,430),(54,525),(27,590)]:
  factor=height/148;small=x.resize((round(184*factor),round(192*factor)),Image.Resampling.BILINEAR);view.paste(small,(left,250-round(172*factor)),small)
 views.append(view)
views[0].save(P/'review.gif',save_all=True,append_images=views[1:],duration=state['frameDurationsMs'],loop=0)
print(json.dumps({'scale':scale,'normalStates':1,'derivedReturns':6,'exactHeldEndpoints':True,'candidate':True}))
