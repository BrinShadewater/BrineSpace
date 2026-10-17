from pathlib import Path
import json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];review=json.loads((P/'review-evidence.json').read_text());cov=json.loads((R/'character/james-animation-coverage-2026-09-30/runtime-coverage.json').read_text());data={}
def region(direction,pose):
    folder=R/'character'/('james-north-rest-polish-v1' if direction=='north' else 'james-lying-'+direction+'-v1');reg=json.loads((folder/'registration.json').read_text());body=reg['tracking'][pose]['protectedHeadBox']
    head=reg['helmetTracking'][pose]['editRegion'] if direction=='north' else json.loads((folder/'helmet-registration.json').read_text())['tracking'][pose]['editRegion']
    return [min(body[0],head[0]),min(body[1],head[1]),max(body[2],head[2]),max(body[3],head[3])]
def masks(a,box,sample=False):
    rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);protect=np.zeros(a.shape[:2],bool);x0,y0,x1,y1=box;protect[y0:y1,x0:x1]=True
    opaque=a[:,:,3]>(240 if sample else 0);gold=opaque&~protect&(r-b>35)&(g-b>20)
    neutral=opaque&~protect&~gold&(np.ptp(rgb,2)<28)&(rgb.mean(2)>20)&(rgb.mean(2)<110)&~((r-b>12)&(r-g>5))
    return neutral,gold,protect
for direction in ['north','south','east','west']:
    samples={'neutral':[],'gold':[]};seen=set();rows=[]
    for row in review['records']:
        if row['mode']!='bare' or not row['key'].endswith('-'+direction):continue
        pack=R/cov['body'][row['key']]['path'];m=json.loads(pack.read_text());state=next(s for s in m['states'] if s['id']==row['key']);pose=state['provenance']['sourcePoses'][row['index']]
        a=np.array(Image.open(R/row['path']).convert('RGBA'));box=region(direction,pose);neutral,gold,_=masks(a,box,True)
        rows.append({'key':row['key'],'index':row['index'],'sourcePose':pose,'headProtected':box,'neutralMedian':np.median(a[:,:,:3][neutral],0).tolist(),'goldMedian':np.median(a[:,:,:3][gold],0).tolist() if gold.any() else None,'goldPixels':int(gold.sum())})
        if pose==0 or row['sha256'] in seen:continue
        seen.add(row['sha256'])
        for name,mask in [('neutral',neutral),('gold',gold)]:
            if mask.any():samples[name].append(a[:,:,:3][mask])
    file=R/cov['body']['idle-'+direction]['path'];m=json.loads(file.read_text());state=next(s for s in m['states'] if s['id']=='idle-'+direction);ma=Image.new('RGBA',(256,256));ma.alpha_composite(Image.open(file.parent/state['frameFiles'][0]).convert('RGBA'),(128-int(m['pivot'][0]),224-int(m['pivot'][1])));a=np.array(ma);neutral,gold,_=masks(a,region(direction,0),True)
    stats={}
    for name,mask in [('neutral',neutral),('gold',gold)]:
        pooled=np.median(np.concatenate(samples[name]),0);target=np.median(a[:,:,:3][mask],0);stats[name]={'sourcePooledMedian':pooled.tolist(),'masterMedian':target.tolist(),'fixedGain':(target/pooled).tolist()}
    data[direction]={'uniqueInteriorSourceImages':len(seen),'stats':stats,'rows':rows}
(P/'material-diagnostics.json').write_text(json.dumps({'scope':'Pooled unique interior bare source pixels outside existing protected bare/head and common-shell edit regions. Broad neutral/gold material masks are not semantic shoulder-only selections; no source changed. Same protected region supports shared bare/helmet treatment.','directions':data},indent=2)+'\n',encoding='utf-8');print(json.dumps({d:{'unique':v['uniqueInteriorSourceImages'],'stats':v['stats']} for d,v in data.items()}))
