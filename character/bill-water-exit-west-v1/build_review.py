from pathlib import Path
from PIL import Image, ImageDraw
from scipy.ndimage import label
import numpy as np, json, hashlib
P=Path(__file__).resolve().parent;R=P.parent
review=json.loads((P/'review.json').read_text(encoding='utf-8'))
helmet=json.loads((P/'helmet-registration.json').read_text(encoding='utf-8'))
crowns=[(131,188)]+[tuple(x) for x in review['crowns']]+[(157,80)]
board=Image.new('RGB',(2800,640),'#182932');d=ImageDraw.Draw(board);components=[]
for row,gear in enumerate(['bare','helmet']):
    for i,(x,y) in enumerate(crowns):
        im=Image.open(P/f'{gear}/frames/swim-land-west/{i:03}.png').convert('RGBA')
        crop=im.crop((x-35,y-10,x+45,y+50)).resize((400,300),Image.Resampling.NEAREST)
        board.paste(crop,(i*400,row*320+20),crop);d.text((i*400+4,row*320+3),f'{gear} pose{i} /native5x',fill='white')
        a=np.array(im);lab,_=label(a[:,:,3]>160);counts=np.bincount(lab.ravel())[1:]
        substantial=[int(x) for x in counts if x>20];assert len(substantial)==1,(gear,i,substantial)
        components.append(dict(gear=gear,pose=i,substantialComponentsAlpha160=substantial))
board.save(P/'helmet-neck-details.png')
review.update(decodedPairedAPNGFramesExact=14,connectedSilhouetteDiagnostics=components,visualReview='Master and complete paired source boards inspected. Distinct low elbow/palm push/knee tuck/half kneel/rise articulation; no reversed entry or mirrored East art. Low elbow V1 rejected for changed size; rise V1 replaced by source anatomical head/knee repair. Body details closer to original master, but face warmth/head fidelity, endpoint grade/detail differences, support trajectory and continuous movement remain pending. Paired native5x head/collar crops reviewed after tightening overbroad head erase mask; retained collar joins behind shell. Helmet component native scale1/rotation0; mask is pose-family-specific, not universal.',visualAcceptance='Source candidate only. No station exit bridge, actual collision/material/source-phase or save/Continue evidence.')
(P/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Bill — West water exit</title><style>body{margin:24px;background:#182932;color:#edf1f2;font:16px system-ui}main{max-width:1200px;margin:auto}.pair{display:flex;flex-wrap:wrap;gap:20px}.pose{text-align:center}canvas{background:#14242c;width:480px;height:480px;max-width:100%}button{padding:8px 15px;margin-right:8px}input{width:min(650px,95%)}img{max-width:100%}p{line-height:1.5}summary{cursor:pointer;margin:20px 0}</style>
<main><h1>Bill — West water exit</h1><p>New push-up and rise sequence: low elbow support, palm push, knee tuck, half-kneel and standing rise.</p><p>Source candidate. Face and suit matching, full-speed motion and movement in the station still need review.</p>
<div class="pair"><div class="pose"><h2>Bare</h2><canvas id="bare" width="640" height="640"></canvas></div><div class="pose"><h2>Helmet</h2><canvas id="helmet" width="640" height="640"></canvas></div></div>
<p><button id="play">Play</button><button id="prev">Previous pose</button><button id="next">Next pose</button><select id="speed"><option value="1">Normal speed</option><option value="0.25">Quarter speed</option></select></p><input id="scrub" type="range" min="0" max="500" value="0"><p id="label">Loading poses…</p>
<details><summary>Original master and all poses at one scale</summary><img src="master-review.png"><img src="paired-helmet-review.png"></details>
<details><summary>Head, collar and shoulder close-ups</summary><img src="helmet-neck-details.png"></details></main>
<script>
const times=[60,50,60,70,100,100,60],starts=[0];times.forEach(t=>starts.push(starts.at(-1)+t));const banks={},names=['Swimming context','Low elbow','Palm push','Knee tuck','Half kneel','Rise','Standing context'];let ready=false,playing=false,time=0,last=0;
function frame(){let i=0;while(i<6&&time>=starts[i+1])i++;return i}
function draw(){if(!ready)return;const i=frame();for(const gear of ['bare','helmet']){const c=document.getElementById(gear),ctx=c.getContext('2d');ctx.clearRect(0,0,640,640);ctx.imageSmoothingEnabled=false;ctx.drawImage(banks[gear][i],0,0,640,640)}document.getElementById('scrub').value=Math.round(time);document.getElementById('label').textContent=names[i]+' · pose '+(i+1)+' of 7 · '+Math.round(time)+' ms'}
function pause(){playing=false;document.getElementById('play').textContent='Play'}
document.getElementById('play').onclick=()=>{if(!playing&&time>=500)time=0;playing=!playing;document.getElementById('play').textContent=playing?'Pause':'Play'};
document.getElementById('scrub').oninput=e=>{pause();time=Number(e.target.value);draw()};
document.getElementById('prev').onclick=()=>{pause();time=starts[Math.max(0,frame()-1)];draw()};document.getElementById('next').onclick=()=>{pause();time=starts[Math.min(6,frame()+1)];draw()};
function animate(now){if(last&&playing&&ready){time=Math.min(500,time+(now-last)*Number(document.getElementById('speed').value));if(time>=500)pause()}last=now;draw();requestAnimationFrame(animate)}
Promise.all(['bare','helmet'].map(async gear=>{banks[gear]=await Promise.all(times.map((_,i)=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=gear+'/frames/swim-land-west/'+String(i).padStart(3,'0')+'.png'})))})).then(()=>{ready=true;requestAnimationFrame(animate)}).catch(()=>{document.getElementById('label').textContent='Could not load a pose.'});
</script></html>'''
bank=json.loads((P/'bare/manifest.json').read_text(encoding='utf-8')); times=bank['states'][0]['frameDurationsMs']; assert times==json.loads((P/'helmet/manifest.json').read_text(encoding='utf-8'))['states'][0]['frameDurationsMs']; assert sum(times)==500
html=html.replace('const times=[60,50,60,70,100,100,60]', 'const times='+json.dumps(times))
(P/'index.html').write_text(html,encoding='utf-8')
print('Paired source player and neck board built; fourteen connected-alpha diagnostics, no motion acceptance claim.')
