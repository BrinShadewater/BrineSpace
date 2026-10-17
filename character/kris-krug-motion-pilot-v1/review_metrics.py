from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import argparse,json
import numpy as np
from PIL import Image

p=argparse.ArgumentParser();p.add_argument('--version',type=int,choices=[1,2],default=1);args=p.parse_args()
ROOT=Path(__file__).resolve().parent
if args.version==2:ROOT=ROOT.parent/'kris-krug-motion-pilot-v2'
report={}
for state in ['idle-east','walk-east','tablet-east']:
    folder=ROOT/state
    if not (folder/'checks.json').exists():continue
    check=json.loads((folder/'checks.json').read_text());samples=[]
    for n in range(check['frame_count']):
        a=np.asarray(Image.open(folder/'frames'/f'{n:03}.png')).astype(float)
        opaque=a[:,:,3]>180;ys,xs=np.where(opaque);top=ys.min();bottom=ys.max();yy=np.indices(opaque.shape)[0]
        roi=opaque & (yy>top+(bottom-top)*.35) & (yy<top+(bottom-top)*.8)
        color=np.median(a[:,:,:3][roi],axis=0)
        green=float(color[1]-(color[0]+color[2])/2)
        magenta=float((color[0]+color[2])/2-color[1])
        samples.append({'frame':n,'median_body_rgb':color.tolist(),'green_delta':round(green,2),'magenta_delta':round(magenta,2)})
    report[state]={'green_tint_warnings':[s['frame'] for s in samples if s['green_delta']>12],
                   'magenta_tint_warnings':[s['frame'] for s in samples if s['magenta_delta']>12],
                   'samples':samples,'method':'Median lower-torso/thigh RGB on opaque source body. Diagnostic only; geometry and material equality not certified.'}
(ROOT/'color-diagnostics.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:{'green_warnings':v['green_tint_warnings'],'magenta_warnings':v['magenta_tint_warnings']} for k,v in report.items()}))
