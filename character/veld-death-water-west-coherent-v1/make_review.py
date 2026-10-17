"""Finite one-shot comparison, with a held terminal and explicit replay."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1];tracks={};bound={}
audit=json.loads((R/'character/veld-life-death-audit-v1/coverage.json').read_text(encoding='utf-8'))
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text(encoding='utf-8'));s=m['states'][0]
 old=audit['selected'][gear]['death-water-west'];ref=R/f'character/veld-water-west-coherent-v1/frames/{gear}/swim-west/000.png'
 def url(f):
  bound[f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
  return '../'+f.relative_to(R/'character').as_posix()+'?v='+bound[f.relative_to(R).as_posix()][:12]
 tracks[gear]={'candidate':[url(P/f) for f in s['frameFiles']],'old':[url(R/f) for f in old['files']],'master':url(ref),'durations':s['frameDurationsMs'],'oldDurations':old['durations'],'oldPivot':old['pivot'],'oldHeight':old['standingHeight']}
html='''<!doctype html><meta charset="utf-8"><title>Veld west water death — finite master comparison</title>
<style>body{background:#202a30;color:#e6ecee;font:16px system-ui;margin:24px}p{max-width:90ch}main{display:grid;grid-template-columns:repeat(3,240px);gap:16px}canvas{display:block}button,select{font:inherit;padding:6px}a{color:#9bd3ed}</style>
<h1>Veld west prone water death — candidate</h1><p>One finite1560ms sequence, then held terminal. Exact selected swim entry, one fixed body ruler/belt anchor, master material grade and native helmet hardware with authored closing eyes. Candidate only: upright tread entrance, world/restore/normal selection and other directions remain.</p>
<button id="replay">Replay</button> <button id="play">Pause</button> <label>Standing height <select id="size"><option>82</option><option>148</option><option>54</option></select></label> <button id="background">Light background</button><p id="status">Loading</p>
<main><div>Selected bare swim<canvas id="bare-master" width="240" height="180"></canvas></div><div>Previous bare death<canvas id="bare-old" width="240" height="180"></canvas></div><div>Candidate bare death<canvas id="bare-candidate" width="240" height="180"></canvas></div><div>Selected helmet swim<canvas id="helmet-master" width="240" height="180"></canvas></div><div>Previous helmet death<canvas id="helmet-old" width="240" height="180"></canvas></div><div>Candidate helmet death<canvas id="helmet-candidate" width="240" height="180"></canvas></div></main>
<p><a href="paired-contact.png">All poses/master</a> · <a href="station-scale-contact.png">Station-scale board</a> · <a href="../veld-life-death-audit-v1/">Cardinal death audit</a></p>
<script>const tracks=TRACKS;let elapsed=0,last=performance.now(),playing=true,light=false;const size=document.querySelector('#size'),play=document.querySelector('#play'),status=document.querySelector('#status');document.querySelector('#replay').onclick=()=>{elapsed=0;playing=true;play.textContent='Pause'};play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};document.querySelector('#background').onclick=()=>{light=!light};
function slot(t,d){let i=0;while(i<d.length-1&&t>=d[i])t-=d[i++];return i}
async function load(files){return Promise.all(files.map(f=>new Promise((yes,no)=>{let im=new Image;im.onload=()=>yes(im);im.onerror=()=>no(new Error(f));im.src=f})))}
Promise.all(Object.values(tracks).map(async t=>{t.c=await load(t.candidate);t.o=await load(t.old);t.m=(await load([t.master]))[0]})).then(()=>{function frame(now){if(playing)elapsed+=now-last;last=now;let text=[];for(const gear of ['bare','helmet']){let t=tracks[gear],i=slot(elapsed,t.durations),j=slot(elapsed,t.oldDurations);text.push(gear+' '+i);for(const [name,image,pivot,height] of [['master',t.m,[128,128],148],['old',t.o[j],t.oldPivot,t.oldHeight],['candidate',t.c[i],[128,128],148]]){let ctx=document.querySelector('#'+gear+'-'+name).getContext('2d');ctx.fillStyle=light?'#d7d9d7':'#202a30';ctx.fillRect(0,0,240,180);let scale=Number(size.value)/height;ctx.drawImage(image,120-pivot[0]*scale,90-pivot[1]*scale,image.width*scale,image.height*scale)}}status.textContent=text.join(' · ')+(elapsed>=1560?' · terminal held':' · '+Math.round(elapsed)+'ms');requestAnimationFrame(frame)}requestAnimationFrame(frame)}).catch(e=>status.textContent='Missing frame: '+e.message);</script>'''.replace('TRACKS',json.dumps(tracks))
(P/'index.html').write_text(html,encoding='utf-8')
(P/'review-bindings.json').write_text(json.dumps({'frames':bound,'scope':'literal selected old clips versus candidate/master; one finite preview with held terminal, not world proof'},indent=2)+'\n',encoding='utf-8')
print('Built finite master/previous/candidate comparison with explicit Replay; held terminal')
