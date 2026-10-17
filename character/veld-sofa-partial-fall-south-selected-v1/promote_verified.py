"""Descriptive metadata promotion; retain the exact native-test interval bytes."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
O=R/'output/veld-sofa-partial-south-normal-continue-v1'
v=json.loads((O/'validation.json').read_text(encoding='utf-8'))
e=json.loads((P/'normal-continue-review-evidence.json').read_text(encoding='utf-8'))
assert v['passed'] and e['reviewedSourceNativePairs']==72
for relative,digest in e['bindings'].items():assert hashlib.sha256((R/relative).read_bytes()).hexdigest()==digest,relative
before=json.loads((O/'inputs-before.json').read_text(encoding='utf-8'))
proof=P/'verified-manifests';proof.mkdir(exist_ok=True)
changes={}
for gear in ['bare','helmet']:
    path=P/f'{gear}-manifest.json';raw=path.read_bytes();old=json.loads(raw)
    saved=proof/path.name
    if not saved.exists():
        assert hashlib.sha256(raw).hexdigest()==before[path.relative_to(R).as_posix()]
        saved.write_bytes(raw)
    assert hashlib.sha256(saved.read_bytes()).hexdigest()==before[path.relative_to(R).as_posix()]
    new=dict(old);new['status']='selected'
    assert {k:v for k,v in new.items() if k!='status'}=={k:v for k,v in json.loads(saved.read_bytes()).items() if k!='status'}
    path.write_text(json.dumps(new,indent=2)+'\n',encoding='utf-8')
    changes[gear]={'testedManifest':saved.relative_to(R).as_posix(),'testedSHA256':hashlib.sha256(saved.read_bytes()).hexdigest(),'selectedSHA256':hashlib.sha256(path.read_bytes()).hexdigest(),'runtimeMetadataUnchanged':True}
(P/'normal-admission.json').write_text(json.dumps({'normalVerificationPassed':True,'normalReviewPairs':72,'descriptiveOnlyField':'status','manifests':changes,'scope':'24 prescribed normal-world mortality/ordinary disk fresh-main cases; no source/runtime metadata change, full goal still incomplete'},indent=2)+'\n',encoding='utf-8')
print('Paired selected status; exact tested bytes preserved, runtime/source metadata unchanged')
