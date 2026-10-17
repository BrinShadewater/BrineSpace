"""Whole cup sources and exact reversed South deposit chains, staged only."""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
sys.path.insert(0,str(R/'character/james-meal-family-v1'))
from build import grade
raw=Image.open(P/'cup-source-v2.png').convert('RGBA');a=np.array(raw)
scale=(994-344)*.13/(515-135)
cup_poses=[];records=[]
for i,(x0,y0,x1,y1,sole,left,right) in enumerate([
 (0,0,614,590,515,(256,335),(447,532)),
 (614,0,1227,590,515,(725,805),(915,997)),
 (0,590,614,1281,1152,(279,360),(442,532)),
 (614,590,1227,1281,1153,(750,835),(893,980))]):
 centers=[]
 for lo,hi in [left,right]:
  yy,xx=np.where(a[sole-3:sole+1,lo:hi,3]>180);centers.append(float(xx.mean()+lo))
 anchor=((centers[0]+centers[1])*.5-x0,sole-y0);cell=raw.crop((x0,y0,x1,y1));out=Image.new('RGBA',(256,256))
 at=(round(128-anchor[0]*scale),round(224-anchor[1]*scale));out.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),at)
 out=grade(out,'south');cup_poses.append(out);records.append({'pose':i,'anchor':anchor,'translation':at,'soleSeparation':(centers[1]-centers[0])*scale})
ref=np.array(Image.open(P/'cup-retract-body-reference.png').convert('RGBA'));ry=np.where(ref[:,:,3]>180)[0]
body_height=float((ry.max()-ry.min())*.3147751605995717)
retract=Image.open(P/'cup-retract-source.png').convert('RGBA');ra=np.array(retract);top=int(np.where(ra[:,:,3]>180)[0].min());sole=1128
retract_scale=body_height/(sole-top)
centers=[]
for lo,hi in [(370,580),(690,910)]:
 yy,xx=np.where(ra[sole-4:sole+1,lo:hi,3]>180);centers.append(float(xx.mean()+lo))
at=(round(128-np.mean(centers)*retract_scale),round(224-sole*retract_scale));near=Image.new('RGBA',(256,256));near.alpha_composite(retract.resize((round(retract.width*retract_scale),round(retract.height*retract_scale)),Image.Resampling.LANCZOS),at);near=grade(near,'south')
bowl=json.loads((P/'reach-manifest.json').read_text())['states'][0]
bowl_frames=[Image.open(P/f).convert('RGBA') for f in bowl['frameFiles']]
held=Image.new('RGBA',(256,256));held.alpha_composite(Image.open(R/'character/james-meal-south-v1/frames/drink/000.png').convert('RGBA'),(36,52))
cup=bowl_frames[:4]+[cup_poses[1],cup_poses[2],near,held]
master=np.array(bowl_frames[0]);qs=[.1,.25,.5,.75,.9,.97]
def masks(a):
 rgb=a[:,:,:3].astype(float);lum=rgb.mean(2);r,g,b=rgb.transpose(2,0,1)
 neutral=(a[:,:,3]>0)&(rgb.max(2)-rgb.min(2)<25)&(lum>25)&(lum<190)
 gold=(a[:,:,3]>0)&(g-b>20)&((g-b)>1.2*(r-g))&(r-g>0)
 return rgb,lum,neutral,gold
mrgb,mlum,mn,mg=masks(master);target=np.quantile(mlum[mn&(master[:,:,3]>180)],qs);targetgold=np.median(mrgb[mg&(master[:,:,3]>180)],axis=0);grades=[]
for source,indices in [('cup-source-v2',[4,5]),('cup-retract-source',[6])]:
 arrays=[np.array(cup[i]) for i in indices];nv=[];gv=[]
 for a in arrays:
  rgb,lum,n,g=masks(a);nv.append(lum[n&(a[:,:,3]>180)]);gv.append(rgb[g&(a[:,:,3]>180)])
 sourceq=np.quantile(np.concatenate(nv),qs);goldgain=targetgold/np.median(np.concatenate(gv),axis=0)
 for i,a in zip(indices,arrays):
  rgb,lum,n,g=masks(a);mapped=np.interp(lum,np.r_[25,sourceq,190],np.r_[25,target,190]);gain=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0);rgb[n]*=gain[n,None];rgb[g]*=goldgain;a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');cup[i]=Image.fromarray(a)
 grades.append({'source':source,'frames':indices,'neutralSourceQ':sourceq.tolist(),'neutralMasterQ':target.tolist(),'goldGain':goldgain.tolist()})
files=[]
for i,im in enumerate(cup):
 dest=P/'cup-staged'/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True);im.save(dest);files.append(dest.relative_to(P).as_posix())
cupstate={'id':'cup-acquire-south','frameCount':8,'frameFiles':files,'frameDurationsMs':bowl['frameDurationsMs'],'loop':False,'facings':['south']*8,'waterPoses':[False]*8,'depthOffsets':[0,0,0,49,49,0,0,0]}
states=[bowl,cupstate]
for source,id in [(bowl,'meal-deposit-south'),(cupstate,'cup-deposit-south')]:
 state=json.loads(json.dumps(source));state['id']=id
 for key in ['frameFiles','frameDurationsMs','facings','waterPoses','depthOffsets']:state[key]=list(reversed(source[key]))
 state['provenance']={'derivation':'Exact reverse of complete authored South pickup; held to table contact/release then exact empty standing. Same facing, no mirror/limb splice.'};states.append(state)
# Padded exact existing meal loops provide common-pivot source joins in this candidate.
family=R/'character/james-meal-family-v1';loops=json.loads((family/'bare-manifest.json').read_text())
for state in loops['states']:
 if state['id'] not in ['eat-south','drink-south']:continue
 state=json.loads(json.dumps(state));paths=[]
 for i,f in enumerate(state['frameFiles']):
  src=(family/f).resolve();im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(src).convert('RGBA'),(36,52));dest=P/'loop-staged'/state['id']/f'{i:03d}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest);paths.append(dest.relative_to(P).as_posix())
 state['frameFiles']=paths;states.append(state)
sources=states.copy();byid={s['id']:s for s in sources}
return_proof=[]
for source in sources:
 action=source['id'].removesuffix('-south')
 for index in range(len(source['frameFiles'])):
  if action in ['meal-acquire','cup-acquire']:chain=[(source,j) for j in range(index,-1,-1)]
  elif action in ['meal-deposit','cup-deposit']:chain=[(source,j) for j in range(index,len(source['frameFiles']))]
  else:
   deposit=byid['meal-deposit-south' if action=='eat' else 'cup-deposit-south']
   same_neutral=Image.open(P/source['frameFiles'][index]).convert('RGBA').tobytes()==Image.open(P/source['frameFiles'][0]).convert('RGBA').tobytes()
   chain=[(source,index)] if same_neutral else [(source,j) for j in range(index,-1,-1)]
   chain += [(deposit,j) for j in range(1,len(deposit['frameFiles']))]
  row={'id':f'meal-return-{action}-{index}-south','frameCount':len(chain),'loop':False}
  for key in ['frameFiles','frameDurationsMs','depthOffsets','facings','waterPoses']:
   row[key]=[s.get(key,[0 if key=='depthOffsets' else False]*len(s['frameFiles']))[j] for s,j in chain]
  row['frameDurationsMs'][0]=min(row['frameDurationsMs'][0],80)
  row['provenance']={'sourceState':source['id'],'sourceIndex':index,'derivation':'Exact current pose then complete source prefix reversal or deposit suffix; mouth poses lower to exact neutral before deposit. Reuses authored South figures, not new pose coverage.'}
  first=Image.open(P/row['frameFiles'][0]).convert('RGBA').tobytes();current=Image.open(P/source['frameFiles'][index]).convert('RGBA').tobytes();last=Image.open(P/row['frameFiles'][-1]).convert('RGBA').tobytes();empty=bowl_frames[0].tobytes()
  assert first==current and last==empty
  return_proof.append({'id':row['id'],'firstMatchesCurrentPixels':True,'lastMatchesExactStandingPixels':True,'durationMs':sum(row['frameDurationsMs'])});states.append(row)
manifest={'name':'James South supported meal handoffs','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'production_supported_contact_owner_review_pending','states':states}
(P/'handoffs-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(P/'return-prefix-package-evidence.json').write_text(json.dumps({'variants':len(return_proof),'rows':return_proof,'scope':'Pixel endpoints and finite source-derived chains only; actual interruption decision/clearance, normal loader and Continue remain unproven'},indent=2)+'\n')
(P/'cup-registration.json').write_text(json.dumps({'cupSharedScale':scale,'cupPoses':records,'retractScale':retract_scale,'retractBodyHeightAuthority':body_height,'retractTranslation':at,'unusedCupSourcePoses':[0,3],'reasonUnusedUpright':'Lower-leg projection too compressed versus master; use independent bowl-retract-body-matched cup instead','materialGroups':grades,'productionInstalled':True,'ownerVisualAcceptance':False},indent=2)+'\n')
board=Image.new('RGB',(2048,560),'#303b40');d=ImageDraw.Draw(board)
for row,sequence in enumerate([bowl_frames,cup]):
 for i,im in enumerate(sequence):board.paste(im,(i*256,row*280+20),im);d.text((i*256+6,row*280+7),('bowl' if row==0 else 'cup')+f' {i}',fill='white')
board.save(P/'bowl-cup-master-review.png')
print(json.dumps({'normalStates':6,'returnVariants':len(return_proof),'totalStates':len(states),'cupScale':scale,'retractScale':retract_scale,'productionBound':True,'ownerVisualAcceptance':False}))
