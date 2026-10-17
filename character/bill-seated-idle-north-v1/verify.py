from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(ok,label):checks.append({'passed':bool(ok),'check':label})
 r=json.loads((P/'registration.json').read_text(encoding='utf-8'))
 check(sha(P/'sources/seated-breathing-v1.png')==r['source'],'Raw source binding')
 for file,digest in json.loads((P/'frame-hashes.json').read_text(encoding='utf-8')).items():check(sha(P/file)==digest,'Frame hash '+file)
 for gear,folder in [('bare','bill-seated-north-coherent-v1'),('helmet','bill-seated-helmet-north-coherent-v1')]:
  m=json.loads((P/(gear+'-manifest.json')).read_text(encoding='utf-8'));s=m['states'][0];frames=[np.array(Image.open(P/f).convert('RGBA')) for f in s['frameFiles']];endpoint=np.array(Image.open(P.parent/folder/'frames/sit-down-north/005.png').convert('RGBA'))
  check(np.array_equal(frames[0],endpoint) and np.array_equal(frames[-1],endpoint),gear+' exact entry and closure')
  check(s['loop'] and sum(s['frameDurationsMs'])==960 and s['depthOffsets']==[40]*6,gear+' retained seated timing/depth')
  check(len({a.tobytes() for a in frames[1:5]})==4,gear+' four authored interior poses')
  check(m['pivot']==[128,224] and m['standingHeight']==148,gear+' transition registration')
  for a in frames:
   y,x=np.where(a[:,:,3]>180);check(abs(int(y.max())-222)<=1 and x.min()>0 and x.max()<255,gear+' contained local boot contact')
 for row in r['frames']:
  hy=row['headAxis'][1];bare=np.array(Image.open(P/f"frames/bare/{row['frame']:03}.png"));helmet=np.array(Image.open(P/f"frames/helmet/{row['frame']:03}.png"));check(np.array_equal(bare[hy+31:],helmet[hy+31:]),'Body preserved below native helmet')
 result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks};(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':result['passed'],'checks':len(checks)}));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
