"""Synchronized independent side carrying candidates with metadata world pivots."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
tracks=[]
for direction in ['east','west','north','south']:
    for equipped in [False,True]:
        folder=f'bill-swim-carry-{"helmet-" if equipped else ""}{direction}-coherent-v1'
        pack=json.loads((HERE.parent/folder/'manifest.json').read_text(encoding='utf-8'));state=pack['states'][0]
        tracks.append({'label':direction+' · '+('selected helmet' if equipped else 'bare')+' · candidate','pivot':pack['pivot'],'width':pack['frameWidth'],'height':pack['frameHeight'],'files':['../'+folder+'/'+file for file in state['frameFiles']],'durations':state['frameDurationsMs']})
html='''<!doctype html><meta charset="utf-8"><title>Bill water carrying candidates</title>
<style>body{background:#152027;color:#e6eff1;font:16px system-ui;margin:20px}p{max-width:85ch;color:#bdd0d2}.grid{display:flex;gap:12px;flex-wrap:wrap}.card{background:#22343e;padding:12px}canvas{display:block}button,select{font:inherit;background:#29404a;color:white;padding:6px}a{color:#84c5da}</style>
<h1>Bill — four-direction water carrying</h1><p>Independent master-relative bodies and compact supply cases, leg-driven kicks and selected native helmets. One fixed anatomical scale and grade per atlas.960ms loops;candidate frame,clock,movement/pause and wrap checks340 pass. These eight packs are staged while matching turn endpoints remain unfinished. Runtime selections and owner acceptance remain separate.</p>
<p><a href="../bill-swim-transitions-east-coherent-v1/">Compare east basic water</a> · <a href="../bill-swim-transitions-west-coherent-v1/">Compare west basic water</a></p>
<button id="play">Pause</button> <button id="step">Next pose</button> Height <select id="size"><option>148</option><option selected>82</option><option>54</option></select> Speed <select id="speed"><option value="1">1×</option><option value=".5" selected>0.5×</option></select><span id="status"> Loading…</span><div class="grid" id="grid"></div>
<script>const tracks=DATA;let time=0,last=performance.now(),playing=true,manual=0;for(const t of tracks){const el=document.createElement('div');el.className='card';el.innerHTML='<strong>'+t.label+'</strong><canvas width="460" height="430"></canvas>';grid.append(el);t.canvas=el.querySelector('canvas')};play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};step.onclick=()=>{playing=false;manual=(manual+1)%6;play.textContent='Play'};
Promise.all(tracks.map(async t=>{t.images=await Promise.all(t.files.map(file=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=file+'?v=carry-candidate-v1'})))})).then(()=>{function draw(now){if(playing)time+=(now-last)*Number(speed.value);last=now;const i=playing?Math.floor(time%960/160):manual;const s=Number(size.value)/148;for(const t of tracks){const c=t.canvas.getContext('2d');c.fillStyle='#22343e';c.fillRect(0,0,460,215);c.fillStyle='#dae1e0';c.fillRect(0,215,460,215);for(const y of [100,315])c.drawImage(t.images[i],230-t.pivot[0]*s,y-t.pivot[1]*s,t.width*s,t.height*s)}document.querySelector('#status').textContent=' Eight streams loaded · pose '+(i+1)+'/6';requestAnimationFrame(draw)}requestAnimationFrame(draw)}).catch(e=>document.querySelector('#status').textContent='Load failed '+e);</script>'''
(HERE/'index.html').write_text(html.replace('DATA',json.dumps(tracks)),encoding='utf-8')
print('Built paired side carry review:eight streams,six synchronized poses')
