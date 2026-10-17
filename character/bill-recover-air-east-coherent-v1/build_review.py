from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
packs={k:json.loads((folder/'manifest.json').read_text(encoding='utf-8'))['states'] for k,folder in [('bare',HERE),('helmet',HERE.parent/'bill-recover-air-helmet-east-coherent-v1')]}
for state in packs['helmet']:
 state['frameFiles']=['../bill-recover-air-helmet-east-coherent-v1/'+f for f in state['frameFiles']]
html='''<!doctype html><meta charset="utf-8"><title>Bill east dry recovery candidate</title>
<style>body{font:16px system-ui;background:#152027;color:#e6eff1;margin:20px}p{max-width:80ch;color:#bdd0d2}button,select{font:inherit;padding:6px}canvas{display:block;margin-top:15px}a{color:#92d9dc}</style>
<h1>Bill — east air recovery</h1><p>Finite three-second dry recovery. Planted boots, authored forward lean, selected matte materials and native tilted dry helmet. Exact idle entry and exit. Staged; other directions and live recovery trigger/restore proof follow.</p>
<label>Gear <select id="gear"><option value="bare">Bare</option><option value="helmet">Helmet</option></select></label>
<label>Route <select id="route"></select></label>
<label>Height <select id="size"><option>148</option><option selected>82</option><option>54</option></select></label>
<button id="play">Pause</button><button id="step">Next pose</button> <span id="status"></span><canvas id="view" width="460" height="430"></canvas>
<script>const packs=DATA;let playing=true,last=performance.now(),elapsed=0,manual=0;
for(const s of packs.bare){const o=document.createElement('option');o.value=s.id;o.textContent=s.id;route.append(o)}route.value='recover-air-east';
gear.onchange=route.onchange=()=>{elapsed=0;manual=0};play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};step.onclick=()=>{playing=false;manual=(manual+1)%selected().frameFiles.length;play.textContent='Play'};
function selected(){return packs[gear.value].find(s=>s.id===route.value)}
Promise.all(Object.values(packs).flat().map(async s=>{s.images=await Promise.all(s.frameFiles.map(f=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f}))) })).then(()=>{function draw(now){if(playing)elapsed+=(now-last);last=now;const s=selected();let index=manual;if(playing){let total=s.frameDurationsMs.reduce((a,b)=>a+b,0);let cursor=elapsed%(total+600);cursor=Math.min(cursor,total-1);index=s.images.length-1;for(let i=0;i<s.images.length;i++){if(cursor<s.frameDurationsMs[i]){index=i;break}cursor-=s.frameDurationsMs[i]}}const c=view.getContext('2d');c.fillStyle='#22343e';c.fillRect(0,0,460,215);c.fillStyle='#dae1e0';c.fillRect(0,215,460,215);const factor=Number(size.value)/148;for(const y of [190,405])c.drawImage(s.images[index],230-128*factor,y-224*factor,256*factor,256*factor);document.querySelector('#status').textContent=' pose '+(index+1)+'/'+s.images.length;requestAnimationFrame(draw)}requestAnimationFrame(draw)});</script>'''
(HERE/'index.html').write_text(html.replace('DATA',json.dumps(packs)),encoding='utf-8')
print('Built paired east recovery review')
