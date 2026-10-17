from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
m=json.loads((P/'action-manifest.json').read_text());original=np.array(Image.open(R/m['canonicalIdleSource']).convert('RGBA'));mask=np.array(Image.open(P/'patch-mask.png'))>0
errors=[];checks=0
def check(ok,name):
    global checks
    checks+=1
    if not ok:errors.append(name)
check(hashlib.sha256((R/m['canonicalIdleSource']).read_bytes()).hexdigest()==m['canonicalIdleSha256'],'canonical source unchanged')
for i in range(8):
    a=np.array(Image.open(P/f'frames/{i:03}.png').convert('RGBA'))
    check(a.shape==(184,184,4),f'{i} canvas')
    check(np.array_equal(a[~mask],original[~mask]),f'{i} protected pixels')
    check(np.array_equal(a[:62],original[:62]) and np.array_equal(a[106:],original[106:]),f'{i} head and legs')
for s in m['states']:
    apng=Image.open(P/f'review/{s["id"]}.png')
    check(apng.n_frames==s['frameCount'],s['id']+' count')
    for i,path in enumerate(s['frameFiles']):
        apng.seek(i)
        check(np.array_equal(np.array(apng.convert('RGBA')),np.array(Image.open(P/path).convert('RGBA'))),s['id']+f' decode {i}')
        check(round(apng.info['duration'])==s['frameDurationsMs'][i],s['id']+f' duration {i}')
raise_state,typing,lower=m['states']
check(raise_state['frameFiles'][0]==lower['frameFiles'][-1]=='frames/000.png','exact idle aliases')
check(raise_state['frameFiles'][-1]==typing['frameFiles'][0]==typing['frameFiles'][-1]==lower['frameFiles'][0],'exact held joins')
result={'checks':checks,'errors':errors,'visualAcceptance':False,'coverage':'west bare raise/type/lower candidate'}
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(bool(errors))
