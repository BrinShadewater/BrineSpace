from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
m=json.loads((P/'action-manifest.json').read_text());provenance=json.loads((P/'provenance.json').read_text());original=np.array(Image.open(R/m['canonicalIdleSource']).convert('RGBA'));mask=np.array(Image.open(P/'patch-mask.png'))>0
checks=0;errors=[]
def check(ok,name):
    global checks
    checks+=1
    if not ok:errors.append(name)
check(hashlib.sha256((R/m['canonicalIdleSource']).read_bytes()).hexdigest()==m['canonicalIdleSha256'],'idle source unchanged')

for record in provenance['records']:
    check(hashlib.sha256((P/record['source']).read_bytes()).hexdigest()==record['sourceSha256'],'generated '+record['kind'])
check(len(provenance['records'])==3,'isolated source count')
for path,h in provenance['sourceHashes'].items():check(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'registered source '+path)
paths=set(path for s in m['states'] for path in s['frameFiles'])
for record in provenance['records']:
    check((f'frames/{record["kind"]}.png' in paths)==record['admitted'],record['kind']+' playback admission')
for path in paths:
    a=np.array(Image.open(P/path).convert('RGBA'))
    check(a.shape==(184,184,4),path+' dimensions')
    check(np.array_equal(a[~mask],original[~mask]),path+' protected pixels')
    check(np.array_equal(a[:62],original[:62]) and np.array_equal(a[106:],original[106:]),path+' head and legs')
    check(not any(a[y,x,3]>0 for y,x in [(0,0),(0,183),(183,0),(183,183)]),path+' canvas corners')
for state in m['states']:
    apng=Image.open(P/f'review/{state["id"]}.png')
    check(apng.n_frames==state['frameCount'],state['id']+' frame count')
    for i,path in enumerate(state['frameFiles']):
        apng.seek(i);check(np.array_equal(np.array(apng.convert('RGBA')),np.array(Image.open(P/path).convert('RGBA'))),path+' APNG decode')
        check(round(apng.info['duration'])==state['frameDurationsMs'][i],path+' duration')
raise_state,typing,lower=m['states']
check(raise_state['frameFiles'][0]==lower['frameFiles'][-1]=='frames/idle.png','idle aliases')
check(raise_state['frameFiles'][-1]==typing['frameFiles'][0]==typing['frameFiles'][-1]==lower['frameFiles'][0],'held joins')
check(np.array_equal(np.array(Image.open(P/'frames/idle.png')),original),'idle pixel exact')
result={'checks':checks,'errors':errors,'uniqueFrames':len(paths),'newAuthoredPoses':sum(r['admitted'] for r in provenance['records']),'visualAcceptance':False}
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));raise SystemExit(bool(errors))
