from pathlib import Path
import json
P=Path(__file__).resolve().parent
packs={g:json.loads((P/g/'manifest.json').read_text()) for g in ['bare','helmet']}
assert packs['bare']['states'][0]['frameDurationsMs']==packs['helmet']['states'][0]['frameDurationsMs']
data={g:{'frames':[g+'/'+f for f in m['states'][0]['frameFiles']],'times':m['states'][0]['frameDurationsMs']} for g,m in packs.items()}
page='''<!doctype html><meta charset="utf-8"><title>Bill North water entry</title>
<style>body{background:#182932;color:#eef;font:16px sans-serif}canvas{background:#182932;height:min(704px,calc(100vh - 190px));width:auto;max-width:100%}img{max-width:100%}button,select,input{margin:8px}</style>
<h1>Bill North water entry — paired source candidate</h1><p>Nine poses,500ms. Source review only; native motion/contact, normal admission and independent exit pending. Bent-elbow reach revision; full motion and master acceptance pending.</p>
<button id="play">Play once</button><button id="pause">Pause</button><button id="prev">Previous</button><button id="next">Next</button>
<select id="gear"><option value="bare">Bare head</option><option value="helmet">Helmet</option></select>
<select id="speed"><option value="1">Normal speed</option><option value="4">Quarter speed</option></select>
<input id="scrub" type="range" min="0" max="8" value="0"><span id="pose"></span><br>
<canvas width="640" height="704"></canvas><br><img src="paired-entry-contact.png"><br><img src="helmet-neck-details.png">
<script>const data=DATA;const images={};for(const gear of Object.keys(data))images[gear]=data[gear].frames.map(src=>{let im=new Image();im.src=src;return im});
const ctx=document.querySelector('canvas').getContext('2d');let index=0,run=0;
function draw(){ctx.clearRect(0,0,640,704);let im=images[document.querySelector('#gear').value][index];if(im.complete)ctx.drawImage(im,0,0,640,704);document.querySelector('#pose').textContent='Pose '+index;document.querySelector('#scrub').value=index}
function move(delta){run++;index=(index+delta+9)%9;draw()}
document.querySelector('#prev').onclick=()=>move(-1);document.querySelector('#next').onclick=()=>move(1);document.querySelector('#pause').onclick=()=>run++;
document.querySelector('#scrub').oninput=e=>{run++;index=Number(e.target.value);draw()};document.querySelector('#gear').onchange=draw;
document.querySelector('#play').onclick=async()=>{const token=++run;for(let i=0;i<9;i++){if(run!==token)return;index=i;draw();await new Promise(r=>setTimeout(r,data.bare.times[i]*Number(document.querySelector('#speed').value)))}};
Object.values(images).flat().forEach(im=>im.onload=draw);draw()</script>'''
(P/'entry.html').write_text(page.replace('DATA',json.dumps(data)),encoding='utf-8')
e=json.loads((P/'entry-review.json').read_text())
e['scope']='Nine-frame500ms paired bare/helmet source candidate. Static selected endpoint pixels preserved; no native integration, actual phase handoffs, continuous-motion or full master acceptance.'
e['visualReview']='Complete bare and paired nine-pose contact boards and all seven close head/collar/body fitting pairs inspected. Crouch-to-prone projection now visible, matte quilt and rear equipment retained, shell/collar joins connected in inspected captures. Axial lift5 revised; hair/metal/normal-endpoint grade and timing/full motion remain pending. Atlas scale fixed. Board review does not prove temporal/physical contact.'
e['helmetVisualReview']='Seven native-scale canonical rear-shell fittings inspected in neck board. No visible collar gap; protected source-body/foreground pixels exact. Not full motion/occlusion acceptance.'
e['browserMotionReview']='Not exercised; finite player generated, technical APNG decode exact only.'
(P/'entry-review.json').write_text(json.dumps(e,indent=2)+'\n')
print(json.dumps({'pairedSourceFrames':18,'finitePlayer':'entry.html','motionAcceptance':'pending'}))
