"""Package/source contracts; visual review and actual runtime are separate evidence."""
from pathlib import Path
import json, numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
reg=json.loads((P/'registration.json').read_text());checks=[]
def check(name,value):checks.append({'name':name,'pass':bool(value)})
case=np.array(Image.open(P/'case.png').convert('RGBA'));cx,cy=reg['casePosition'];ch,cw=case.shape[:2]
check('one fixed source ruler',all(t['fixedScale']==reg['fixedScale']==.25 for t in reg['tracking']))
check('finite pooled material grades',all(np.isfinite(g).all() for cohort in reg['sourceGrade'].values() for g in cohort.values()))
check('complete independently authored case native dimensions',reg['caseSize']==[41,30] and cw==41 and ch==30)
yy,xx=np.indices((276,256));head=reg['headTarget']
allowed=((xx-head[0])/14)**2+((yy-(head[1]-1))/14)**2<=1
px,py=reg['helmetPosition'];pw,ph=reg['helmetPatchSize'];allowed[py:py+ph,px:px+pw]=True
for i in range(5):
    b=np.array(Image.open(P/f'frames/bare/{i:03d}.png'));h=np.array(Image.open(P/f'frames/helmet/{i:03d}.png'))
    check(f'paired full body{i} outside owned head',np.array_equal(b[~allowed],h[~allowed]))
    if i==0:check('first empty release glove clears case core',not np.any((b[cy:cy+ch,cx:cx+cw,3]>180)&(case[:,:,3]>180)))
for gear in ['bare','helmet']:
    m=json.loads((P/f'{gear}-manifest.json').read_text());cargo=P.parent/'james-water-cargo-south-v1'
    cm=json.loads((cargo/f'{gear}-manifest.json').read_text());source=next(s for s in cm['states'] if s['id']=='swim-pickup-south')
    for index,state in enumerate(m['states'],1):
        files=[P/f for f in state['frameFiles']]
        check(f'{gear}{index} exact selected entrance',files[0].read_bytes()==(cargo/source['frameFiles'][index]).read_bytes())
        check(f'{gear}{index} exact selected reverse',all(files[j].read_bytes()==(cargo/source['frameFiles'][index-j]).read_bytes() for j in range(index)))
        check(f'{gear}{index} new full empty-handed interiors',state['frameFiles'][index:index+5]==[f'frames/{gear}/{i:03d}.png' for i in range(5)])
        check(f'{gear}{index} exact neutral endpoint',files[-1].read_bytes()==(P.parent/'james-water-south-v1'/('frames/swim/000.png' if gear=='bare' else 'frames/helmet/swim/000.png')).read_bytes())
        check(f'{gear}{index} finite coherent clock',not state['loop'] and sum(state['frameDurationsMs'])==430+50*index and state['caseReleaseMs']==50*index)
        check(f'{gear}{index} native plane',all(Image.open(f).size==(256,276) for f in files))
e={'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'checks':checks,'scope':'South package/ruler/paired body/first release clearance and exact10paired source clocks. Not tool semantics, actual world/Continue or anatomical master-height acceptance.'}
(P/'contract-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
print(json.dumps({k:e[k] for k in ['passed','failed']}));assert e['failed']==0
