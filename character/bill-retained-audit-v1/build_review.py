"""Focused retained-art comparison from actual Godot loader exports."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
HERE=Path(__file__).resolve().parent
tracks=json.loads((HERE/'runtime-tracks.json').read_text())
keys=['idle-east','equip-helmet-east','remove-helmet-east','weld-east','carry-east','pickup-east','swim-east','tread-east','death-ground-east','death-water-east']
selected=sorted([t for t in tracks if t['key'] in keys],key=lambda t:(keys.index(t['key']),t['variant']))
out=Image.new('RGB',(1104,len(selected)*155),(34,48,56));draw=ImageDraw.Draw(out)
for row,t in enumerate(selected):
    draw.text((5,row*155+2),t['variant']+' '+t['key'],fill='white')
    for col in range(6):
        idx=round(col*(len(t['files'])-1)/5)
        im=Image.open(HERE/t['files'][idx]).convert('RGBA')
        scale=0.8;im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
        p=(col*184+92-round(t['pivot'][0]*scale),row*155+145-round(t['pivot'][1]*scale))
        out.paste(im,p,im)
out.save(HERE/'retained-contact-sheet.png')
html='''<!doctype html><meta charset="utf-8"><title>Bill retained animation audit</title><style>body{background:#152027;color:#e6eff1;font:16px system-ui;margin:20px}.grid{display:grid;grid-template-columns:repeat(2,380px);gap:12px}.card{background:#22343e;padding:12px}canvas{display:block}button,select{font:inherit;background:#29404a;color:white;padding:6px}.controls{position:sticky;top:0;background:#152027;padding:10px}</style><h1>Bill — retained animation audit</h1><p>Actual loaded artwork. Accepted east idle is the identity reference. Older equipment handling, cargo, welding and water states remain unchanged in this comparison.</p><div class="controls"><button id="play">Pause</button> <label>Height <select id="size"><option>82</option><option>54</option><option>27</option><option>148</option></select></label><span id="status">Loading</span></div><div class="grid" id="grid"></div><script>
const tracks=TRACKS;let time=0,last=performance.now(),playing=true;document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play'};
for(const t of tracks){let el=document.createElement('div');el.className='card';el.innerHTML='<strong>'+t.key+' · '+t.variant+'</strong><canvas width="368" height="245"></canvas>';document.querySelector('#grid').append(el);t.canvas=el.querySelector('canvas')}
Promise.all(tracks.map(async t=>{t.images=await Promise.all(t.files.map(f=>new Promise((resolve,reject)=>{let im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f})));t.total=t.durations.reduce((a,b)=>a+b,0)})).then(()=>{document.querySelector('#status').textContent='All retained comparison tracks loaded';function draw(now){if(playing)time+=now-last;last=now;for(const t of tracks){let v=time%t.total,i=0;while(i<t.images.length-1&&v>=t.durations[i])v-=t.durations[i++];const c=t.canvas.getContext('2d'),s=2*Number(document.querySelector('#size').value)/148;c.clearRect(0,0,368,245);c.drawImage(t.images[i],184-t.pivot[0]*s,225-t.pivot[1]*s,t.width*s,t.height*s)}requestAnimationFrame(draw)}requestAnimationFrame(draw)});</script>'''
(HERE/'index.html').write_text(html.replace('TRACKS',json.dumps(selected)),encoding='utf-8')
print('Focused comparison:',len(selected),'tracks; full runtime inventory:',len(tracks))
