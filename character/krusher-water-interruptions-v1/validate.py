from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;inv=json.load(open(R/'character/krusher-complete-animation-v1/source-coverage.json'));proof=json.load(open(P/'provenance.json'));checks=0;errors=[]
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
def arr(q):return np.array(Image.open(q).convert('RGBA'))
def check(ok,why):
 global checks
 checks+=1
 if not ok:errors.append(why)
for q in proof['records']:
 a=arr(R/q['source']);b=arr(P/q['output']);mask=np.array(Image.open(P/q['allowedMask']))>0;check(sha(R/q['source'])==q['sourceHash'],'source hash');check(sha(P/q['output'])==q['outputHash'],'output hash');check(sha(R/q['headSource'])==q['headHash'],'head hash');check(a.shape==b.shape,'original complete canvas');check(np.array_equal(a[~mask],b[~mask]),'protected source pixels');d=q['state'].rsplit('-',1)[1];yy,xx=np.indices(a.shape[:2]);x0,y0,x1,y1=q['headBox']
 far=(yy>y1+55)
 if d=='east':far|=xx<x0-60
 elif d=='west':far|=xx>x1+60
 check(np.array_equal(a[far],b[far]),'distant body/legs')
 if q['state']=='swim-carry-turn-north-west' and q['frame']==3:
  check(np.array_equal(a[152:174,135:146],b[152:174,135:146]),'reviewed quarter-view hip hardware exact source pixels '+q['gear'])
 if q['gear']=='helmet' and 'canonical idle' not in q['method']:check(np.array_equal(a[:,:,3],b[:,:,3]),'helmet alpha')
 # Geometric edits confined to actual head, never surrounding distant body.
 head=(xx>=x0-25)&(xx<x1+25)&(yy>=y0-25)&(yy<y1+12);check(np.array_equal(a[:,:,3][~head],b[:,:,3][~head]),'body geometry')
for family in ['cancel','distress']:
 for gear in ['bare','helmet']:
  m=json.load(open(P/f'{family}-{gear}-manifest.json'));mapped={q['output']:q for q in proof['records']}
  wm=json.load(open(R/f'character/krusher-water-family-v1/water-{gear}-manifest.json'));core={s['id']:s for s in wm['states']}
  for s in m['states']:
   resolved=inv['resolved'][gear][s['id']];profile=resolved['profile'];check(all(m.get(k)==v for k,v in profile.items() if k not in ['name','status']),'whole root '+s['id']);check({k:v for k,v in s.items() if k not in ['frameFiles','provenance']}=={k:v for k,v in resolved['state'].items() if k not in ['frameFiles','provenance']},'state clocks/events '+s['id'])
   for i,f in enumerate(s['frameFiles']):
    original=resolved['state']['frameFiles'][i];source=R/original[6:] if original.startswith('res://') else (R/resolved['manifest'][6:]).parent/original
    check(np.array_equal(arr(source),arr(R/mapped[f]['source'])),'every slot donor '+gear+s['id'])
   check(s['provenance']['sourceProvenance']==resolved['state'].get('provenance',{}),'source derivation retained')
   if family=='cancel':
    origin=resolved['state'].get('provenance',{});entrance=origin.get('entrance','');index=origin.get('entranceIndex',0)
    if 'release' in s['id']:
     parts=s['id'].split('-');entrance='swim-pickup-'+parts[-1];index=int(parts[-2])
    available=json.load(open(R/'character/krusher-complete-animation-v1/progress.json'))['coverage'][gear]['available']
    if entrance in available:
     em=R/available[entrance]['manifest'][6:];donor=next(v for v in json.load(open(em))['states'] if v['id']==entrance)
     check(np.array_equal(arr(P/s['frameFiles'][0]),arr(em.parent/donor['frameFiles'][index])),'exact indexed cancellation entrance '+gear+s['id'])
    else:check(False,'unresolved cancellation entrance '+gear+s['id']+entrance)
   d=s['id'].rsplit('-',1)[1];gait=arr(R/'character/krusher-water-family-v1'/core['swim-'+d]['frameFiles'][0])
   if family=='distress':
    padded=np.zeros((360,256,4),dtype=np.uint8);padded[96:]=gait[:264];check(not gait[264:,:,3].any(),'padding does not crop artwork')
    for i in [0,-1]:check(np.array_equal(arr(P/s['frameFiles'][i]),padded),'distress whole padded gait join '+gear+s['id'])
   else:check(np.array_equal(arr(P/s['frameFiles'][-1]),gait),'cancel complete empty gait join '+gear+s['id'])
result={'checks':checks,'errors':errors,'scope':'Whole source pixels, hashes, protected geometry/material, complete root/state metadata and event clocks; every cancellation final gait and padded distress endpoint. Native station lifecycle/contact and full-library visual acceptance remain open.'};(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':checks,'errors':errors}));assert not errors

