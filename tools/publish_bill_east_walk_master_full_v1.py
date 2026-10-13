"""Publish a synchronized full-source walking comparison without runtime admission."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
D=R/'character/bill-east-walk-master-full-v1'
timings=json.loads((D/'manifest.json').read_text(encoding='utf-8'))['states'][0]['frameDurationsMs']
html='''<!doctype html><meta charset="utf-8"><title>Bill · complete East walk review</title>
<style>body{background:#17252d;color:#e8e0cf;font:16px system-ui;margin:24px}button,select,input{font:inherit;margin:8px}main{display:flex;gap:24px;flex-wrap:wrap}section{background:#20343d;padding:12px;border-radius:8px}canvas{display:block;background:#17252d}p{max-width:850px}small{color:#b5c5c8}</style>
<h1>Bill · complete East walk</h1><p>All 48 revised poses, compared with the current walk and original master. Room placement checks passed. Natural walking and action joins still need review before this replaces the current set.</p>
<button id="run">Pause</button><button id="reset">Restart</button><label>Speed <select id="speed"><option value="1">Normal</option><option value="4">Quarter speed</option></select></label><label>Pose <input id="pose" type="number" min="0" max="47" value="0"></label><p id="status">Loading…</p><main id="cards"></main>
<script>
const durations=TIMINGS, heights=[148,82,54,27], images=[[],[],[]];let running=true,elapsed=0,last=0,cycles=0,visited=new Set(),slot=0,speed=1;
const cards=document.querySelector('#cards'),contexts=[];
for(const [i,title] of ['Revised walk','Current walk','Original master'].entries()){let s=document.createElement('section');s.innerHTML='<h2>'+title+'</h2><canvas width="280" height="440"></canvas><small>Enlarged · gameplay sizes 82 / 54 / 27</small>';cards.append(s);contexts.push(s.querySelector('canvas').getContext('2d'));}
const load=p=>new Promise((ok,no)=>{let im=new Image();im.onload=()=>ok(im);im.onerror=()=>no(Error(p));im.src=p;});
function draw(){contexts.forEach((c,j)=>{c.clearRect(0,0,280,440);let im=images[j][j===2?0:slot];heights.forEach((h,k)=>{let sc=h/148*(k===0?1.5:1);let x=k===0?140:48+(k-1)*92,y=k===0?320:422;c.imageSmoothingEnabled=true;c.drawImage(im,x-128*sc,y-224*sc,256*sc,256*sc);});});document.querySelector('#pose').value=slot;document.querySelector('#status').textContent='Pose '+slot+' / 47 · '+cycles+' complete loops · '+visited.size+' poses displayed';window.billWalkReview={loaded:true,slot,completedCycles:cycles,speed,visitedIndices:[...visited]};}
function tick(t){if(last&&running){elapsed+=(t-last)/speed;while(elapsed>=durations[slot]){elapsed-=durations[slot];slot=(slot+1)%48;visited.add(slot);if(slot===0)cycles++;}}last=t;draw();requestAnimationFrame(tick);}
document.querySelector('#run').onclick=()=>{running=!running;document.querySelector('#run').textContent=running?'Pause':'Play';};document.querySelector('#reset').onclick=()=>{slot=0;elapsed=0;cycles=0;visited=new Set([0]);};document.querySelector('#speed').onchange=e=>{speed=Number(e.target.value);};document.querySelector('#pose').oninput=e=>{running=false;document.querySelector('#run').textContent='Play';slot=Math.max(0,Math.min(47,Number(e.target.value)));elapsed=0;visited.add(slot);};
Promise.all([Promise.all(Array.from({length:48},(_,i)=>load('frames/'+String(i).padStart(3,'0')+'.png'))),Promise.all(Array.from({length:48},(_,i)=>load('../bill-walk-east-material-v1/frames/bare/walk-east/'+String(i).padStart(3,'0')+'.png'))),load('master.png')]).then(([a,b,m])=>{images[0]=a;images[1]=b;images[2]=[m];visited.add(0);requestAnimationFrame(tick);}).catch(e=>{document.querySelector('#status').textContent='Unable to load comparison: '+e.message;});
</script>'''.replace('TIMINGS',json.dumps(timings))
(D/'index.html').write_text(html,encoding='utf-8')
print('Published complete 48-pose comparison.')
