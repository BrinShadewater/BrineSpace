"""Independent visible boot registration on native captures; sparse-chain diagnosis."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2];O=R/'output/veld-east-key-chain-v1'
records=json.loads((O/'records.json').read_text(encoding='utf-8'))['records'];reports=[]
for gear in ['bare','helmet']:
 rows=[r for r in records if r['gear']==gear]
 images=[Image.open(O/(r['name']+'-native.png')).convert('RGBA') for r in rows]
 durations=[max(1,round((rows[i+1]['time']-r['time'])*1000)) if i+1<len(rows) else 40 for i,r in enumerate(rows)]
 images[0].save(P/f'{gear}-native-moving-key-replay.png',save_all=True,append_images=images[1:],duration=durations,loop=1,disposal=0,blend=0)
 # Verify full native replay exact source frames and diagnostic timestamp holds.
 replay=Image.open(P/f'{gear}-native-moving-key-replay.png');assert replay.n_frames==len(images)
 for i,im in enumerate(images):replay.seek(i);assert np.array_equal(np.array(replay.convert('RGBA')),np.array(im));assert round(replay.info['duration'])==durations[i]
 board=Image.new('RGB',(1100,800),(32,43,49));d=ImageDraw.Draw(board)
 for j,r in enumerate(rows):
  crop=images[j].crop((190,395,290,570));x=(j%10)*110;y=(j//10)*200
  board.paste(crop,(x,y+25),crop);d.text((x+2,y+3),f"{r['time']:.3f}s / {r['slot']}",fill='white')
 board.save(P/f'{gear}-native-chronology.png')
 for height,box in [(148,(209,547,239,565)),(93,(217,316,237,330))]:
  a=np.array(images[0].convert('RGB')).astype(float);x0,y0,x1,y1=box;t=a[y0:y1,x0:x1];mask=(t[:,:,0]>t[:,:,1]+3)&(t[:,:,0]>t[:,:,2]+3)&(t.mean(2)>40)&(t.mean(2)<220)
  assert mask.sum()>10;v=t[mask];v-=v.mean(0);den=np.sqrt((v*v).sum());measures=[]
  for r,im in zip(rows,images):
   a=np.array(im.convert('RGB')).astype(float);best=None
   for dy in range(-2,3):
    for dx in range(-8,9):
     w=a[y0+dy:y1+dy,x0+dx:x1+dx][mask];w-=w.mean(0);score=float((v*w).sum()/max(1e-8,den*np.sqrt((w*w).sum())))
     if best is None or score>best[0]:best=(score,dx,dy)
   measures.append({'time':r['time'],'slot':r['slot'],'dx':best[1],'dy':best[2],'NCC':round(best[0],4)})
  jumps=[]
  for i in range(1,len(measures)):
   if measures[i]['slot']!=measures[i-1]['slot']:jumps.append({'before':measures[i-1],'after':measures[i],'deltaX':measures[i]['dx']-measures[i-1]['dx']})
  reports.append({'gear':gear,'height':height,'templateBox':box,'maskPixels':int(mask.sum()),'dxSpan':max(m['dx'] for m in measures)-min(m['dx'] for m in measures),'minimumNCC':min(m['NCC'] for m in measures),'joins':jumps,'measurements':measures})
report={'nativeReplayChecks':len(records)*2,'nativeReplayFailures':0,'bootRegistration':reports,'scope':'Read-only visible warm boot-material translation proxy on all37prescribed-time captures per gear, not rigid sole/support proof. Root8nativepx/sec is illustrative. Sparse3keys omit intermediates. Replay is exact prescribed native snapshots, not continuous station screen recording. No full transition/controller/save acceptance.','bindings':{str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'study-record.json',O/'validation.json',O/'records.json',Path(__file__)]}}
(P/'native-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'replayChecks':report['nativeReplayChecks'],'rows':[{k:r[k] for k in ['gear','height','dxSpan','minimumNCC','joins']} for r in reports]}))
