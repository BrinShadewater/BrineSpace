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
for family in ['cargo','turn','cargo-turn']:
 for gear in ['bare','helmet']:
  m=json.load(open(P/f'{family}-{gear}-manifest.json'));mapped={q['output']:q for q in proof['records']}
  for s in m['states']:
   resolved=inv['resolved'][gear][s['id']];profile=resolved['profile'];check(all(m.get(k)==v for k,v in profile.items() if k not in ['name','status']),'whole source root profile '+s['id']);check({k:v for k,v in s.items() if k not in ['frameFiles','provenance']}=={k:v for k,v in resolved['state'].items() if k not in ['frameFiles','provenance']},'source timing metadata '+s['id']);check(len(s['frameFiles'])==len(resolved['state']['frameFiles']),'original pose count')
   for i,f in enumerate(s['frameFiles']):
    original_file=resolved['state']['frameFiles'][i];source=R/original_file[6:] if original_file.startswith('res://') else (R/resolved['manifest'][6:]).parent/original_file
    check(np.array_equal(arr(source),arr(R/mapped[f]['source'])),'equivalent whole source pixels for every referenced slot '+gear+s['id'])
  states={s['id']:s for s in m['states']}
  wm=json.load(open(R/f'character/krusher-water-family-v1/water-{gear}-manifest.json'));core={s['id']:s for s in wm['states']}
  cm=json.load(open(P/f'cargo-{gear}-manifest.json'));cargo={s['id']:s for s in cm['states']}
  sm=json.load(open(R/f'character/krusher-recovery-salvage-v1/salvage-{gear}-manifest.json'));salvage={s['id']:s for s in sm['states']}
  for key,s in states.items():
   if family=='cargo':
    d=key.rsplit('-',1)[1]
    if key.startswith('swim-pickup-'):
     check(np.array_equal(arr(P/s['frameFiles'][0]),arr(R/'character/krusher-recovery-salvage-v1'/salvage['salvage-'+d]['frameFiles'][0])),'salvage-to-pickup exact whole pose '+gear+key)
     check(np.array_equal(arr(P/s['frameFiles'][-1]),arr(P/cargo['swim-carry-'+d]['frameFiles'][0])),'pickup-to-carry exact whole pose '+gear+key)
    else:check(np.array_equal(arr(P/s['frameFiles'][0]),arr(P/s['frameFiles'][-1])),'carry closed-loop shared pose '+gear+key)
   else:
    origin,target=key.split('-')[-2:];prefix='swim' if family=='turn' else 'swim-carry';path=R/'character/krusher-water-family-v1' if family=='turn' else P;gaits=core if family=='turn' else cargo
    for index,d in [(0,origin),(-1,target)]:check(np.array_equal(arr(P/s['frameFiles'][index]),arr(path/gaits[prefix+'-'+d]['frameFiles'][0])),'exact turn-to-gait whole pose '+gear+key)
    reverse=states[prefix+'-turn-'+target+'-'+origin]
    source=inv['resolved'][gear][key];rev=inv['resolved'][gear][reverse['id']]
    def original(q,f):return R/f[6:] if f.startswith('res://') else (R/q['manifest'][6:]).parent/f
    if all(np.array_equal(arr(original(source,a)),arr(original(rev,b))) for a,b in zip(source['state']['frameFiles'],reversed(rev['state']['frameFiles']))):
     check(all(np.array_equal(arr(P/a),arr(P/b)) for a,b in zip(s['frameFiles'],reversed(reverse['frameFiles']))),'whole reversed source choreography '+gear+key)
result={'checks':checks,'errors':errors,'scope':'Original complete canvases/profiles/state clocks and water flags; source/output/head hashes; protected source pixels, helmet alpha and distant body geometry; complete salvage/pickup/carry and turn/gait pose joins; exact source reversal choreography. Does not prove complete native station lifecycle/contact or final full-library material/camera acceptance.'};(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':checks,'errors':errors}));assert not errors
