from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-carry-south-start-station-v2'
d=json.loads((O/'journeys.json').read_text());v=json.loads((O/'validation.json').read_text());assert v['passed'] and d['failures']==0
cases=[]
for j in d['journeys']:
 if not j['candidate']:continue
 gear='helmet' if j['helmet'] else 'bare';start=next(r['time'] for r in j['records'] if r['starting']);chosen={};timeline=[]
 for r in j['records']:
  if r['time']<start or not (r['starting'] or r['slot']>=0):continue
  elapsed=r['time']-start
  if r['starting']:
   ms=elapsed*1000;acc=0;index=5
   for i,dt in enumerate([40,50,55,65,65,45]):
    acc+=dt
    if ms<acc:index=i;break
   path=f'frames/{gear}/carry-start-south/{index:03}.png'
  else:path=f'../bill-carry-south-gait-v3/frames/{gear}/carry-south/{r["slot"]:03}.png'
  timeline.append({'time':elapsed,'path':path,'foot':r['foot']})
 for c in j['captures']:
  r=min(j['records'],key=lambda r:abs(r['time']-c['time']))
  if r['time']<start or not (r['starting'] or r['slot']>=0):continue
  path=min(timeline,key=lambda t:abs(t['time']-(r['time']-start)))['path']
  # Keep every source row, including repeated contact rows4/5 with equal pixels.
  chosen.setdefault(path,c)
 b=Image.new('RGB',(1200,600),'#22343e');dr=ImageDraw.Draw(b)
 for i,(path,c) in enumerate(chosen.items()):
  x0=(i%6)*200;y0=(i//6)*300;a=Image.open(O/c['room']).convert('RGB');x=255+(c['foot'][0]-7680)*398/384;y=287+(c['foot'][1]-8064)*398/384;b.paste(a.crop((round(x)-75,round(y)-130,round(x)+75,round(y)+50)),(x0+25,y0))
  src=Image.open(O/c['source']).convert('RGBA');expected=Image.open(P/path).convert('RGBA');assert src.tobytes()==expected.tobytes(),'Actual displayed source differs'
  scale=82/148;src=src.resize((round(src.width*scale),round(src.height*scale)),Image.Resampling.LANCZOS);b.paste(src,(round(x0+100-128*scale),round(y0+280-224*scale)),src);dr.text((x0+5,y0+285),('step ' if 'carry-start' in path else 'gait ')+Path(path).stem,fill='white')
 assert len(chosen)==12
 b.save(P/(gear+'-native-review.png'));cases.append({'gear':gear,'timeline':timeline,'duration':timeline[-1]['time']})
(P/'replay.json').write_text(json.dumps(cases,indent=2)+'\n')
html='''<!doctype html><meta charset="utf-8"><title>Bill - south articulated step</title><style>body{background:#182932;color:#dde8e9;font:16px system-ui;margin:24px}canvas{background:#22343e;border:1px solid #4c626d;max-width:100%}img{max-width:100%}label,button{margin:8px}h2{font-size:20px}</style><h1>Bill - south articulated step</h1><p>South motion polish preview.</p><p>The held pose opens into the first step, then joins the new walking contact. Head, helmet, shoulders, hands and cargo retain the accepted master art.</p><label>Size <select id="size"><option>82</option><option>148</option></select></label><label>Review <select id="mode"><option value="first">First step</option><option value="full">First step and walk</option><option value="loop">Walking loop</option></select></label><button id="play">Pause</button><p id="clock"></p><section><h2>Bare · master / first step and walk</h2><canvas id="bare" width="480" height="270"></canvas></section><section><h2>Helmet · master / first step and walk</h2><canvas id="helmet" width="480" height="270"></canvas></section><p>Moving preview replays source choices at recorded room timestamps, at a fixed review pivot. Walking loop repeats the six authored gait poses on their 840ms clock to expose the end-to-start join. Room captures below show all six first-step rows and all six walking poses. New sessions use this South set. Existing saves retain their paired North/South source version. Save/resume and interruptions pass the current station checks; natural routes and broader contact/loop polish remain under review. <a href="version-continue.html" style="color:#adcddd">View station Continue comparisons</a> Compare directional masters: <a style="color:#adcddd" href="../bill-carry-south-gait-v3/bare-cross-family-review.png">bare</a> / <a style="color:#adcddd" href="../bill-carry-south-gait-v3/helmet-cross-family-review.png">helmet</a>.</p><h2>Actual workshop · bare</h2><img src="bare-native-review.png"><h2>Actual workshop · helmet</h2><img src="helmet-native-review.png"><script>const cases=CASES,images=new Map();for(const c of cases){for(const p of [...c.timeline.map(t=>t.path),`../bill-cargo-south-master-head-v1/frames/${c.gear}/pickup-south/011.png`]){if(images.has(p))continue;let a=new Image();a.src=p;images.set(p,a)}}let playing=true,elapsed=0,last=performance.now();document.querySelector('#mode').onchange=()=>elapsed=0;document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play'};function tick(now){if(playing)elapsed+=(now-last)/1000;last=now;let mode=document.querySelector('#mode').value,first=mode==='first',loop=mode==='loop',t=loop?.32+elapsed%.84:elapsed%(first?1.07:Math.max(...cases.map(c=>c.duration))+.7)-.25;if(first)t=Math.min(t,.32);for(const c of cases){const canvas=document.querySelector('#'+c.gear),ctx=canvas.getContext('2d'),scale=Number(document.querySelector('#size').value)/148;ctx.clearRect(0,0,480,270);let master=`../bill-cargo-south-master-head-v1/frames/${c.gear}/pickup-south/011.png`,path=master;if(t>=0){for(const r of c.timeline){if(r.time>t)break;path=r.path}}if(loop)path=`../bill-carry-south-gait-v3/frames/${c.gear}/carry-south/${String(Math.floor(elapsed%.84/.14)).padStart(3,'0')}.png`;for(const [p,x] of [[master,120],[path,360]]){let a=images.get(p);if(a&&a.complete&&a.naturalWidth)ctx.drawImage(a,x-128*scale,240-224*scale,a.width*scale,a.height*scale)}}document.querySelector('#clock').textContent=loop?'Walking loop':t<0?'Held master':t<.32?'First step':'Walking';requestAnimationFrame(tick)}requestAnimationFrame(tick)</script>'''
(P/'index.html').write_text(html.replace('CASES',json.dumps(cases)),encoding='utf-8')
(P/'runtime-evidence.json').write_text(json.dumps({'validation':v,'journeys':d,'directEntryGuards':json.loads((R/'output/bill-carry-south-start-player-v2/validation.json').read_text()),'normalSelectionChanged':False,'scope':'Actual workshop dispatch, prescribed East-facing start/graph-clear South lane, staged planted turn/finite bridge/exact contact join and production walk. Direct-entry/gear/backwards-clock separate headless guards. No normal loader/title Continue, natural routes, interruptions or anatomical contact acceptance.'},indent=2)+'\n');print('24 unique first-step/gait source selections exactly match actual room captures; paired native review and recorded-clock preview saved')


if (P/"review-assessment.json").exists():
 e=json.loads((P/"runtime-evidence.json").read_text());e.update(json.loads((P/"review-assessment.json").read_text()));(P/"runtime-evidence.json").write_text(json.dumps(e,indent=2)+"\n")
