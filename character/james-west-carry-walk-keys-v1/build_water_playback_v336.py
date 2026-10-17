from pathlib import Path
import hashlib,json,shutil
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'water-playback-v336';o.mkdir(exist_ok=True);(o/'frames').mkdir(exist_ok=True)
d=json.loads((p/'water-family-review-v335/review.json').read_bytes())
inv=json.loads((p/'selected-family-audit-v333/selected-inventory.json').read_bytes())
bank={};bindings={}
for x in d['samples']:
 if x['key'].startswith(('tread-','swim-distress-')):continue
 source=r/x['source'];h=hashlib.sha256(source.read_bytes()).hexdigest();dest=o/'frames'/f'{h}.png'
 if not dest.exists():shutil.copyfile(source,dest)
 assert dest.read_bytes()==source.read_bytes()
 row=next(z for z in inv['gears'][x['gear']] if z['key']==x['key'])
 key=x['gear']+'/'+x['key'];bank.setdefault(key,[]).append(dict(src='frames/'+dest.name,duration=row['durationsMs'][x['slot']],offset=x['offset'],slot=x['slot']))
 bindings[str(source.relative_to(r))]=h
html='''<!doctype html><meta charset="utf-8"><title>James swimming playback</title>
<style>body{background:#303b40;color:#ddd;font:15px Arial;margin:16px}header{max-width:1100px}button,select{margin:8px;padding:7px}main{display:grid;grid-template-columns:repeat(4,256px);gap:8px}canvas{width:256px;height:400px;background:#303b40}p{margin:5px}small{color:#bbb}</style>
<header><h2>James swimming comparison</h2><p>Exact selected sources at their declared scale and pivot. Left: swim / carry loops. Right: start → swim → stop source sequence. This viewer does not simulate game movement or interruptions.</p>
<label>Direction <select id="direction"><option>west</option><option>east</option><option>north</option><option>south</option></select></label>
<label>Speed <select id="speed"><option value="1">Normal</option><option value="0.25">Quarter speed</option></select></label><button id="replay">Replay</button><button id="pause">Pause</button><p id="clock">Loading images</p></header><main></main>
<script>
const BANK=__BANK__;let origin=performance.now(),held=0,paused=false,last=origin;const panels=[];
for(const type of ['swim','swim-carry','sequence'])for(const gear of ['bare','diving-helmet']){const div=document.createElement('div'),label=document.createElement('p'),canvas=document.createElement('canvas'),status=document.createElement('small');label.textContent=type+' / '+gear;canvas.width=256;canvas.height=400;div.append(label,canvas,status);document.querySelector('main').append(div);panels.push({type,gear,canvas,status});}
const images={};Promise.all(Object.values(BANK).flat().map(f=>{if(images[f.src])return;const im=new Image();images[f.src]=im;return new Promise((resolve,reject)=>{im.onload=resolve;im.onerror=reject;im.src=f.src;});})).then(()=>requestAnimationFrame(draw));
function reset(){held=0;last=performance.now();origin=last;}
document.querySelector('#replay').onclick=reset;document.querySelector('#direction').onchange=reset;document.querySelector('#speed').onchange=reset;
document.querySelector('#pause').onclick=()=>{paused=!paused;document.querySelector('#pause').textContent=paused?'Play':'Pause';last=performance.now();};
function draw(now){if(!paused)held+=(now-last)*Number(document.querySelector('#speed').value);last=now;const direction=document.querySelector('#direction').value;document.querySelector('#clock').textContent=`${paused?'Paused':'Playing'} · ${Math.floor(held)} ms · ${direction}`;
for(const p of panels){const kinds=p.type==='sequence'?['swim-start','swim','swim','swim-stop']:[p.type];const frames=kinds.flatMap(kind=>BANK[p.gear+'/'+kind+'-'+direction].map(f=>({...f,kind})));const total=frames.reduce((a,f)=>a+f.duration,0);let t=held%total,frame=frames[0];for(const f of frames){frame=f;if(t<f.duration)break;t-=f.duration;}const ctx=p.canvas.getContext('2d');ctx.clearRect(0,0,256,400);ctx.drawImage(images[frame.src],...frame.offset);ctx.strokeStyle='#506269';ctx.beginPath();ctx.moveTo(0,224);ctx.lineTo(256,224);ctx.stroke();p.status.textContent=`${frame.kind}-${direction} pose ${frame.slot} · cycle ${Math.floor(held/total)}`;}
requestAnimationFrame(draw);}
</script>'''.replace('__BANK__',json.dumps(bank))
(o/'index.html').write_text(html,encoding='utf-8')
(o/'inputs.json').write_text(json.dumps(dict(sourceBindings=bindings,bank=bank,normalChanged=False,scope='Exact selected source playback; sequence deliberately starts swim loop at phase zero, not an ordinary controller simulation.'),indent=2)+'\n')
print(json.dumps(dict(slots=sum(map(len,bank.values())),uniqueFiles=len(list((o/'frames').glob('*.png'))))))
