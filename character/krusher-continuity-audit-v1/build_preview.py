"""Export the complete review library to the existing private preview Site."""
from pathlib import Path
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import json,shutil,sys,re
import numpy as np
H=Path(__file__).resolve().parent;R=H.parents[1];P=R/'character/krusher-animation-package-v10'
site=Path(sys.argv[1]);O=site/'dist/animations';O.mkdir(parents=True,exist_ok=True)
index=json.loads((P/'package.json').read_text());(O/'frames').mkdir(exist_ok=True)
def convert(rel):
 src=P/rel;dest=O/Path(rel).with_suffix('.webp');im=Image.open(src).convert('RGBA')
 if not dest.exists():im.save(dest,lossless=True,exact=True,method=4)
 assert np.array_equal(np.array(im),np.array(Image.open(dest).convert('RGBA'))),rel
 return dest.stat().st_size
with ThreadPoolExecutor(max_workers=4) as pool:sizes=list(pool.map(convert,index['files']))
library={'bare':{},'helmet':{}};manifests={}
for full,q in index['states'].items():
 gear,key=full.split(':',1);mp=P/q['manifest'];m=manifests.setdefault(str(mp),json.loads(mp.read_text()));s=next(s for s in m['states'] if s['id']==key)
 library[gear][key]={'files':[(mp.parent/f).resolve().relative_to(P.resolve()).with_suffix('.webp').as_posix() for f in s['frameFiles']],'durations':s['frameDurationsMs'],'loop':s.get('loop',False),'width':m['frameWidth'],'height':m['frameHeight'],'pivot':m['pivot']}
(O/'library.js').write_text('const LIBRARY='+json.dumps(library)+';\n')
shutil.copyfile(P/'references/character-sheet.png',O/'character-sheet.png')
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krusher Dom · Animation library</title>
<style>*{box-sizing:border-box}body{margin:0;background:#151d21;color:#e0e8e8;font:17px system-ui,sans-serif}main{max-width:1080px;margin:auto;padding:24px}a{color:#acd2d5}h1{font-size:clamp(32px,6vw,58px);margin:16px 0 8px}p{color:#b2c4c7;line-height:1.55}.eyebrow{letter-spacing:.15em;font-size:12px;color:#83a5aa}section{margin-top:24px;padding:20px;background:#202a2e;border:1px solid #3a4d53;border-radius:14px}.controls{display:grid;grid-template-columns:1fr 1fr;gap:10px}select,input,button{font:inherit;min-height:44px;padding:9px;border:1px solid #527c80;background:#162125;color:#e0e8e8;border-radius:7px;width:100%}label{font-size:13px;color:#b2c4c7}.wide{grid-column:1/-1}.buttons{display:flex;gap:8px;margin:12px 0}canvas{display:block;background:#303b40;image-rendering:pixelated;width:100%;height:auto;max-width:640px;margin:auto;border-radius:8px}img{max-width:100%;height:auto}.small{font-size:13px}#info{font-variant-numeric:tabular-nums;min-height:3em}.scrub{width:100%}summary{cursor:pointer}button{cursor:pointer}a:focus,button:focus,input:focus,select:focus{outline:2px solid #c2dfe1;outline-offset:3px}</style>
<main><a href="../">← Character reference</a><h1>Krusher Dom</h1><div class="eyebrow">SYSTEM ADMINISTRATOR / AI &amp; ROBOTICS</div><p>586 animation states · 338 bare / 248 helmet · 8,058 authored frame holds.<br>Current likeness, connected collar and muted cyan suit throughout the set.</p>
<section><div class="controls"><label>Equipment<select id="gear"><option value="bare">Bare head</option><option value="helmet">Diving helmet</option></select></label><label>Find an action<input id="search" type="search" placeholder="repair, swim, sleep…"></label><label class="wide">Animation<select id="state"></select></label><label>Display scale<select id="scale"><option value="1">Native pixels</option><option value="2" selected>2× nearest</option><option value="3">3× nearest</option></select></label><label>Playback speed<select id="speed"><option value=".5">Half speed</option><option value="1" selected>Original timing</option><option value="2">Double speed</option></select></label></div>
<div class="buttons"><button id="previous">← Previous</button><button id="play">Pause</button><button id="next">Next →</button></div><canvas id="view" width="640" height="720" aria-label="Animated character preview"></canvas><input class="scrub" id="scrub" aria-label="Animation position" type="range" min="0" max="1000" value="0"><p id="info" class="small" aria-live="off">Loading…</p><p class="small">One-shot actions replay here for review. The floor cross marks the declared pivot. Gaits replay by time here; station locomotion uses travel distance.</p></section>
<section><details><summary>Four-direction character sheet</summary><img src="character-sheet.png" alt="Current bare and helmet turnaround"></details><p class="small">A complete animation asset candidate. Normal crew roster integration and owner visual acceptance are separate. Original body poses, tools, equipment shells, timing and per-pack geometry are retained.</p></section></main><script src="library.js"></script><script>
const $=s=>document.querySelector(s),g=$('#gear'),s=$('#state'),c=$('#view'),ctx=c.getContext('2d'),info=$('#info'),scrub=$('#scrub');let imgs=[],record=null,epoch=performance.now(),running=true,paused=0,frameIndex=0,loadId=0;
function options(){const old=s.value,query=$('#search').value.toLowerCase();s.replaceChildren();for(const key of Object.keys(LIBRARY[g.value]).sort()){if(!key.includes(query))continue;const o=document.createElement('option');o.value=o.textContent=key;s.append(o)}if([...s.options].some(x=>x.value===old))s.value=old;else if(!query)s.value='idle-south';load()}
function load(){record=LIBRARY[g.value][s.value]||null;const id=++loadId;imgs=record?record.files.map(p=>{const im=new Image();im.src=p;return im}):[];epoch=performance.now();paused=0;frameIndex=0;window.previewState={gear:g.value,key:s.value,loaded:false};Promise.all(imgs.map(im=>im.decode())).then(()=>{if(id===loadId)window.previewState.loaded=true}).catch(()=>{if(id===loadId)info.textContent='An image could not be loaded.'})}
g.onchange=options;s.onchange=load;$('#search').oninput=options;$('#speed').onchange=load;$('#play').onclick=()=>{if(running)paused=(performance.now()-epoch)*Number($('#speed').value);else epoch=performance.now()-paused/Number($('#speed').value);running=!running;$('#play').textContent=running?'Pause':'Play'};
function step(delta){if(!s.options.length)return;s.selectedIndex=(s.selectedIndex+delta+s.options.length)%s.options.length;load()}$('#previous').onclick=()=>step(-1);$('#next').onclick=()=>step(1);
scrub.oninput=()=>{running=false;$('#play').textContent='Play';if(record)paused=Number(scrub.value)/1000*record.durations.reduce((a,b)=>a+b,0)};
function draw(now){ctx.clearRect(0,0,c.width,c.height);if(record){const total=record.durations.reduce((a,b)=>a+b,0),t=(running?(now-epoch)*Number($('#speed').value):paused)%total;let elapsed=t,i=0;while(i<record.durations.length-1&&elapsed>=record.durations[i])elapsed-=record.durations[i++];frameIndex=i;ctx.imageSmoothingEnabled=false;const z=Number($('#scale').value),im=imgs[i],x=320-record.pivot[0]*z,y=600-record.pivot[1]*z;if(im.complete&&im.naturalWidth)ctx.drawImage(im,x,y,record.width*z,record.height*z);ctx.strokeStyle='#7aa3a8';ctx.beginPath();ctx.moveTo(310,600);ctx.lineTo(330,600);ctx.moveTo(320,596);ctx.lineTo(320,604);ctx.stroke();scrub.value=Math.floor(t/total*1000);info.textContent=g.value+' / '+s.value+' · pose '+(i+1)+' of '+imgs.length+' · '+total+' ms · '+record.width+' × '+record.height+' · pivot '+record.pivot.join(', ');window.previewState={...window.previewState,frame:i,totalMs:total,running};}else info.textContent='No animations match this search.';requestAnimationFrame(draw)}options();requestAnimationFrame(draw);
</script></html>'''
(O/'index.html').write_text(html,encoding='utf8')
home=site/'dist/index.html';text=home.read_text(encoding='utf8')
link='<section id="complete-animation-library" style="padding:20px;margin:20px 0;border:1px solid #527c80;border-radius:12px"><h2>Complete animation library</h2><p>586 revised states, bare and helmet. Browse work, cargo, meals, rest, recovery and underwater actions.</p><a href="animations/" style="font-size:22px">Open all animations →</a></section>'
if 'id="complete-animation-library"' not in text:text=re.sub(r'(</h1>)',lambda m:m.group(1)+link,text,count=1)
home.write_text(text,encoding='utf8')
report={'states':sum(map(len,library.values())),'frameHolds':sum(len(s['files']) for rows in library.values() for s in rows.values()),'losslessWebP':len(sizes),'bytes':sum(sizes),'decodedRgbaChecks':len(sizes),'output':str(O)}
(H/'preview-export.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))


