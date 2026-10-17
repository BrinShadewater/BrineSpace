from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parents[1];m=json.loads((P/'manifest.json').read_text());reg=json.loads((P/'head-registration.json').read_text());head=np.array(Image.open(P/reg['componentFile']).convert('RGBA'));master=np.array(Image.open(R/reg['master']).convert('RGBA'));x0,y0,x1,y1=reg['sourceBox'];checks=[];hashes={};yy,xx=np.indices((256,256))
def check(ok,name):
 assert ok,name
 checks.append(name)
mask=head[:,:,3]>0;check(np.array_equal(head[mask],master[y0:y1,x0:x1][mask]),'Exact accepted master head and alpha')
top=int(np.where((master[:,:,3]>180)&(yy>=65)&(yy<105)&(xx>=100)&(xx<166))[0].min());crown=(master[:,:,3]>0)&(yy>=top)&(yy<top+14)&(xx>=105)&(xx<145);full=np.zeros_like(master);full[y0:y1,x0:x1]=head;check(np.array_equal(full[crown],master[crown]),'Complete native master crown and soft edges')
original=json.loads((R/reg['sourceManifest']).read_text());s=next(s for s in original['states'] if s['id']=='walk-north');new=m['states'][0]
check(new['frameDurationsMs']==s['frameDurationsMs'] and new['gaitCycles']==s['gaitCycles'],'Original gait clock retained')
check(m['strideDistanceCells']['walk-north']==original['strideDistanceCells']['walk-north'],'Original stride retained')
check(m['pivot']==[128,224] and m['standingHeight']==148,'Native density and foot origin')
for f,row in zip(new['frameFiles'],reg['frames']):
 old=Image.open(R/row['originalFile'][6:]).convert('RGBA');plane=Image.new('RGBA',(256,256));plane.alpha_composite(old,row['nativePlaneOffset']);old=np.array(plane);a=np.array(Image.open(R/f[6:]).convert('RGBA'));erase=np.array(Image.open(P/row['eraseMask']))>0;px,py=row['headPosition'];h,w=head.shape[:2];region=erase|((xx>=px)&(xx<px+w)&(yy>=py)&(yy<py+h))
 check(np.array_equal(a[~region],old[~region]),'Protected original body pixels exact after canvas translation')
 opaque=head[:,:,3]==255;check(np.array_equal(a[py:py+h,px:px+w][opaque],head[opaque]),'Native master head stamp exact')
 sizes=np.bincount(label(a[:,:,3]>160)[0].ravel());check(sum(n>30 for n in sizes[1:])==1,'Single substantial connected silhouette')
 check(hashlib.sha256((R/row['originalFile'][6:]).read_bytes()).hexdigest()==row['originalSha256'],'Original source unchanged');hashes[f]=hashlib.sha256((R/f[6:]).read_bytes()).hexdigest()
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':len(checks),'labels':checks,'sha256':hashes,'scope':'Native master component, protected body, canvas/pivot and source gait; visual motion and runtime remain separate'},indent=2)+'\n');print(str(len(checks))+' package checks pass')
