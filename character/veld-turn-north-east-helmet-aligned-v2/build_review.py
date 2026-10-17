from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-north-east-helmet-aligned-v2'
records=json.loads((O/'records.json').read_text());groups={}
for gear in ['bare','helmet']:
    for route in ['north-east','east-north']:
        rows=[r for r in records if r['gear']==gear and r['action']==route]
        assert len(rows)==27
        groups[gear+'-'+route]=[{'url':'/'+(O/(r['name']+'-native.png')).relative_to(R).as_posix(),'slot':r['slot'],'time':r['time']} for r in rows]
B=R/'character/veld-turn-north-east-original-master-v2';old=R/'character/veld-turn-north-east-helmet-aligned-v1'
rows=[('bare head',json.loads((P/'bare-manifest.json').read_text())['states'][0]['frameFiles']),('previous helmet',json.loads((old/'helmet-manifest.json').read_text())['states'][0]['frameFiles']),('actual-head fit',json.loads((P/'helmet-manifest.json').read_text())['states'][0]['frameFiles'])]
board=Image.new('RGB',(1440,690),'#202a30');d=ImageDraw.Draw(board)
for row,(label,refs) in enumerate(rows):
    for i,ref in enumerate(refs):
        im=Image.open(R/ref[6:]).convert('RGBA').crop((99,60,159,110));im=im.resize((240,200),Image.Resampling.NEAREST)
        board.paste(im,(i*240,row*230+25),im);d.text((i*240+5,row*230+5),f'{label} phase{i}',fill='white')
board.save(P/'actual-head-correspondence.png')
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Veld helmet turn</title>
<style>body{background:#182229;color:#e5e9e8;font:17px system-ui;margin:0;padding:28px}main{max-width:1000px;margin:auto}h1{margin-top:0}p{max-width:800px;line-height:1.5}section{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0;align-items:center}button,select{font:inherit;background:#2c3c46;color:inherit;border:1px solid #73858e;padding:9px 14px;border-radius:6px}canvas{display:block;max-width:100%;height:auto;background:#202a30}output{display:block;margin:15px 0;color:#c4d5de}details{margin:25px 0}img{max-width:100%;display:block}label{display:flex;gap:8px;align-items:center}</style>
<main><h1>Veld helmet turn</h1><p>The helmet follows the actual head angle: the original profile appears when her head reaches profile. Her body, starting pose, final pose and timing stay the same.</p><p>This is a work in progress. The partial-face view still needs a closer match to the master’s skin, hair and helmet finish.</p>
<section><label>View <select id="gear"><option value="helmet">Helmet</option><option value="bare">Bare head</option></select></label><label>Direction <select id="route"><option value="north-east">North to east</option><option value="east-north">East to north</option></select></label><button id="play">Play</button><button id="prev">Previous pose</button><button id="next">Next pose</button></section>
<output id="status" aria-live="polite">Loading review images…</output><canvas width="760" height="600" aria-label="Previous fit above, actual-head fit below at three character sizes"></canvas>
<p>Previous fit above; revised fit below. The three sizes show the character small, medium and full size.</p>
<details><summary>All head angles</summary><img src="actual-head-correspondence.png" alt="Bare head, previous helmet, revised helmet across six poses"></details><details><summary>All full-body poses</summary><img src="helmet-native-source-poses.png" alt="Six helmet poses at three sizes"><img src="bare-native-source-poses.png" alt="Six bare poses at three sizes"></details></main>
<script>
const groups=GROUPS,cache=new Map(),gear=document.querySelector('#gear'),route=document.querySelector('#route'),play=document.querySelector('#play'),status=document.querySelector('#status'),canvas=document.querySelector('canvas'),ctx=canvas.getContext('2d');
let playing=false,frame=0,cycles=0,start=0;
const current=()=>groups[gear.value+'-'+route.value];
function draw(){const rows=current(),r=rows[frame],im=cache.get(r.url);if(im)ctx.drawImage(im,0,0);status.textContent=`${gear.options[gear.selectedIndex].text} · ${route.options[route.selectedIndex].text} · Pose ${r.slot+1} of 6 · ${Math.round(r.time*1000)} ms · ${cycles} completed previews`;}
function stop(){playing=false;play.textContent='Play';}
function tick(t){if(!playing)return;const elapsed=t-start;cycles=Math.floor(elapsed/1400);const ms=elapsed%1400;frame=Math.min(26,Math.floor(ms/(1000/30)));draw();requestAnimationFrame(tick);}
play.addEventListener('click',()=>{if(playing){stop();return;}playing=true;play.textContent='Pause';start=performance.now()-frame*(1000/30);requestAnimationFrame(tick);});
function step(delta){stop();const rows=current(),slot=rows[frame].slot;let positions=[];for(let i=0;i<rows.length;i++)if(!i||rows[i].slot!==rows[i-1].slot)positions.push(i);let n=positions.findIndex(i=>rows[i].slot===slot);frame=positions[Math.max(0,Math.min(positions.length-1,n+delta))];draw();}
document.querySelector('#prev').addEventListener('click',()=>step(-1));document.querySelector('#next').addEventListener('click',()=>step(1));
for(const select of [gear,route])select.addEventListener('change',()=>{stop();frame=0;cycles=0;draw();});
Promise.all(Object.values(groups).flat().map(r=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{cache.set(r.url,im);resolve();};im.onerror=()=>reject(new Error('Could not load '+r.url));im.src=r.url;}))).then(draw).catch(e=>{status.textContent=e.message;});
</script></html>'''.replace('GROUPS',json.dumps(groups))
(P/'index.html').write_text(html,encoding='utf-8');print('108 exact native review images linked; interactive four-way finite-turn replay and source-pose stepping prepared.')
