"""Admit the reviewed North walk and phase-specific stop-entry aliases together."""
from pathlib import Path
import json,hashlib,copy,shutil
ROOT=Path(__file__).resolve().parents[1];CAT=ROOT/'character/marsh-v2/catalog.json'
SOURCE=ROOT/'character/marsh-north-walk-family-detail-v1'
OUT=ROOT/'character/marsh-v2/supplemental/north-walk-polish-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inv=json.loads((ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-west-walk/inventory.json').read_text())
assert sha(CAT)==inv['catalog']['sha256']
for e in inv['orderedBodyManifests']:assert sha(ROOT/e['path'])==e['sha256']
r=json.loads((SOURCE/'native-acceptance-review.json').read_text())
assert r['reviewed'] and (r['checks'],r['failures'],r['boardsReviewed'])==(3816,0,18)
assert sha(SOURCE/'manifest.json')==r['manifestSha256']
assert sha(SOURCE/'stop-entry-aliases.json')==r['stopEntryAliasesSha256']
assert sha(SOURCE/'world-review/verification.json')==r['verificationSha256']
v=json.loads((SOURCE/'world-review/verification.json').read_text())
assert all(b['reviewed'] and sha(ROOT/b['path'])==b['sha256'] for b in v['boards'])
assert v['bothActorsVisibleAgainstBlank'] and v['minimumVisibilityDifference']>80
assert not OUT.exists()
def effective(c):
 states={}
 for rel in c['body']:
  p=(CAT.parent/rel).resolve();m=json.loads(p.read_text())
  for s in m['states']:
   s=copy.deepcopy(s)
   s['frameFiles']=['res://'+(ROOT/f.removeprefix('res://') if f.startswith('res://') else (p.parent/f).resolve()).relative_to(ROOT).as_posix() for f in s['frameFiles']]
   states[s['id']]={'state':s,'pivot':m['pivot'],'standingHeight':m['standingHeight']}
 return states
before=CAT.read_bytes();catalog=json.loads(before);old=effective(catalog)
assert len(old)==228 and len(catalog['body'])==91
manifest=json.loads((SOURCE/'manifest.json').read_text());keys=[s['id'] for s in manifest['states']]
assert keys==['walk-north']+['walk-stop-p%d-north'%i for i in range(6)]
# Validate complete metadata and all later stop paths before modifying the catalogue.
for s in manifest['states']:
 check=copy.deepcopy(s);check['frameFiles']=old[s['id']]['state']['frameFiles'];assert check==old[s['id']]['state']
 assert manifest['pivot']==old[s['id']]['pivot'] and manifest['standingHeight']==old[s['id']]['standingHeight']
 if s['id']!='walk-north':assert s['frameFiles'][1:]==old[s['id']]['state']['frameFiles'][1:]
OUT.mkdir();(OUT/'catalog-before.json').write_bytes(before)
for i in range(6):shutil.copyfile(SOURCE/f'{i:03}.png',OUT/f'{i:03}.png')
for s in manifest['states']:
 s['frameFiles']=[f.replace('res://character/marsh-north-walk-family-detail-v1/','res://character/marsh-v2/supplemental/north-walk-polish-v1/') for f in s['frameFiles']]
manifest['normalAdmission']=True;manifest['fullGoalComplete']=False
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
catalog['body'].append((OUT/'manifest.json').relative_to(CAT.parent).as_posix());new=effective(catalog)
changed=[k for k in old if old[k]!=new[k]];assert set(changed)==set(keys)
for k in changed:
 x=copy.deepcopy(new[k]);x['state']['frameFiles']=old[k]['state']['frameFiles'];assert x==old[k]
assert sum(sum(a!=b for a,b in zip(old[k]['state']['frameFiles'],new[k]['state']['frameFiles'])) for k in changed)==12
CAT.write_text(json.dumps(catalog,indent=2)+'\n')
receipt={'normalAdmission':True,'fullGoalComplete':False,'catalogBeforeSha256':hashlib.sha256(before).hexdigest(),'catalogAfterSha256':sha(CAT),'changedStates':changed,'unchangedEffectiveStates':221,'changedSlots':12,'uniqueRevisedDrawings':6,'unchangedLaterStopFrames':24,'bodyStates':228,'bodySlots':sum(len(x['state']['frameFiles']) for x in new.values()),'bodyManifests':len(catalog['body']),'oldStates':{k:old[k] for k in keys},'newStates':{k:new[k] for k in keys},'sourceNativeAcceptanceSha256':sha(SOURCE/'native-acceptance-review.json'),'limits':'Source admission proven; actual normal catalogue loading/native review follows.'}
(OUT/'admission.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('North walk +six stop entries selected:7states/12slots/6drawings; other221states and24later stop drawings exact;228states1190slots92manifests.')
