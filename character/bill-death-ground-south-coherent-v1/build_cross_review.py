from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
directions=['east','west','north','south'];groups=[];bindings={};checks=[];metrics={}
board=Image.new('RGB',(1536,2048),(34,52,62));draw=ImageDraw.Draw(board)
for g,direction in enumerate(directions):
 p=P.parent/f'bill-death-ground-{direction}-coherent-v1';m=json.loads((p/'manifest.json').read_text());s=m['states'][0]
 groups.append({'direction':direction,'files':['/'+(p/f).relative_to(ROOT).as_posix() for f in s['frameFiles']],'durations':s['frameDurationsMs']})
 checks.append({'passed':m['pivot']==[128,224] and m['standingHeight']==148 and m['precomposed'],'check':'Shared plane '+direction})
 checks.append({'passed':not s['loop'] and sum(s['frameDurationsMs'])==2000 and s['terminalFrame']==5,'check':'Finite corpse clock '+direction})
 metrics[direction]=[]
 for i,f in enumerate(s['frameFiles']):
  path=p/f;im=Image.open(path).convert('RGBA');board.paste(im,(i*256,g*512),im)
  idle=Image.open(p/s['frameFiles'][0]).convert('RGBA');board.paste(idle,(i*256,g*512+256),idle)
  draw.text((i*256+5,g*512+5),f'{direction} {i}',fill='white')
  a=np.array(im);y,x=np.where(a[:,:,3]>180);metrics[direction].append({'frame':i,'bounds':[int(x.min()),int(y.min()),int(x.max()),int(y.max())]})
  bindings[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
checks.append({'passed':all(g['durations']==groups[0]['durations'] for g in groups),'check':'Same four-direction finite timeline'})
board.save(P/'cross-direction-review.png')
(P/'cross-direction-review.json').write_text(json.dumps({'passed':all(c['passed'] for c in checks),'checks':checks,'sha256':bindings,'poseMetrics':metrics,'scope':'plane/finite clock and visual comparison aid; fine identity, physical clearance, helmet and mortality acceptance separate'},indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>Bill four-direction collapse candidates</title><style>body{font:16px system-ui;background:#152027;color:#e6eff1;margin:24px}button,select{font:inherit;padding:6px}canvas{max-width:100%;height:auto}p{max-width:95ch}</style><h1>Bill — four-direction ground collapse comparison</h1><p>Independent whole figures beside their selected idle masters. Shared finite2s timeline, terminal hold. Candidate review: detail, materials, body proportions and physical floor contact remain open. Side falls and axial foreshortening have different silhouettes; identical bounding heights are not a physical consistency criterion.</p><select id="size"><option>148</option><option>82</option><option>54</option></select><button id="replay">Replay</button><input id="scrub" type="range" min="0" max="2000"><span id="stamp"></span><br><canvas id="view" width="1440" height="420"></canvas><p><a href="cross-direction-review.png">All six frames and master comparison board</a></p><script>const data=DATA,load=f=>new Promise((resolve,reject)=>{let im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f});let t=0,last=performance.now(),playing=true;replay.onclick=()=>{t=0;playing=true};scrub.oninput=()=>{t=Number(scrub.value);playing=false};Promise.all(data.map(async s=>s.images=await Promise.all(s.files.map(load)))).then(()=>{function draw(now){if(playing)t=Math.min(2000,t+now-last);last=now;scrub.value=t;stamp.textContent=(t/1000).toFixed(2)+' s';const c=view.getContext('2d'),scale=Number(size.value)/148;c.fillStyle='#22343e';c.fillRect(0,0,1440,420);data.forEach((s,g)=>{let elapsed=t,index=5;for(let i=0;i<6;i++){if(elapsed<s.durations[i]){index=i;break}elapsed-=s.durations[i]}let x=100+g*360;c.drawImage(s.images[index],x-128*scale,330-224*scale,256*scale,256*scale);c.drawImage(s.images[0],x+155-128*scale,330-224*scale,256*scale,256*scale);c.fillStyle='#e6eff1';c.fillText(s.direction+' candidate / idle',x-60,380)});requestAnimationFrame(draw)}requestAnimationFrame(draw)});</script>'''
(P/'cross-direction-review.html').write_text(html.replace('DATA',json.dumps(groups)),encoding='utf-8');print('Four-direction comparison:9 shared contract checks,24 bound frames')
