"""Replay recorded native actor positions and exact displayed sources; no artwork synthesis."""
from pathlib import Path
import json,hashlib,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
planted=len(sys.argv)>1 and sys.argv[1]=='planted'
output_name='bill-carry-corner-planted-preview' if planted else 'bill-carry-corner-staged'
OUT=ROOT/'output'/output_name
data=json.loads((OUT/'journeys.json').read_text())
validation=json.loads((OUT/'validation.json').read_text())
assert validation['passed'] and data['failures']==0
html='''<!doctype html><meta charset="utf-8"><title>Bill moving corner review</title>
<style>body{background:#182932;color:#dde8e9;font:16px system-ui;margin:24px}canvas{background:#22343e;max-width:100%;border:1px solid #536770}button,a{margin-right:12px;color:inherit}button{background:#344952;padding:8px;border:1px solid #71838b}</style>
<h1>Bill — moving corner comparison</h1><p>Staged and current art, bare and helmet, both directions. Orange marker marks the physical foot at turn onset.</p>
<p>Recorded real Bill movement and sprite-player output in a prescribed clear-room fixture. This replay uses exact captured source pixels and positions; it is not a continuous station recording.</p>
<p><strong>Remaining issue:</strong> physical travel continues during the planted pivot, followed by an abrupt walking stride. Replacement remains staged.</p>
<button id="pause">Pause</button><button id="restart">Restart</button><a href="./">Source-pose review</a><p id="clock"></p><canvas width="900" height="1440"></canvas>
<script>const DATA=RECORDS;const base='../../output/bill-carry-corner-staged/';const images={};let paused=false,started=performance.now(),held=0;
const canvas=document.querySelector('canvas'),ctx=canvas.getContext('2d');
document.querySelector('#pause').onclick=()=>{if(!paused){held=performance.now()-started;paused=true}else{started=performance.now()-held;paused=false}document.querySelector('#pause').textContent=paused?'Play':'Pause'};
document.querySelector('#restart').onclick=()=>{started=performance.now();held=0};
async function boot(){await Promise.all([...new Set(DATA.journeys.flatMap(j=>j.records.map(r=>r.sourceCapture)))].map(name=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{images[name]=im;resolve()};im.onerror=reject;im.src=base+name})));requestAnimationFrame(draw)}
function draw(now){const elapsed=((paused?held:now-started)%1750)/1000,t=Math.min(elapsed,.95);ctx.fillStyle='#22343e';ctx.fillRect(0,0,900,1440);ctx.font='15px system-ui';DATA.journeys.forEach((j,i)=>{const origin=j.records[0].foot,r=j.records.filter(r=>r.turnElapsed<=t).at(-1)||j.records[0],y=i*180+95;ctx.strokeStyle='#455b65';ctx.beginPath();ctx.moveTo(300,y);ctx.lineTo(700,y);ctx.stroke();ctx.fillStyle='#ffad59';ctx.fillRect(448,y-2,4,4);const x=450+(r.foot[0]-origin[0])*82/(384*.17),py=y+(r.foot[1]-origin[1])*82/(384*.17),s=82/148;ctx.drawImage(images[r.sourceCapture],x-128*s,py-224*s,256*s,256*s);ctx.fillStyle='#dde8e9';ctx.fillText(`${j.candidate?'STAGED':'CURRENT'} · ${j.gear?'helmet':'bare'} · ${j.reverse?'south → east':'east → south'}`,12,i*180+25);ctx.fillText(r.turning?'turn':'carrying walk',710,i*180+65)});document.querySelector('#clock').textContent=`Turn clock ${t.toFixed(2)}s — repeats after a short hold`;requestAnimationFrame(draw)}boot();</script>'''
if planted:
 html=html.replace('Remaining issue:</strong> physical travel continues during the planted pivot, followed by an abrupt walking stride. Replacement remains staged.','Preview fix:</strong> physical foot holds during the pivot. The first walking stride still needs a smoother art handoff. Movement subclass and artwork remain unselected.').replace('bill-carry-corner-staged',output_name)
(HERE/('corner-planted-review.html' if planted else 'corner-review.html')).write_text(html.replace('RECORDS',json.dumps(data)),encoding='utf-8')
evidence={'scope':data['scope'],'checks':data['checks'],'validation':validation,'visualFinding':'Preview physical foot stays planted during turn; reverse still exits abruptly into large East stride.' if planted else 'Planted source translates during turn; reverse exits abruptly into large East stride. Unresolved.','turnTravelWorldUnits':[j['turnTravelWorldUnits'] for j in data['journeys']],'normalSelectionChanged':False,'goalComplete':False,'hashTiming':'Recorded after native interval; dependency stability during interval unmeasured.','hashes':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [OUT/'corner-board.png',OUT/'journeys.json',ROOT/'tests/test_bill_carry_corner_staged.gd',ROOT/'scripts/bill_npc.gd',ROOT/'scripts/crew_sprite_player.gd']}}
if planted:
 for p in [ROOT/'tests/test_bill_carry_corner_planted_preview.gd',HERE/'carry_motion_preview.gd']:
  evidence['hashes'][str(p.relative_to(ROOT)).replace('\\','/')]=hashlib.sha256(p.read_bytes()).hexdigest()
 evidence['displayedTurnFootRanges']=[{'candidate':j['candidate'],'gear':j['gear'],'reverse':j['reverse'],'rangeX':max(r['foot'][0] for r in j['records'] if r['turning'])-min(r['foot'][0] for r in j['records'] if r['turning']),'rangeY':max(r['foot'][1] for r in j['records'] if r['turning'])-min(r['foot'][1] for r in j['records'] if r['turning'])} for j in data['journeys']]
(HERE/('corner-planted-runtime-evidence.json' if planted else 'corner-runtime-evidence.json')).write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
print(f"Built replay: {len(data['journeys'])} journeys, {sum(len(j['records']) for j in data['journeys'])} recorded updates; {data['checks']} native checks")
