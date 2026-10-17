"""Source/timing contracts of the installed indexed West layer branch."""
from pathlib import Path
import json
from PIL import Image
P=Path(__file__).resolve().parent
checks=[]
def check(name,value):checks.append({'name':name,'pass':bool(value)})
for gear in ['bare','helmet']:
    manifest=json.loads((P/f'{gear}-manifest.json').read_text())
    cargo=P.parent/'james-water-cargo-west-v1'
    cm=json.loads((cargo/f'{gear}-manifest.json').read_text())
    source=next(s for s in cm['states'] if s['id']=='swim-pickup-west')
    stow=P.parent/'james-water-torch-stow-west-v1'
    sm=json.loads((stow/f'{gear}-manifest.json').read_text())['states'][0]
    check(gear+' five source-index profiles',len(manifest['states'])==5)
    for index,state in enumerate(manifest['states'],1):
        files=[P/f for f in state['frameFiles']]
        check(gear+str(index)+' exact entrance',files[0].read_bytes()==(cargo/source['frameFiles'][index]).read_bytes())
        check(gear+str(index)+' whole selected reverse to1',all(files[i].read_bytes()==(cargo/source['frameFiles'][index-i]).read_bytes() for i in range(index)))
        check(gear+str(index)+' authored full release',files[index].read_bytes()==(P/f'body-{gear}.png').read_bytes())
        check(gear+str(index)+' empty-handed authored interiors only',all(f'followthrough/{gear}/' in f for f in state['frameFiles'][index+1:index+5]))
        check(gear+str(index)+' exact empty endpoint',files[-1].read_bytes()==(stow/sm['frameFiles'][-1]).read_bytes())
        check(gear+str(index)+' finite coherent release clock',not state['loop'] and sum(state['frameDurationsMs'])==430+50*index and state['caseReleaseMs']==50*index)
        check(gear+str(index)+' shared source ruler',all(Image.open(f).size==(256,276) for f in files))
        check(gear+str(index)+' water/facing contracts',state['waterPoses']==[True]*len(files) and state['facings']==['west']*len(files))
import numpy as np
reg=json.loads((P/'registration.json').read_text());b=np.array(Image.open(P/'body-bare.png').convert('RGBA'));h=np.array(Image.open(P/'body-helmet.png').convert('RGBA'));c=np.array(Image.open(P/'case.png').convert('RGBA'));yy,xx=np.indices(b.shape[:2]);head=reg['headTarget'];allow=((xx-head[0])/15)**2+((yy-(head[1]-1))/15)**2<=1;px,py=reg['helmetPosition'];pw,ph=reg['helmetPatchSize'];allow[py:py+ph,px:px+pw]=True
check('paired exact body outside declared head/shell',np.array_equal(b[~allow],h[~allow]))
check('one physical ruler for both authored components',all(x['fixedScale']==reg['fixedScale']==.1 for x in reg['tracking']))
check('finite matte grades',all(np.isfinite(reg[k]).all() for k in ['neutralGain','goldGain','faceGain','hairGain','caseGain']))
cx,cy=reg['casePosition'];ch,cw=c.shape[:2]
check('complete case/glove release clearance',not np.any((b[cy:cy+ch,cx:cx+cw,3]>180)&(c[:,:,3]>180)))
check('recorded detached physical case size',(cw,ch)==(30,31))
check('selected head anchor',np.allclose(head,[114.48698058428597,117.85696788241698]))
e={'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'checks':checks,'scope':'Ten paired indexed source/clock/water/whole-body package contracts. Actual world/Continue evidence has separate scope.'}
(P/'runtime-contract-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
print(json.dumps({k:e[k] for k in ['passed','failed']}));assert e['failed']==0
