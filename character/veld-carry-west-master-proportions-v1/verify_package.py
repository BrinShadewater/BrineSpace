from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def check(ok,why):
    global checks
    assert ok,why
    checks+=1
reg=json.loads((P/'package-registration.json').read_text(encoding='utf-8'))
original=json.loads((R/'character/veld-carry-west-consistent-v1/original-selection.json').read_text(encoding='utf-8'))
check(hashlib.sha256((P/reg['source']).read_bytes()).hexdigest()==reg['sourceSHA256'],'Authored source bound')
check(hashlib.sha256((R/reg['nativeHelmetSource']).read_bytes()).hexdigest()==reg['nativeHelmetSHA256'],'Shared helmet bound')
for gear in ['bare','helmet']:
    data=json.loads((P/f'{gear}-manifest.json').read_text(encoding='utf-8'));state=data['states'][0]
    check(data['pivot']==original['profile']['pivot'] and data['standingHeight']==148,'Physical ruler retained')
    check(data['strideDistanceCells']['carry-west']==original['profile']['strideDistanceCells']['carry-west'],'Motion stride retained')
    check({k:v for k,v in state.items() if k not in ['frameFiles','frameCount']}=={k:v for k,v in original['state'].items() if k not in ['frameFiles','frameCount']},'Exact original timing/loop/facing/water/depth contract')
    check(len(state['frameFiles'])==6,'Six ordered poses')
    for i,relative in enumerate(state['frameFiles']):
        path=P/relative;im=Image.open(path);a=np.array(im)
        check(im.mode=='RGBA' and im.size==(256,256),'RGBA native canvas')
        check(hashlib.sha256(path.read_bytes()).hexdigest()==reg['sourceBindings'][path.relative_to(R).as_posix()],'Exact frozen package pixels')
        source=np.array(Image.open(P/f'v2-study/study-frames/{i:03}.png'))
        if gear=='bare':
            check(np.array_equal(a[:,:,3],source[:,:,3]),'Source alpha/silhouette unchanged by grading')
            check(np.array_equal(a[107:157,:128],source[107:157,:128]),'Case/near hand region protected')
        else:
            bare=np.array(Image.open(P/f'frames/bare/{i:03}.png'))
            cut=reg['helmetFits'][i]['bodyCutY']
            end=reg['helmetFits'][i]['position'][1]+46
            check(np.array_equal(a[max(cut,end):],bare[max(cut,end):]),'Body below fitted component exact')
        check(not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20),'No clipped opaque edges')
(P/'package-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'scope':'source provenance/silhouette/matte processing protection/unchanged shared helmet and body/original cargo metadata; no motion/normal-world/adoption acceptance'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0}))
