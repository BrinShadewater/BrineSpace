from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math,numpy as np
P=Path(__file__).resolve().parent;R=P.parents[2];N=R/'output/veld-east-grounded-stride-probe-v1'
records=json.loads((N/'records.json').read_text(encoding='utf-8'))['records']
windows=json.loads((P/'support-window-diagnostic.json').read_text(encoding='utf-8'))['windows']
checks=0;results=[]
for trial,gear in [(t,g) for t in range(2) for g in ['bare','helmet']]:
 rows=[r for r in records if r['gear']==gear and r['trial']==trial];frames=[Image.open(N/(r['name']+'-native.png')).convert('RGBA') for r in rows]
 boundaries=[round(r['time']*1000) for r in rows];durations=[max(1,b-a) for a,b in zip(boundaries,boundaries[1:])]+[30]
 target=P/f'trial{trial}-{gear}-native-stride-travel.png';frames[0].save(target,save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0)
 replay=Image.open(target);assert replay.n_frames==len(frames)
 for i,im in enumerate(frames):
  replay.seek(i);assert replay.convert('RGBA').tobytes()==im.tobytes();assert round(replay.info['duration'])==durations[i];checks+=2
  ref=P/'clip-frames'/gear/f"{rows[i]['rawSlot']:03}.png"
  assert Image.open(N/(rows[i]['name']+'-source.png')).convert('RGBA').tobytes()==Image.open(ref).convert('RGBA').tobytes();checks+=1
 board=Image.new('RGB',(1040,700),(32,43,49));d=ImageDraw.Draw(board)
 for j,r in enumerate(rows[1:22]):
  root=120+r['travelWorld']*148/65.28
  crop=Image.open(N/(r['name']+'-native.png')).crop((round(root-65),395,round(root+65),570))
  xy=((j%8)*130,(j//8)*215+25);board.paste(crop,(xy[0],xy[1]+20));d.text((xy[0]+3,xy[1]),f"raw{r['rawSlot']}",fill='white')
 board.save(P/f'native-trial{trial}-{gear}-stride-full-cycle.png')
 for cycle in range(2):
  for height,floor in [(93,330),(148,565)]:
   scale=height/148
   for win in windows:
    selected=[r for r in rows if 1<=r['sample']<=42 and (r['sample']-1)//21==cycle and win['frames'][0]<=r['rawSlot']<=win['frames'][1]]
    base=next(r for r in selected if r['rawSlot']==win['templateFrame'])
    root=120+base['travelWorld']*height/65.28;x0,y0,x1,y1=win['box']
    box=(math.floor(root+(x0-128)*scale),math.floor(floor+(y0-224)*scale),math.ceil(root+(x1-128)*scale),math.ceil(floor+(y1-224)*scale))
    x0,y0,x1,y1=box;im=np.array(Image.open(N/(base['name']+'-native.png')).convert('RGB')).astype(float);t=im[y0:y1,x0:x1]
    mask=(t[:,:,0]>t[:,:,1]+3)&(t[:,:,0]>t[:,:,2]+3)&(t.mean(2)>35)&(t.mean(2)<220);assert mask.sum()>12
    v=t[mask];v-=v.mean(0);den=np.sqrt((v*v).sum());matches=[]
    for r in selected:
     a=np.array(Image.open(N/(r['name']+'-native.png')).convert('RGB')).astype(float);best=None
     for dy in range(-3,4):
      for dx in range(-8,9):
       w=a[y0+dy:y1+dy,x0+dx:x1+dx][mask];w-=w.mean(0);score=float((v*w).sum()/max(1e-8,den*np.sqrt((w*w).sum())))
       if best is None or score>best[0]:best=(score,dx,dy)
     matches.append({'rawSlot':r['rawSlot'],'dx':best[1],'dy':best[2],'NCC':round(best[0],4)})
    results.append({'trial':trial,'gear':gear,'cycle':cycle,'height':height,'role':win['role'],'matches':matches,'screenMaterialDxSpan':max(m['dx'] for m in matches)-min(m['dx'] for m in matches),'screenMaterialDySpan':max(m['dy'] for m in matches)-min(m['dy'] for m in matches),'minimumNCC':min(m['NCC'] for m in matches)})
boundary=Image.new('RGB',(900,2480),(32,43,49));d=ImageDraw.Draw(boundary)
for j,(trial,gear,sample) in enumerate([(t,g,n) for t in range(2) for g in ['bare','helmet'] for n in [21,22]]):
 r=next(r for r in records if r['trial']==trial and r['gear']==gear and r['sample']==sample);im=Image.open(N/(r['name']+'-native.png')).crop((0,330,900,620));boundary.paste(im,(0,j*310+20));d.text((5,j*310+2),f"trial{trial} {gear} wrap raw{r['rawSlot']} actual traveling root",fill='white')
boundary.save(P/'native-stride-boundary-review.png')
before=json.loads((N/'inputs-after.json').read_text(encoding='utf-8'));assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==sha for p,sha in before.items())
report={'checks':checks,'failures':0,'sourcePosePixelChecks':len(records),'nativeInputsStillStable':len(before),'nativeValidation':json.loads((N/'validation.json').read_text(encoding='utf-8')),'independentRenderedMaterialWindows':results,'scope':'Two hypotheses/two actual distance-driven cycles/all21poses/both gears/47,93,148. Exact timestamped native replay and exact selected source pixels. Independent rendered warm-boot appearance correspondence in two short support windows/cycle at93/148. Not physical rigid sole, complete heel/toe roll, near/far occlusion continuity, final loop/contact/start-stop or normal station integration.'}
(P/'native-stride-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'inputsStable':len(before),'supportWindows':[{'trial':r['trial'],'gear':r['gear'],'cycle':r['cycle'],'height':r['height'],'role':r['role'],'dxSpan':r['screenMaterialDxSpan'],'dySpan':r['screenMaterialDySpan'],'minNCC':r['minimumNCC']} for r in results]}))
