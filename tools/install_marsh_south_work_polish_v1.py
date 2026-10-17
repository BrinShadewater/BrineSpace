"""Install reviewed South work drawings and exact idle endpoints across four aliases."""
from pathlib import Path
import json,hashlib,copy,shutil
ROOT=Path(__file__).resolve().parents[1];CAT=ROOT/'character/marsh-v2/catalog.json';SOURCE=ROOT/'character/marsh-south-work-polish-v1';OUT=ROOT/'character/marsh-v2/supplemental/south-work-polish-v1';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inv=json.loads((ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-south-walk/inventory.json').read_text());assert h(CAT)==inv['catalog']['sha256']
for e in inv['orderedBodyManifests']:assert h(ROOT/e['path'])==e['sha256']
for state in inv['states'].values():
 for e in state['frames']:assert h(ROOT/e['path'])==e['sha256']
accept=json.loads((SOURCE/'native-acceptance-review.json').read_text());assert accept['reviewed'] and accept['failures']==0 and accept['boardsReviewed']==4
assert h(SOURCE/'candidate-manifest.json')==accept['manifestSha256'] and h(SOURCE/'world-review/verification.json')==accept['verificationSha256']
for e in json.loads((SOURCE/'world-review/verification.json').read_text())['boards']:assert e['reviewed'] and h(ROOT/e['path'])==e['sha256']
def effective(catalog):
 result={}
 for rel in catalog['body']:
  p=(CAT.parent/rel).resolve();m=json.loads(p.read_text())
  for state in m['states']:
   s=copy.deepcopy(state);s['frameFiles']=['res://'+(ROOT/f.removeprefix('res://') if f.startswith('res://') else (p.parent/f).resolve()).relative_to(ROOT).as_posix() for f in s['frameFiles']];result[s['id']]={'state':s,'pivot':m['pivot'],'standingHeight':m['standingHeight']}
 return result
before=CAT.read_bytes();catalog=json.loads(before);old=effective(catalog);assert len(old)==228 and len(catalog['body'])==93
m=json.loads((SOURCE/'candidate-manifest.json').read_text());keys=[s['id'] for s in m['states']];assert keys==['repair-south','interact-south','inspect-south','salvage-south']
for state in m['states']:
 probe=copy.deepcopy(state);probe['frameFiles']=old[state['id']]['state']['frameFiles'];assert probe==old[state['id']]['state'];assert old[state['id']]['pivot']==m['pivot'] and old[state['id']]['standingHeight']==m['standingHeight']
assert not OUT.exists();OUT.mkdir();(OUT/'catalog-before.json').write_bytes(before)
names={'pilot-000.png':'working-a.png','pilot-001-retry.png':'working-b.png','idle-entry.png':'neutral.png'}
for source,name in names.items():shutil.copyfile(SOURCE/source,OUT/name)
for state in m['states']:state['frameFiles']=['res://'+(OUT/names[Path(f).name]).relative_to(ROOT).as_posix() for f in state['frameFiles']]
m['normalAdmission']=True;(OUT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');catalog['body'].append((OUT/'manifest.json').relative_to(CAT.parent).as_posix());new=effective(catalog)
changed=[k for k in old if old[k]!=new[k]];assert set(changed)==set(keys)
for key in changed:
 probe=copy.deepcopy(new[key]);probe['state']['frameFiles']=old[key]['state']['frameFiles'];assert probe==old[key]
CAT.write_text(json.dumps(catalog,indent=2)+'\n',encoding='utf-8')
receipt={'normalAdmission':True,'catalogBeforeSha256':hashlib.sha256(before).hexdigest(),'catalogAfterSha256':h(CAT),'changedStates':changed,'changedSlots':24,'unchangedEffectiveStates':224,'bodyStates':228,'bodySlots':sum(len(s['state']['frameFiles']) for s in new.values()),'bodyManifests':len(catalog['body']),'uniqueWorkingDrawings':2,'neutralCopySha256':h(OUT/'neutral.png'),'sourceAcceptanceSha256':h(SOURCE/'native-acceptance-review.json'),'oldStates':{k:old[k] for k in keys},'newStates':{k:new[k] for k in keys},'scope':'Source admission. Actual normal renderer validation follows. Unrelated life/furniture neutral aliases remain selected as previously.'}
(OUT/'admission.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print('Installed4states/24slots;224other effective states exact;228states1190slots94body manifests')
