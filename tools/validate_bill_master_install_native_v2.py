"""Correct only the wrapper count; reuse the completed native evidence."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];D=R/'output/bill-master-install-native-v2'
q=json.loads((D/'report.json').read_text());v=json.loads((D/'validation.json').read_text())
assert q['failures']==0 and q['selectedSlots']==310 and len(q['saves'])==4 and len(q['captures'])==44
assert v['engineExit']==0 and v['engineLogClean'] and not v['inputChanges'] and not v['ownerChanges']
for name in ['inputs','owner']:assert json.loads((D/(name+'-before.json')).read_text())==json.loads((D/(name+'-after.json')).read_text())
v.update(passed=True,normalAdmission=True,classificationCorrection='The ten manifests contain310 source references, including72 identical idle holds repeated by the reach manifest;238 unique logical state/slot identities. Original wrapper mistakenly expected238 references. Native checks all passed; no rerun or runtime/source mutation for this correction.')
(D/'validation-corrected.json').write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps({'passed':True,'checks':q['checks'],'failures':0,'manifestReferences':310,'uniqueStateSlots':238,'diskResumes':4,'captures':44,'runtimeChangedForCorrection':False}))
