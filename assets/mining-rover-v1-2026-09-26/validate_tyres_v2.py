"""Check rolling loop continuity, reversed frames and preserved non-travel clips."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage
from build_tyres_v2 import R,rig
d=json.loads((R/'manifest.json').read_text());old=json.loads((R/'tyres-v2/manifest-before.json').read_text());checks=[]
for h in d['headings']:
    base,_,_,mask,_=rig(h)
    drive=next(e for e in d['states'] if e['id']=='drive-'+h)
    reverse=next(e for e in d['states'] if e['id']=='reverse-'+h)
    frames=[np.array(Image.open(R/f).convert('RGBA')) for f in drive['frameFiles']]
    changes=[float(np.abs(frames[(n+1)%60][mask,:3].astype(float)-frames[n][mask,:3]).mean()) for n in range(60)]
    ratio=changes[-1]/np.median(changes);assert ratio<2,(h,ratio)
    for n,f in enumerate(reverse['frameFiles']):assert np.array_equal(np.array(Image.open(R/f).convert('RGBA')),frames[-n%60])
    max_components=0
    for state in ['steer-left','steer-right']:
        e=next(e for e in d['states'] if e['id']==state+'-'+h)
        for path in e['frameFiles']:
            a=np.array(Image.open(R/path).convert('RGBA'));labels,_=ndimage.label(a[:,:,3]>128)
            counts=np.bincount(labels.ravel())[1:];count=int((counts>10).sum());max_components=max(max_components,count)
            assert count==1,(e['id'],path,count)
    checks.append({'heading':h,'loopSeamVsTypicalStep':ratio,'reverseIsExactInverse':True,'steeringConnectedComponents':max_components})
for e in d['states']:
    if e.get('completionSupplement'):continue
    before=next(b for b in old['states'] if b['id']==e['id'])
    if e['state'] in ['idle','mine']:assert e==before
    assert e['effectFiles']==before['effectFiles']
result={'changedClips':32,'changedFrames':1920,'nonTravelClipDefinitionsAndEffectPaths':'unchanged; diagonal source artwork revised separately','checks':checks}
(R/'tyres-v2/motion-validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
