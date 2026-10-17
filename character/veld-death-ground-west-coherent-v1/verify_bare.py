"""Staged west package evidence; does not claim runtime or visual acceptance."""
from pathlib import Path
import subprocess,sys,json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def check(ok):
    global checks
    assert ok;checks+=1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=json.loads((P/'bare-manifest.json').read_text());s=m['states'][0];r=json.loads((P/'bare-registration.json').read_text())
    check(m['status']=='staged_candidate');check(m['pivot']==[128,224] and m['standingHeight']==148)
    check(not s['loop'] and s['terminalFrame']==5);check(sum(s['frameDurationsMs'])==1420)
    check(s['facings']==['west']*6 and s['waterPoses']==[False]*6)
    check(sha(P/r['source'])==r['sourceSha256']);check(sha(R/r['idle'])==r['idleSha256'])
    check(abs(r['fixedRuler']-148/471)<1e-12)
    master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(R/r['idle']).convert('RGBA'),(36,52))
    check(Image.open(P/s['frameFiles'][0]).tobytes()==master.tobytes())
    crowns=[]
    for p in s['frameFiles']:
        im=Image.open(P/p);a=np.array(im);check(im.mode=='RGBA' and im.size==(256,256))
        check(not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20))
        y,x=np.where(a[:,:,3]>180);crowns.append(int(y.min()));check(abs(int(y.max())-223)<=1)
    check(all(a<b for a,b in zip(crowns,crowns[1:])))
    original=np.array(Image.open(P/'sources/death-v1.png'));local=np.array(Image.open(P/'sources/death-badge-local-v2.png'));mask=np.array(Image.open(P/'sources/badge-transfer-mask.png'))>0
    check(np.array_equal(original[:,:,3],local[:,:,3]));check(np.array_equal(original[~mask],local[~mask]))
    tracked=s['frameFiles']+['bare-manifest.json','bare-registration.json','bare-frame-hashes.json','material-grade.json']
    before={p:sha(P/p) for p in tracked}
    subprocess.run([sys.executable,str(P/'repair_badges.py')],check=True,capture_output=True)
    subprocess.run([sys.executable,str(P/'review_scale.py')],check=True,capture_output=True)
    subprocess.run([sys.executable,str(P/'build_bare.py')],check=True,capture_output=True)
    check(before=={p:sha(P/p) for p in tracked})
    data={'checks':checks,'failures':0,'sourceBadgeAlphaExact':True,'sourceOutsideBadgesExact':True,'deterministicFiles':len(tracked),'crowns':crowns,'normalSelection':False,'nativePlayerVerified':False,'scope':'staged bare packaging only; anatomy/material reviewed separately, helmet/mortality/Continue/clearance pending'}
    (P/'bare-verification.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data))
if __name__=='__main__':main()
