from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
P=Path(__file__).resolve().parent;N=P/'review/native'
report=json.loads((N/'report.json').read_text());run=json.loads((N/'run-verification.json').read_text());manifest=json.loads((P/'action-manifest.json').read_text());checks=0;errors=[];captures={}
def check(ok,name):
    global checks
    checks+=1
    if not ok:errors.append(name)
check(run['engineExit']==0,'native engine exit');check(not run['ownerFilesChanged'],'owner files unchanged');check(not report['errors'],'native capture errors');check(report['renderer']!='headless','real native display')
expected=[(s,i,path,s['frameDurationsMs'][i]) for s in manifest['states'] for i,path in enumerate(s['frameFiles'])]
check(len(expected)==len(report['samples']),'native coverage count')
bill=None
for (state,index,path,duration),sample in zip(expected,report['samples']):
    check((state['id'],index,path,duration)==(sample['state'],sample['index'],sample['source'],sample['durationMs']),'native source/time binding')
    check(duration<=sample['observedHoldMs']<duration+120,'native hold bound')
    im=np.array(Image.open(N/sample['capture']).convert('RGBA'));check(im.shape==(720,1200,4),sample['capture']+' viewport')
    fixed=im[95:463,100:468];check(bill is None or np.array_equal(bill,fixed),'Bill comparison stable');bill=fixed
    captures[(state['id'],index)]=im[95:463,580:948]
raise_state,typing,lower=manifest['states']
idle=captures[(raise_state['id'],0)]
check(np.array_equal(idle,captures[(lower['id'],lower['frameCount']-1)]),'native idle endpoints exact')
held=captures[(raise_state['id'],raise_state['frameCount']-1)]
for key in [(typing['id'],0),(typing['id'],typing['frameCount']-1),(lower['id'],0)]:check(np.array_equal(held,captures[key]),'native held join exact')
mask=np.array(Image.open(P/'release-mask.png').resize((368,368),Image.Resampling.NEAREST))>0;mask=binary_dilation(mask,iterations=2)
release=captures[(lower['id'],lower['frameCount']-2)]
check(np.array_equal(release[~mask],idle[~mask]),'native release protected pixels, filter edge allowance')
result={'checks':checks,'errors':errors,'scope':'native standalone art rendering and prescribed pose holds; no gameplay integration or continuous-motion acceptance','captureCount':len(captures)}
(N/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(bool(errors))
