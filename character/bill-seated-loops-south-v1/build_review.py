from pathlib import Path
import json
P=Path(__file__).resolve().parent
packs={}
for gear,folder in [('bare',P.parent/'bill-seated-south-coherent-v1'),('helmet',P.parent/'bill-seated-helmet-south-coherent-v1')]:
 states=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))['states']
 for state in states:state['frameFiles']=['../'+folder.name+'/'+f for f in state['frameFiles']]
 states+=json.loads((P/(gear+'-manifest.json')).read_text(encoding='utf-8'))['states'];packs[gear]=states
html='''<!doctype html><meta charset="utf-8"><title>Bill south seated breathing and reading</title>
<style>body{font:16px system-ui;background:#152027;color:#e6eff1;margin:24px}p{max-width:76ch;color:#bdd0d2}select,button{font:inherit;padding:6px}canvas{display:block;margin-top:16px}</style>
<h1>Bill — south seated breathing and reading</h1><p>Sit, breathe twice, rise. Exact seated endpoint joins, matte suit grade and native rear helmet. Staged south breathing/reading loops; real observation sofa contact and tablet entry/exit review pending. Runtime unchanged.</p>
<label>Gear <select id="gear"><option value="bare">Bare</option><option value="helmet">Helmet</option></select></label>
<label>Route <select id="route"><option value="chain">Sit, breathe, rise</option><option value="loop">Seated breathing</option><option value="reading" selected>Seated reading</option></select></label>
<label>Height <select id="size"><option>148</option><option selected>82</option><option>54</option></select></label>
<button id="play">Pause</button><button id="step">Next pose</button><span id="status"></span><canvas id="view" width="460" height="430"></canvas>
<script>const status=document.getElementById("status");const packs=DATA;let elapsed=0,last=performance.now(),playing=true,manual=0;
function selected(){const p=packs[gear.value],a=p.find(s=>s.id==='sit-down-south'),l=p.find(s=>s.id==='sit-idle-south'),b=p.find(s=>s.id==='sit-rise-south');if(route.value==='loop')return l;if(route.value==='reading')return p.find(s=>s.id==='read-seated-south');return {images:[...a.images,...l.images,...l.images,...b.images],frameDurationsMs:[...a.frameDurationsMs,...l.frameDurationsMs,...l.frameDurationsMs,...b.frameDurationsMs]}}
gear.onchange=route.onchange=()=>{elapsed=0;manual=0};play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};step.onclick=()=>{playing=false;play.textContent='Play';manual=(manual+1)%selected().images.length};
Promise.all(Object.values(packs).flat().map(async s=>{s.images=await Promise.all(s.frameFiles.map(f=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f}))) })).then(()=>{function draw(now){if(playing)elapsed+=now-last;last=now;const s=selected();let index=manual;if(playing){let cursor=elapsed%s.frameDurationsMs.reduce((a,b)=>a+b,0);for(let i=0;i<s.images.length;i++){index=i;if(cursor<s.frameDurationsMs[i])break;cursor-=s.frameDurationsMs[i]}}const c=view.getContext('2d');c.fillStyle='#22343e';c.fillRect(0,0,460,215);c.fillStyle='#dae1e0';c.fillRect(0,215,460,215);const factor=Number(size.value)/148;for(const y of [190,405])c.drawImage(s.images[index],230-128*factor,y-224*factor,256*factor,256*factor);status.textContent=' pose '+(index+1)+'/'+s.images.length;requestAnimationFrame(draw)}requestAnimationFrame(draw)});</script>'''
(P/'index.html').write_text(html.replace('DATA',json.dumps(packs)),encoding='utf-8')
