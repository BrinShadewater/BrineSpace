"""Whole-source sheet registration at one ruler; contact and endpoints exact."""
from pathlib import Path
import json, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
sys.path.insert(0,str(R/'character/james-meal-family-v1'))
from build import grade
raw=Image.open(P/'reach-sheet-source-v2.png').convert('RGBA');a=np.array(raw)
anchors=[(320,478),(768,478),(1218,478),(320,965),(768,970),(1216,970)]
master=Image.open(R/'character/james-meal-pickup-south-v1/selected/000.png').convert('RGBA')
ma=np.array(master);my=np.where(ma[:,:,3]>180)[0];targetheight=my.max()-my.min()+1
cells=[]
for i in range(6):
 x0=(i%3)*512;y0=(i//3)*512
 cell=a[y0:y0+512,x0:x0+512].copy();labs,n=label(cell[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;key=counts.argmax()
 mask=binary_dilation(labs==key,iterations=2);cell[~mask]=0
 cells.append(Image.fromarray(cell))
cy=np.where(np.array(cells[0])[:,:,3]>180)[0];scale=float(targetheight/(cy.max()-cy.min()+1))
frames=[];rows=[]
for i,cell in enumerate(cells):
 anchor=(anchors[i][0]-(i%3)*512,anchors[i][1]-(i//3)*512)
 out=Image.new('RGBA',(256,256));at=(round(128-anchor[0]*scale),round(224-anchor[1]*scale))
 out.alpha_composite(cell.resize((round(512*scale),round(512*scale)),Image.Resampling.LANCZOS),at)
 out=grade(out,'south');frames.append(out);rows.append({'sourcePose':i,'fixedScale':scale,'sourceAnchor':anchor,'translation':at})
exactidle=Image.new('RGBA',(256,256));exactidle.alpha_composite(master,(36,52))
exactheld=Image.new('RGBA',(256,256));exactheld.alpha_composite(Image.open(R/'character/james-meal-pickup-south-v1/selected/005.png').convert('RGBA'),(36,52))
contact=Image.open(P/'fresh-contact.png').convert('RGBA')
emptyraw=Image.open(P/'empty-contact-source.png').convert('RGBA')
empty=Image.new('RGBA',(256,256));empty.alpha_composite(emptyraw.resize((round(emptyraw.width*.13),round(emptyraw.height*.13)),Image.Resampling.LANCZOS),(round(128-614*.13),round(224-995*.13)))
empty=grade(empty,'south');empty.save(P/'empty-contact.png')
# Independent complete contact source, never a body or limb splice.
middleempty=Image.open(P/'middle-pair-registered/001.png').convert('RGBA')
middlelift=Image.open(P/'middle-pair-registered/003.png').convert('RGBA')
sequence=[exactidle,frames[1],middleempty,empty,contact,middlelift,frames[4],exactheld]
durations=[60,100,130,90,160,110,130,120]
def material_masks(a):
 rgb=a[:,:,:3].astype(float);lum=rgb.mean(2);r,g,b=rgb.transpose(2,0,1)
 neutral=(a[:,:,3]>0)&(rgb.max(2)-rgb.min(2)<25)&(lum>25)&(lum<190)
 gold=(a[:,:,3]>0)&(g-b>20)&((g-b)>1.2*(r-g))&(r-g>0)
 return rgb,lum,neutral,gold
ma=np.array(exactidle);mrgb,mlum,mneutral,mgold=material_masks(ma)
quantiles=[.1,.25,.5,.75,.9,.97]
target_q=np.quantile(mlum[mneutral&(ma[:,:,3]>180)],quantiles)
target_gold=np.median(mrgb[mgold&(ma[:,:,3]>180)],axis=0)
calibration=[]
# One pooled transform per independent source, never a changing per-pose gain.
for source_name,indices in [('reach-sheet-v2',[1,6]),('middle-pair',[2,5]),('empty-contact',[3]),('bowl-contact',[4])]:
 samples=[np.array(sequence[i]) for i in indices]
 neutral_values=[];gold_values=[]
 for a in samples:
  rgb,lum,neutral,gold=material_masks(a)
  neutral_values.append(lum[neutral&(a[:,:,3]>180)]);gold_values.append(rgb[gold&(a[:,:,3]>180)])
 source_q=np.quantile(np.concatenate(neutral_values),quantiles)
 gold_gain=target_gold/np.median(np.concatenate(gold_values),axis=0)
 xp=np.r_[25,source_q,190];fp=np.r_[25,target_q,190]
 for i,a in zip(indices,samples):
  rgb,lum,neutral,gold=material_masks(a)
  mapped=np.interp(lum,xp,fp);gain=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0)
  rgb[neutral]*=gain[neutral,None];rgb[gold]*=gold_gain
  a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');sequence[i]=Image.fromarray(a)
 calibration.append({'source':source_name,'frames':indices,'neutralSourceQuantiles':source_q.tolist(),'neutralMasterQuantiles':target_q.tolist(),'goldGain':gold_gain.tolist()})
(P/'reach-material-calibration.json').write_text(json.dumps({'method':'Whole foreground source-level pooled neutral quantile curve and muted gold RGB gain against exact standing master; unchanged alpha/anatomy and untouched exact endpoints','sourceQuantiles':quantiles,'groups':calibration},indent=2)+'\n')
files=[]
for i,im in enumerate(sequence):
 dest=P/'reach-staged'/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True);im.save(dest);files.append(dest.relative_to(P).as_posix())
manifest={'name':'James South supported pickup reach staged','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'staged_master_motion_review_pending_not_installed','states':[{'id':'meal-acquire-south','frameCount':8,'frameFiles':files,'frameDurationsMs':durations,'loop':False,'facings':['south']*8,'waterPoses':[False]*8,'depthOffsets':[0,0,0,49,49,0,0,0]}]}
(P/'reach-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
board=Image.new('RGB',(2304,280),'#303b40');draw=ImageDraw.Draw(board)
for i,im in enumerate(sequence+[exactidle]):
 board.paste(im,(i*256,20),im);draw.text((i*256+8,8),['exact idle','early reach','middle empty','empty contact','exact contact','middle lift','retract','exact held','idle master'][i],fill='white');draw.line((i*256,244,(i+1)*256,244),fill='#77888e')
board.save(P/'reach-master-contact.png')
views=[]
for im in sequence:
 view=Image.new('RGB',(720,320),'#303b40');d=ImageDraw.Draw(view);d.text((8,8),'South reach candidate / fixed master and 82px 54px 27px / NOT INSTALLED',fill='white')
 for sprite,x in [(im,0),(exactidle,230)]:view.paste(sprite,(x,60),sprite)
 for h,x in [(82,500),(54,610),(27,680)]:
  s=h/148;small=im.resize((round(256*s),round(256*s)),Image.Resampling.BILINEAR);view.paste(small,(x,284-round(224*s)),small)
 views.append(view)
views[0].save(P/'reach-staged-review.gif',save_all=True,append_images=views[1:],duration=durations,loop=0)
(P/'reach-registration.json').write_text(json.dumps({'scale':scale,'poses':rows,'exactEndpoints':True,'independentContactSource':'deep-contact-source-v4.png','contactWholeScale':.13,'productionInstalled':False},indent=2)+'\n')
fixture=(P/'native-deep-contact.gd').read_text().replace('deep-contact-manifest.json','reach-manifest.json').replace('deep-captures','reach-captures').replace('native-deep-contact','native-reach-candidate').replace('frames.size()==6','frames.size()==8').replace('All six candidate source poses','All eight candidate source poses').replace('JAMES SOUTH DEEP CONTACT DIAGNOSTIC','JAMES SOUTH REACH CANDIDATE')
fixture=fixture.replace('Single replacement contact pose amongst older source frames, deliberately not a motion pack.', 'Eight-pose reach candidate from independent whole authored sources, exact registered endpoints; staged only, not installed or visually accepted.')
(P/'native-reach-candidate.gd').write_text(fixture)
print(json.dumps({'sheetScale':scale,'frameCount':8,'durationMs':sum(durations),'status':'staged_visual_review_pending'}))
