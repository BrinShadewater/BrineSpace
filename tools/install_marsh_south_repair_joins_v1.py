from pathlib import Path
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[1]
STUDY=ROOT/'character/marsh-south-repair-joins-v1'
CATALOG=ROOT/'character/marsh-v2/catalog.json'
TARGET=ROOT/'character/marsh-v2/supplemental/south-repair-joins-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def effective(catalog):
 states={}
 for rel in catalog['body']:
  path=(CATALOG.parent/rel).resolve();m=json.loads(path.read_text())
  for s in m['states']:
   frames=[ROOT/f.removeprefix('res://') if f.startswith('res://') else (path.parent/f).resolve() for f in s['frameFiles']]
   states[s['id']]={'state':s,'header':{k:v for k,v in m.items() if k!='states'},'frames':[sha(p) for p in frames]}
 return states
receipt=json.loads((STUDY/'staged-acceptance.json').read_text())
assert receipt['reviewed'] and receipt['failures']==0 and receipt['ownerStable']
assert sha(STUDY/'staged-native-transitions.png')==receipt['boardSha256']
assert sha(STUDY/'complete-source-comparison.png')==receipt['sourceBoardSha256']
assert sha(STUDY/'candidate-manifest.json')==receipt['candidateSha256']
assert CATALOG.read_bytes()==(STUDY/'catalog-before.json').read_bytes()
frozen=json.loads((ROOT/'output/marsh-animation-audit/repair-joins-staged-v1-2026-10-04/inputs-before.json').read_text())
for rel,h in frozen.items():
 if rel.startswith('character/') or rel.startswith('scripts/marsh') or rel=='scripts/crew_life.gd':assert sha(ROOT/rel)==h,rel
catalog=json.loads(CATALOG.read_text());before=effective(catalog)
candidate=json.loads((STUDY/'candidate-manifest.json').read_text());keys=['kneel-south','stand-south']
assert [s['id'] for s in candidate['states']]==keys
for entry in candidate['states']:
 old=before[entry['id']]
 assert {k:v for k,v in old['state'].items() if k!='frameFiles'}=={k:v for k,v in entry.items() if k!='frameFiles'}
 assert old['header']=={k:v for k,v in candidate.items() if k!='states'}
assert not TARGET.exists();TARGET.mkdir()
(TARGET/'manifest.json').write_bytes((STUDY/'candidate-manifest.json').read_bytes())
(TARGET/'catalog-before.json').write_bytes(CATALOG.read_bytes())
catalog['body'].append('supplemental/south-repair-joins-v1/manifest.json')
CATALOG.write_text(json.dumps(catalog,indent=2)+'\n',encoding='utf-8')
after=effective(catalog);assert before.keys()==after.keys()
changed=[key for key in before if before[key]!=after[key]];assert sorted(changed)==sorted(keys),changed
for key in keys:
 assert before[key]['header']==after[key]['header']
 assert {k:v for k,v in before[key]['state'].items() if k!='frameFiles'}=={k:v for k,v in after[key]['state'].items() if k!='frameFiles'}
admission={'normalAdmission':True,'catalogBeforeSha256':sha(TARGET/'catalog-before.json'),'catalogAfterSha256':sha(CATALOG),'changedStates':changed,'changedSlots':6,'unchangedEffectiveStates':len(before)-2,'bodyStates':len(after),'bodySlots':sum(len(s['state']['frameFiles']) for s in after.values()),'bodyManifests':len(catalog['body']),'source':'Three existing selected whole PNGs reused. Neutral-B-A kneel, A-B-neutral stand. No new generated or edited image.','stagedReceiptSha256':sha(STUDY/'staged-acceptance.json'),'oldStates':{k:before[k] for k in keys},'newStates':{k:after[k] for k in keys}}
(TARGET/'admission.json').write_text(json.dumps(admission,indent=2)+'\n',encoding='utf-8')
print('Installed 2 states/6 slots; other226states and all timing/pivot/density unchanged.')
