from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seated-journey-v1'
data=json.loads((O/'captures.json').read_text());assert json.loads((O/'validation.json').read_text())['passed']
page='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Veld lounge motion review</title>
<style>body{background:#202a30;color:#e1e7eb;font:16px system-ui;margin:24px}p{max-width:80ch;line-height:1.5}a{color:#8cc6e7}.row{display:flex;gap:20px;flex-wrap:wrap}canvas{background:#26353d}button,select,input{font:inherit}#room{max-width:100%;height:auto}input{width:260px}h1{font-size:28px}</style>
<h1>Veld — lounge approach and seated motion</h1>
<p>Veld now walks to a clear spot directly in front of the chair before sitting. The sideways slide during lowering and rising is removed from this approach. The helmet, proportions and matte materials stay consistent. These frames come from the actual room review. The seated artwork remains a candidate; older seated checkpoints retain their original chair position.</p>
<label>Version <select id="gear"><option value="bare">Bare</option><option value="helmet">Helmet</option></select></label> <label>Moment <input id="moment" type="range" min="0" max="34" value="12"></label> <span id="status"></span>
<div class="row"><div><h2>Standing master</h2><canvas id="master" width="256" height="256"></canvas></div><div><h2>Current pose</h2><canvas id="pose" width="256" height="256"></canvas></div></div>
<h2>In the lounge</h2><img id="room" width="1024" alt="Veld in the actual lounge at the selected moment">
<p>Scrub the lowering and rising poses to check the aligned chair contact. Approach samples are spaced apart; seated frames include each change in the pose.</p>
<p><a href="journey-bare-source.png">Bare pose sequence</a> · <a href="journey-helmet-source.png">Helmet pose sequence</a> · <a href="journey-bare-room.png">Bare room sequence</a> · <a href="journey-helmet-room.png">Helmet room sequence</a> · <a href="FRONT_CONTACT_HANDOFF.md">Review findings</a></p>
<script>const records=__RECORDS__;const gear=document.querySelector('#gear'),moment=document.querySelector('#moment');let revision=0;
const load=p=>new Promise((ok,no)=>{let im=new Image;im.onload=()=>ok(im);im.onerror=no;im.src=p+'?v=front-contact-v1'});
const masters={bare:'../crew-runtime-matte-v1/veld/frames/idle-north-breathing-v1/000.png',helmet:'../veld-shared-helmet-v1/frames/idle-north/000.png'};
async function draw(){const stamp=++revision;const rows=records.filter(r=>r.gear===gear.value);moment.max=rows.length-1;const r=rows[Number(moment.value)];document.querySelector('#status').textContent=`${(r.tick/60).toFixed(2)}s · ${({'life_sit':'Lowering','life_seated':'Breathing','life_rise':'Rising'})[r.stage]||r.state}`;document.querySelector('#room').src='../../output/veld-seated-journey-v1/'+r.screenshot+'?v=front-contact-v1';const images=await Promise.all([load(masters[gear.value]),load('../../output/veld-seated-journey-v1/'+r.source)]);if(stamp!==revision)return;['master','pose'].forEach((id,i)=>{let c=document.querySelector('#'+id).getContext('2d');c.clearRect(0,0,256,256);c.drawImage(images[i],images[i].width===184?36:0,images[i].height===184?52:0)})}
gear.onchange=draw;moment.oninput=draw;draw();</script>'''
(P/'journey-review.html').write_text(page.replace('__RECORDS__',json.dumps(data['records'])),encoding='utf-8')
print(f'Journey review page:{len(data["records"])} native moments, paired masters and registered source canvases')
