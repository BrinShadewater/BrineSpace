from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;H=P.parent/'bill-seated-helmet-west-coherent-v1'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    checks=[]
    def check(ok,label):checks.append({'passed':bool(ok),'check':label})
    r=json.loads((P/'registration.json').read_text());hr=json.loads((H/'helmet-registration.json').read_text())
    for name,digest in r['sources'].items():check(sha(P/name)==digest,'Authored source '+name)
    check(len({tuple(row['targetFrontBoot']) for row in r['frames']})==1,'Fixed local boot contact')
    for row in r['frames']:check([row['scaleX'],row['scaleY']]==r['primaryRuler'],'Frozen whole-source ruler')
    crowns=[76]+[row['headAxis'][1] for row in r['frames']]
    check(crowns[0]<crowns[1]<crowns[2] and all(abs(y-crowns[-1])<=4 for y in crowns[2:]),'Lowering then stable seated head plane')
    for folder,authority in [(P,P.parent/r['idleAuthority']),(H,P.parent/hr['donor'])]:
        m=json.loads((folder/'manifest.json').read_text());down,rise=m['states'];hashes=json.loads((folder/'frame-hashes.json').read_text())
        check(m['pivot']==[128,224] and m['standingHeight']==148,'Common figure plane')
        check(down['id']=='sit-down-west' and rise['id']=='sit-rise-west','West action coverage')
        check(rise['frameFiles']==down['frameFiles'][::-1] and rise['frameDurationsMs']==down['frameDurationsMs'][::-1],'Exact reversed rise')
        check(sum(down['frameDurationsMs'])==800 and not down['loop'] and not rise['loop'],'Finite retained800ms timing')
        idle=Image.new('RGBA',(256,256));idle.paste(Image.open(authority).convert('RGBA'),(36,52))
        for i,file in enumerate(down['frameFiles']):
            im=Image.open(folder/file).convert('RGBA');a=np.array(im);y,x=np.where(a[:,:,3]>180)
            check(im.size==(256,256) and y.max()==223 and x.min()>0 and x.max()<255,'Contained selected boot contact')
            check(sha(folder/file)==hashes[file],'Frame binding')
            if i==0:check(im.tobytes()==idle.tobytes(),'Exact selected standing entry')
            elif folder==H:
                row=next(row for row in hr['frames'] if row['frame']==i)
                b=np.array(Image.open(P/file).convert('RGBA'));limit=row['protectedBodyFromY']
                check(np.array_equal(a[limit:],b[limit:]),'Original body below fitted helmet')
    check(hr['nativeScale']==1 and sha(P.parent/hr['donor'])==hr['donorSha256'],'Native west helmet donor')
    result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'headYs':crowns,'results':checks,'scope':'paired candidates;furniture,loops and selection pending'}
    (P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'checks':len(checks),'headYs':crowns}));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
