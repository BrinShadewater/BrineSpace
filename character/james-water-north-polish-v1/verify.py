from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;old=P.parent/'james-water-north-v1';checks=0
def check(ok,message):
    global checks
    checks+=1
    if not ok:raise AssertionError(message)
hashes=json.loads((P/'frame-hashes.json').read_text());reg=json.loads((P/'registration.json').read_text())
check(hashlib.sha256((P.parents[1]/reg['source']).read_bytes()).hexdigest()==reg['sourceSha256'],'source hash')
check(len({t['fixedScale'] for t in reg['tracking'] if t['source']!='source-lead-in-v7.png'})==1,'single atlas density')
check(hashlib.sha256((P.parents[1]/reg['leadInSource']).read_bytes()).hexdigest()==reg['leadInSourceSha256'],'lead-in source hash')
check(abs(reg['tracking'][6]['fixedScale']*188-reg['fixedScale']*66)<.000001,'independent cranial density calibration')
packs={mode:json.loads((P/(mode+'-manifest.json')).read_text()) for mode in ['bare','helmet']}
for mode,pack in packs.items():
    check(len(pack['states'])==3,'three states')
    states={s['id']:s for s in pack['states']}
    prior=json.loads((old/(mode+'-manifest.json')).read_text());priorstates={s['id']:s for s in prior['states']}
    for key,s in states.items():
        for field in ['frameDurationsMs','loop','facings','waterKinds']:
            check(s[field]==priorstates[key][field],'retained clock/pose contract '+field)
        for file in s['frameFiles']:
            image=Image.open(P/file).convert('RGBA');a=np.array(image)
            check(image.size==(256,276),'canvas')
            check(hashlib.sha256((P/file).read_bytes()).hexdigest()==hashes[file],'frame hash')
            check(a[:,:,3].min()==0 and a[:,:,3].max()>180,'genuine alpha')
            check(not np.any(a[[0,-1],:,3]) and not np.any(a[:,[0,-1],3]),'unclipped')
    def pixels(key,i):return np.array(Image.open(P/states[key]['frameFiles'][i]))
    check(np.array_equal(pixels('tread-north',0),pixels('tread-north',5)),'closed tread')
    for i in range(6):check(np.array_equal(pixels('swim-start-north',i),pixels('swim-stop-north',5-i)),'exact reverse')
    check(np.array_equal(pixels('tread-north',0),pixels('swim-start-north',0)),'tread join')
    endpoint=np.array(Image.open(old/priorstates['swim-north']['frameFiles'][0]))
    check(np.array_equal(endpoint,pixels('swim-start-north',5)),'exact selected swim endpoint')
for bs,hs in zip(packs['bare']['states'],packs['helmet']['states']):
    check(bs['frameDurationsMs']==hs['frameDurationsMs'],'paired clock')
    for file,hfile,index in zip(bs['frameFiles'],hs['frameFiles'],bs['provenance']['sourcePoses']):
        if index==-1:continue
        b=np.array(Image.open(P/file));h=np.array(Image.open(P/hfile));x0,y0,x1,y1=reg['helmetTracking'][index]['editRegion'];mask=np.ones(b.shape[:2],bool);mask[y0:y1,x0:x1]=False
        check(np.array_equal(b[mask],h[mask]),'body protected outside owned head')
(P/'package-verification.json').write_text(json.dumps(dict(checks=checks,failures=0,scope='Source/frame contracts, alpha, clock preservation, protected body and exact joins; not anatomical/motion acceptance'),indent=2)+'\n')
print(str(checks)+' package checks PASS; source/frame contracts only')
