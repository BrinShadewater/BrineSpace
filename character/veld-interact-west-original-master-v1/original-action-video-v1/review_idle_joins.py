from pathlib import Path
import json, hashlib, re
import numpy as np
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent
R=P.parents[2]
D=P/'idle-join-review-v1';D.mkdir(exist_ok=True)
inventory_path=R/'character/veld-master-consistency-current-v2/selected-library.json'
inventory=json.loads(inventory_path.read_bytes())
native_bindings=json.loads((R/'output/veld-west-interact-source-v1/inputs-after.json').read_bytes())
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in native_bindings.items())
bindings={inventory_path:hashlib.sha256(inventory_path.read_bytes()).hexdigest()}
grid_path=R/'scripts/grid_canvas.gd';catalog_path=R/'character/dr-veld-v2/catalog.json'
block=grid_path.read_text(encoding='utf-8').split('if actor == "veld":',1)[1].split('elif actor == "branforth":',1)[0]
catalog=json.loads(catalog_path.read_bytes())
assert inventory['loader']['bare']==['character/dr-veld-v2/'+s for s in catalog['body']]+re.findall(r'player\.load_manifest\("res://([^"\n]+)"',block)
assert inventory['loader']['helmet']==['character/dr-veld-v2/'+s for s in catalog['equipment']]+re.findall(r'player\.load_equipment_manifest\("diving-helmet", "res://([^"\n]+)"',block)
for path in [grid_path,catalog_path]:bindings[path]=hashlib.sha256(path.read_bytes()).hexdigest()
for name,h in inventory['bindings'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==h
tracks={};report={};checks=0
def load(path):
 global checks
 bindings[path]=hashlib.sha256(path.read_bytes()).hexdigest();checks+=1
 return Image.open(path).convert('RGBA')
def stats(im):
 a=np.asarray(im);y,x=np.where(a[:,:,3]>200)
 return dict(top=int(y.min()),bottom=int(y.max()),height=int(y.max()-y.min()+1),left=int(x.min()),right=int(x.max()))
def difference(a,b):
 aa=np.asarray(a);bb=np.asarray(b);union=(aa[:,:,3]>128)|(bb[:,:,3]>128);common=(aa[:,:,3]>200)&(bb[:,:,3]>200)
 return dict(unionPixels=int(union.sum()),commonPixels=int(common.sum()),alphaDifferentPixels=int(np.count_nonzero(aa[:,:,3]!=bb[:,:,3])),commonRGBMeanAbsoluteDifference=round(float(np.abs(aa[:,:,:3].astype(float)-bb[:,:,:3])[common].mean()),3),note='Spatial correspondence only; combines pose, detail and colour differences, not pure grading.')
for gear in ['bare','helmet']:
 entry=inventory['resolved'][gear]['idle-west'];idle=[];idle_urls=[]
 manifest_path=R/entry['manifest'];bindings[manifest_path]=hashlib.sha256(manifest_path.read_bytes()).hexdigest()
 for i,name in enumerate(entry['frameFiles']):
  path=R/name;assert hashlib.sha256(path.read_bytes()).hexdigest()==inventory['sourceBindings'][name]
  im=load(path);plate=Image.new('RGBA',(256,256));px,py=entry['pivot'];plate.alpha_composite(im,(128-round(px),224-round(py)))
  dest=D/f'{gear}-idle-{i:03}.png';plate.save(dest);idle.append(plate);idle_urls.append(dest.name)
 ds=entry['frameDurationsMs'];assert len(ds)==len(idle)==72
 action=[load(P/f'clip-frames/{gear}/{i:03}.png') for i in range(142)]
 manifest=json.loads((P/f'{gear}-source-manifest.json').read_bytes())
 ad=manifest['states'][0]['frameDurationsMs'];assert len(ad)==142
 master=load(P/f'{gear}-original-reference.png')
 action_urls=[f'../clip-frames/{gear}/{i:03}.png' for i in range(142)]
 tracks[gear]={
  'selected':dict(urls=idle_urls+action_urls+idle_urls,durations=ds+ad+ds,labels=[f'Idle {i}' for i in range(72)]+[f'Scanner {i}' for i in range(142)]+[f'Idle {i}' for i in range(72)]),
  'master':dict(urls=[f'../{gear}-original-reference.png']+action_urls+[f'../{gear}-original-reference.png'],durations=[1000]+ad+[1000],labels=['Master']+[f'Scanner {i}' for i in range(142)]+['Master'])}
 rows=[('Idle 71',idle[-1]),('Action 0',action[0]),('Action 1',action[1]),('Action 140',action[140]),('Action 141',action[-1]),('Idle 0',idle[0])]
 board=Image.new('RGB',(1536,540),'#202a30');draw=ImageDraw.Draw(board)
 for i,(label,im) in enumerate(rows):
  board.paste(im,(i*256,26),im);draw.text((i*256+8,5),label,fill='white')
  detail=im.crop((100,60,164,124)).resize((256,256),Image.Resampling.NEAREST)
  board.paste(detail,(i*256,284),detail)
 board.save(D/f'{gear}-join-details.png')
 board=Image.new('RGB',(1536,1728),'#202a30');draw=ImageDraw.Draw(board)
 for i,im in enumerate(idle):
  xy=((i%12)*128,(i//12)*288);board.paste(im.crop((80,60,208,244)),(xy[0],xy[1]+25),im.crop((80,60,208,244)));draw.text((xy[0]+3,xy[1]+3),f'Idle {i}',fill='white')
 board.save(D/f'{gear}-full-idle.png')
 report[gear]=dict(idleFrames=len(idle),actionFrames=len(action),selectedChainDurationMs=sum(ds)*2+sum(ad),idleBounds=[stats(im) for im in idle],actionEndpoints=[stats(action[0]),stats(action[-1])],masterBounds=stats(master),entry=difference(idle[-1],action[0]),exit=difference(action[-1],idle[0]),masterEntry=difference(master,action[0]),masterExit=difference(action[-1],master))
 assert all(hashlib.sha256(path.read_bytes()).hexdigest()==h for path,h in bindings.items())
payload=dict(tracks=tracks,report=report)
(D/'tracks.json').write_text(json.dumps(payload,indent=2)+'\n')
html='''<!doctype html><meta charset="utf-8"><title>Veld West idle and scanner transitions</title><style>body{background:#202a30;color:#eee;font:16px system-ui;margin:24px}button,select{font:inherit;padding:8px;margin:4px}canvas{display:block}a{color:#b7daee}</style><h1>Veld West idle and scanner transitions</h1><p>Full current idle → scanner action → full current idle. Compare with the same action between original master holds.</p><select id="gear"><option value="bare">Standard</option><option value="helmet">Helmet</option></select><select id="route"><option value="selected">Current idle transitions</option><option value="master">Original master transitions</option></select><button id="play">Play / pause</button><button id="entry">At entry</button><button id="exit">At exit</button><button id="restart">Restart</button><p id="label"></p><canvas id="view" width="780" height="340"></canvas><p><a href="bare-join-details.png">Standard transition details</a> · <a href="helmet-join-details.png">Helmet transition details</a></p><script>
let data,images={},track,index=0,running=false,last=0,elapsed=0;
let gear=document.querySelector('#gear'),route=document.querySelector('#route'),canvas=document.querySelector('#view'),ctx=canvas.getContext('2d');
function draw(){ctx.fillStyle='#202a30';ctx.fillRect(0,0,780,340);ctx.imageSmoothingEnabled=true;let x=0;for(let h of [47,93,148]){let s=h/148,w=256*s;ctx.fillStyle='#eee';ctx.font='16px system-ui';ctx.fillText(h+' px',x+8,24);ctx.drawImage(images[track.urls[index]],x,40,w,w);x+=w+24;}document.querySelector('#label').textContent=track.labels[index]+' · '+(index+1)+' / '+track.urls.length;}
function reset(){running=false;index=0;elapsed=0;track=data.tracks[gear.value][route.value];draw();}
function tick(t){if(running){elapsed+=Math.min(t-last,100);while(elapsed>=track.durations[index]){elapsed-=track.durations[index];index=(index+1)%track.urls.length;}draw();}last=t;requestAnimationFrame(tick);}
document.querySelector('#play').onclick=()=>running=!running;document.querySelector('#restart').onclick=reset;gear.onchange=route.onchange=reset;
document.querySelector('#entry').onclick=()=>{running=false;elapsed=0;index=route.value==='selected'?71:0;draw();};document.querySelector('#exit').onclick=()=>{running=false;elapsed=0;index=route.value==='selected'?212:141;draw();};
let next=document.createElement('button');next.textContent='Next frame';document.querySelector('#restart').after(next);next.onclick=()=>{running=false;elapsed=0;index=(index+1)%track.urls.length;draw();};
document.querySelector('#label').textContent='Loading frames…';document.querySelectorAll('button,select').forEach(e=>e.disabled=true);
fetch('tracks.json').then(r=>r.json()).then(async d=>{data=d;let urls=[...new Set(Object.values(d.tracks).flatMap(g=>Object.values(g).flatMap(t=>t.urls)))];await Promise.all(urls.map(u=>new Promise((resolve,reject)=>{let i=new Image();i.onload=()=>{images[u]=i;resolve()};i.onerror=reject;i.src=u})));reset();document.querySelectorAll('button,select').forEach(e=>e.disabled=false);requestAnimationFrame(tick);});
</script>'''
(D/'index.html').write_text(html,encoding='utf-8')
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in native_bindings.items())
evidence=dict(checks=checks,failures=0,nativeInputsUnchanged=len(native_bindings),bindings={p.relative_to(R).as_posix():h for p,h in bindings.items()},report=report,scope='Complete unchanged source-clock review. Browser scaling uses common148px ruler and fixed canvas; no native controller or contact claim.')
(D/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps(dict(checks=checks,nativeInputsUnchanged=len(native_bindings),joins={g:{k:report[g][k] for k in ['entry','exit','masterEntry','masterExit']} for g in report})))
