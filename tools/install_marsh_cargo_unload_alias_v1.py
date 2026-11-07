"""Align retained same-action aliases with selected reviewed whole unload sources."""
from pathlib import Path
import hashlib,json,copy
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-v2/supplemental/cargo-unload-matched-v1'
CAT=ROOT/'character/marsh-v2/catalog.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before_bytes=CAT.read_bytes();before_sha=sha(CAT)
catalog=json.loads(CAT.read_text());before=copy.deepcopy(catalog);selected={}
for rel in catalog['body']:
    path=(CAT.parent/rel).resolve();data=json.loads(path.read_text())
    for state in data['states']:selected[state['id']]=(path,data,state)
assert not BASE.exists(),'Do not overwrite admission'
states=[];receipts=[]
for d in ['east','west','north','south']:
    op,om,old=selected['cargo-unload-'+d];np,nm,new=selected['unload-'+d]
    assert om['pivot']==nm['pivot'] and om['standingHeight']==nm['standingHeight']
    assert old['frameDurationsMs']==new['frameDurationsMs'] and old['loop']==new['loop']==False
    assert len(old['frameFiles'])==len(new['frameFiles'])==4
    revised=copy.deepcopy(old);revised['frameFiles']=new['frameFiles']
    assert all(p.startswith('res://') for p in revised['frameFiles'])
    states.append(revised)
    receipts.append({'id':old['id'],'oldManifest':op.relative_to(ROOT).as_posix(),'oldManifestSha256':sha(op),'oldState':old,'newSourceState':new['id'],'newManifest':np.relative_to(ROOT).as_posix(),'newManifestSha256':sha(np),'selectedSources':[{'path':p,'sha256':sha(ROOT/p.removeprefix('res://'))} for p in revised['frameFiles']]})
manifest={'version':1,'canvas':[184,184],'pivot':[92,172],'standingHeight':148,'states':states,'normalAdmission':True,'fullGoalComplete':False,'revision':'Whole selected unload sources reused for retained cargo-unload same-action aliases; original metadata preserved.'}
BASE.mkdir();(BASE/'catalog-before.json').write_bytes(before_bytes)
mp=BASE/'manifest.json';mp.write_text(json.dumps(manifest,indent=2)+'\n')
catalog['body'].append(mp.relative_to(CAT.parent).as_posix());CAT.write_text(json.dumps(catalog,indent=2)+'\n')
(BASE/'selection.json').write_text(json.dumps({'manifests':[mp.relative_to(ROOT).as_posix()],'states':4,'slots':16},indent=2)+'\n')
(BASE/'admission.json').write_text(json.dumps({'catalogBefore':before,'catalogBeforeSha256':before_sha,'catalogAfterSha256':sha(CAT),'manifestSha256':sha(mp),'aliases':receipts,'changedStates':[s['id'] for s in states],'unchangedStates':224,'normalAdmission':True,'fullGoalComplete':False},indent=2)+'\n')
print('4retained aliases/16slots aligned;224other states preserved;whole selected sources reused')
