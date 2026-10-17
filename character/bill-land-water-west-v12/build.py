"""Reconcile a staged entry endpoint with the actual new swim authority."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent
V=R/'bill-land-water-west-v11';SW=R/'bill-swim-west-master-v7'
inputs=[Path(__file__)]+[V/g/'manifest.json' for g in ['bare','helmet']]+[V/g/f'frames/land-swim-west/{i:03}.png' for g in ['bare','helmet'] for i in range(7)]+[SW/g/'manifest.json' for g in ['bare','helmet']]+[SW/g/'frames/swim-west/000.png' for g in ['bare','helmet']]+[SW/g/'frames/swim-west/001.png' for g in ['bare','helmet']]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
before={f.relative_to(R).as_posix():sha(f) for f in inputs}
banks={};checks=[]
for gear in ['bare','helmet']:
    m=json.loads((V/gear/'manifest.json').read_text(encoding='utf-8'));bank=[]
    for i in range(7):
        if i==6:
            im=Image.open(SW/gear/'frames/swim-west/000.png').convert('RGBA')
            assert im.size==(352,320)
        else:
            prior=Image.open(V/gear/f'frames/land-swim-west/{i:03}.png').convert('RGBA');assert prior.size==(320,320)
            im=Image.new('RGBA',(352,320));im.alpha_composite(prior,(0,0))
            assert im.crop((0,0,320,320)).tobytes()==prior.tobytes()
            assert not np.any(np.array(im)[:,320:,3])
        path=P/gear/f'frames/land-swim-west/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path);bank.append(im)
        checks.append(dict(gear=gear,index=i,priorBodyExactAfterCanvasPadding=i<6,newSwimEndpointExact=i==6,pivotUnchanged=True,physicalScaleUnchanged=True))
    m['name']='Bill West original-master entry with matte swim endpoint';m['frameWidth']=352;m['status']='source_candidate_unselected'
    m['states'][0]['provenance']='First six V11 poses exact after transparent right-canvas padding; final context exact V7 matte swim0. Same physical H148/p160224, no scale or anatomical changes. Candidate only.'
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
    for col,(name,im) in enumerate([('Near-prone V11',banks[gear][5]),('Old compact endpoint',prior),('New exact matte swim0',banks[gear][6]),('Next swim sweep',sweep)]):
        join.paste(im,(col*352,row*360+25),im);d.text((col*352+4,row*360+4),gear+' / '+name,fill='white')
join.save(P/'endpoint-comparison.png')
assert before=={f.relative_to(R).as_posix():sha(f) for f in inputs}
report=dict(inputSHA256=before,frozenInputsStable=len(before),checks=checks,unchangedDecodedPosesAfterPadding=12,newEndpointsExactSwimV7=2,decodedAPNGFramesExact=14,canvas=[352,320],pivot=[160,224],standingHeight=148,totalMs=500,APNGLoop=1,normalSelected=False,nativeAcceptance=False,visualAcceptance='Pending entry materials/body chronology/contact and full moving joins. Independent exit untouched.')
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>Bill west entry - new swim endpoint</title><style>body{background:#182932;color:#eee;font:18px sans-serif;margin:24px}section{display:flex;gap:20px}canvas{background:#14242e;max-width:45vw}img{width:100%;max-width:1600px;display:block;margin:20px 0}button{font:inherit;margin:12px 6px}a{color:#9ad7dc}</style><h1>Bill west - entry to the new swimmer</h1><p>The first six poses are preserved. The last pose now matches the new matte swim loop. Full motion and gameplay review remain pending.</p><section><div>Bare<br><canvas id="bare" width="352" height="320"></canvas></div><div>Helmet<br><canvas id="helmet" width="352" height="320"></canvas></div></section><button id="play">Play entry</button><button id="prev">Previous pose</button><button id="next">Next pose</button><span id="status"></span><p><a href="../bill-swim-west-master-v7/">Review the matte swim loop</a></p><h2>Entry sequence</h2><img src="paired-entry-review.png"><h2>Previous and new endpoint</h2><img src="endpoint-comparison.png"><script>const names=['Idle','Ready','Crouch','Push off','Levelling','Near prone','Swimming'],starts=[0,60,130,210,270,350,440],banks={},ctx={};let phase=0,time=0,playing=false,last=0;function draw(){for(const g of ['bare','helmet']){ctx[g].clearRect(0,0,352,320);ctx[g].drawImage(banks[g][phase],0,0)}document.querySelector('#status').textContent=names[phase]+' / pose '+(phase+1)+' of 7'}Promise.all(['bare','helmet'].map(async g=>{ctx[g]=document.querySelector('#'+g).getContext('2d');banks[g]=await Promise.all(names.map((_,i)=>new Promise(resolve=>{const im=new Image;im.onload=()=>resolve(im);im.src=g+'/frames/land-swim-west/'+String(i).padStart(3,'0')+'.png'})))})).then(draw);document.querySelector('#play').onclick=()=>{if(!playing){time=0;phase=0;draw()}playing=!playing;last=performance.now();document.querySelector('#play').textContent=playing?'Pause':'Play entry'};function step(delta){playing=false;document.querySelector('#play').textContent='Play entry';phase=Math.max(0,Math.min(6,phase+delta));time=starts[phase];draw()}document.querySelector('#next').onclick=()=>step(1);document.querySelector('#prev').onclick=()=>step(-1);function tick(now){if(playing){time=Math.min(500,time+now-last);phase=starts.filter(x=>x<=time).length-1;draw();if(time===500){playing=false;document.querySelector('#play').textContent='Play entry'}}last=now;requestAnimationFrame(tick)}requestAnimationFrame(tick);</script>'''
(P/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(before),preservedPoses=12,exactNewEndpoints=2,APNGFrames=14,ms=500)))
