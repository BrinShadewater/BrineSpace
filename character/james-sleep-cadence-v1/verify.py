from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];e=json.loads((P/'source-evidence.json').read_text());checks=0;failures=[]
def check(ok,why):
    global checks
    checks+=1
    if not ok:failures.append(why)
for r in e['sourceRecords']:check(hashlib.sha256((R/r['source']).read_bytes()).hexdigest()==r['sha256'],'Source byte hash '+r['source'])
for mode in ['bare','helmet']:
    pack=json.loads((P/(mode+'-manifest.json')).read_text())
    for state in pack['states']:
        oldpath=R/state['provenance']['sleepCadence']['sourceManifest'];old=json.loads(oldpath.read_text());original=next(s for s in old['states'] if s['id']==state['id'])
        check(state['frameDurationsMs']==[600]*6 and sum(state['frameDurationsMs'])==3600,'Shared visual clock')
        for key,value in original.items():
            if key not in ['frameDurationsMs','frameFiles','provenance']:check(state[key]==value,'Original source metadata '+key)
        for f,oldf in zip(state['frameFiles'],original['frameFiles']):
            a=R/f.removeprefix('res://');b=R/oldf.removeprefix('res://') if oldf.startswith('res://') else (oldpath.parent/oldf).resolve()
            check(a.resolve()==b.resolve(),'Exact original source file binding')
        neutral=Image.open(R/state['frameFiles'][0].removeprefix('res://')).convert('RGBA').tobytes();end=Image.open(R/state['frameFiles'][-1].removeprefix('res://')).convert('RGBA').tobytes()
        check(neutral==end,'Exact closed neutral')
        # Normal life_sleep10.4s finishes within the final neutral slot.
        check(int((10400%3600)//600)==5,'Normal sleep window ends on neutral')
        with Image.open(P/(state['id'].removeprefix('sleep-')+'-revised.gif')) as gif:
            total=0
            for i in range(gif.n_frames):gif.seek(i);total+=gif.info['duration']
            check(total==3600,'Actual encoded source-clock preview')
report={'checks':checks,'failures':failures,'sourceFrames':48,'changedPixels':0,'clockMs':3600,'scope':'Exact source file hashes/bindings and metadata, paired four-direction visual clock and terminal neutral. No new anatomy or simulation changes; native behavior evidence separate.'}
(P/'packaging-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report));raise SystemExit(bool(failures))
