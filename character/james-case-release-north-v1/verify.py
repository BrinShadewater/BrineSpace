from pathlib import Path
import json, numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
reg=json.loads((P/'registration.json').read_text());checks=[]
def check(name,value):checks.append({'name':name,'pass':bool(value)})
case=np.array(Image.open(P/'case.png').convert('RGBA'));cx,cy=reg['casePosition'];ch,cw=case.shape[:2]
donor=np.array(Image.open(P.parent/'james-water-cargo-north-v1/frames/bare/swim-pickup/001.png').convert('RGBA'))[cy:cy+ch,cx:cx+cw]
visible=case[:,:,3]>0
check('retained complete case pixels exact selected',np.array_equal(case[visible],donor[visible]))
check('original case860opaque pixels preserved',int((case[:,:,3]>180).sum())==860)
check('original case native scale',reg['caseProvenance']['nativeScale']==1)
check('one source ruler',all(t['fixedScale']==reg['fixedScale']==.23 for t in reg['tracking']))
check('finite pooled material grades',all(np.isfinite(reg[k]).all() for k in ['neutralGain','goldGain','hairGain']))
yy,xx=np.indices((276,256));head=reg['headTarget'];allowed=((xx-head[0])/14)**2+((yy-(head[1]-1))/14)**2<=1;px,py=reg['helmetPosition'];pw,ph=reg['helmetPatchSize'];allowed[py:py+ph,px:px+pw]=True
for i in range(6):
    b=np.array(Image.open(P/f'frames/bare/{i:03d}.png'));h=np.array(Image.open(P/f'frames/helmet/{i:03d}.png'))
    check(f'paired whole body{i} outside cranial ownership',np.array_equal(b[~allowed],h[~allowed]))
    fg=(yy<head[1]-12)&(b[:,:,3]>0)
    check(f'original North gloves foreground{i}',np.array_equal(b[fg],h[fg]))
    if i==1:check('release pose hand clear of original case',not np.any((b[cy:cy+ch,cx:cx+cw,3]>180)&(case[:,:,3]>180)))
for gear in ['bare','helmet']:
    m=json.loads((P/f'{gear}-manifest.json').read_text());cargo=P.parent/'james-water-cargo-north-v1';cm=json.loads((cargo/f'{gear}-manifest.json').read_text());source=next(s for s in cm['states'] if s['id']=='swim-pickup-north')
    for index,state in enumerate(m['states'],1):
        files=[P/f for f in state['frameFiles']]
        check(f'{gear}{index} exact selected entrance',files[0].read_bytes()==(cargo/source['frameFiles'][index]).read_bytes())
        check(f'{gear}{index} whole-source reverse',all(files[j].read_bytes()==(cargo/source['frameFiles'][index-j]).read_bytes() for j in range(index)))
        check(f'{gear}{index} correct empty bodies',state['frameFiles'][index:index+5]==[f'frames/{gear}/{i:03d}.png' for i in [1,0,2,3,4]])
        check(f'{gear}{index} exact neutral endpoint',files[-1].read_bytes()==(P.parent/'james-water-north-v1'/('frames/swim/000.png' if gear=='bare' else 'frames/helmet/swim/000.png')).read_bytes())
        check(f'{gear}{index} coherent finite release clock',not state['loop'] and sum(state['frameDurationsMs'])==430+50*index and state['caseReleaseMs']==50*index)
        check(f'{gear}{index} full native plane',all(Image.open(f).size==(256,276) for f in files))
e={'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'checks':checks,'scope':'North independent whole-body/ruler/paired helmet/glove foreground, selected complete case,10paired indexed sources/clock/endpoint contracts. Not actual world/Continue/obstruction or master anatomical-height acceptance.'}
(P/'contract-evidence.json').write_text(json.dumps(e,indent=2)+'\n');print(json.dumps({k:e[k] for k in ['passed','failed']}));assert e['failed']==0
