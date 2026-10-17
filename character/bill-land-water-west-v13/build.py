"""Reconcile a staged entry endpoint with the actual new swim authority."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent
V=R/'bill-land-water-west-v12';SW=R/'bill-swim-west-calibrated-v6';EXIT=R/'bill-water-exit-west-master-v13'
IDLES={'bare':R/'crew-runtime-matte-v1/bill','helmet':R/'bill-shared-helmet-runtime-v2'}
inputs=[Path(__file__)]+[V/g/'manifest.json' for g in ['bare','helmet']]+[V/g/f'frames/land-swim-west/{i:03}.png' for g in ['bare','helmet'] for i in range(7)]+[SW/g/'manifest.json' for g in ['bare','helmet']]+[SW/g/'frames/swim-west/000.png' for g in ['bare','helmet']]+[SW/g/'frames/swim-west/001.png' for g in ['bare','helmet']]
inputs += [EXIT/g/'frames/swim-land-west/007.png' for g in ['bare','helmet']]
for gear,root in IDLES.items():
 inputs.append(root/'manifest.json');m=json.loads((root/'manifest.json').read_text());st=next(st for st in m['states'] if st['id']=='idle-west');inputs.append(root/st['frameFiles'][0])
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
before={f.relative_to(R).as_posix():sha(f) for f in inputs}
banks={};checks=[]
for gear in ['bare','helmet']:
    m=json.loads((V/gear/'manifest.json').read_text(encoding='utf-8'));bank=[]
    for i in range(7):
        if i==6:
            im=Image.open(SW/gear/'frames/swim-west/000.png').convert('RGBA')
            assert im.size==(352,320)
        elif i==0:
            im=Image.open(EXIT/gear/'frames/swim-land-west/007.png').convert('RGBA')
            root=IDLES[gear];idleManifest=json.loads((root/'manifest.json').read_text());st=next(st for st in idleManifest['states'] if st['id']=='idle-west')
            idle=Image.open(root/st['frameFiles'][0]).convert('RGBA');assert idle.size==(184,184)
            padded=Image.new('RGBA',(352,320));padded.alpha_composite(idle,(68,52))
            assert im.tobytes()==padded.tobytes()
        else:
            prior=Image.open(V/gear/f'frames/land-swim-west/{i:03}.png').convert('RGBA');assert prior.size==(352,320)
            im=prior.copy();assert im.tobytes()==prior.tobytes()
        path=P/gear/f'frames/land-swim-west/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path);bank.append(im)
        checks.append(dict(gear=gear,index=i,priorCompletePoseExact=0<i<6,currentConfiguredIdleExact=i==0,newSwimEndpointExact=i==6,pivotUnchanged=True,physicalScaleUnchanged=True))
    m['name']='Bill West current idle entry with calibrated swim endpoint';m['frameWidth']=352;m['status']='source_candidate_unselected'
    m['states'][0]['provenance']='Five V12 interiors exact; first context exact current configured idle0 padded68/52, also exitV13 final; last context exact calibrated swimV6 Extend0. H148/p160224 unchanged. Mixed interior scale/grade/articulation candidate, not native admission.'
    (P/gear/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
    durations=m['states'][0]['frameDurationsMs'];assert durations==[60,70,80,60,80,90,60]
    bank[0].save(P/gear/'source-entry.png',save_all=True,append_images=bank[1:],duration=durations,loop=1,disposal=0,blend=0)
    with Image.open(P/gear/'source-entry.png') as ap:
        assert ap.n_frames==7 and ap.info['loop']==1
        for i,im in enumerate(bank):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==durations[i]
    banks[gear]=bank
board=Image.new('RGB',(2464,720),'#182932');d=ImageDraw.Draw(board)
names=['Current idle','Arm ready','Crouch','Push off','Levelling','Near prone','New swim context']
for row,gear in enumerate(['bare','helmet']):
    for i,im in enumerate(banks[gear]):
        board.paste(im,(i*352,row*360+25),im);d.text((i*352+4,row*360+4),gear+' / '+names[i],fill='white')
board.save(P/'paired-entry-review.png')
join=Image.new('RGB',(1408,720),'#182932');d=ImageDraw.Draw(join)
for row,gear in enumerate(['bare','helmet']):
    prior=Image.open(V/gear/'frames/land-swim-west/006.png').convert('RGBA')
    sweep=Image.open(SW/gear/'frames/swim-west/001.png').convert('RGBA')
    for col,(name,im) in enumerate([('Near-prone V12',banks[gear][5]),('Old larger endpoint',prior),('New calibrated Extend0',banks[gear][6]),('Next swim sweep',sweep)]):
        join.paste(im,(col*352,row*360+25),im);d.text((col*352+4,row*360+4),gear+' / '+name,fill='white')
join.save(P/'endpoint-comparison.png')
assert before=={f.relative_to(R).as_posix():sha(f) for f in inputs}
report=dict(inputSHA256=before,frozenInputsStable=len(before),checks=checks,unchangedInteriorPosesExact=10,newEndpointsExactSwimV6=2,currentConfiguredIdleEndpointsExact=2,decodedAPNGFramesExact=14,canvas=[352,320],pivot=[160,224],standingHeight=148,totalMs=500,APNGLoop=1,normalSelected=False,nativeAcceptance=False,visualAcceptance='Pending entry materials/body chronology/contact and full moving joins. Independent exit untouched.')
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>Bill west entry - new swim endpoint</title><style>body{background:#182932;color:#eee;font:18px sans-serif;margin:24px}section{display:flex;gap:20px}canvas{background:#14242e;max-width:45vw}img{width:100%;max-width:1600px;display:block;margin:20px 0}button{font:inherit;margin:12px 6px}a{color:#9ad7dc}</style><h1>Bill west - entry to the new swimmer</h1><p>Both endpoints now match the current idle and calibrated swim loop. Five older interior poses remain for scale, grade and motion repair; gameplay review is pending.</p><section><div>Bare<br><canvas id="bare" width="352" height="320"></canvas></div><div>Helmet<br><canvas id="helmet" width="352" height="320"></canvas></div></section><select id="speed" aria-label="Playback speed"><option value="1">Normal speed</option><option value=".25">Quarter speed</option></select><button id="play">Play entry</button><button id="prev">Previous pose</button><button id="next">Next pose</button><span id="status"></span><p><a href="../bill-swim-west-calibrated-v6/">Review the matte swim loop</a></p><h2>Entry sequence</h2><img src="paired-entry-review.png"><h2>Previous and new endpoint</h2><img src="endpoint-comparison.png"><script>const names=['Idle','Ready','Crouch','Push off','Levelling','Near prone','Swimming'],starts=[0,60,130,210,270,350,440],banks={},ctx={};let phase=0,time=0,playing=false,last=0;function draw(){for(const g of ['bare','helmet']){ctx[g].clearRect(0,0,352,320);ctx[g].drawImage(banks[g][phase],0,0)}document.querySelector('#status').textContent=names[phase]+' / pose '+(phase+1)+' of 7'}Promise.all(['bare','helmet'].map(async g=>{ctx[g]=document.querySelector('#'+g).getContext('2d');banks[g]=await Promise.all(names.map((_,i)=>new Promise(resolve=>{const im=new Image;im.onload=()=>resolve(im);im.src=g+'/frames/land-swim-west/'+String(i).padStart(3,'0')+'.png'})))})).then(draw);document.querySelector('#play').onclick=()=>{if(!playing){time=0;phase=0;draw()}playing=!playing;last=performance.now();document.querySelector('#play').textContent=playing?'Pause':'Play entry'};function step(delta){playing=false;document.querySelector('#play').textContent='Play entry';phase=Math.max(0,Math.min(6,phase+delta));time=starts[phase];draw()}document.querySelector('#next').onclick=()=>step(1);document.querySelector('#prev').onclick=()=>step(-1);function tick(now){if(playing){time=Math.min(500,time+(now-last)*Number(document.querySelector("#speed").value));phase=starts.filter(x=>x<=time).length-1;draw();if(time===500){playing=false;document.querySelector('#play').textContent='Play entry'}}last=now;requestAnimationFrame(tick)}requestAnimationFrame(tick);</script>'''
(P/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(before),preservedInteriorPoses=10,exactSwimEndpoints=2,exactCurrentIdleEndpoints=2,APNGFrames=14,ms=500)))
