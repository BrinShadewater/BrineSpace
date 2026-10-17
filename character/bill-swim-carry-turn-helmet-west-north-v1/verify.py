from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;BARE=HERE.parent/'bill-swim-carry-turn-west-north-v1'
p=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'));r=json.loads((HERE/'helmet-registration.json').read_text(encoding='utf-8'));hashes=json.loads((HERE/'frame-hashes.json').read_text(encoding='utf-8'));checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
check(p['equipment']=='diving-helmet' and p['pivot']==[128,128] and p['standingHeight']==148,'equipment registration')
check(hashlib.sha256((HERE/r['source']).read_bytes()).hexdigest()==r['sourceSha256'],'source provenance')
check(all(c['scale']==.09 for c in r['components']),'frozen shell scale')
bare=json.loads((BARE/'manifest.json').read_text(encoding='utf-8'))
for state,base in zip(p['states'],bare['states']):
 check(state['frameDurationsMs']==base['frameDurationsMs'] and state['facings']==base['facings'],'paired timing/facing')
 for file in state['frameFiles']:
  im=Image.open(HERE/file).convert('RGBA');box=im.getchannel('A').getbbox();check(im.size==(256,256) and 0<box[0]<box[2]<256 and 0<box[1]<box[3]<256,'clearance')
  check(hashlib.sha256((HERE/file).read_bytes()).hexdigest()==hashes[file],'frame hash')
for frame in r['frames']:
 a=np.array(Image.open(HERE/frame['file']));b=np.array(Image.open(BARE/frame['file']));y=frame['protectedBodyFromY'];check(np.array_equal(a[y:],b[y:]),'protected body')
 x0,y0,x1,y1=frame['protectedCaseBox'];case=b[y0:y1,x0:x1,3]>0;check(np.array_equal(a[y0:y1,x0:x1][case],b[y0:y1,x0:x1][case]),'protected case/grip')
 check(hashlib.sha256((BARE/frame['file']).read_bytes()).hexdigest()==frame['bareSha256'],'bare provenance')
for i,authority in enumerate(r['endpointAuthorities']):
 expected=Image.new('RGBA',(256,256));expected.alpha_composite(Image.open(HERE.parent/authority['path']).convert('RGBA'),tuple(authority['padding']));a=Image.open(HERE/p['states'][0]['frameFiles'][0 if i==0 else -1]);check(np.array_equal(np.array(a),np.array(expected)),'exact helmet loop endpoint')
for a,b in zip(p['states'][0]['frameFiles'],p['states'][1]['frameFiles'][::-1]):check(np.array_equal(np.array(Image.open(HERE/a)),np.array(Image.open(HERE/b))),'exact reverse')
(HERE/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'paired gear timing/registration/provenance,protected body/case,exact endpoints/reverse;visual/native/owner evidence separate'},indent=2)+'\n',encoding='utf-8');print(f'{checks} helmet turn checks PASS')
