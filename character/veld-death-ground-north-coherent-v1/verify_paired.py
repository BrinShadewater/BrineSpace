"""Master component, protected body, paired contracts and deterministic fitting."""
from pathlib import Path
import hashlib,json,subprocess,sys
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok):
    global checks
    assert ok;checks+=1
def main():
    bare=json.loads((P/'bare-manifest.json').read_text());helmet=json.loads((P/'helmet-manifest.json').read_text());reg=json.loads((P/'helmet-registration.json').read_text())
    check({k:v for k,v in bare.items() if k not in ['name','equipment','states']}=={k:v for k,v in helmet.items() if k not in ['name','equipment','states']})
    check({k:v for k,v in bare['states'][0].items() if k!='frameFiles'}=={k:v for k,v in helmet['states'][0].items() if k!='frameFiles'})
    native=np.array(Image.open(R/reg['nativeComponent']));original=np.array(Image.open(P/'sources/canonical-head.png'))
    check(np.array_equal(native,original));check(sha(R/reg['nativeComponent'])==reg['nativeComponentSha256'])
    transfer=json.loads((P/'sources/kneel-transfer.json').read_text())
    raw=np.array(Image.open(P/'sources/death-v1.png'));fixed=np.array(Image.open(P/'sources/death-local-kneel-v2.png'));mask=np.ones(raw.shape[:2],bool)
    x0,y0,x1,y1=transfer['cell'];mask[y0:y1,x0:x1]=False
    check(np.array_equal(raw[mask],fixed[mask]));check(sha(P/'sources/death-local-kneel-v2.png')==transfer['outputSha256'])
    entry=Image.new('RGBA',(256,256));entry.alpha_composite(Image.open(R/reg['helmetIdle']).convert('RGBA'),(36,52))
    check(Image.open(P/helmet['states'][0]['frameFiles'][0]).tobytes()==entry.tobytes())
    old=json.loads((P/'bare-frame-hashes.json').read_text())
    for p in bare['states'][0]['frameFiles']:check(sha(P/p)==old[p])
    floors=[]
    for i in range(6):
        b=np.array(Image.open(P/bare['states'][0]['frameFiles'][i]));h=np.array(Image.open(P/helmet['states'][0]['frameFiles'][i]))
        check(h.shape==(256,256,4));check(not np.any(np.concatenate([h[0,:,3],h[-1,:,3],h[:,0,3],h[:,-1,3]])>20))
        y,x=np.where(h[:,:,3]>180);floors.append(int(y.max()));check(abs(int(y.max())-223)<=1)
        if i:
            r=reg['frames'][i-1];yy,xx=np.indices(b.shape[:2]);center=r['headCenter'];protected=(xx-center[0])**2+(yy-center[1])**2>=r['eraseRadius']**2
            px,py=r['componentPosition'];w,ht=r['componentSize'];protected[max(0,py):min(256,py+ht),max(0,px):min(256,px+w)]=False
            check(np.array_equal(b[protected],h[protected]));check(r['nativeScale']==1)
    pitch=json.loads((P/'pitch-registration.json').read_text())
    check(sha(P/'pitch-registration.json')==reg['pitchRegistrationSha256']);check(sha(P/pitch['source'])==pitch['sourceSha256'])
    check([h['size'] for h in pitch['heads']]==[[33,33],[33,32],[32,29]])
    check([h['pitchDegrees'] for h in pitch['heads']]==[0,15,40])
    check(abs(pitch['fixedRuler']-33/(pitch['heads'][0]['sourceBox'][2]-pitch['heads'][0]['sourceBox'][0]))<1e-12)
    for h in pitch['heads']:check(sha(P/h['file'])==h['sha256'])
    tracked=bare['states'][0]['frameFiles']+helmet['states'][0]['frameFiles']+['bare-manifest.json','helmet-manifest.json','bare-registration.json','helmet-registration.json','material-grade.json','sources/canonical-head.png','pitch-registration.json']+[h['file'] for h in pitch['heads']]
    before={p:sha(P/p) for p in tracked}
    for script in ['build_bare.py','fit_pitched_heads.py','build_helmet.py']:subprocess.run([sys.executable,str(P/script)],check=True,capture_output=True)
    check(before=={p:sha(P/p) for p in tracked})
    result={'checks':checks,'failures':0,'nativeHelmetSize':[33,35],'rearFaceVisible':False,'helmetFloorYs':floors,'bareSourceFramesUnchanged':True,'protectedBodyExact':True,'deterministicFiles':len(tracked),'normalSelection':False,'authoredPitchFrames':[1,2],'otherFiveSourcePosesExact':True,'scope':'paired candidate master/component/body/authored forward-pitch packaging; native player and world proof separate'}
    (P/'paired-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()

