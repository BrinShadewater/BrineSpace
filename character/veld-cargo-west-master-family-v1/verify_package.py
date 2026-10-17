from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def check(ok,why):
    global checks
    assert ok,why
    checks+=1
reg=json.loads((P/'family-registration.json').read_text(encoding='utf-8'))
for key in ['source','sharedMaterialRecipe','helmetSource','caseSource']:
    file=P/reg[key] if key=='source' else R/reg[key]
    check(hashlib.sha256(file.read_bytes()).hexdigest()==reg[key+'SHA256'],'Original source/component/recipe binding')
case=np.array(Image.open(R/reg['caseSource']).convert('RGBA').crop(tuple(reg['caseSourceBox'])))
for gear in ['bare','helmet']:
    d=json.loads((P/f'{gear}-manifest.json').read_text(encoding='utf-8'));states={s['id']:s for s in d['states']}
    check(d['pivot']==[128,224] and d['standingHeight']==148,'Physical ruler')
    check(len(states)==3,'Paired carry/unload/pickup')
    unload=states['unload-west'];pickup=states['pickup-west']
    check(pickup['frameFiles']==list(reversed(unload['frameFiles'])),'Exact shared reverse source aliases')
    for action in ['unload','pickup']:
        original=json.loads((R/f'character/veld-{action}-west-consistent-v1/original-state.json').read_text(encoding='utf-8'))
        state=states[action+'-west']
        check({k:v for k,v in state.items() if k not in ['frameFiles','frameCount']}=={k:v for k,v in original.items() if k not in ['frameFiles','frameCount']},'Original finite timing/facing/dry/depth metadata')
        check(not state['loop'] and sum(state['frameDurationsMs'])==520,'Finite520ms')
    for i,source in enumerate(unload['frameFiles']):
        check(source.startswith('res://'),'Whole source path')
        path=R/source[6:];im=Image.open(path);a=np.array(im)
        check(im.mode=='RGBA' and im.size==(256,256),'NativeRGBAcanvas')
        check(hashlib.sha256(path.read_bytes()).hexdigest()==reg['newFrameBindings'][path.relative_to(R).as_posix()],'Frozen export pixels')
        check(not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20),'No clipped opaque border')
        if i in [3,4,5]:
            cx,cy=reg['floorCasePosition'];region=a[cy:cy+case.shape[0],cx:cx+case.shape[1]]
            opaque=case[:,:,3]==255
            check(np.array_equal(region[opaque],case[opaque]),'Same authored case opaque pixels/fixed floor after release')
    # The living body at the terminal remains exact selected idle; floor prop
    # is separate source pixels beside it, not a recreated standing anatomy.
    idlepath=R/'character/crew-runtime-matte-v1/veld/frames/idle-west-transition-matte-v1/000.png' if gear=='bare' else R/reg['helmetSource']
    idle=np.array(Image.open(idlepath).convert('RGBA'));out=np.array(Image.open(R/unload['frameFiles'][5][6:]))
    region=out[52:52+idle.shape[0],36:36+idle.shape[1]];opaque=idle[:,:,3]>200
    cx,cy=reg['floorCasePosition'];occlusion=np.zeros_like(opaque)
    occlusion[cy-52:cy-52+case.shape[0],cx-36:cx-36+case.shape[1]]=case[:,:,3]>0
    opaque &= ~occlusion
    check(np.array_equal(region[opaque],idle[opaque]),'Exact selected idle body at exit')
(P/'package-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'statesPerGear':3,'newFrames':12,'sourceSlots':36,'scope':'exact original finite metadata/paired reverse aliases/shared recipe/provenance/case lock/idle-body terminal; native/controller/world/full-family adoption separate'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'sourceSlots':36}))
