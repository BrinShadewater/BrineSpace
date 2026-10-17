"""Rejected hue-derived ruler experiment; kept as diagnostic evidence."""
raise SystemExit('Rejected hair run ruler: use register_heads.py and accepted cargo body scale.')
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_closing,label
H=Path(__file__).resolve().parent;records={}
R=H.parents[1];C=R/'character/veld-swim-carry-north-coherent-v1'
original=np.array(Image.open(C/'source-v3.png').convert('RGBA'));authority=json.loads((C/'head-landmarks-v3.json').read_text());original_widths=[]
for mark in authority['records']:
 span=mark['hairSpan'];row=mark['hairRow'];scan=original[row,span[0]:span[1],:3].astype(float);m=(scan[:,0]>35)&(scan[:,0]<160)&(scan[:,0]>1.15*scan[:,1])&(scan[:,1]>1.1*scan[:,2]);runs,count=label(binary_closing(m,iterations=1));rid=int(runs[len(runs)//2]);assert rid;original_widths.append(int((runs==rid).sum()))
target_core=float(np.median(original_widths))*json.loads((C/'fit-checks.json').read_text())['fixedAtlasScale']
regions={'work':[(200,98,313,180),(573,98,690,180),(977,98,1090,181),(198,712,313,799),(574,712,690,799),(976,713,1090,799)],'pickup':[(254,68,350,139),(732,68,829,139),(1185,68,1290,140),(254,578,355,650),(730,578,833,650),(1185,578,1290,650)]}
for role,rois in regions.items():
 p=H/('work-source-v1.png' if role=='work' else 'pickup-source-v3.png');a=np.array(Image.open(p).convert('RGBA'));out=[]
 for i,b in enumerate(rois):
  cut=a[b[1]:b[3],b[0]:b[2]];v=cut[:,:,:3].astype(float);m=(cut[:,:,3]>200)&(v[:,:,0]>35)&(v[:,:,0]<160)&(v[:,:,0]>v[:,:,1]*1.15)&(v[:,:,1]>v[:,:,2]*1.1)
  spans=[]
  # The lower ROI reaches bun/collar; measure upper skull core only.
  for row in range(round(m.shape[0]*.60)):
   # Reject sparse coloured alpha noise and cuffs outside the central hair run.
   runs,count=label(binary_closing(m[row],iterations=1))
   if count:
    center=m.shape[1]//2;rid=int(runs[center])
    if rid:
     xs=np.where(runs==rid)[0];spans.append((int(xs.max()-xs.min()+1),row,int(xs.min()),int(xs.max()+1)))
  width,row,left,right=max(spans);assert 60<width<115,(role,i,width)
  central=m[:,m.shape[1]//2-5:m.shape[1]//2+6];yy,xx=np.where(central);crown=int(yy.min()+b[1]);out.append(dict(sourceCell=i,sourceViewedROI=b,hairRow=row+b[1],hairSpan=[left+b[0],right+b[0]],crown=crown))
 records[role]=dict(source=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),targetHairWidth=21,targetCoreWidth=target_core,authorityCoreWidths=original_widths,targetCrown=104,targetCenter=128,fixedAtlasScale=target_core/float(np.median([x['hairSpan'][1]-x['hairSpan'][0] for x in out])),records=out)
(H/'head-landmarks-v1.json').write_text(json.dumps(dict(method='Source-viewed bounded hair ROIs;35<R<160/R>1.15G/G>1.1B;largest core-row span;one median ruler per source density, same native21px skull',roles=records),indent=2)+'\n')
print({role:dict(scale=r['fixedAtlasScale'],marks=r['records']) for role,r in records.items()})
