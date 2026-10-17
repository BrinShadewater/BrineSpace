from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage
import json,numpy as np
P=Path(__file__).resolve().parent
frames=[np.array(Image.open(P/f'full-clip-frames-v2/{n:03}.png').convert('RGBA')).astype(float) for n in range(142)]
windows=[];board=Image.new('RGB',(1200,3600),(32,43,49));d=ImageDraw.Draw(board)
cases=[(f'{role} cycle{k}',first+21*k,last+21*k,base+21*k) for k in range(6) for role,first,last,base in [('far',19,23,21),('near',9,13,11)]]
for wi,(name,first,last,base) in enumerate(cases):
 a=frames[base];lab,k=ndimage.label(a[201:231,:,3]>200);parts=[]
 for j in range(1,k+1):
  y,x=np.where(lab==j)
  if len(x)>15 and x.mean()>128:parts.append((len(x),int(x.min()),int(y.min()+201),int(x.max()+1),int(y.max()+202)))
 assert parts,'No separated front support boot'
 _,x0,y0,x1,y1=max(parts);template=a[y0:y1,x0:x1,:3];alpha=a[y0:y1,x0:x1,3]
 mask=(alpha>220)&(template[:,:,0]>template[:,:,1]+3)&(template[:,:,0]>template[:,:,2]+3)&(template.mean(2)>35)&(template.mean(2)<220)
 assert mask.sum()>12
 v=template[mask];v-=v.mean(0);den=np.sqrt((v*v).sum());rows=[]
 for col,n in enumerate(range(first,last+1)):
  a=frames[n];best=None
  for dy in range(-4,5):
   for dx in range(-20,21):
    w=a[y0+dy:y1+dy,x0+dx:x1+dx,:3][mask];w-=w.mean(0)
    score=float((v*w).sum()/max(1e-8,den*np.sqrt((w*w).sum())))
    if best is None or score>best[0]:best=(score,dx,dy)
  rows.append({'frame':n,'NCC':round(best[0],4),'dx':best[1],'dy':best[2],'nativeX':float((x0+x1)/2+best[1]),'nativeY':float((y0+y1)/2+best[2])})
  im=Image.fromarray(a.astype('uint8'));crop=im.crop((80,185,175,231)).resize((228,110),Image.Resampling.NEAREST)
  xy=(col*240,wi*300+25);board.paste(crop,xy,crop);d.text((xy[0]+3,xy[1]-20),f'{name.split()[0]} raw{n}',fill='white')
  marked=Image.fromarray(a.astype('uint8'));md=ImageDraw.Draw(marked);md.rectangle((x0+best[1],y0+best[2],x1+best[1],y1+best[2]),outline=(255,190,80),width=1)
  crop=marked.crop((80,185,175,231)).resize((228,110),Image.Resampling.NEAREST);board.paste(crop,(xy[0],xy[1]+115),crop)
  d.text((xy[0]+3,xy[1]+235),f'dx{best[1]} dy{best[2]} NCC{best[0]:.3f}',fill='white')
 slope=float(np.polyfit([r['frame']/24 for r in rows],[r['nativeX'] for r in rows],1)[0])
 windows.append({'role':name,'frames':[first,last],'templateFrame':base,'box':[x0,y0,x1,y1],'maskPixels':int(mask.sum()),'rows':rows,'sourceHorizontalRatePxPerSecond':slope,'candidateConstantRootSpeedPxPerSecond':-slope,'candidateStrideFor21Frames':-slope*21/24,'minimumNCC':min(r['NCC'] for r in rows),'verticalSpan':max(r['nativeY'] for r in rows)-min(r['nativeY'] for r in rows)})
board.save(P/'repeated-support-review.png')
report={'windows':windows,'scope':'Read-only twelve five-frame repeated FLAT/front support windows at provisional21-frame appearance recurrence, excluding initial heel-landing frames18/8. Expanded search20px avoids former12px saturation; all source poses remain intact. Near/far role assigned from visually reviewed original-size knee-pad continuity, not nearest boot match across occlusion. Warm boot material translation is an appearance proxy, not literal rigid sole/roll contact or approved world speed. No artwork changed.'}
(P/'repeated-support-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps([{'role':w['role'],'frames':w['frames'],'rate':round(w['candidateConstantRootSpeedPxPerSecond'],2),'NCC':w['minimumNCC'],'verticalSpan':w['verticalSpan']} for w in windows]))
