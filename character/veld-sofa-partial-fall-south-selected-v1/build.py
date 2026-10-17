from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];S=R/'character/veld-sofa-partial-fall-south-v1'
bindings={}
for gear in ['bare','helmet']:
    path=S/f'{gear}-manifest.json';raw=path.read_bytes();d=json.loads(raw)
    bindings[path.relative_to(R).as_posix()]=hashlib.sha256(raw).hexdigest()
    assert len(d['states'])==6 and d['standingHeight']==148 and d['pivot']==[128,224]
    d['name']='Veld selected South partial sofa falls '+gear
    admission=P/'normal-admission.json'
    d['status']='selected' if admission.exists() and json.loads(admission.read_text(encoding='utf-8'))['normalVerificationPassed'] else 'selected_pending_normal_verification'
    (P/f'{gear}-manifest.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
(P/'source-bindings.json').write_text(json.dumps(bindings,indent=2)+'\n',encoding='utf-8')
print('Paired normal bundle references same72source slots; no source changes')
