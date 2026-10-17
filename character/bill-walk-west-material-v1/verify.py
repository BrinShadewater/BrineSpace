from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parents[1];reg=json.loads((P/'material-registration.json').read_text());head=np.array(Image.open(P/'sources/west-master-head.png').convert('RGBA'));master=np.array(Image.open(R/reg['master']).convert('RGBA'));x0,y0,x1,y1=reg['headSourceBox'];L=np.array([.2126,.7152,.0722]);yy,xx=np.indices((256,256));checks=[];hashes={};oldbare={}
def check(ok,name):
 assert ok,name
 checks.append(name)
mask=head[:,:,3]>0;check(np.array_equal(head[mask],master[y0:y1,x0:x1][mask]),'Exact native accepted head component')
top=int(np.where((master[:,:,3]>180)&(yy>=65)&(yy<105)&(xx>=100)&(xx<166))[0].min());crown=(master[:,:,3]>0)&(yy>=top)&(yy<top+14)&(xx>=105)&(xx<145);component=np.zeros_like(master);component[y0:y1,x0:x1]=head;check(np.array_equal(component[crown],master[crown]),'Complete master crown coverage, not just subset equality')
for gear,name in [('bare','manifest.json'),('helmet','helmet-manifest.json')]:
 m=json.loads((P/name).read_text());s=m['states'][0];inventory=json.loads((R/reg['sourceInventory']).read_text());ref=inventory['selectedStateSources'][gear]['walk-west'];original=json.loads((R/ref['manifest']).read_text());o=next(o for o in original['states'] if o['id']=='walk-west')
 check(s['frameDurationsMs']==o['frameDurationsMs'] and s['gaitCycles']==o['gaitCycles'],'Original paired gait clock retained')
 check(m['strideDistanceCells']['walk-west']==original['strideDistanceCells']['walk-west'],'Original stride retained')
 check(m['pivot']==[128,224] and m['standingHeight']==148,'Native density and foot origin')
 rows=[x for x in reg['frames'] if x['gear']==gear]
 for f,row in zip(s['frameFiles'],rows):
  im=Image.open(R/row['originalFile'][6:]).convert('RGBA');plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,row['canvasTranslation']);old=np.array(plane);a=np.array(Image.open(R/f[6:]).convert('RGBA'));mask=np.array(Image.open(P/row['mask']))>0;erase=np.array(Image.open(P/row['eraseMask']))>0;region=mask.copy();headregion=erase.copy()
  if gear=='bare':
   px,py=row['headPosition'];h,w=head.shape[:2];headregion|=(xx>=px)&(xx<px+w)&(yy>=py)&(yy<py+h);region|=headregion;oldbare[row['frame']]=old;opaque=head[:,:,3]==255
   check(np.array_equal(a[py:py+h,px:px+w][opaque],head[opaque]),'Exact opaque native head stamp')
   sizes=np.bincount(label(a[:,:,3]>160)[0].ravel());check(sum(n>30 for n in sizes[1:])==1,'One substantial connected silhouette')
  else:
   different=np.any(old!=oldbare[row['frame']],axis=2);check(np.array_equal(a[different],old[different]),'Equipment-specific pixels unchanged')
  check(np.array_equal(a[~region],old[~region]),'Protected original source pixels exact')
  check(np.array_equal(a[:,:,3][~headregion],old[:,:,3][~headregion]),'Fabric alpha exactly retained')
  delta=np.abs(a[:,:,:3].astype(float)@L-old[:,:,:3].astype(float)@L);check(float(delta[~headregion].max())<=.5,'Fabric luminance retained within rounding')
  check(hashlib.sha256((R/row['originalFile'][6:]).read_bytes()).hexdigest()==row['originalSha256'],'Original source unchanged');hashes[f]=hashlib.sha256((R/f[6:]).read_bytes()).hexdigest()
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':len(checks),'labels':checks,'sha256':hashes,'scope':'Protected source body, alpha/luminance, exact native head and equipment-specific pixels, original gait; visual motion/runtime acceptance separate'},indent=2)+'\n');print(str(len(checks))+' package checks pass')
