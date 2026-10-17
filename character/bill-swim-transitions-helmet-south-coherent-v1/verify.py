from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
BARE=HERE.parent/'bill-swim-transitions-south-coherent-v1'
checks=0
def check(ok,message):
    global checks
    assert ok,message
    checks+=1
pack=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'));bare=json.loads((BARE/'manifest.json').read_text(encoding='utf-8'))
reg=json.loads((HERE/'helmet-registration.json').read_text(encoding='utf-8'));hashes=json.loads((HERE/'frame-hashes.json').read_text(encoding='utf-8'))
check(pack['equipment']=='diving-helmet','gear');check(pack['pivot']==[128,128] and pack['standingHeight']==148,'world plane')
check(len(reg['frames'])==4,'four pitched shell interiors')
for state,authority in zip(pack['states'],bare['states']):
    for field in ['frameDurationsMs','loop','facings','waterKinds','waterPoses']:check(state[field]==authority[field],'paired '+field)
    for file in state['frameFiles']:
        im=Image.open(HERE/file).convert('RGBA');box=im.getchannel('A').getbbox()
        check(im.size==(256,256),'canvas');check(box[0]>0 and box[1]>0 and box[2]<256 and box[3]<256,'clearance')
        check(hashlib.sha256((HERE/file).read_bytes()).hexdigest()==hashes[file],'frame hash')
start,stop=pack['states']
for i in range(6):check(np.array_equal(np.array(Image.open(HERE/start['frameFiles'][i])),np.array(Image.open(HERE/stop['frameFiles'][5-i]))),'exact reverse')
for file,authority,offset in zip([start['frameFiles'][0],start['frameFiles'][-1]],reg['endpointAuthorities'],reg['endpointOffsets']):
    canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(Image.open(HERE.parent/authority).convert('RGBA'),tuple(offset))
    check(np.array_equal(np.array(canvas),np.array(Image.open(HERE/file))),'exact equipped endpoint')
    m=json.loads((HERE.parent/authority.split('/')[0]/'manifest.json').read_text(encoding='utf-8'));check([m['pivot'][0]+offset[0],m['pivot'][1]+offset[1]]==[128,128],'world join')
for record in reg['frames']:
    a=np.array(Image.open(HERE/record['file']).convert('RGBA'));b=np.array(Image.open(BARE/record['file']).convert('RGBA'));y=record['protectedBodyFromY']
    check(np.array_equal(a[y:],b[y:]),'protected authored body')
    check(hashlib.sha256((BARE/record['file']).read_bytes()).hexdigest()==record['bareSha256'],'body provenance')
    check(hashlib.sha256((HERE.parent/record['component']).read_bytes()).hexdigest()==record['componentSha256'],'frozen authored pitch component')
(HERE/'verification.json').write_text(json.dumps({'checks':checks,'passed':True,'scope':'paired clocks,exact endpoints/reverse,body preservation and donor provenance;visual/native review separate'},indent=2)+'\n',encoding='utf-8')
print(str(checks)+' transition helmet packaging checks PASS')
