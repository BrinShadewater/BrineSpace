"""Select the reviewed six whole poses without changing other effective states."""
from pathlib import Path
import json,hashlib,copy,shutil
ROOT=Path(__file__).resolve().parents[1];CAT=ROOT/'character/marsh-v2/catalog.json'
SOURCE=ROOT/'character/marsh-west-walk-family-contact-v1'
OUT=ROOT/'character/marsh-v2/supplemental/west-walk-polish-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inv=json.loads((ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-east-walk/inventory.json').read_text())
assert sha(CAT)==inv['catalog']['sha256']
for e in inv['orderedBodyManifests']:assert sha(ROOT/e['path'])==e['sha256']
reviewpath=ROOT/'character/marsh-west-walk-family-detail-v1/review.json'
review=json.loads(reviewpath.read_text())
native=json.loads((SOURCE/'world-review/verification.json').read_text())
assert native['checks']==1561 and native['failures']==0 and all(b['reviewed'] for b in native['boards'])
assert not OUT.exists()
for r in review['records']:assert sha(SOURCE/f"{r['slot']:03}.png")==r['frameSha256'] and r['soleDisplacement']==0
# Crown-only closing residual is recorded; exact soles and reviewed station geometry retained.
crowns=[r['opaqueBounds'][1] for r in review['records']]
assert max(abs(crowns[(i+1)%6]-crowns[i]) for i in range(6))==3
before=CAT.read_bytes();catalog=json.loads(before)
def effective(c):
    states={}
    for rel in c['body']:
        p=(CAT.parent/rel).resolve();m=json.loads(p.read_text())
        for s in m['states']:states[s['id']]={'state':s,'pivot':m['pivot'],'standingHeight':m['standingHeight']}
    return states
old=effective(catalog);assert len(old)==228
OUT.mkdir();(OUT/'catalog-before.json').write_bytes(before)
for i in range(6):shutil.copyfile(SOURCE/f'{i:03}.png',OUT/f'{i:03}.png')
manifest=json.loads((SOURCE/'manifest.json').read_text())
manifest['states'][0]['frameFiles']=['res://'+(OUT/f'{i:03}.png').relative_to(ROOT).as_posix() for i in range(6)]
manifest['normalAdmission']=True;manifest['fullGoalComplete']=False
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
catalog['body'].append((OUT/'manifest.json').relative_to(CAT.parent).as_posix())
new=effective(catalog);changed=[k for k in old if old[k]!=new[k]];assert changed==['walk-west']
state=copy.deepcopy(new['walk-west']);state['state']['frameFiles']=old['walk-west']['state']['frameFiles'];assert state==old['walk-west']
CAT.write_text(json.dumps(catalog,indent=2)+'\n')
receipt={'normalAdmission':True,'fullGoalComplete':False,'catalogBeforeSha256':hashlib.sha256(before).hexdigest(),'catalogAfterSha256':sha(CAT),'changedStates':changed,'unchangedEffectiveStates':227,'bodyStates':228,'bodySlots':sum(len(x['state']['frameFiles']) for x in new.values()),'bodyManifests':len(catalog['body']),'oldState':old['walk-west'],'newState':new['walk-west'],'sourceReviewSha256':sha(reviewpath),'crownSequence':crowns,'maxAdjacentCrownChange':3,'residual':'Closing crown3nativepixels vs original2; extra1=.441081worldunits at65.28/148, original soles exact. Reviewed closing/source and station-density board; no forced anatomical fit. Source/native validation of normal selected family follows.'}
(OUT/'admission.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Selected six reviewed West walk poses;227effective states/metadata preserved;228states1190slots91body manifests.')
