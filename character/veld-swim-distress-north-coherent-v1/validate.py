"""Read-only candidate contract and consumed life-clearance envelope audit."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
e=json.loads((P/'build-evidence.json').read_text());profile=R/'character/dr-veld-v2/clearance.json';c=json.loads(profile.read_text());records=[]
check(sha(P/'sources/distress-v1.png')==e['sourceSha256'],'source binding')
check(all(sha(R/f)==h for f,h in e['references'].items()),'unchanged reference masters')
check(all(r['anatomicalScale']==e['physicalRulers'][r['source']] for r in e['records']),'one fixed ruler per source density')
for i,r in enumerate(e['records']):
 check(r['source']==('sources/distress-arm-edit-v2.png' if i==3 else 'sources/distress-v1.png'),'five original cells and one edited correction')
 check(sha(P/r['source'])==r['sourceSha256'],'selected raw source binding')
check(e['records'][3]['sourceCellSlot']==5,'corrected provider bottom-right cell mapped to loop slot3')
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text());s=m['states'][0]
 check(m['pivot']==[128,128] and m['standingHeight']==148,'swim registration')
 check(s['loop'] and s['frameDurationsMs']==[160]*6 and s['waterKinds']==['swim']*6 and s['waterPoses']==[True]*6,'inherited distress contract')
 extents=[]
 for f in s['frameFiles']:
  im=Image.open(P/f);a=np.array(im);y,x=np.where(a[:,:,3]>20)
  check(im.mode=='RGBA' and im.size==(256,256),'native RGBA canvas')
  check(x.min()>0 and y.min()>0 and x.max()<255 and y.max()<255,'uncropped alpha')
  check(sha(P/f)==e['frameHashes'][f],'packaged pixel binding')
  extents.append(((np.array([x.min(),y.min(),x.max()+1,y.max()+1])-np.array([128]*4))*65.28/148).tolist())
 a=np.array(extents);bounds=[float(a[:,0].min()),float(a[:,1].min()),float(a[:,2].max()),float(a[:,3].max())]
 prior=c['life'][gear]['swim-distress-north']
 union=[min(prior[i],bounds[i]) if i<2 else max(prior[i],bounds[i]) for i in range(4)]
 union=[math.floor(v*1000)/1000 if i<2 else math.ceil(v*1000)/1000 for i,v in enumerate(union)]
 base=c['swim'][gear]['north']
 effective=[min(base[i],union[i]) if i<2 else max(base[i],union[i]) for i in range(4)]
 selected_effective=[min(base[i],prior[i]) if i<2 else max(base[i],prior[i]) for i in range(4)]
 covered=all(selected_effective[i]<=bounds[i] if i<2 else selected_effective[i]>=bounds[i] for i in range(4))
 check(covered,'current consumed base/life union already contains every north candidate')
 records.append({'gear':gear,'frameEnvelopes':extents,'candidateEnvelope':bounds,'selectedLifeAdditionalExtent':prior,'conservativeCandidateExtent':union,'baseSwimExtent':base,'selectedEffectiveConsumedExtent':selected_effective,'effectiveConsumedCandidateExtent':effective,'coveredBySelectedEffective':covered,'coveredBySelected':all(prior[i]<=bounds[i] if i<2 else prior[i]>=bounds[i] for i in range(4))})
 check(all(union[i]<=bounds[i] if i<2 else union[i]>=bounds[i] for i in range(4)),'conservative union')
report={'passed':True,'checks':checks,'selected':False,'profileSha256':sha(profile),'records':records,'scope':'pixel/source/metadata and life.swim-distress-north union; selected clearance unchanged. Geometry/lifecycle checked separately.'}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'{checks} candidate contract/source/envelope checks PASS; current effective swim/life union covers {sum(r["coveredBySelectedEffective"] for r in records)}/2 gear states')
