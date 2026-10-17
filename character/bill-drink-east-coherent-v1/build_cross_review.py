from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;E=P.parent/'bill-meal-east-coherent-v1';M=P.parent/'bill-seated-east-coherent-v1/frames/sit-down-east/000.png'
bindings={};board=Image.new('RGB',(1792,768),(34,52,62));preview={}
for row,(label,root) in enumerate([('drink',P),('eat',E)]):
    manifest=json.loads((root/'manifest.json').read_text());state=manifest['states'][0]
    preview[label]={'files':['/'+(root/f).relative_to(P.parent.parent).as_posix() for f in state['frameFiles']],'durations':state['frameDurationsMs']}
    for i,file in enumerate(state['frameFiles']):
        path=root/file;im=Image.open(path).convert('RGBA');board.paste(im,(i*256,row*256),im);bindings[path.relative_to(P.parent.parent).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
master=Image.open(M).convert('RGBA')
for i in range(7):board.paste(master,(i*256,512),master)
bindings[M.relative_to(P.parent.parent).as_posix()]=hashlib.sha256(M.read_bytes()).hexdigest()
board.save(P/'cross-action-review.png')
(P/'cross-action-bindings.json').write_text(json.dumps({'scope':'drink/eat candidate source comparison against selected idle; not actual meal service','sha256':bindings},indent=2)+'\n')
html='''<!doctype html><meta charset="utf-8"><title>Bill east meal consistency</title><style>body{font:16px system-ui;background:#152027;color:#e6eff1;margin:24px}button,select{font:inherit;padding:6px}p{max-width:90ch;color:#bdd0d2}</style><h1>Bill — eating, drinking and idle</h1><p>Two new bareheaded candidates against the selected master. Shared standing density, fixed atlas rulers, master matte grading and planted boots. Meal pickup/return transitions and normal service installation remain pending.</p><select id="size"><option>148</option><option>82</option><option>54</option></select><button id="play">Pause</button><canvas id="view" width="900" height="420"></canvas><script>const data=DATA;let time=0,last=performance.now(),playing=true;play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};const load=f=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f});Promise.all(Object.values(data).map(async s=>s.images=await Promise.all(s.files.map(load)))).then(async()=>{const master=await load('/character/bill-seated-east-coherent-v1/frames/sit-down-east/000.png');function draw(now){if(playing)time+=now-last;last=now;const c=view.getContext('2d'),scale=Number(size.value)/148;c.fillStyle='#22343e';c.fillRect(0,0,900,420);Object.entries(data).forEach(([name,s],j)=>{let t=time%960,index=0;for(let i=0;i<s.images.length;i++){index=i;if(t<s.durations[i])break;t-=s.durations[i]}c.fillStyle='#e6eff1';c.fillText(name,135+j*300,35);c.drawImage(s.images[index],150+j*300-128*scale,330-224*scale,256*scale,256*scale)});c.fillStyle='#e6eff1';c.fillText('master idle',710,35);c.drawImage(master,750-128*scale,330-224*scale,256*scale,256*scale);requestAnimationFrame(draw)}requestAnimationFrame(draw)});</script>'''
(P/'cross-action-review.html').write_text(html.replace('DATA',json.dumps(preview)))
print('Built source-bound drink/eat/master cross-action review')
