from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
groups=[];bindings={};checks=[];metrics={};board=Image.new('RGB',(1536,1024),(34,52,62));draw=ImageDraw.Draw(board)
def check(ok,label):checks.append({'passed':bool(ok),'check':label})
for direction in ['west','east']:
    p=P.parent/f'bill-death-ground-{direction}-coherent-v1';m=json.loads((p/'manifest.json').read_text());s=m['states'][0]
    groups.append({'direction':direction,'files':['/'+(p/f).relative_to(ROOT).as_posix() for f in s['frameFiles']],'durations':s['frameDurationsMs']})
    check(m['pivot']==[128,224] and m['standingHeight']==148 and m['precomposed'],'Shared physical sprite contract '+direction)
    check(not s['loop'] and sum(s['frameDurationsMs'])==2000 and s['terminalFrame']==5,'Finite shared pacing/terminal '+direction)
    metrics[direction]=[]
    for i,f in enumerate(s['frameFiles']):
        path=p/f;im=Image.open(path).convert('RGBA');row=0 if direction=='west' else 2;board.paste(im,(i*256,row*256),im)
        idle=Image.open(p/s['frameFiles'][0]).convert('RGBA');board.paste(idle,(i*256,(row+1)*256),idle)
        draw.text((i*256+5,row*256+5),f'{direction} {i}',fill='white')
        a=np.array(im);y,x=np.where(a[:,:,3]>180);metrics[direction].append({'frame':i,'bounds':[int(x.min()),int(y.min()),int(x.max()),int(y.max())]})
        bindings[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
check(groups[0]['durations']==groups[1]['durations'],'Same east/west authored clock')
board.save(P/'cross-direction-review.png')
(P/'cross-direction-review.json').write_text(json.dumps({'passed':all(c['passed'] for c in checks),'checks':checks,'sha256':bindings,'poseMetrics':metrics,'scope':'shared plane/clock and visual review aid; source identity/body-detail/actual mortality acceptance separate'},indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>Bill side-view collapse comparison</title><style>body{font:16px system-ui;background:#152027;color:#e6eff1;margin:24px}button,select{font:inherit;padding:6px}p{max-width:90ch}</style><h1>Bill — independent east / west ground-collapse candidates</h1><p>Shared two-second presentation clock with terminal hold. Independently authored figures, one fixed ruler per source. Candidate art comparison only; normal mortality and helmet variants remain pending.</p><select id="size"><option>148</option><option>82</option><option>54</option></select><button id="replay">Replay</button><canvas id="view" width="960" height="420"></canvas><script>const data=DATA,load=f=>new Promise((resolve,reject)=>{let im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f});let t=0,last=performance.now();replay.onclick=()=>t=0;Promise.all(data.map(async s=>s.images=await Promise.all(s.files.map(load)))).then(()=>{function draw(now){t=Math.min(2000,t+now-last);last=now;const c=view.getContext('2d'),scale=Number(size.value)/148;c.fillStyle='#22343e';c.fillRect(0,0,960,420);data.forEach((s,g)=>{let elapsed=t,index=5;for(let i=0;i<6;i++){if(elapsed<s.durations[i]){index=i;break}elapsed-=s.durations[i]}let x=210+g*520;c.drawImage(s.images[index],x-128*scale,330-224*scale,256*scale,256*scale);c.drawImage(s.images[0],x+145-128*scale,330-224*scale,256*scale,256*scale);c.fillStyle='#e6eff1';c.fillText(s.direction+' candidate / master',x-90,375)});requestAnimationFrame(draw)}requestAnimationFrame(draw)});</script>'''
(P/'cross-direction-review.html').write_text(html.replace('DATA',json.dumps(groups)),encoding='utf-8');print('Built hash-bound side-view collapse comparison: five shared-contract checks')
