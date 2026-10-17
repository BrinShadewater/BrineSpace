from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2];old=P.parent/'first-lift-row-source-v1'
reports={}
for folder,label in [(old,'before'),(P,'after')]:
 frames=[np.array(Image.open(folder/f'diagnostic-frames/{i:03d}.png').convert('RGBA')).astype(float) for i in range(6)]
 box=(103,202,133,224);x0,y0,x1,y1=box;t=frames[0][y0:y1,x0:x1,:3];alpha=frames[0][y0:y1,x0:x1,3];mask=(alpha>200)&(t[:,:,0]>t[:,:,1]+3)&(t[:,:,0]>t[:,:,2]+3)&(t.mean(2)>40)&(t.mean(2)<220);assert mask.sum()>10
 v=t[mask];v-=v.mean(0);den=np.sqrt((v*v).sum());matches=[]
 for i,a in enumerate(frames):
  best=None
  for dy in range(-2,3):
   for dx in range(-5,6):
    w=a[y0+dy:y1+dy,x0+dx:x1+dx,:3][mask];w-=w.mean(0);score=float((v*w).sum()/max(1e-8,den*np.sqrt((w*w).sum())))
    if best is None or score>best[0]:best=(score,dx,dy)
  matches.append({'pose':i,'NCC':round(best[0],4),'dx':best[1],'dy':best[2]})
 reports[label]={'box':box,'warmMaskPixels':int(mask.sum()),'matches':matches,'dxSpan':max(m['dx'] for m in matches)-min(m['dx'] for m in matches),'minimumNCC':min(m['NCC'] for m in matches),'sourceAudit':json.loads((folder/'transition-audit.json').read_text(encoding='utf-8'))}
board=Image.new('RGB',(1792,740),(32,43,49));d=ImageDraw.Draw(board)
master=Image.open(R/'character/veld-east-held-original-master-v1/frames/bare/000.png').convert('RGBA')
for row,(folder,label) in enumerate([(old,'Before'),(P,'After')]):
 for i,im in enumerate([master]+[Image.open(folder/f'diagnostic-frames/{n:03d}.png').convert('RGBA') for n in range(6)]):
  xy=(i*256,row*370+25);board.paste(im,xy,im);d.text((i*256+4,row*370+5),label+(' master' if i==0 else f' pose{i-1}'),fill='white')
board.save(P/'before-after-master-review.png')
report={'comparison':reports,'scope':'Independent broad near-boot material translation proxy across complete six-source rows. Template region excludes most far boot, but occlusion/artistic shape changes still affect correspondence. Not rigid sole/support/native contact proof. No artwork changed.'}
(P/'repair-comparison.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:{z:v[z] for z in ['dxSpan','minimumNCC','matches']} for k,v in reports.items()}))
