from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1]
checks=0;failures=[]
def check(ok,label):
    global checks
    checks+=1
    if not ok:failures.append(label)
def pixels(path):return np.array(Image.open(path).convert('RGBA'))
packs={mode:json.loads((P/(mode+'-manifest.json')).read_text()) for mode in ['bare','helmet']}
hr=json.loads((P/'helmet-registration-v3.json').read_text());records=[]
for mode,pack in packs.items():
    check(pack['pivot']==[128,224] and pack['standingHeight']==148,'fixed scale '+mode)
    states={s['id']:s for s in pack['states']}
    original=json.loads((R/'character/james-rest-material-continuity-v1'/(mode+'-manifest.json')).read_text())
    for key,state in states.items():
        old=next(s for s in original['states'] if s['id']==key)
        for field in old:
            if field in ['frameFiles','provenance','restHeadOffset']:continue
            check(state.get(field)==old[field],mode+' unchanged '+key+' '+field)
        for i,ref in enumerate(state['frameFiles']):
            im=pixels(P/ref);check(im.shape==(256,256,4),'canvas '+mode+key+str(i))
            check(np.any(im[:,:,3]>192),'nonempty '+mode+key+str(i))
            records.append({'mode':mode,'key':key,'index':i,'path':ref,'sha256':hashlib.sha256((P/ref).read_bytes()).hexdigest()})
    lie=[pixels(P/f) for f in states['lie-down-east']['frameFiles']]
    sleep=[pixels(P/f) for f in states['sleep-east']['frameFiles']]
    rise=[pixels(P/f) for f in states['get-up-east']['frameFiles']]
    master_ref=next(s for s in original['states'] if s['id']=='lie-down-east')['frameFiles'][0]
    check(np.array_equal(lie[0],pixels(R/'character/james-rest-material-continuity-v1'/master_ref)),mode+' exact standing master')
    check(all(np.array_equal(a,b) for a,b in zip(lie,rise[::-1])),mode+' reverse exact')
    check(np.array_equal(lie[-1],sleep[0]) and np.array_equal(sleep[0],sleep[-1]) and np.array_equal(sleep[-1],rise[0]),mode+' exact all rest joins')
    check(sum(states['sleep-east']['frameDurationsMs'])==3600,mode+' cadence retained')
for bare,helmet in zip(packs['bare']['states'],packs['helmet']['states']):
    for i,pose in enumerate(bare['provenance']['sourcePoses']):
        if pose==0:continue
        a=pixels(P/bare['frameFiles'][i]);b=pixels(P/helmet['frameFiles'][i]);t=hr['tracking'][pose]
        x0,y0,x1,y1=t['editRegion'];mask=np.ones(a.shape[:2],bool);mask[y0:y1,x0:x1]=False
        # Exact head ownership includes the recorded erase ellipse as well as donor.
        yy,xx=np.indices(mask.shape);cx,cy,rx,ry=t['eraseEllipse'];mask&=((xx-cx)/rx)**2+((yy-cy)/ry)**2>1
        check(np.array_equal(a[mask],b[mask]),'shared revised body outside shell '+bare['id']+str(i))
check(len(records)==36,'36 selected candidate references')
result={'checks':checks,'failures':failures,'references':records,'runtimeInstalled':False,'scope':'Metadata and joins, fixed ruler, exact standing masters, shared body outside recorded helmet donor/erase union. Numeric checks do not prove identity or motion quality.'}
(P/'packaging-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':checks,'failures':failures,'runtimeInstalled':False}));raise SystemExit(bool(failures))
