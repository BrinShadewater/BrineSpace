from pathlib import Path
import json,copy
HERE=Path(__file__).resolve().parent
p=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
states=copy.deepcopy(p['states'])
for state in states:state['id']+=' · bare candidate'
helmet=json.loads((HERE.parent/'bill-swim-carry-turn-helmet-south-west-v1/manifest.json').read_text(encoding='utf-8'))
for state in helmet['states']:
 state['id']+=' · helmet candidate';state['frameFiles']=['../bill-swim-carry-turn-helmet-south-west-v1/'+file for file in state['frameFiles']];states.append(state)
html='''<!doctype html><meta charset="utf-8"><title>Bill water cargo turn — south/west candidate</title>
<style>body{font:16px system-ui;background:#152027;color:#e6eff1;margin:20px}p{max-width:80ch;color:#bdd0d2}canvas{display:block}button,select{font:inherit;padding:6px}</style>
<h1>Bill — south/west water carrying turn</h1><p>Bare and helmet candidates. Four authored intermediate views, exact registered carrying-loop endpoints and derived reverse. Canonical ring insignia; independently authored west-facing views. 670 candidate native checks pass including finite turn phases, pauses and destination resume. Remaining direction pairs are pending. Runtime selection unchanged.</p>
<button id="play">Pause</button> <button id="step">Next pose</button> Height <select id="size"><option>148</option><option selected>82</option><option>54</option></select> <span id="status"></span><main id="tracks"></main>
<script>const states=DATA;let playing=true,last=performance.now(),elapsed=0,manual=0;play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};step.onclick=()=>{playing=false;manual=(manual+1)%6;play.textContent='Play'};for(const state of states){const card=document.createElement('div');card.innerHTML='<p>'+state.id+'</p><canvas width="460" height="430"></canvas>';tracks.append(card);state.canvas=card.querySelector('canvas')};Promise.all(states.map(async s=>{s.images=await Promise.all(s.frameFiles.map(f=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f}))) })).then(()=>{function draw(now){if(playing)elapsed+=(now-last)*.5;last=now;let index=manual;if(playing){let cursor=elapsed%1040;index=5;for(let i=0;i<6;i++){if(cursor<states[0].frameDurationsMs[i]){index=i;break}cursor-=states[0].frameDurationsMs[i]}}for(const state of states){const c=state.canvas.getContext('2d');c.fillStyle='#22343e';c.fillRect(0,0,460,215);c.fillStyle='#dae1e0';c.fillRect(0,215,460,215);const factor=Number(size.value)/148;for(const y of [110,325])c.drawImage(state.images[index],230-128*factor,y-128*factor,256*factor,256*factor)}document.querySelector('#status').textContent=' pose '+(index+1)+'/6';requestAnimationFrame(draw)}requestAnimationFrame(draw)});</script>'''
(HERE/'index.html').write_text(html.replace('DATA',json.dumps(states)),encoding='utf-8')
print('Built bare/helmet turn paired review')
