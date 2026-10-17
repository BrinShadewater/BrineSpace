"""Same-clock selected-master/action review without changing source frames."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
tracks={};bindings={}
for direction in ['east','west','north','south']:
 tracks[direction]={}
 for gear in ['bare','helmet']:
  candidate=json.loads((P/f'{gear}-manifest.json').read_text());c=next(s for s in candidate['states'] if s['id']=='swim-distress-'+direction)
  folder=R/f'character/veld-water-{direction}-coherent-v1';master=json.loads((folder/f'{gear}-manifest.json').read_text());m=next(s for s in master['states'] if s['id']=='swim-'+direction)
  paths=[folder/f for f in m['frameFiles']]+[P/f for f in c['frameFiles']]
  bindings.update({f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths})
  tracks[direction][gear]={'master':['../'+folder.name+'/'+f+'?v='+hashlib.sha256((folder/f).read_bytes()).hexdigest()[:12] for f in m['frameFiles']],'candidate':[f+'?v='+hashlib.sha256((P/f).read_bytes()).hexdigest()[:12] for f in c['frameFiles']],'masterDurations':m['frameDurationsMs'],'candidateDurations':c['frameDurationsMs']}
html='''<!doctype html><meta charset="utf-8"><title>Veld distress motion and master joins</title>
<style>body{background:#202a30;color:#e1e7eb;font:16px system-ui;margin:24px}label,button,select{font:inherit}button,select{padding:7px}canvas{display:block}main{display:grid;grid-template-columns:250px 250px;gap:18px}a{color:#9bd3ed}p{max-width:85ch}</style>
<h1>Veld distress — selected swim comparison</h1><p>Same pivot and standing-height scale. Left: selected swimming loop. Right: selected distress. Actual manifest timing, full speed. The join mode previews swimming → distress → swimming with each action entering at frame zero and distress exiting after the chosen phase; this is a visual review sequence, not an escape journey.</p>
<label>Direction <select id="direction"><option>east</option><option>west</option><option>north</option><option>south</option></select></label>
<label>Sequence <select id="mode"><option value="loop">Distress loop</option><option value="join">Swim → distress → swim</option></select></label>
<label>Standing height <select id="size"><option>82</option><option>148</option><option>54</option></select></label>
<label>Distress exit phase <select id="exit"><option value="5">5 — closure</option><option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option></select></label>
<button id="play">Pause</button><button id="background">Light background</button>
<p id="status">Loading</p><main><div>Selected bare swim<canvas id="bare-master" width="240" height="180"></canvas></div><div>Selected bare distress<canvas id="bare-candidate" width="240" height="180"></canvas></div><div>Selected helmet swim<canvas id="helmet-master" width="240" height="180"></canvas></div><div>Selected helmet distress<canvas id="helmet-candidate" width="240" height="180"></canvas></div></main>
<p><a href="index.html">Cardinal contact and original loops</a></p>
<script>const tracks=TRACKS;const dir=document.querySelector('#direction'),mode=document.querySelector('#mode'),size=document.querySelector('#size'),exit=document.querySelector('#exit'),play=document.querySelector('#play'),background=document.querySelector('#background');let elapsed=0,last=performance.now(),running=true,light=false;
dir.onchange=mode.onchange=exit.onchange=()=>{elapsed=0};play.onclick=()=>{running=!running;play.textContent=running?'Pause':'Play'};background.onclick=()=>{light=!light;background.textContent=light?'Dark background':'Light background'};
function index(t,d){t%=d.reduce((a,b)=>a+b,0);let i=0;while(i<d.length-1&&t>=d[i])t-=d[i++];return i}
async function load(files){return Promise.all(files.map(f=>new Promise((yes,no)=>{let im=new Image;im.onload=()=>yes(im);im.onerror=()=>no(new Error(f));im.src=f})))}
Promise.all(Object.values(tracks).flatMap(pair=>Object.values(pair).map(async t=>{t.m=await load(t.master);t.c=await load(t.candidate)}))).then(()=>{function frame(now){if(running)elapsed+=now-last;last=now;let text=[];
for(const gear of ['bare','helmet']){const t=tracks[dir.value][gear];let mi=index(elapsed,t.masterDurations),ci=index(elapsed,t.candidateDurations),im=t.c[ci],stage='distress';
if(mode.value==='join'){let a=t.masterDurations.reduce((x,y)=>x+y,0),b=t.candidateDurations.slice(0,Number(exit.value)+1).reduce((x,y)=>x+y,0),v=elapsed%(a+b+a);if(v<a){ci=index(v,t.masterDurations);im=t.m[ci];stage='swim entry'}else if(v<a+b){ci=index(v-a,t.candidateDurations);im=t.c[ci]}else{ci=index(v-a-b,t.masterDurations);im=t.m[ci];stage='swim exit'}}
text.push(gear+': '+stage+' '+ci);for(const [lane,image] of [['master',t.m[mi]],['candidate',im]]){let ctx=document.querySelector('#'+gear+'-'+lane).getContext('2d');ctx.fillStyle=light?'#d7d9d7':'#202a30';ctx.fillRect(0,0,240,180);let scale=Number(size.value)/148;ctx.imageSmoothingEnabled=true;ctx.drawImage(image,120-128*scale,90-128*scale,256*scale,256*scale)}}
document.querySelector('#status').textContent=text.join(' · ');requestAnimationFrame(frame)}requestAnimationFrame(frame)}).catch(e=>document.querySelector('#status').textContent='Missing image: '+e.message);
</script>'''.replace('TRACKS',json.dumps(tracks))
(P/'motion.html').write_text(html,encoding='utf-8')
(P/'motion-review-bindings.json').write_text(json.dumps({'boundFrames':bindings,'scope':'selected swim and candidate exact pixels/manifest timing; visual sequence does not prove actual world escape'},indent=2)+'\n',encoding='utf-8')
print('Built same-clock four-direction master/action and entry/exit review; source pixels unchanged')
