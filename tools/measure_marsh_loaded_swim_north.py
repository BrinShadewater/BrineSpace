"""Report whole source bounds at own-neutral scale before canvas registration."""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1';rev=sys.argv[1]
raw=Image.open(B/f'sources/north-loop-{rev}.raw.png').convert('RGBA');a=np.array(raw)[:,:,3]
xs=np.flatnonzero(np.sum(a>=128,axis=0)>=2);groups=np.split(xs,np.flatnonzero(np.diff(xs)>8)+1);assert len(groups)==5
edges=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(4)]+[raw.width]
cells=[raw.crop((edges[i],0,edges[i+1],raw.height)) for i in range(5)]
def binary(im):
    a=np.array(im);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);return Image.fromarray(a)
n=binary(cells[-1]).getbbox();scale=146/(n[3]-n[1]);sizes=[]
for im in cells:
    im=binary(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.BOX));b=im.getbbox();sizes.append([b[2]-b[0],b[3]-b[1]])
r={'revision':rev,'commonNeutralScale':scale,'occupiedSizes':sizes,'standingTarget':146,'oldAnchorTop':105,'canvasHeight':208,'oldAnchorFits':[105+h<=208 for w,h in sizes[:4]],'normalAdmission':False}
(B/f'sources/north-loop-{rev}.measurement.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
