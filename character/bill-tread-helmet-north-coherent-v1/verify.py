"""Check protected authored bodies, selected donor provenance and paired clocks."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
BARE=HERE.parent/'bill-tread-north-coherent-v1'
checks=0
def check(ok,message):
    global checks
    assert ok,message
    checks+=1
pack=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'));bare=json.loads((BARE/'manifest.json').read_text(encoding='utf-8'))
reg=json.loads((HERE/'helmet-registration.json').read_text(encoding='utf-8'));hashes=json.loads((HERE/'frame-hashes.json').read_text(encoding='utf-8'))
check(pack['equipment']=='diving-helmet','gear');check(pack['pivot']==bare['pivot'] and pack['standingHeight']==148,'world registration')
check(hashlib.sha256((HERE.parent/reg['donor']).read_bytes()).hexdigest()==reg['donorSha256'],'selected donor unchanged')
for state,authority in zip(pack['states'],bare['states']):
    for field in ['frameDurationsMs','loop','facings','waterKinds','waterPoses']:check(state[field]==authority[field],'paired '+field)
    for i,file in enumerate(state['frameFiles']):
        im=Image.open(HERE/file).convert('RGBA');a=np.array(im);b=np.array(Image.open(BARE/file).convert('RGBA'));r=reg['frames'][i];y=r['protectedBodyFromY']
        check(np.array_equal(a[y:],b[y:]),'protected collar/backpack/body '+file)
        check(hashlib.sha256((BARE/file).read_bytes()).hexdigest()==r['bareSha256'],'authored body provenance')
        check(r['scale']==1 and r['rotationDegrees']==0,'native shell fit')
        check(im.size==(pack['frameWidth'],pack['frameHeight']),'canvas')
        box=im.getchannel('A').getbbox();check(box[0]>0 and box[1]>0 and box[2]<im.width and box[3]<im.height,'clearance')
        check(hashlib.sha256((HERE/file).read_bytes()).hexdigest()==hashes[file],'frame hash')
        hx=pack['pivot'][0];hy=48 if state['id']=='swim-north' else 34
        check(np.array_equal(a[:hy+21,:hx-20],b[:hy+21,:hx-20]) and np.array_equal(a[:hy+21,hx+20:],b[:hy+21,hx+20:]),'protected outer arms')
(HERE/'verification.json').write_text(json.dumps({'checks':checks,'passed':True,'scope':'paired clocks,protected body/outer arms,donor/hash/registration;visual and native acceptance separate'},indent=2)+'\n',encoding='utf-8')
print(str(checks)+' helmet packaging checks PASS')
