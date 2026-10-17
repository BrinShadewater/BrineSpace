"""Lossless source-only review; no generated/selected actor pixels are edited."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
items=[];hashes={};checks=0
case=Image.open(P/'floor-case-north.png').convert('RGBA')
for gear in ['bare','helmet']:
 manifest=json.loads((R/f'character/bill-unload-north-rise-v1/{gear}-manifest.json').read_text())
 clip=next(s for s in manifest['states'] if s['id']=='unload-north')
 paths=[R/path.removeprefix('res://') for path in clip['frameFiles']]
 frames=[Image.open(path).convert('RGBA') for path in paths]
 for path in paths:hashes[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
 idle_path=R/f'character/bill-carry-start-south-v2/short-route-captures/rot0-{gear}-completed-north-source.png'
 idle=Image.open(idle_path).convert('RGBA');assert idle.size==(184,184)
 body=Image.new('RGBA',(256,256));body.paste(idle,(36,52));terminal=Image.alpha_composite(case,body)
 # New prop composite is preview-only; opaque original master pixels remain exact.
 for a,b in zip(body.get_flattened_data(),terminal.get_flattened_data()):
  if a[3]==255:assert a==b;checks+=1
 hashes[idle_path.relative_to(R).as_posix()]=hashlib.sha256(idle_path.read_bytes()).hexdigest()
 for cut in [1,4,7,10]:
  seq=frames[cut:]+[terminal];lengths=[round(v) for v in clip['frameDurationsMs'][cut:]]+[600]
  lengths[0]-=1
  name=f'{gear}-finish-from-{cut:02d}.png'
  seq[0].save(P/name,save_all=True,append_images=seq[1:],duration=lengths,loop=0,disposal=0,blend=0)
  decoded=Image.open(P/name);assert decoded.n_frames==len(seq)
  for i,original in enumerate(seq):
   decoded.seek(i);assert decoded.convert('RGBA').tobytes()==original.tobytes();checks+=1
  items.append({'gear':gear,'cut':cut,'file':name,'remainingAuthoredMs':sum(lengths[:-1]),'terminalViewerHoldMs':600,'sourceOnly':True})
 board=Image.new('RGB',(1536,640),'#182932');draw=ImageDraw.Draw(board)
 for i,frame in enumerate(frames[7:]+[terminal]):
  x=(i%4)*384;y=(i//4)*320
  draw.text((x+8,y+6),f'{gear} · source {i+7}' if i<7 else f'{gear} · idle + separate prop study',fill='#dde8e9')
  board.paste(frame,(x,y+25),frame)
  native=frame.resize((113,113),Image.Resampling.LANCZOS)
  board.paste(native,(x+264,y+145),native)
  draw.text((x+264,y+265),'65.28/148 scale',fill='#dde8e9')
 board.save(P/f'{gear}-finish-source-review.png')
e={'checks':checks,'passed':True,'clips':items,'originalHashes':hashes,'scope':'Source-only ordinary service exit study: retain exact displayed original unload interior, continue remaining authored clock to terminal, then preview idle with independent prop. No new actor art, normal selection, runtime interruption or save/Continue admission. Fire/flood/death/gear priority disposition remains separate.'}
(P/'finish-source-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
html='''<!doctype html><meta charset="utf-8"><title>Bill ordinary set-down exit study</title><style>body{background:#182932;color:#dde8e9;font:15px system-ui;margin:22px}p{max-width:900px}section{display:flex;gap:26px;margin:24px 0}figure{margin:0}img.motion{width:113px;image-rendering:auto}.strip{max-width:none}</style><h1>Bill · ordinary service exit study</h1><p>Continue the remaining original North set-down/rise instead of restarting or snapping upright. Four cancellation source interiors, both gears. Lossless original RGBA frames and timing; first hold retains its remaining milliseconds. The terminal idle + separate floor prop is a preview composite, not a replacement body sprite.</p><p>Source-only study. Native density thumbnails use 65.28/148 scale; full registered sources below. 600ms terminal hold and repeat are viewer behavior. No live interruption, needs/hazard, Continue or normal integration acceptance. Arrival turns and other directions still require their own exits.</p>'''
for gear in ['bare','helmet']:
 html+=f'<h2>{gear}</h2><section>'
 for row in [r for r in items if r['gear']==gear]:html+=f'<figure><figcaption>From source {row["cut"]}</figcaption><img class="motion" src="{row["file"]}"></figure>'
 html+=f'</section><img class="strip" src="{gear}-finish-source-review.png">'
(P/'finish-source-review.html').write_text(html,encoding='utf-8')
print(f'{len(items)}lossless source-motion studies;{checks} decoded/pixel guards passed.')
