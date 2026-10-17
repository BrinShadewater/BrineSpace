from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parent;packs={};checks=[];bindings={};preview={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,label):checks.append({'passed':bool(ok),'check':label})
for gear in ['bare','helmet']:
 states=[]
 for direction in ['east','south','west','north']:
  loop_root=ROOT/f'bill-inspect-{direction}-coherent-v1';entry_root=ROOT/f'bill-inspect-entry-{direction}-v1'
  loop_path=loop_root/(gear+'-manifest.json');entry_path=entry_root/(gear+'-manifest.json')
  loop=json.loads(loop_path.read_text())['states'][0];enter,exit=json.loads(entry_path.read_text())['states']
  check([enter['id'],loop['id'],exit['id']]==['inspect-enter-'+direction,'inspect-'+direction,'inspect-exit-'+direction],gear+' action identities '+direction)
  check(sum(enter['frameDurationsMs'])==480 and sum(loop['frameDurationsMs'])==960 and sum(exit['frameDurationsMs'])==480,gear+' retained timing '+direction)
  check(enter['frameFiles'][::-1]==exit['frameFiles'] and enter['frameDurationsMs'][::-1]==exit['frameDurationsMs'],gear+' exact reverse '+direction)
  check(Image.open(entry_root/enter['frameFiles'][-1]).tobytes()==Image.open(loop_root/loop['frameFiles'][0]).tobytes() and Image.open(entry_root/exit['frameFiles'][0]).tobytes()==Image.open(loop_root/loop['frameFiles'][-1]).tobytes(),gear+' exact held joins '+direction)
  for root,path,state in [(entry_root,entry_path,enter),(loop_root,loop_path,loop),(entry_root,entry_path,exit)]:
   expected=json.loads((root/'frame-hashes.json').read_text());bindings[path.relative_to(ROOT).as_posix()]=sha(path)
   check(all(sha(root/file)==expected[file] for file in state['frameFiles']),gear+' source bindings '+state['id'])
   check(len(state['frameFiles'])==6 and state['depthOffsets']==[0]*6 and state['facings']==[direction]*6 and state['waterPoses']==[False]*6,gear+' standing metadata '+state['id'])
   result=dict(state);result['frameFiles']=['res://'+(root/file).relative_to(ROOT.parent).as_posix() for file in state['frameFiles']];states.append(result)
   for file in state['frameFiles']:bindings[(root/file).relative_to(ROOT).as_posix()]=sha(root/file)
  preview.setdefault(direction,{})[gear]=[{**s,'frameFiles':['/'+f.removeprefix('res://') for f in s['frameFiles']]} for s in [states[-3],states[-2],states[-2],states[-1]]]
 m={'name':'Bill cardinal standing inspection '+gear,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'selected_runtime','states':states}
 if gear=='helmet':m['equipment']='diving-helmet'
 (P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n');packs[gear]=m
result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'states':sum(len(m['states']) for m in packs.values()),'refs':sum(len(s['frameFiles']) for m in packs.values() for s in m['states']),'scope':'source/join bindings; normal selection and actual activity separately verified by selected renderer and service fixtures','results':checks,'sha256':bindings}
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
html='''<!doctype html><meta charset="utf-8"><title>Bill cardinal reader transitions</title><style>body{font:16px system-ui;background:#152027;color:#e6eff1;margin:24px}button,select{font:inherit;padding:6px}p{max-width:85ch;color:#bdd0d2}</style><h1>Bill — cardinal reader draw, inspect, stow</h1><p>All four directions in both gear states. Top: complete preview cycle. Bottom: matching selected idle endpoint. Exact idle/held joins; native master helmets, fixed source rulers and matte grading. Candidate family; actual activity integration and full-set polish remain pending.</p><select id="gear"><option value="bare">Bare</option><option value="helmet">Helmet</option></select><select id="size"><option selected>82</option><option>148</option><option>54</option></select><button id="play">Pause</button><canvas id="view" width="1000" height="620"></canvas><script>const data=DATA;let time=0,last=performance.now(),playing=true;play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};const load=f=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f});Promise.all(Object.values(data).flatMap(d=>Object.values(d).flat()).map(async s=>s.images=await Promise.all(s.frameFiles.map(load)))).then(()=>{function draw(now){if(playing)time+=now-last;last=now;const c=view.getContext('2d'),scale=Number(size.value)/148;c.fillStyle='#22343e';c.fillRect(0,0,1000,620);Object.entries(data).forEach(([direction,d],j)=>{const states=d[gear.value],images=states.flatMap(s=>s.images),durations=states.flatMap(s=>s.frameDurationsMs);let elapsed=time%durations.reduce((a,b)=>a+b,0),index=0;for(let i=0;i<images.length;i++){index=i;if(elapsed<durations[i])break;elapsed-=durations[i]}const x=125+j*250;c.fillStyle='#e6eff1';c.fillText(direction,x-25,30);c.drawImage(images[index],x-128*scale,280-224*scale,256*scale,256*scale);c.drawImage(images[0],x-128*scale,550-224*scale,256*scale,256*scale)});requestAnimationFrame(draw)}requestAnimationFrame(draw)});</script>'''
(P/'index.html').write_text(html.replace('Candidate family; actual activity integration and full-set polish remain pending.','Service draw/stow installed; broader contact checks and full-set polish remain pending.').replace('DATA',json.dumps(preview)))
print(json.dumps({k:result[k] for k in ['passed','checks','states','refs']}))
raise SystemExit(0 if result['passed'] else 1)
