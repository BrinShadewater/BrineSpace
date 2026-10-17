from pathlib import Path
import json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;N=P/'review/native';report=json.loads((N/'report.json').read_text());run=json.loads((N/'run-verification.json').read_text());bare=json.loads((P/'bare-manifest.json').read_text());helmet=json.loads((P/'helmet-manifest.json').read_text());checks=0;errors=[];captures={};head={}
def check(ok,name):
    global checks
    checks+=1
    if not ok:errors.append(name)
check(run['engineExit']==0,'native exit');check(not run['ownerFilesChanged'],'owner data unchanged');check(not report['errors'],'capture errors');check(report['renderer']!='headless','native display')
expected=[(s,i,path,s['frameDurationsMs'][i],helmet['states'][si]['frameFiles'][i]) for si,s in enumerate(bare['states']) for i,path in enumerate(s['frameFiles'])];check(len(expected)==len(report['samples']),'paired native coverage')
for (s,i,path,duration,gear_path),sample in zip(expected,report['samples']):
    check((s['id'],i,path,duration,gear_path)==(sample['state'],sample['index'],sample['bareSource'],sample['durationMs'],sample['helmetSource']),'paired source/time binding');check(duration<=sample['observedHoldMs']<duration+120,'native hold bound')
    im=np.array(Image.open(N/sample['capture']).convert('RGBA'));check(im.shape==(720,1200,4),'native viewport');left=im[95:463,100:468];right=im[95:463,580:948];check(np.array_equal(left[128:],right[128:]),'rendered body below gear/filter boundary exact')
    for variant,crop in [('bare',left),('helmet',right)]:
        check(variant not in head or np.array_equal(head[variant],crop[:120]),variant+' rendered head/helmet stable');head[variant]=crop[:120]
        captures[(variant,s['id'],i)]=crop
for variant,m in [('bare',bare),('helmet',helmet)]:
    rise,typing,lower=m['states'];check(np.array_equal(captures[(variant,rise['id'],0)],captures[(variant,lower['id'],lower['frameCount']-1)]),variant+' native idle joins exact')
    held=captures[(variant,rise['id'],rise['frameCount']-1)]
    for key in [(typing['id'],0),(typing['id'],typing['frameCount']-1),(lower['id'],0)]:check(np.array_equal(held,captures[(variant,*key)]),variant+' native held join exact')
result={'checks':checks,'errors':errors,'pairedCaptures':len(report['samples']),'scope':'native paired source/timing, rendered body/helmet stability and joins; not continuous-motion or gameplay acceptance'};(N/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(bool(errors))
