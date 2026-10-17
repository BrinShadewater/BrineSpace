from pathlib import Path
import json,math
import numpy as np
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;D=H/'review';q=json.loads((D/'report.json').read_text())
for gear in ['bare','helmet']:
 rows=[r for r in q['records'] if r['gear']==gear]
 full=np.array(Image.open(D/(gear+'-bunk-enter-full.png')).convert('RGB'));room=np.array(Image.open(D/rows[0]['file']).convert('RGB'))
 rh,rw=room.shape[:2];fh,fw=full.shape[:2]
 match=np.ones((fh-rh+1,fw-rw+1),dtype=bool)
 for dy,dx in [(0,0),(20,20),(rh//2,rw//2),(rh-1,rw-1)]:match &= np.all(full[dy:dy+match.shape[0],dx:dx+match.shape[1]]==room[dy,dx],axis=2)
 ys,xs=np.where(match);origins=[(int(x),int(y)) for y,x in zip(ys,xs) if np.array_equal(full[y:y+rh,x:x+rw],room)]
 assert len(origins)==1,origins
 origin=origins[0]
 rects=[r['screen'] for r in rows]
 box=(math.floor(min(r[0] for r in rects)-origin[0]-6),math.floor(min(r[1] for r in rects)-origin[1]-6),math.ceil(max(r[0]+r[2] for r in rects)-origin[0]+6),math.ceil(max(r[1]+r[3] for r in rects)-origin[1]+6))
 assert box[0]>=0 and box[1]>=0 and box[2]<=room.shape[1] and box[3]<=room.shape[0],box
 frames=[];durations=[];witnesses=[];previous=None
 for i,r in enumerate(rows):
  im=Image.open(D/r['file']).convert('RGB');d=ImageDraw.Draw(im);d.rectangle((0,0,im.width,18),fill='#142129');d.text((6,3),gear+' / '+r['action']+' / %.3fs'%r['time'],fill='white');frames.append(im)
  durations.append(round((i+1)*1000/30)-round(i*1000/30))
  if (r['action'],r['sourceHash'])!=previous:
   witnesses.append((r,Image.open(D/r['file']).convert('RGB').crop(box)))
  previous=(r['action'],r['sourceHash'])
 output=H/(gear+'-native.webp')
 if not output.exists() or output.stat().st_size==0:frames[0].save(output,save_all=True,append_images=frames[1:],duration=durations,loop=0,lossless=True,method=3)
 cellw=max(220,box[2]-box[0]+10);cellh=box[3]-box[1]+28
 board=Image.new('RGB',(cellw*5,math.ceil(len(witnesses)/5)*cellh),'#1b272d');d=ImageDraw.Draw(board)
 for i,(r,im) in enumerate(witnesses):
  x=i%5*cellw;y=i//5*cellh;board.paste(im,(x,y+22));d.text((x+4,y+4),r['action']+' / %.3fs'%r['time'],fill='white')
 board.save(H/(gear+'-native-witnesses.png'))
 print(gear,{'nativeFrames':len(rows),'poseChanges':len(witnesses),'matchedRoomOrigin':origin,'cropBox':box,'durationMs':sum(durations)})
q['visualScope']='Every native pose-change witness and complete room context reviewed by the agent. Animated WebP reconstructs the 30Hz simulation; actual capture ran slower than real time.'
(H/'native-review.json').write_text(json.dumps({k:v for k,v in q.items() if k!='records'},indent=2))
html='''<!doctype html><meta charset="utf-8"><title>Krusher Dom · Native station motion</title><style>body{background:#172127;color:#d9e6e8;font:17px system-ui;max-width:1100px;margin:40px auto}img{max-width:100%;image-rendering:pixelated}.pair{display:flex;gap:24px}.pair>div{flex:1}p{line-height:1.5}</style><h1>Krusher Dom · Station handoffs</h1><p>V11 candidate, actual default bunk and production actor updates. Entry → sleep → exit → idle in both equipment variants. Captured native frames replay at their 30Hz simulation cadence; capture itself ran slower than real time. Looping back to entry is a review reset.</p><div class=pair><div><h2>Bare head</h2><img src="bare-native.webp"></div><div><h2>Diving helmet</h2><img src="helmet-native.webp"></div></div><p>852 native frames · 4,317 checks · zero failures · owner profile unchanged. The source-scale handoff review covers 198 contextual plans, including all 72 turns. Normal roster integration remains separate.</p><h2>Chronological pose witnesses</h2><img src="helmet-native-witnesses.png"><img src="bare-native-witnesses.png">'''
(H/'index.html').write_text(html,encoding='utf-8')
