"""Create a portable, timed review of selected locker clips and their idle joins."""
import base64
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/crew-helmet-fit-v2/review'
data={}
for actor,folder in [('veld','dr-veld-v2'),('branforth','chief-engineer-branforth-v2')]:
    art=ROOT/'character'/folder
    catalog=json.loads((art/'catalog.json').read_text())
    clips={}
    for variant in ['body','equipment']:
        for rel in catalog[variant]:
            path=art/rel
            manifest=json.loads(path.read_text())
            for state in manifest['states']:
                if state['id'] not in ['idle-east','equip-helmet-east','remove-helmet-east']: continue
                clips[variant+'/'+state['id']]={
                    'frames':['data:image/png;base64,'+base64.b64encode((path.parent/f).read_bytes()).decode() for f in state['frameFiles']],
                    'durations':state['frameDurationsMs'],
                    'pivot':manifest['pivot'],
                }
    data[actor]=clips
html='''<!doctype html><meta charset="utf-8"><title>Fitted crew helmets — motion review</title>
<style>body{background:#24343b;color:#e3ddd0;font:16px system-ui;margin:24px}main{display:flex;gap:24px}canvas{background:#33464d;image-rendering:pixelated}button,input{margin:8px}p{max-width:850px}</style>
<h1>Fitted crew helmet sequences</h1><p>Selected game frames. Bare idle → pickup and fitting → helmeted idle → removal and deposit. Large view shows source detail; small view shows 65.28-unit standing height. Scrub to inspect joins.</p>
<button id="play">Pause</button><button id="restart">Restart</button><input id="scrub" type="range" min="0" max="8280" value="0" style="width:480px"><span id="time"></span><main></main>
<script>const data=DATA;const views=[];let elapsed=0,last=performance.now(),running=true;
for(const [actor,clips] of Object.entries(data)){
for(const c of Object.values(clips))c.images=c.frames.map(src=>{let im=new Image();im.src=src;return im});
let section=document.createElement('section');section.innerHTML='<h2>'+actor+'</h2><canvas width="420" height="270"></canvas><p></p>';document.querySelector('main').append(section);
views.push({clips,canvas:section.querySelector('canvas'),label:section.querySelector('p')});}
const schedule=[['body/idle-east',1200],['body/equip-helmet-east',2140],['equipment/idle-east',1800],['body/remove-helmet-east',2140],['body/idle-east',1000]];
const total=schedule.reduce((a,v)=>a+v[1],0);scrub.max=total-1;
play.onclick=()=>{running=!running;play.textContent=running?'Pause':'Play'};
restart.onclick=()=>{elapsed=0};scrub.oninput=()=>{elapsed=Number(scrub.value);running=false;play.textContent='Play'};
function draw(now){if(running)elapsed=(elapsed+now-last)%total;last=now;scrub.value=elapsed;time.textContent=(elapsed/1000).toFixed(2)+'s';
for(const v of views){let t=elapsed,key=schedule[0][0];for(const s of schedule){key=s[0];if(t<s[1])break;t-=s[1]}
const c=v.clips[key];let frame=0;const duration=c.durations.reduce((a,b)=>a+b,0);if(key.endsWith('idle-east'))t%=duration;
while(frame<c.images.length-1&&t>=c.durations[frame])t-=c.durations[frame++];
let ctx=v.canvas.getContext('2d');ctx.clearRect(0,0,420,270);ctx.imageSmoothingEnabled=false;
const p=Array.isArray(c.pivot)?c.pivot:[c.pivot.x,c.pivot.y];for(const [x,y,scale] of [[120,240,1],[325,240,65.28/148]])if(c.images[frame].complete)ctx.drawImage(c.images[frame],x-p[0]*scale,y-p[1]*scale,c.images[frame].width*scale,c.images[frame].height*scale);
v.label.textContent=key+' · frame '+frame;}
requestAnimationFrame(draw)}requestAnimationFrame(draw);</script>'''.replace('DATA',json.dumps(data))
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'motion.html').write_text(html,encoding='utf-8')
print((OUT/'motion.html').relative_to(ROOT))
