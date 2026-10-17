from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(ok,why):checks.append({'passed':bool(ok),'check':why})
 r=json.loads((P/'registration.json').read_text(encoding='utf-8'))
 for action,reg in r.items():
  check(sha(P/'sources'/reg['source'])==reg['sourceSha256'],action+' source binding')
  check(all([row['scaleX'],row['scaleY']]==reg['fixedRuler'] for row in reg['frames']),action+' fixed source ruler')
 for file,digest in json.loads((P/'frame-hashes.json').read_text(encoding='utf-8')).items():check(sha(P/file)==digest,'Frame binding '+file)
 for gear,folder in [('bare','bill-seated-west-coherent-v1'),('helmet','bill-seated-helmet-west-coherent-v1')]:
  m=json.loads((P/(gear+'-manifest.json')).read_text(encoding='utf-8'));check(m['pivot']==[128,224] and m['standingHeight']==148,gear+' figure plane')
  for s in m['states']:
   frames=[np.array(Image.open(P/f).convert('RGBA')) for f in s['frameFiles']];check(len(frames)==6 and s['loop'] and s['frameDurationsMs']==[160]*6 and s['depthOffsets']==[40]*6,s['id']+' retained seated loop contract')
   check(len({a.tobytes() for a in frames})>3,s['id']+' distinct authored motion')
   if s['id']=='sit-idle-west':
    endpoint=np.array(Image.open(P.parent/folder/'frames/sit-down-west/005.png').convert('RGBA'));check(np.array_equal(frames[0],endpoint) and np.array_equal(frames[-1],endpoint),gear+' exact sitting endpoint joins')
   for a in frames:
    y,x=np.where(a[:,:,3]>180);check(int(y.max())==223 and x.min()>0 and x.max()<255,gear+' local boot contact/contained figure')
 for action,reg in r.items():
  for row in reg['frames']:
   file=f"{action}-west/{row['frame']:03}.png";bare=np.array(Image.open(P/'frames/bare'/file));helmet=np.array(Image.open(P/'frames/helmet'/file));sy=row['protectedBodyFromY'];check(np.array_equal(bare[sy:],helmet[sy:]),'Body preserved below native helmet')
 result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks};(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':result['passed'],'checks':len(checks)}));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
