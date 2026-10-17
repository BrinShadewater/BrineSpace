from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
groups={'idle':[P.parent/'bill-seated-north-coherent-v1/frames/sit-down-north/000.png']*7,'eat':[P.parent/f'bill-meal-north-coherent-v1/frames/eat-north/{i:03}.png' for i in range(7)],'drink':[P/f'frames/drink-north/{i:03}.png' for i in range(7)]}
board=Image.new('RGB',(1792,768),(34,52,62));draw=ImageDraw.Draw(board);stats={};bindings={}
for row,(key,files) in enumerate(groups.items()):
 stats[key]=[]
 for i,f in enumerate(files):
  im=Image.open(f).convert('RGBA');board.paste(im,(256*i,256*row),im);draw.text((256*i+5,256*row+5),f'{key} {i}',fill='white')
  a=np.array(im);y,x=np.where(a[:,:,3]>180);bands={}
  for name,lo,hi in [('head',76,100),('legs',175,195),('boots',210,224)]:
   bx=x[(y>=lo)&(y<=hi)];bands[name]=[int(bx.min()),int(bx.max())] if len(bx) else []
  stats[key].append({'crown':int(y.min()),'sole':int(y.max()),'bands':bands})
  bindings[f.relative_to(ROOT).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
board.save(P/'cross-action-review.png')
(P/'cross-action-review.json').write_text(json.dumps({'sha256':bindings,'poseMetrics':stats,'scope':'independent alpha bands support visual comparison; no per-pose scaling or geometric warp'},indent=2)+'\n')
html='''<!doctype html><meta charset="utf-8"><title>Bill north meals/master</title><style>body{background:#152027;color:#e6eff1;font:16px system-ui;margin:24px}select,button{font:inherit;padding:6px}</style><h1>Bill north — master / eating / drinking</h1><p>Same standing plane and matte authority. Rear-held bowl and cup stay in front of torso. Staged loops; pickup, return and actual service phases pending.</p><select id="size"><option>148</option><option>82</option><option>54</option></select><button id="play">Pause</button><canvas id="view" width="960" height="420"></canvas><script>
let playing=true,time=0,last=performance.now();play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};const load=f=>new Promise((resolve,reject)=>{let im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f});Promise.all([fetch('/character/bill-meal-north-coherent-v1/manifest.json').then(r=>r.json()),fetch('manifest.json').then(r=>r.json())]).then(async ms=>{let groups=await Promise.all(ms.map(m=>Promise.all(m.states[0].frameFiles.map(f=>load('/character/'+(m.states[0].id==='eat-north'?'bill-meal-north-coherent-v1/':'bill-drink-north-coherent-v1/')+f))))),idle=await load('/character/bill-seated-north-coherent-v1/frames/sit-down-north/000.png');function draw(now){if(playing)time+=now-last;last=now;const c=view.getContext('2d'),scale=Number(size.value)/148;c.fillStyle='#22343e';c.fillRect(0,0,960,420);let pictures=[idle];ms.forEach((m,g)=>{let t=time%960,index=0;for(let i=0;i<7;i++){index=i;if(t<m.states[0].frameDurationsMs[i])break;t-=m.states[0].frameDurationsMs[i]}pictures.push(groups[g][index])});pictures.forEach((im,i)=>{c.drawImage(im,180+i*300-128*scale,330-224*scale,256*scale,256*scale);c.fillStyle='#e6eff1';c.fillText(['Selected idle','Eating candidate','Drinking candidate'][i],105+i*300,375)});requestAnimationFrame(draw)}requestAnimationFrame(draw)});
</script>'''
(P/'cross-action-review.html').write_text(html)
print(json.dumps({'crownRanges':{k:[min(s['crown'] for s in v),max(s['crown'] for s in v)] for k,v in stats.items()},'bandsFrame0':{k:v[0]['bands'] for k,v in stats.items()}}))
