from pathlib import Path
import json
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
tracks=[]
for folder,label in [(HERE/'review-retained','Retained'),(HERE,'New')]:
    pack=json.loads((folder/'manifest.json').read_text())
    for state in pack['states']:
        tracks.append({'key':state['id'],'label':label,'files':[(folder/f).relative_to(HERE).as_posix() for f in state['frameFiles']],'durations':state['frameDurationsMs'],'pivot':pack['pivot'],'width':pack['frameWidth'],'height':pack['frameHeight']})
tracks.sort(key=lambda t:(t['key']!='equip-helmet-east',t['label']=='New'))
html='''<!doctype html><meta charset="utf-8"><title>Bill helmet fitting</title><style>body{background:#152027;color:#e6eff1;font:16px system-ui;margin:20px}p{max-width:90ch;color:#bdd0d2}button,select{font:inherit;background:#29404a;color:white;padding:6px}.grid{display:grid;grid-template-columns:repeat(2,390px);gap:12px}.card{background:#22343e;padding:12px}canvas{display:block}.controls{position:sticky;top:0;background:#152027;padding:10px}</style><h1>Bill — helmet fitting and removal</h1><p>Current bare and equipped idle endpoints, whole connected figures, empty carried helmet. Removal reverses the authored fitting poses with its own timing and locker return event. Installed east transition; owner visual review pending.</p><div class="controls"><button id="play">Pause</button> <button id="step">Next frame</button> <label>Height <select id="size"><option>155</option><option>82</option><option>54</option><option>27</option></select></label> <span id="status">Loading...</span></div><div class="grid" id="grid"></div><script>
const tracks=TRACKS;let time=0,last=performance.now(),playing=true,manual=0;document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play'};document.querySelector('#step').onclick=()=>{playing=false;document.querySelector('#play').textContent='Play';manual=(manual+1)%12};for(const t of tracks){let el=document.createElement('div');el.className='card';el.innerHTML='<strong>'+t.key+' · '+t.label+'</strong><canvas width="368" height="400"></canvas><small></small>';document.querySelector('#grid').append(el);t.card=el}
Promise.all(tracks.map(async t=>{t.total=t.durations.reduce((a,b)=>a+b,0);t.images=await Promise.all(t.files.map(f=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f+'?v=scale-v2'})))})).then(()=>{document.querySelector('#status').textContent='All four tracks loaded';function draw(now){if(playing)time+=now-last;last=now;for(const t of tracks){let v=time%t.total,i=manual;if(playing){i=0;while(i<11&&v>=t.durations[i])v-=t.durations[i++]};const c=t.card.querySelector('canvas').getContext('2d'),s=2*Number(document.querySelector('#size').value)/148;c.clearRect(0,0,368,400);c.drawImage(t.images[i],184-t.pivot[0]*s,380-t.pivot[1]*s,t.width*s,t.height*s);t.card.querySelector('small').textContent='Frame '+i+' /11'}requestAnimationFrame(draw)}requestAnimationFrame(draw)});</script>'''
(HERE/'index.html').write_text(html.replace('TRACKS',json.dumps(tracks)),encoding='utf-8')
pack=json.loads((HERE/'manifest.json').read_text());out=Image.new('RGB',(850,600));draw=ImageDraw.Draw(out)
for row,(bg,height) in enumerate([((25,38,45),82),((220,225,220),82),((25,38,45),54),((220,225,220),54),((25,38,45),27),((220,225,220),27)]):
    draw.rectangle((0,row*100,850,row*100+99),fill=bg);draw.text((4,row*100+4),str(height)+'px',fill=(145,155,160))
    for col,idx in enumerate([0,1,2,4,5,6,7,8,9,11]):
        im=Image.open(HERE/pack['states'][0]['frameFiles'][idx]).convert('RGBA');s=height/148
        im=im.resize((round(256*s),round(256*s)),Image.Resampling.LANCZOS)
        out.paste(im,(70+col*77-round(128*s),row*100+96-round(224*s)),im)
out.save(HERE/'gameplay-review.png')
print('Helmet fitting comparison:4 tracks,48 references')
