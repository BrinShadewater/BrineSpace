from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
p=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'));r=json.loads((HERE/'registration.json').read_text(encoding='utf-8'));hashes=json.loads((HERE/'frame-hashes.json').read_text(encoding='utf-8'));checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
check(p['pivot']==[128,128] and p['standingHeight']==148,'physical registration')
check(hashlib.sha256((HERE/r['source']).read_bytes()).hexdigest()==r['sourceSha256'],'selected source provenance')
check(all(f['scale']==.28 for f in r['frames']),'one frozen anatomical ruler')
forward,reverse=p['states'];check(reverse['frameDurationsMs']==forward['frameDurationsMs'][::-1],'reverse clock')
for state in p['states']:
 check(not state['loop'] and sum(state['frameDurationsMs'])==640,'finite turn clock')
 check(state['waterKinds']==['swim']*6 and state['waterPoses']==[True]*6,'water metadata')
 for file in state['frameFiles']:
  im=Image.open(HERE/file).convert('RGBA');box=im.getchannel('A').getbbox()
  check(im.size==(256,256),'canvas');check(0<box[0]<box[2]<256 and 0<box[1]<box[3]<256,'clearance')
  check(hashlib.sha256((HERE/file).read_bytes()).hexdigest()==hashes[file],'frame provenance')
for i,authority in enumerate(r['endpointAuthorities']):
 src=Image.open(HERE.parent/authority['path']).convert('RGBA');expected=Image.new('RGBA',(256,256));expected.alpha_composite(src,tuple(authority['padding']))
 actual=Image.open(HERE/forward['frameFiles'][0 if i==0 else -1]).convert('RGBA')
 check(np.array_equal(np.array(actual),np.array(expected)),'exact padded loop endpoint')
for a,b in zip(forward['frameFiles'],reverse['frameFiles'][::-1]):check(np.array_equal(np.array(Image.open(HERE/a)),np.array(Image.open(HERE/b))),'exact reverse artwork')
(HERE/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'source/frames,finite timing,registration,clearance,exact loop endpoints/reversal;native selection/helmet/owner acceptance pending'},indent=2)+'\n',encoding='utf-8')
print(f'{checks} water-basic swim turn packaging checks PASS')
