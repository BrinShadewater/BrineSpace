from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
checks=[];bindings={};states=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,label):checks.append({'passed':bool(ok),'check':label})
for name,indices in [('bill-meal-entry-south-v1',[0]),('bill-meal-south-coherent-v1',[0]),('bill-meal-entry-south-v1',[1]),('bill-drink-entry-south-v1',[0]),('bill-drink-south-coherent-v1',[0]),('bill-drink-entry-south-v1',[1])]:
    root=P.parent/name;path=root/'manifest.json';m=json.loads(path.read_text());v=json.loads((root/'verification.json').read_text())
    bindings[path.relative_to(ROOT).as_posix()]=sha(path)
    check(v['passed'] and m['status']=='staged_candidate','Verified source candidate '+name)
    check(m['pivot']==[128,224] and m['standingHeight']==148 and m['frameWidth']==256 and m['frameHeight']==256 and m['precomposed'],'Shared density/plane '+name)
    for index in indices:
        state=m['states'][index];expected=json.loads((root/'frame-hashes.json').read_text())
        check(len(state['frameFiles'])==7 and state['facings']==['south']*7 and state['waterPoses']==[False]*7 and state['depthOffsets']==[0]*7,'Seven dry south frames '+state['id'])
        check(all(sha(root/f)==expected[f] for f in state['frameFiles']),'Source pixels bound '+state['id'])
        check(sum(state['frameDurationsMs'])==(960 if state['loop'] else 580),'Authored pacing '+state['id'])
        for file in state['frameFiles']:bindings[(root/file).relative_to(ROOT).as_posix()]=sha(root/file)
        states.append({**state,'frameFiles':['res://'+(root/f).relative_to(ROOT).as_posix() for f in state['frameFiles']]})
check([s['id'] for s in states]==['eat-enter-south','eat-south','eat-exit-south','drink-enter-south','drink-south','drink-exit-south'],'Full ordered south bare meal family')
def pixels(file):return Image.open(ROOT/file.removeprefix('res://')).convert('RGBA').tobytes()
for i in range(5):check(pixels(states[i]['frameFiles'][-1])==pixels(states[i+1]['frameFiles'][0]),'Exact ordered adjacent join '+states[i]['id'])
check(pixels(states[-1]['frameFiles'][-1])==pixels(states[0]['frameFiles'][0]),'Exact full meal idle closure')
for a,b in [(0,2),(3,5)]:check(states[a]['frameFiles'][::-1]==states[b]['frameFiles'] and states[a]['frameDurationsMs'][::-1]==states[b]['frameDurationsMs'],'Exact reverse transition '+states[a]['id'])
manifest={'name':'Bill south bare meal family','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':states}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'states':len(states),'refs':sum(len(s['frameFiles']) for s in states),'results':checks,'sha256':bindings,'scope':'assembled source/pacing/joins; candidate native loading and normal service integration are separate'}
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
preview=[{**s,'frameFiles':['/'+f.removeprefix('res://') for f in s['frameFiles']]} for s in states]
html='''<!doctype html><meta charset="utf-8"><title>Bill south meal family</title><style>body{font:16px system-ui;background:#152027;color:#e6eff1;margin:24px}button,select{font:inherit;padding:6px}p{max-width:90ch;color:#bdd0d2}</style><h1>Bill — south full meal sequence</h1><p>Left: new bareheaded bowl pickup, eating, bowl return, cup pickup, drinking, cup return. Right: selected idle master. Candidate preview uses the existing six-second eating and three-second drinking service durations. Actual normal runtime integration, counter contact and restore checks remain pending.</p><select id="size"><option>148</option><option>82</option><option>54</option></select><button id="play">Pause</button><canvas id="view" width="720" height="420"></canvas><script>const data=DATA;let time=0,last=performance.now(),playing=true;play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};const load=f=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f});Promise.all(data.map(async s=>s.images=await Promise.all(s.frameFiles.map(load)))).then(()=>{function draw(now){if(playing)time+=now-last;last=now;let t=time%9000,base=0,duration=6000;if(t>=6000){t-=6000;base=3;duration=3000}let clip=base,elapsed=t;if(t>=duration-580){clip=base+2;elapsed=t-(duration-580)}else if(t>=580){clip=base+1;elapsed=(t-580)%960}const s=data[clip];let index=0;for(let i=0;i<s.images.length;i++){index=i;if(elapsed<s.frameDurationsMs[i])break;elapsed-=s.frameDurationsMs[i]}const c=view.getContext('2d'),scale=Number(size.value)/148;c.fillStyle='#22343e';c.fillRect(0,0,720,420);c.fillStyle='#e6eff1';c.fillText(s.id,155,30);c.fillText('selected idle',475,30);c.drawImage(s.images[index],200-128*scale,330-224*scale,256*scale,256*scale);c.drawImage(data[0].images[0],520-128*scale,330-224*scale,256*scale,256*scale);requestAnimationFrame(draw)}requestAnimationFrame(draw)});</script>'''
(P/'index.html').write_text(html.replace('Actual normal runtime integration, counter contact and restore checks remain pending.','Staged south family. Current galley approaches face south or south; activity transitions, counter contact and restore checks remain pending.').replace('DATA',json.dumps(preview)),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['passed','checks','states','refs']}));raise SystemExit(0 if result['passed'] else 1)
