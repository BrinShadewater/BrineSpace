from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];src=p/'finite-bridge-v36';out=p/'motion-review-v37';out.mkdir(exist_ok=True)
frames=out/'frames';frames.mkdir(exist_ok=True)
clock=[]
with Image.open(src/'paired-start-and-walk.apng') as im:
    assert im.n_frames==52
    for i in range(im.n_frames):
        im.seek(i);im.convert('RGBA').save(frames/('%03d.png'%i));clock.append(im.info['duration'])
assert sum(clock)==1890
html='''<!doctype html><html><head><meta charset="utf-8"><title>James carrying motion review</title><style>
body{margin:24px;background:#202a2e;color:#e0e5e7;font:16px system-ui;max-width:1080px}h1{font-size:22px}button,select{font:inherit;padding:8px;margin:4px;border:1px solid #66767c;border-radius:5px;background:#344348;color:white}canvas{display:block;background:#303b3f;width:768px;height:423px;image-rendering:pixelated;margin:16px 0}input{width:768px}small{color:#afbdc2}.gallery{display:flex;gap:6px}.gallery img{width:256px;height:141px;image-rendering:pixelated}
</style></head><body><h1>James carrying motion review</h1><p>Staged candidate · bare and helmet · fixed foot position</p>
<select id="clip"><option value="journey">Start + one walking cycle</option><option value="prepare">Preparation</option><option value="return">Return study</option></select>
<button id="play">Play</button><button id="restart">Restart</button><button id="next">Next frame</button><select id="speed"><option value="1">Normal speed</option><option value="0.25">Quarter speed</option></select>
<canvas id="view" width="512" height="282"></canvas><input id="scrub" type="range" min="0" max="51" value="0"><p id="status">Loading…</p><small>Four transition poses. The walking cycle uses all49 original chronological frames. Return is a reversed preparation study, not a case-unloading animation.</small>
<h2>Transition poses</h2><div class="gallery"><img src="frames/000.png"><img src="frames/001.png"><img src="frames/002.png"><img src="frames/003.png"></div>
<script>
const durations=CLOCK;const images=Array.from({length:52},(_,i)=>{let im=new Image();im.src='frames/'+String(i).padStart(3,'0')+'.png';return im});
let playing=false,slot=0,elapsed=0,last=performance.now(),loops=0;const view=document.querySelector('#view'),ctx=view.getContext('2d'),status=document.querySelector('#status'),scrub=document.querySelector('#scrub');ctx.imageSmoothingEnabled=false;
function sequence(){const c=document.querySelector('#clip').value;return c==='prepare'?{ids:[0,1,2,3],clock:[70,70,70,40]}:c==='return'?{ids:[3,2,1,0],clock:[40,70,70,70]}:{ids:Array.from({length:52},(_,i)=>i),clock:durations}}
function draw(){const seq=sequence(),im=images[seq.ids[slot]];if(im.complete&&im.naturalWidth){ctx.clearRect(0,0,512,282);ctx.drawImage(im,0,0)}scrub.max=seq.ids.length-1;scrub.value=slot;status.textContent=(playing?'Playing':'Paused')+' · frame '+(slot+1)+' / '+seq.ids.length+' · loops '+loops+' · '+Math.round(seq.clock.slice(0,slot).reduce((a,b)=>a+b,0))+' ms';document.querySelector('#play').textContent=playing?'Pause':'Play'}
function reset(){slot=0;elapsed=0;loops=0;last=performance.now();draw()}
document.querySelector('#play').onclick=()=>{playing=!playing;last=performance.now();draw()};document.querySelector('#restart').onclick=reset;document.querySelector('#next').onclick=()=>{playing=false;slot=(slot+1)%sequence().ids.length;elapsed=0;draw()};document.querySelector('#clip').onchange=()=>{playing=false;reset()};scrub.oninput=()=>{playing=false;slot=Number(scrub.value);elapsed=0;draw()};
function tick(now){const delta=now-last;last=now;if(playing){elapsed+=delta*Number(document.querySelector('#speed').value);const seq=sequence();while(elapsed>=seq.clock[slot]){elapsed-=seq.clock[slot];slot++;if(slot===seq.ids.length){slot=0;loops++}}}draw();requestAnimationFrame(tick)}
Promise.all(images.map(im=>im.decode())).then(()=>{draw();requestAnimationFrame(tick)}).catch(e=>status.textContent='Failed to load preview: '+e.message);
</script></body></html>'''.replace('CLOCK',json.dumps(clock))
(out/'review.html').write_text(html,encoding='utf-8')
sources=[src/'paired-start-and-walk.apng',src/'inputs.json',Path(__file__)]+list(frames.glob('*.png'))+[out/'review.html']
(out/'inputs.json').write_text(json.dumps(dict(sourceSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sources},journeyFrames=52,durationMs=1890,normalChanged=False,scope='Browser review media from exact decoded paired source frames; no invented tween or new artwork. Browser/native/visual review pending.'),indent=2)+'\n')
print('V37 local motion-review page and52 exact paired frames prepared.')
