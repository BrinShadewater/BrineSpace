"""Compare complete cargo cycles rather than resetting a held case to the ground."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
tracks=[]
for folder,label in [(HERE/'review-retained','Approved bare west'),(HERE,'Equipped west')]:
    pack=json.loads((folder/'manifest.json').read_text());states={s['id']:s for s in pack['states']}
    files=[];durations=[];phases=[]
    for key in ['pickup-west',*['carry-west']*3,'unload-west']:
        s=states[key]
        files.extend([(folder/p).relative_to(HERE).as_posix() for p in s['frameFiles']]);durations.extend(s['frameDurationsMs']);phases.extend([key]*len(s['frameFiles']))
    files.append(files[-1]);durations.append(700);phases.append('rest')
    tracks.append({'label':label,'files':files,'durations':durations,'phases':phases,'pickupCount':len(states['pickup-west']['frameFiles'])})
html='''<!doctype html><meta charset="utf-8"><title>Bill equipped west cargo</title><style>body{background:#152027;color:#e6eff1;font:16px system-ui;margin:20px}p{max-width:85ch;color:#bdd0d2}button,select{font:inherit;background:#29404a;color:white;padding:6px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,390px));max-width:820px;gap:12px}.card{background:#22343e;padding:12px}canvas{display:block;width:100%;height:auto}.controls{padding:10px}</style><h1>Bill — west cargo</h1><p>Every moving frame uses the actual approved west idle face and helmet, translated and tilted around the neck. Cargo body and case preserved below the fitted neck. Twelve pickup poses; set-down reverses those poses with its own retained timing. Whole alternating carry cycle; fixed anatomy and matte materials. Staged for visual review.</p><div class="controls"><button id="play">Pause</button> <button id="step">Next pickup pose</button> <label>Height <select id="size"><option>155</option><option selected>82</option><option>54</option><option>27</option></select></label> <span id="status">Loading...</span></div><div class="grid" id="grid"></div><script>
const tracks=TRACKS;let time=0,last=performance.now(),playing=true,manual=0;document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play'};document.querySelector('#step').onclick=()=>{playing=false;document.querySelector('#play').textContent='Play';manual=(manual+1)%12};for(const t of tracks){let el=document.createElement('div');el.className='card';el.innerHTML='<strong>'+t.label+'</strong><canvas width="368" height="400"></canvas><small></small>';document.querySelector('#grid').append(el);t.card=el}
Promise.all(tracks.map(async t=>{t.total=t.durations.reduce((a,b)=>a+b,0);t.images=await Promise.all(t.files.map(f=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f+'?v=cargo-v1'})))})).then(()=>{document.querySelector('#status').textContent='Both complete cargo cycles loaded';function draw(now){if(playing)time+=now-last;last=now;for(const t of tracks){let v=time%t.total,i=Math.floor(manual*t.pickupCount/12);if(playing){i=0;while(i<t.images.length-1&&v>=t.durations[i])v-=t.durations[i++]};const c=t.card.querySelector('canvas').getContext('2d'),s=2*Number(document.querySelector('#size').value)/148;c.clearRect(0,0,368,400);c.drawImage(t.images[i],184-128*s,380-224*s,256*s,256*s);t.card.querySelector('small').textContent=t.phases[i]+' · pose '+(i+1)}requestAnimationFrame(draw)}requestAnimationFrame(draw)}).catch(e=>document.querySelector('#status').textContent='Load failed '+e);</script>'''
(HERE/'index.html').write_text(html.replace('TRACKS',json.dumps(tracks)),encoding='utf-8')
pack=json.loads((HERE/'manifest.json').read_text());pickup=pack['states'][0]
out=Image.new('RGB',(850,600));draw=ImageDraw.Draw(out)
for row,(bg,height) in enumerate([((25,38,45),82),((220,225,220),82),((25,38,45),54),((220,225,220),54),((25,38,45),27),((220,225,220),27)]):
    draw.rectangle((0,row*100,850,row*100+99),fill=bg);draw.text((4,row*100+4),str(height)+'px',fill=(145,155,160))
    for col,p in enumerate(pickup['frameFiles']):
        im=Image.open(HERE/p).convert('RGBA');s=height/148;im=im.resize((round(256*s),round(256*s)),Image.Resampling.LANCZOS)
        out.paste(im,(50+col*67-round(128*s),row*100+96-round(224*s)),im)
out.save(HERE/'gameplay-review.png')
print('Cargo review:two complete cycles;12 pickup poses;82/54/27px dark/light samples')
