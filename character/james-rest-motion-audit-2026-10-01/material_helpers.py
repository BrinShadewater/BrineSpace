from pathlib import Path
import json
import numpy as np
R=Path(__file__).resolve().parents[2]
def region(direction,pose):
    folder=R/'character'/('james-north-rest-polish-v1' if direction=='north' else 'james-lying-'+direction+'-v1');reg=json.loads((folder/'registration.json').read_text());body=reg['tracking'][pose]['protectedHeadBox']
    head=reg['helmetTracking'][pose]['editRegion'] if direction=='north' else json.loads((folder/'helmet-registration.json').read_text())['tracking'][pose]['editRegion']
    return [min(body[0],head[0]),min(body[1],head[1]),max(body[2],head[2]),max(body[3],head[3])]
def masks(a,box,sample=False):
    rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);protect=np.zeros(a.shape[:2],bool);x0,y0,x1,y1=box;protect[y0:y1,x0:x1]=True
    opaque=a[:,:,3]>(240 if sample else 0);gold=opaque&~protect&(r-b>35)&(g-b>20)
    neutral=opaque&~protect&~gold&(np.ptp(rgb,2)<28)&(rgb.mean(2)>20)&(rgb.mean(2)<110)&~((r-b>12)&(r-g>5))
    return neutral,gold,protect
