from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;m=json.loads((P/'action-manifest.json').read_text());p=json.loads((P/'provenance.json').read_text());original=np.array(Image.open(R/m['canonicalIdleSource']).convert('RGBA'));checks=0;errors=[]
def check(ok,name):
    global checks
    checks+=1
    if not ok:errors.append(name)
check(hashlib.sha256((R/m['canonicalIdleSource']).read_bytes()).hexdigest()==m['canonicalIdleSha256'],'corrected master unchanged')
check(hashlib.sha256((P/'frames/idle.png').read_bytes()).hexdigest()==m['canonicalIdleSha256'],'shared idle file exact')
for path,h in p['sourceHashes'].items():check(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'authored source unchanged '+path)
for record in p['records']:
    out=np.array(Image.open(P/record['output']).convert('RGBA'));mask=np.array(Image.open(P/record['mask']))>0;check(np.array_equal(out[~mask],original[~mask]),record['output']+' protected pixels');check(np.array_equal(out[:62],original[:62]) and np.array_equal(out[110:],original[110:]),record['output']+' head and lower body')
for state in m['states']:
    apng=Image.open(P/f'review/{state["id"]}.png');check(apng.n_frames==state['frameCount'],state['id']+' count')
    for i,path in enumerate(state['frameFiles']):
        im=Image.open(P/path).convert('RGBA');apng.seek(i);check(im.size==(184,184),path+' canvas');check(np.array_equal(np.array(apng.convert('RGBA')),np.array(im)),path+' APNG decode');check(round(apng.info['duration'])==state['frameDurationsMs'][i],path+' duration')
rise,typing,lower=m['states'];check(rise['frameFiles'][0]==lower['frameFiles'][-1]=='frames/idle.png','shared idle aliases');check(rise['frameFiles'][-1]==typing['frameFiles'][0]==typing['frameFiles'][-1]==lower['frameFiles'][0],'held aliases')
result={'checks':checks,'errors':errors,'visualAcceptance':False,'scope':'corrected locomotion/action shared master and action package'};(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(bool(errors))
