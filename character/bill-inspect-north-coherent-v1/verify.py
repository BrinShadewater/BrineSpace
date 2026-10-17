from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    checks=[]
    def check(ok,label):checks.append({'passed':bool(ok),'check':label})
    r=json.loads((P/'registration.json').read_text());cfg=json.loads((P/'source-rulers.json').read_text())
    check(sha(P/r['source'])==r['sourceSha256'],'Raw source binding')
    check(r['fixedRuler']==cfg['fixedRuler'] and r['heads']==cfg['heads'],'Frozen source ruler/head axes')
    check(len({tuple(row['targetFrontBoot']) for row in r['frames']})==1,'Fixed master front-boot contact')
    check(max(row['headAxis'][1] for row in r['frames'])-min(row['headAxis'][1] for row in r['frames'])<=2,'Upright crown range within two native pixels')
    check(r['sourcePoses']==[0,1,2,1,0] and r['excludedSourcePoses']==[3,4,5],'Three authored upright poses; compressed bottom poses excluded')
    check(sha(P.parent/r['idleAuthority'])==r['idleSha256'],'Selected matte master binding')
    for file,digest in json.loads((P/'frame-hashes.json').read_text()).items():check(sha(P/file)==digest,'Frame binding '+file)
    for gear in ['bare','helmet']:
        m=json.loads((P/(gear+'-manifest.json')).read_text());s=m['states'][0]
        check(m['pivot']==[128,224] and m['standingHeight']==148 and m['precomposed'],'Shared whole-figure plane')
        check(s['id']=='inspect-north' and s['loop'] and s['frameDurationsMs']==[160]*6 and s['depthOffsets']==[0]*6,'Retained inspection loop contract')
        images=[np.array(Image.open(P/file).convert('RGBA')) for file in s['frameFiles']]
        check(len({a.tobytes() for a in images})==3,'Three distinct authored inspection poses')
        check(np.array_equal(images[0],images[-1]),'Exact neutral inspection loop closure')
        for a in images:
            y,x=np.where(a[:,:,3]>180);check(a.shape==(256,256,4) and y.max()==r['frames'][0]['targetFrontBoot'][1] and x.min()>0 and x.max()<255,'Contained planted master sole')
    for row in r['frames']:
        i=row['frame'];limit=row['protectedBodyFromY'];a=np.array(Image.open(P/f'frames/bare/{i:03}.png'));b=np.array(Image.open(P/f'frames/helmet/{i:03}.png'))
        check(np.array_equal(a[limit:],b[limit:]),'Original body below fitted helmet')
    result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks,'scope':'candidate source/loop;tool entry-exit and runtime selection pending'}
    (P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'checks':len(checks)}));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
