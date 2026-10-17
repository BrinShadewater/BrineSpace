"""Staged pickup provenance, finite clock, exact endpoints and body protection."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
r=json.loads((P/'registration.json').read_text(encoding='utf-8'))
check(hashlib.sha256((P/r['source']).read_bytes()).hexdigest()==r['sourceSha256'],'source hash')
check(all(f['scale']==.28 and f['targetCrownAxis']==[154,104] for f in r['frames']),'fixed anatomy ruler')
legacy=json.loads((P.parent/'major-bill-v3/clearance.json').read_text(encoding='utf-8'))
for gear,folder in [('bare',P),('helmet',P.parent/'bill-swim-pickup-helmet-east-coherent-v1')]:
 m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));s=m['states'][0];hashes=json.loads((folder/'frame-hashes.json').read_text(encoding='utf-8'))
 check(m['pivot']==[128,128] and m['standingHeight']==148,'physical registration')
 check(s['id']=='swim-pickup-east' and not s['loop'] and s['frameDurationsMs']==[70,80,90,100,100,80],'finite retained clock')
 check(s['waterKinds']==['salvage']+['swim']*5 and s['waterPoses']==[True]*6 and s['facings']==['east']*6 and s['depthOffsets']==[0]*6,'water metadata')
 prefix='bill-salvage-east-coherent-v1' if gear=='bare' else 'bill-salvage-helmet-east-coherent-v1'
 carry='bill-swim-carry-east-coherent-v1' if gear=='bare' else 'bill-swim-carry-helmet-east-coherent-v1'
 for i,path,pad in [(0,f'{prefix}/frames/salvage-east/000.png',(0,0)),(5,f'{carry}/frames/swim-carry-east/000.png',(6,40))]:
  expected=Image.new('RGBA',(256,256));expected.alpha_composite(Image.open(P.parent/path).convert('RGBA'),pad)
  check(np.array_equal(np.array(Image.open(folder/s['frameFiles'][i])),np.array(expected)),'exact endpoint '+str(i))
 boxes=[]
 for i,file in enumerate(s['frameFiles']):
  im=Image.open(folder/file).convert('RGBA');a=np.array(im);box=im.getbbox();boxes.append(box)
  check(im.size==(256,256),'canvas');check(0<box[0]<box[2]<256 and 0<box[1]<box[3]<256,'contained art');check(hashlib.sha256((folder/file).read_bytes()).hexdigest()==hashes[file],'frame hash')
  if gear=='helmet' and i in [1,2,3,4]:
   b=np.array(Image.open(P/file).convert('RGBA'));check(np.array_equal(a[135:],b[135:]),'protected body/case');mask=b[128:135,160:,3]>0;check(np.array_equal(a[128:135,160:][mask],b[128:135,160:][mask]),'protected foreground arm')
 union=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)];extent=[(v-128)*65.28/148 for v in union]
 action=legacy['actions'][gear]['transition-east'];swim=legacy['swim'][gear]['east'];allowed=[min(action[0],swim[0]),min(action[1],swim[1]),max(action[2],swim[2]),max(action[3],swim[3])]
 contained=all(extent[i]>=allowed[i] for i in [0,1]) and all(extent[i]<=allowed[i] for i in [2,3]);check(contained,'actual effective pickup clearance')
 (folder/'clearance-review.json').write_text(json.dumps({'worldExtent':extent,'effectiveRetainedClearance':allowed,'contained':contained,'scope':'retained transition/swim union; exterior expedition pickup is not gated by this room check'},indent=2)+'\n',encoding='utf-8')
h=P.parent/'bill-swim-pickup-helmet-east-coherent-v1';reg=json.loads((h/'helmet-registration.json').read_text(encoding='utf-8'))
check(reg['componentNativeScale']==1,'native helmet ruler');check((h/reg['component']).read_bytes()==(P.parent/reg['donor']).read_bytes(),'canonical helmet')
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'staged paired packaging; live arbitrary work-loop exit remains separate'},indent=2)+'\n',encoding='utf-8')
print(f'{checks} paired pickup packaging checks PASS')
