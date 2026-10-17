from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;inv=json.load(open(R/'character/krusher-complete-animation-v1/source-coverage.json'));proof=json.load(open(R/'character/krusher-water-family-v1/provenance.json'));original_records={(q['gear'],q['state'],q['frame']):q for q in proof['records']}; revision=json.load(open(P/'revision.json')); proof={'records':[dict(original_records[(q['gear'],q['state'],q['frame'])], **dict(q,source=q['source'][6:],allowedMask=q['mask'])) for q in revision['records']]}; checks=0;errors=[]
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
 # Independently inspect foreground regions, separate from the producer's allowed mask.
 k=q['state'];step=q['frame'] if k.startswith('swim-start-') else 5-q['frame'] if k.startswith('swim-stop-') else 5 if k.startswith('swim-') else 0
 hands=(xx>=168) if d=='east' else (xx<=87) if d=='west' else (yy>=y1+4) if d=='south' and step>=2 else (yy<y0-18) if d=='north' and step>=2 else None
 # Bowed south start pose4 puts the visor chin below the old skull box.
 # Visually inspected glove ROI starts at row150; original face ends at148.
 if d=='south' and step==4 and q['gear']=='helmet':hands=(yy>=150)
 if hands is not None:check(np.array_equal(a[hands],b[hands]),'foreground source hands/arms '+q['output'])
 if q['gear']=='helmet' and 'canonical idle' not in q['method']:check(np.array_equal(a[:,:,3],b[:,:,3]),'helmet alpha')
 # Geometric edits confined to actual head, never surrounding distant body.
 head=(xx>=x0-25)&(xx<x1+25)&(yy>=y0-25)&(yy<y1+12);check(np.array_equal(a[:,:,3][~head],b[:,:,3][~head]),'body geometry')
for family in ['water']:
 for gear in ['bare','helmet']:
  m=json.load(open(P/f'{family}-{gear}-manifest.json'))
  for s in m['states']:
   resolved=inv['resolved'][gear][s['id']];profile=resolved['profile'];check(all(m.get(k)==v for k,v in profile.items() if k not in ['name','status']),'whole source root profile '+s['id']);check({k:v for k,v in s.items() if k not in ['frameFiles','provenance']}=={k:v for k,v in resolved['state'].items() if k not in ['frameFiles','provenance']},'source timing metadata '+s['id']);check(len(s['frameFiles'])==6,'six source poses')
  states={s['id']:s for s in m['states']}
  for d in ['east','north','south','west']:
   start=states['swim-start-'+d]['frameFiles'];stop=states['swim-stop-'+d]['frameFiles']
   for left,right in [(start[0],states['tread-'+d]['frameFiles'][0]),(start[-1],states['swim-'+d]['frameFiles'][0]),(stop[0],states['swim-'+d]['frameFiles'][0]),(stop[-1],states['tread-'+d]['frameFiles'][0])]:check(np.array_equal(arr(P/left),arr(P/right)),'whole pose entry/exit join '+gear+d)
   check(all(np.array_equal(arr(P/a),arr(P/b)) for a,b in zip(start,reversed(stop))),'exact reversed start/stop choreography '+gear+d)
   for kind in ['swim','tread']:check(np.array_equal(arr(P/states[kind+'-'+d]['frameFiles'][0]),arr(P/states[kind+'-'+d]['frameFiles'][-1])),'exact authored wrap '+gear+kind+d)

for q in proof['records']:
 if 'Existing manually' in q.get('details',{}).get('method',''):check(sha(R/q['source'])==sha(P/q['output']),'retained pose byte exact')
 check(np.array_equal(arr(R/q['source'])[q['protectedFromRow']:],arr(P/q['output'])[q['protectedFromRow']:]),'lower body byte exact')
for name in ['water-bare-manifest.json', 'water-helmet-manifest.json']:
 check(json.load(open(P/name))==json.load(open(R/'character/krusher-water-family-v1'/name)),'whole manifest unchanged '+name)

result={'checks':checks,'errors':errors,'scope':'Whole source profiles, original canvases/pivots, exact state timing and flags, all source/output/head hashes, protected pixels, helmet geometry, independently selected foreground hand/arm regions, distant body/legs, all32entry/exit joins,8reversed start/stop choreographies and16exact loop endpoints. Does not establish full station lifecycle/contact acceptance.'};(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':checks,'errors':errors}));assert not errors
