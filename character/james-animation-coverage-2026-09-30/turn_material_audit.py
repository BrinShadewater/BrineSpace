from pathlib import Path
import json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def samples(im):
 a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>180)[0].min();lum=rgb.mean(2)
 body=(a[:,:,3]>200)&(yy>top+30)&(yy<top+125)
 cloth=body&(lum>=20)&(lum<=75)&(abs(r-b)<20)&(abs(g-b)<20)
 gold=body&(yy<top+85)&(r-b>35)&(g-b>20)
 return dict(clothCount=int(cloth.sum()),clothMedianRgb=np.median(rgb[cloth],axis=0).round(1).tolist(),goldCount=int(gold.sum()),goldMedianRgb=np.median(rgb[gold],axis=0).round(1).tolist())
out=dict(method='Alpha>200; upper-body region; neutral dark material RGBmean20..75; engineering gold r-b>35/g-b>20. Comparative diagnostics, not a color acceptance test.',masters={},turns={})
p=ROOT/'character/crew-runtime-matte-v1/branforth';m=json.loads((p/'manifest.json').read_text())
for direction in ['east','south','west','north']:
 s=next(s for s in m['states'] if s['id']=='idle-'+direction);out['masters'][direction]=samples(Image.open(p/s['frameFiles'][0]).convert('RGBA'))
for folder,clip in [('james-cargo-turn-east-north-v1','carry-turn-east-north'),('james-cargo-turn-south-west-v1','carry-turn-south-west'),('james-cargo-turn-east-south-height-v3','carry-turn-east-south'),('james-cargo-turn-north-west-v1','carry-turn-north-west')]:
 out['turns'][clip]=[samples(Image.open(ROOT/'character'/folder/f'frames/bare/{clip}/{i:03d}.png').convert('RGBA')) for i in range(6)]
(HERE/'turn-material-audit.json').write_text(json.dumps(out,indent=2)+'\n')
for name,rows in out['turns'].items():
 print(name,'cloth median-channel range',round(min(np.mean(r['clothMedianRgb']) for r in rows),1),round(max(np.mean(r['clothMedianRgb']) for r in rows),1),'gold R range',min(r['goldMedianRgb'][0] for r in rows),max(r['goldMedianRgb'][0] for r in rows))
print('Directional master cloth', {k:v['clothMedianRgb'] for k,v in out['masters'].items()})
