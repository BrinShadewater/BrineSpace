from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
report=json.loads((P/'verification.json').read_text());errors=[];checks=0
def check(ok,label):
    global checks
    checks+=1
    if not ok:errors.append(label)
for path,digest in report['sourceHashes'].items():check(hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,'source changed '+path)
for record in report['records']:
    a=np.array(Image.open(R/record['source']).convert('RGBA'));b=np.array(Image.open(P/record['output']).convert('RGBA'));m=np.array(Image.open(P/record['mask']))>0
    check(b.shape==(184,184,4),record['output']+' size')
    check(np.array_equal(a[~m],b[~m]),record['output']+' protected pixels')
    check(np.array_equal(a[125:],b[125:]),record['output']+' feet/lower legs')
for variant in ['bare','helmet']:
    manifest=json.loads((P/f'{variant}-manifest.json').read_text())
    source=json.loads((R/f'character/krusher-bill-base-test-v2/{variant}-manifest.json').read_text())
    check(manifest['pivot']==source['pivot'],variant+' pivot')
    for s,old in zip(manifest['states'],source['states']):
        check(s['frameDurationsMs']==old['frameDurationsMs'],variant+s['id']+' durations')
        animation=Image.open(P/f'review/{variant}-{s["id"]}.png')
        check(animation.n_frames==len(s['frameFiles']),variant+s['id']+' APNG count')
        for i,path in enumerate(s['frameFiles']):
            animation.seek(i)
            check(np.array_equal(np.array(animation.convert('RGBA')),np.array(Image.open(P/path).convert('RGBA'))),path+' APNG decode')
result={'checks':checks,'errors':errors,'frames':len(report['records']),'visualAcceptance':False}
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(bool(errors))
