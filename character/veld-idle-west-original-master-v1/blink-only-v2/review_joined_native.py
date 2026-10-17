from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2];N=R/'output/veld-west-idle-scanner-joins-v1'
records=json.loads((N/'records.json').read_bytes())['records'];checks=0
for gear in ['bare','helmet']:
 rows=[r for r in records if r['gear']==gear];assert len(rows)==426
 frames=[Image.open(N/(r['name']+'-native.png')).convert('RGBA') for r in rows]
 durations=[r['durationMs'] for r in rows]
 frames[0].save(P/f'{gear}-native-joined.png',save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0)
 replay=Image.open(P/f'{gear}-native-joined.png');assert replay.n_frames==426
 for i,im in enumerate(frames):replay.seek(i);assert np.array_equal(np.asarray(replay.convert('RGBA')),np.asarray(im));assert round(replay.info['duration'])==durations[i];checks+=2
 for start in range(0,142,48):
  board=Image.new('RGB',(990,1520),'#202a30');draw=ImageDraw.Draw(board)
  for j,im in enumerate(frames[start:min(start+48,142)]):
   xy=((j%6)*165,(j//6)*190);board.paste(im.crop((145,395,310,570)).convert('RGB'),(xy[0],xy[1]+15));draw.text((xy[0]+3,xy[1]+1),f'{gear} idle {start+j}',fill='white')
  board.save(P/f'native-{gear}-idle-{start//48:02}.png')
 board=Image.new('RGB',(1320,420),'#202a30');draw=ImageDraw.Draw(board)
 for j,n in enumerate([140,141,142,143,282,283,284,285]):
  im=frames[n];board.paste(im.crop((145,395,310,570)).convert('RGB'),(j*165,24));draw.text((j*165+3,4),f'{gear} joined {n}',fill='white')
  head=im.crop((205,408,254,459)).resize((147,153),Image.Resampling.NEAREST);board.paste(head,(j*165,228))
 board.save(P/f'native-{gear}-join-details.png')
before=json.loads((N/'inputs-after.json').read_bytes());assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in before.items())
(P/'native-review.json').write_text(json.dumps(dict(replayChecks=checks,failures=0,frameCountPerGear=426,durationMs=sum(durations),nativeInputsUnchanged=len(before),scope='Exact full paired native source-clock replay; complete new idle chronology and both boundaries for review. Not ordinary scene/controller/contact or full continuous motion acceptance.'),indent=2)+'\n')
page='''<!doctype html><meta charset="utf-8"><title>Veld West matching idle and scanner</title><style>body{background:#202a30;color:#eee;font:16px system-ui;margin:24px}button{padding:8px;font:inherit;margin:4px}.row{display:flex;gap:24px;align-items:end}figure{margin:12px}a{color:#b7daee}</style><h1>Veld West matching idle and scanner</h1><p>Complete new idle → scanner → idle beside the original master. The stance and helmet now line up. Fabric detail and continuous motion are still being reviewed.</p><button onclick="setGear('bare')">Standard</button><button onclick="setGear('helmet')">Helmet</button><button onclick="setGear(gear)">Replay</button>'''
for h in [47,93,148]:
 page+=f'<h2>{h}px standing height</h2><div class="row"><figure><img class="chain" width="{256*h/148}"><figcaption>Idle / scanner / idle</figcaption></figure><figure><img class="original" width="{256*h/148}"><figcaption>Original master</figcaption></figure></div>'
page+='''<p><a href="bare-native-joined.png">Standard rendered sequence</a> · <a href="helmet-native-joined.png">Helmet rendered sequence</a> · <a href="native-bare-join-details.png">Standard transition details</a> · <a href="native-helmet-join-details.png">Helmet transition details</a></p><script>let gear='bare';function setGear(g){gear=g;document.querySelectorAll('.chain').forEach(i=>i.src=g+'-joined-full-source.png?v='+Date.now());document.querySelectorAll('.original').forEach(i=>i.src=g+'-original-reference.png')}setGear(gear)</script>'''
(P/'index.html').write_text(page,encoding='utf-8');print(f'{checks} native replay checks0;{len(before)} native inputs unchanged; complete426 paired review ready')
