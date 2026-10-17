"""One shared ruler calibrated by the matching maximum hinge reference."""
from pathlib import Path
import sys,json
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1]
sys.path.insert(0,str(R/'character/james-meal-family-v1'))
from build import grade
raw=Image.open(P/'middle-pair-source.png').convert('RGBA');a=np.array(raw)
canonical=np.array(Image.open(P/'empty-contact-source.png').convert('RGBA'))
canonical_top=int(np.where(canonical[:,:,3]>180)[0].min())
canonical_sole=994
sheet_top=int(np.where(a[:640,:614,3]>180)[0].min())
scale=(canonical_sole-canonical_top)*.13/(569-sheet_top)
rows=[]
for i,(x0,y0,x1,y1,sole,left,right) in enumerate([
 (0,0,614,640,569,(210,280),(440,510)),
 (614,0,1227,640,569,(730,805),(950,1020)),
 (0,640,614,1281,1155,(210,280),(440,510)),
 (614,640,1227,1281,1155,(730,805),(950,1020))]):
 centers=[]
 for low,high in [left,right]:
  yy,xx=np.where(a[sole-3:sole+1,low:high,3]>180);centers.append(float(xx.mean()+low))
 anchor=((centers[0]+centers[1])*.5-x0,sole-y0)
 cell=raw.crop((x0,y0,x1,y1));out=Image.new('RGBA',(256,256));at=(round(128-anchor[0]*scale),round(224-anchor[1]*scale))
 out.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),at)
 out=grade(out,'south');dest=P/'middle-pair-registered'/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True);out.save(dest)
 rows.append({'pose':i,'sourceSoleCenters':centers,'sourceAnchor':anchor,'translation':at,'nativeSoleSeparation':(centers[1]-centers[0])*scale})
(P/'middle-pair-registration.json').write_text(json.dumps({'fixedScale':scale,'authority':'Matching canonical deep empty-contact crown-to-sole .13 body ruler, single scale across all four figures','canonicalTop':canonical_top,'canonicalSole':canonical_sole,'rows':rows,'noPerPoseScaling':True},indent=2)+'\n')
print(json.dumps({'fixedScale':scale,'nativeSoleSeparation':[r['nativeSoleSeparation'] for r in rows]}))
