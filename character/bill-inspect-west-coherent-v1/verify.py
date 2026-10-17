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
    check(r.get('nativeFaceGain')==[1.08,1.02,1.07],'Bounded source-specific skin correction')
    check(len({tuple(row['targetFrontBoot']) for row in r['frames']})==1,'Fixed master front-boot contact')
    check(sha(P.parent/r['idleAuthority'])==r['idleSha256'],'Selected matte master binding')
    check(max(row['headAxis'][1] for row in r['frames'])-min(row['headAxis'][1] for row in r['frames'])<=3,'Corrected upright crown amplitude within3native pixels')
    for file,digest in json.loads((P/'frame-hashes.json').read_text()).items():check(sha(P/file)==digest,'Frame binding '+file)
    for gear in ['bare','helmet']:
        m=json.loads((P/(gear+'-manifest.json')).read_text());s=m['states'][0]
        check(m['pivot']==[128,224] and m['standingHeight']==148 and m['precomposed'],'Shared whole-figure plane')
        check(s['id']=='inspect-west' and s['loop'] and s['frameDurationsMs']==[160]*6 and s['depthOffsets']==[0]*6,'Retained inspection loop contract')
        images=[np.array(Image.open(P/file).convert('RGBA')) for file in s['frameFiles']]
        check(len({a.tobytes() for a in images})>3,'Distinct authored inspection poses')
        check(np.array_equal(images[0],images[-1]),'Exact neutral inspection loop closure')
        for a in images:
            y,x=np.where(a[:,:,3]>180);check(a.shape==(256,256,4) and y.max()==223 and x.min()>0 and x.max()<255,'Contained planted master sole')
    for row in r['frames']:
        i=row['frame'];limit=row['protectedBodyFromY'];a=np.array(Image.open(P/f'frames/bare/{i:03}.png'));b=np.array(Image.open(P/f'frames/helmet/{i:03}.png'))
        check(np.array_equal(a[limit:],b[limit:]),'Original body below fitted helmet')
        previous=np.array(Image.open(P/f'prior-grade-v2/frames/bare/{i:03}.png'));y,x=np.indices(a.shape[:2]);hx,hy=row['headAxis'];band=(x<hx)&(x>hx-14)&(y>=hy+7)&(y<hy+22)
        check(np.array_equal(a[~band],previous[~band]) and np.array_equal(a[:,:,3],previous[:,:,3]),'Geometry/body outside face unchanged')
        check(np.array_equal(b,np.array(Image.open(P/f'prior-grade-v2/frames/helmet/{i:03}.png'))),'Native helmet version unchanged')
    import audit_face
    idle=Image.new('RGBA',(256,256));idle.paste(Image.open(P.parent/r['idleAuthority']).convert('RGBA'),(36,52));master=np.array(audit_face.samples(idle,[128,76])['medianRGB'])
    for row in r['frames']:
        skin=audit_face.samples(Image.open(P/f"frames/bare/{row['frame']:03}.png"),row['headAxis']);check(skin['count']>0 and np.max(np.abs(np.array(skin['medianRGB'])-master))<=12,'Skin median near selected west master')
    result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks,'scope':'candidate source/loop;tool entry-exit and runtime selection pending'}
    (P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'checks':len(checks)}));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
