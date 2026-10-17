"""Source ruler, unchanged master hardware, rest contracts and protected body."""
from pathlib import Path
import json,hashlib,subprocess,sys
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok):
    global checks
    assert ok;checks+=1
bare=json.loads((P/'bare-manifest.json').read_text());helm=json.loads((P/'helmet-manifest.json').read_text());reg=json.loads((P/'helmet-registration.json').read_text());br=json.loads((P/'bare-registration.json').read_text())
check(abs(br['fixedRuler']-148/517)<1e-12);check(sha(P/br['source'])==br['sourceSha256'])
original=np.array(Image.open(P/'sources/canonical-head.png'));closed=np.array(Image.open(P/'sources/canonical-head-closed.png'))
check(original.shape==(39,35,4));check(sha(R/reg['nativeComponent'])==reg['nativeComponentSha256']);check(np.array_equal(original,np.array(Image.open(R/reg['nativeComponent']))))
mask=np.ones(original.shape[:2],bool);mask[17:20,24:29]=False
check(np.array_equal(original[mask],closed[mask]));check(np.array_equal(original[:,:,3],closed[:,:,3]));check(np.count_nonzero(np.any(original!=closed,axis=2))==15)
for m in [bare,helm]:
    check([s['id'] for s in m['states']]==['lie-down-east','get-up-east','sleep-east'])
    lie,rise,sleep=m['states'];check(lie['frameFiles']==list(reversed(rise['frameFiles'])));check(sum(lie['frameDurationsMs'])==1840 and sum(rise['frameDurationsMs'])==1840)
    check(not lie['loop'] and not rise['loop']);check(sleep['loop'] and sleep['frameFiles']==[lie['frameFiles'][-1]])
    for f in lie['frameFiles']:
        a=np.array(Image.open(P/f));check(a.shape==(256,256,4));check(not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20))
        check(abs(int(np.where(a[:,:,3]>180)[0].max())-223)<=1)
for gear,m,master in [('bare',bare,br['idle']),('helmet',helm,reg['helmetIdle'])]:
    entry=Image.new('RGBA',(256,256));entry.alpha_composite(Image.open(R/master).convert('RGBA'),(36,52));check(entry.tobytes()==Image.open(P/m['states'][0]['frameFiles'][0]).tobytes())
    hashes=json.loads((P/f'{gear}-frame-hashes.json').read_text())
    for f in m['states'][0]['frameFiles']:check(sha(P/f)==hashes[f])
for i,r in enumerate(reg['frames'],1):
    b=np.array(Image.open(P/bare['states'][0]['frameFiles'][i]));h=np.array(Image.open(P/helm['states'][0]['frameFiles'][i]));yy,xx=np.indices(b.shape[:2]);cx,cy=r['headCenter'];protected=(xx-cx)**2+(yy-cy)**2>=r['eraseRadius']**2
    px,py=r['componentPosition'];w,ht=r['componentSize'];protected[max(0,py):min(256,py+ht),max(0,px):min(256,px+w)]=False
    check(np.array_equal(b[protected],h[protected]));check(r['nativeScale']==1)
tracked=bare['states'][0]['frameFiles']+helm['states'][0]['frameFiles']+['bare-manifest.json','helmet-manifest.json','bare-registration.json','helmet-registration.json','material-grade.json']
before={f:sha(P/f) for f in tracked}
for script in ['review_scale.py','build_bare.py','build_helmet.py']:subprocess.run([sys.executable,str(P/script)],check=True,capture_output=True)
check(before=={f:sha(P/f) for f in tracked})
result={'checks':checks,'failures':0,'states':6,'references':26,'sourcePoses':6,'bodyRuler':148/517,'nativeHelmet':[35,39],'closedEyeRGBPixels':15,'deterministicFiles':len(tracked),'normalSelection':False,'scope':'paired rest source/master/body/contracts, native player/furniture/head-contact/death interrupts separate'}
(P/'paired-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

