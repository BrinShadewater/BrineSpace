from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    checks=[]
    def check(ok,label):checks.append({'passed':bool(ok),'check':label})
    r=json.loads((P/'registration.json').read_text())
    check(sha(P/'sources/reading-v1.png')==r['source'],'Raw source binding')
    check(r['fixedRuler']==[.214,.251],'Frozen north seated ruler')
    for file,digest in json.loads((P/'frame-hashes.json').read_text()).items():check(sha(P/file)==digest,'Frame hash '+file)
    for gear in ['bare','helmet']:
        m=json.loads((P/(gear+'-manifest.json')).read_text());s=m['states'][0]
        check(s['id']=='read-seated-north' and s['loop'] and sum(s['frameDurationsMs'])==960,gear+' cycle')
        check(m['pivot']==[128,224] and m['standingHeight']==148,gear+' shared plane')
        check(s['depthOffsets']==[40]*6 and not any(s['waterPoses']),gear+' dry seated depth')
        frames=[np.array(Image.open(P/file).convert('RGBA')) for file in s['frameFiles']]
        check(len({a.tobytes() for a in frames})==6,gear+' six independent poses')
        for a in frames:
            y,x=np.where(a[:,:,3]>180)
            check(y.max()==222 and x.min()>0 and x.max()<255,gear+' contained boot contact')
    for row in r['frames']:
        bare=np.array(Image.open(P/f"frames/bare/{row['frame']:03}.png"))
        helmet=np.array(Image.open(P/f"frames/helmet/{row['frame']:03}.png"))
        hy=row['protectedBodyFromY']
        check(np.array_equal(bare[hy:],helmet[hy:]),'Body preserved below native helmet')
    result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks}
    (P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'checks':len(checks)}))
    return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
