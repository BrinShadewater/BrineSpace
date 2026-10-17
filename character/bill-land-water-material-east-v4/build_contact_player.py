from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent; R=P.parent.parent
review=json.loads((P/'review.json').read_text(encoding='utf-8')); records=json.loads((R/'output/bill-land-water-material-east-v4/records.json').read_text(encoding='utf-8'))
rows=[r for r in records['records'] if r['name'].endswith('-candidate') and 'tick' in r]
groups={}
for gear in ['bare','helmet']:
 for phase,lo,hi in [('enter',60,105),('exit',410,460)]:
  seq=[r.copy() for r in rows if r['name'].startswith(gear+'-') and lo<=r['tick']<hi]; seq.sort(key=lambda r:r['tick']); assert len(seq)==hi-lo
  for r in seq:
   im=Image.open(P/'captures'/f"{r['name']}-source.png").convert('RGBA'); sha=hashlib.sha256(im.tobytes()).hexdigest(); r['registration']=review['sourceRegistration'][sha]
  groups[gear+' '+phase]=seq
payload=json.dumps(groups,separators=(',',':'))
html='''<!doctype html><meta charset="utf-8"><title>Bill water contact review</title><style>body{background:#182932;color:#e0e5e6;font:16px system-ui;margin:24px}button,select{font:inherit;padding:8px;margin:4px}canvas{background:#14242c;max-width:48%;height:auto}input{width:90%}p{max-width:1000px}#status{font-variant-numeric:tabular-nums}</style><h1>Bill — water transition contact review</h1><p>Recorded native movement and exact source frames at 60 Hz. The source ruler uses a fixed pivot and standing height throughout. Room view is a 2x crop following the physical actor; source view is at 1.5x. Recorded world movement is reported below. Loop restart joins the end back to the beginning for review and is not an authored transition.</p><select id="sequence"></select><button id="play">Play</button><button id="back">Previous frame</button><button id="next">Next frame</button><label>Speed <select id="speed"><option value="1">Normal</option><option value=".25">Quarter speed</option></select></label><div><canvas id="room" width="400" height="400"></canvas><canvas id="source" width="480" height="480"></canvas></div><input id="scrub" aria-label="Frame" type="range" min="0" value="0"><p id="status"></p><p>Green dashed line: dry walking registration pivot. Grey dashed line: canonical standing-height ruler. These are registration guides, not a floor-height plane. Bill uses a 2D navigation anchor; swimming silhouettes may extend below the dry pivot. Actual room obstacle clearance is checked separately. All 120 active captured silhouettes fit the admitted collision outline. Smoothness, new-bank save/resume and normal gameplay integration remain pending.</p><a href="index.html">Full capture boards</a><script>
const groups=PAYLOAD, seq=document.querySelector('#sequence'), slider=document.querySelector('#scrub'), play=document.querySelector('#play');
for(const key of Object.keys(groups)){const option=document.createElement('option');option.textContent=key;seq.append(option)}
const images=new Map();let index=0,running=false,elapsed=0,last=0,ready=false;
async function load(){await Promise.all(Object.values(groups).flat().flatMap(r=>['source','room'].map(kind=>new Promise((resolve,reject)=>{const key=r.name+'-'+kind,im=new Image();im.onload=()=>{images.set(key,im);resolve()};im.onerror=reject;im.src='captures/'+key+'.png'}))));ready=true;draw()}
function draw(){if(!ready)return;const rows=groups[seq.value],r=rows[index],m=r.registration;slider.max=rows.length-1;slider.value=index;
const c=document.querySelector('#source').getContext('2d');c.clearRect(0,0,480,480);c.drawImage(images.get(r.name+'-source'),(160-m.pivot[0])*1.5,(224-m.pivot[1])*1.5,m.size[0]*1.5,m.size[1]*1.5);c.setLineDash([6,6]);c.strokeStyle='#90b89e';c.beginPath();c.moveTo(0,336);c.lineTo(480,336);c.stroke();c.strokeStyle='#697d87';c.beginPath();c.moveTo(0,114);c.lineTo(480,114);c.stroke();c.setLineDash([]);
const n=document.querySelector('#room').getContext('2d'),x=255+(r.foot[0]-7680)*398/384,y=287+(r.foot[1]-8064)*398/384;n.clearRect(0,0,400,400);n.drawImage(images.get(r.name+'-room'),Math.round(x)-100,Math.round(y)-130,200,200,0,0,400,400);
document.querySelector('#status').textContent=`${seq.value} · frame ${index+1}/${rows.length} · tick ${r.tick} · time ${r.clock.toFixed(3)} s · ${r.state} · transition ${r.bridgeActive?'active':'complete/off'} · water ${r.water.toFixed(3)} · foot ${r.foot.map(v=>v.toFixed(2)).join(', ')}`}
function pause(){running=false;play.textContent='Play';elapsed=0}
play.onclick=()=>{running=!running;play.textContent=running?'Pause':'Play';last=performance.now()};seq.onchange=()=>{pause();index=0;draw()};slider.oninput=()=>{pause();index=+slider.value;draw()};document.querySelector('#back').onclick=()=>{pause();index=Math.max(0,index-1);draw()};document.querySelector('#next').onclick=()=>{pause();index=Math.min(groups[seq.value].length-1,index+1);draw()};
function animate(t){if(running&&ready){elapsed+=(t-last)*+document.querySelector('#speed').value;const rows=groups[seq.value];while(elapsed>=1000/60){elapsed-=1000/60;index=(index+1)%rows.length}draw()}last=t;requestAnimationFrame(animate)}requestAnimationFrame(animate);load().catch(()=>document.querySelector('#status').textContent='Capture loading failed');
</script>'''.replace('PAYLOAD',payload)
(P/'contact-player.html').write_text(html,encoding='utf-8'); print('Built synchronized contact player:190 exact source/native pairs, fixed pivot/H148; four sequences.')
