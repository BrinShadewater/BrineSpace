"""Admit one whole revised pose without changing the short-step contract."""
from pathlib import Path
import copy,json,hashlib
ROOT=Path(__file__).resolve().parents[1];CAT=ROOT/'character/marsh-v2/catalog.json'
BASE=ROOT/'character/marsh-v2/supplemental/south-step-detail-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before_bytes=CAT.read_bytes();catalog=json.loads(before_bytes);before=copy.deepcopy(catalog);selected=None
for rel in catalog['body']:
    mp=(CAT.parent/rel).resolve();m=json.loads(mp.read_text())
    for s in m['states']:
        if s['id']=='walk-step-south':selected=(mp,m,s)
assert selected and not BASE.exists()
mp,m,state=selected;old=copy.deepcopy(state);new=copy.deepcopy(state)
files=[ROOT/p.removeprefix('res://') if p.startswith('res://') else (mp.parent/p).resolve() for p in state['frameFiles']]
assert len(files)==7
source=ROOT/'character/marsh-south-step-detail-v1/candidate-02-frame.png'
BASE.mkdir();(BASE/'catalog-before.json').write_bytes(before_bytes)
dest=BASE/'phase-003.png';dest.write_bytes(source.read_bytes())
new['frameFiles']=['res://'+p.relative_to(ROOT).as_posix() for p in files]
new['frameFiles'][3]='res://'+dest.relative_to(ROOT).as_posix()
manifest={k:v for k,v in m.items() if k!='states'};manifest['states']=[new]
manifest.update(normalAdmission=True,fullGoalComplete=False,revision='South short-step phase3 whole detail revision02; original seven-state action metadata and six other drawings preserved.')
out=BASE/'manifest.json';out.write_text(json.dumps(manifest,indent=2)+'\n')
catalog['body'].append(out.relative_to(CAT.parent).as_posix());CAT.write_text(json.dumps(catalog,indent=2)+'\n')
(BASE/'selection.json').write_text(json.dumps({'manifests':[out.relative_to(ROOT).as_posix()],'states':1,'slots':7},indent=2)+'\n')
(BASE/'admission.json').write_text(json.dumps({'catalogBefore':before,'catalogBeforeSha256':hashlib.sha256(before_bytes).hexdigest(),'catalogAfterSha256':sha(CAT),'oldManifest':mp.relative_to(ROOT).as_posix(),'oldManifestSha256':sha(mp),'oldState':old,'newState':new,'revisedSlot':3,'originalSources':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in files],'wholeSource':source.relative_to(ROOT).as_posix(),'wholeSourceSha256':sha(source),'normalAdmission':True,'fullGoalComplete':False},indent=2)+'\n')
print('1state/1whole pose revised;6other step drawings and227other states preserved')
