from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
m=json.loads((P/'action-manifest.json').read_text());p=json.loads((P/'provenance.json').read_text());original=np.array(Image.open(R/m['canonicalIdleSource']).convert('RGBA'));mask=np.array(Image.open(P/'release-mask.png'))>0
checks=0;errors=[]
def check(ok,name):
    global checks
    checks+=1
    if not ok:errors.append(name)
check(hashlib.sha256((R/m['canonicalIdleSource']).read_bytes()).hexdigest()==m['canonicalIdleSha256'],'original idle unchanged')
check(hashlib.sha256((P/p['source']).read_bytes()).hexdigest()==p['sourceSha256'],'generated source unchanged')
for path,h in p['sourceHashes'].items():check(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'prior candidate unchanged '+path)
release=np.array(Image.open(P/'frames/release.png').convert('RGBA'))
check(np.array_equal(release[~mask],original[~mask]),'outside near glove/forearm exact')
check(np.array_equal(release[92:108,88:96],original[92:108,88:96]),'clipped hardware exact')
check(np.array_equal(release[:84],original[:84]) and np.array_equal(release[110:],original[110:]),'head and lower body exact')
for state in m['states']:
    apng=Image.open(P/f'review/{state["id"]}.png')
    check(apng.n_frames==state['frameCount'],state['id']+' count')
    for i,path in enumerate(state['frameFiles']):
        im=Image.open(P/path).convert('RGBA');apng.seek(i)
        check(im.size==(184,184),path+' size')
        check(np.array_equal(np.array(apng.convert('RGBA')),np.array(im)),path+' APNG decode')
        check(round(apng.info['duration'])==state['frameDurationsMs'][i],path+' duration')
rise,typing,lower=m['states'];check(rise['frameFiles'][0]==lower['frameFiles'][-1]=='frames/idle.png','idle aliases');check(rise['frameFiles'][-1]==typing['frameFiles'][0]==typing['frameFiles'][-1]==lower['frameFiles'][0],'held aliases')
check(np.array_equal(np.array(Image.open(P/'frames/idle.png')),original),'idle pixels exact')
result={'checks':checks,'errors':errors,'visualAcceptance':False,'coverage':'west bare raise6/type6/lower7 representative candidate'}
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(bool(errors))
