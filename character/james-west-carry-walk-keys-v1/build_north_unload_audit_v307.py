from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-join-audit-v307';o.mkdir(exist_ok=True);sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
board=Image.new('RGBA',(2048,560),(47,59,63,255));d=ImageDraw.Draw(board);rows=[];clocks={}
for row,gear in enumerate(('bare','helmet')):
 mpath=r/f'character/james-cargo-material-joined-v1/{gear}-manifest.json';m=json.loads(mpath.read_bytes());state=next(s for s in m['states'] if s['id']=='unload-north');clocks[gear]=state['frameDurationsMs']
 files=[r/f'character/james-cargo-turn-north-west-v1/frames/{gear}/carry-turn-west-north/005.png']+[(r/f[6:] if f.startswith('res://') else mpath.parent/f) for f in state['frameFiles']]+[r/f'character/james-cargo-turn-north-west-v1/north-{gear}-standing-master.png']
 assert len(files)==8
 for i,f in enumerate(files):
  im=Image.open(f).convert('RGBA');raw_size=im.size
  if i==7:
   assert raw_size==(1024,1024)
   im=im.resize((256,256),Image.Resampling.NEAREST)
  else:assert raw_size==(256,256)
  board.alpha_composite(im,(i*256,row*280+24));label=['Turn end']+[f'Unload {n}' for n in range(6)]+['Runtime North standing'];d.text((i*256+3,row*280+4),gear+' / '+label[i],fill='white')
  a=np.asarray(im);ys,xs=np.where(a[:,:,3]>=128);rows.append(dict(gear=gear,label=label[i],file=f.relative_to(r).as_posix(),sha256=sha(f),rawCanvasSize=raw_size,reviewCanvasSize=im.size,wholeCanvasMasterScale=.25 if i==7 else 1.0,bounds128=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]))
  d.line((i*256,row*280+248,i*256+255,row*280+248),fill=(100,130,130,255))
 rows.append(dict(gear=gear,label='Manifest',file=mpath.relative_to(r).as_posix(),sha256=sha(mpath)))
board.save(o/'joined-source-audit.png');(o/'inputs.json').write_text(json.dumps(dict(sources=rows,unloadDurationsMs=clocks,normalChanged=False,northReferenceStatus='Runtime-derived standing comparison; reference-derived North raw is not automatically an accepted original master.'),indent=2)+'\n');print(json.dumps(dict(sources=len(rows),durations=clocks,output=str(o))))
