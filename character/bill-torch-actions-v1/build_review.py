"""Render before/after chains and station-scale samples."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
pack=json.loads((HERE/'manifest.json').read_text());data={}
for d in ['east','west','south','north']:
    old=json.loads((HERE.parent/f'bill-torch-{d}-coherent-v1/review-retained/tracks.json').read_text())
    data[d]=[]
    for label in ['Retained','New']:
        chain=[]
        for name in ['torch-draw','weld','weld','weld','torch-stow']:
            key=name+'-'+d
            if label=='New':
                state=next(s for s in pack['states'] if s['id']==key)
                t={'files':state['frameFiles'],'durations':state['frameDurationsMs'],'pivot':pack['pivot'],'width':256,'height':256}
            else:
                t=next(t for t in old if t['key']==key)
                t=dict(t,files=['../bill-torch-'+d+'-coherent-v1/review-retained/'+f for f in t['files']])
            chain.extend([dict(file=f,duration=ms,pivot=t['pivot'],width=t['width'],height=t['height'],key=key) for f,ms in zip(t['files'],t['durations'])])
        data[d].append({'label':label,'frames':chain})
html='''<!doctype html><meta charset="utf-8"><title>Bill new blowtorch actions</title><style>body{background:#152027;color:#e6eff1;font:16px system-ui;margin:20px}p{max-width:88ch;color:#bdd0d2}.grid{display:grid;grid-template-columns:repeat(2,390px);gap:12px}.card{background:#22343e;padding:12px}canvas{display:block}button,select{font:inherit;background:#29404a;color:white;padding:6px}.controls{padding:10px}</style><h1>Bill — new blowtorch actions</h1><p>Independent directional whole figures match the accepted idle. Draw torch → weld three cycles → stow torch. New artwork is installed for construction and dry repairs. North/south torches now aim along the figure facing; visual review pending. Compare body, hair, shoulders and flame at gameplay sizes.</p><div class="controls"><label>Direction <select id="direction"><option>east</option><option>west</option><option>south</option><option>north</option></select></label> <label>Height <select id="size"><option>155</option><option>82</option><option>54</option><option>27</option></select></label> <button id="play">Pause</button> <button id="step">Next frame</button><span id="status">Loading...</span></div><div class="grid"><div class="card"><strong>Retained blowtorch</strong><canvas width="368" height="368"></canvas><small></small></div><div class="card"><strong>New blowtorch</strong><canvas width="368" height="368"></canvas><small></small></div></div><script>
const data=DATA;let playing=true,time=0,last=performance.now(),manual=0;document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play'};document.querySelector('#step').onclick=()=>{playing=false;document.querySelector('#play').textContent='Play';manual=(manual+1)%30};document.querySelector('#direction').onchange=()=>{time=0;manual=0};
Promise.all(Object.values(data).flat().map(async t=>{t.total=t.frames.reduce((a,f)=>a+f.duration,0);await Promise.all(t.frames.map(f=>new Promise((resolve,reject)=>{f.image=new Image;f.image.onload=resolve;f.image.onerror=reject;f.image.src=f.file+'?v=axial-v2'})))})).then(()=>{document.querySelector('#status').textContent='All four directional chains loaded';function draw(now){if(playing)time+=now-last;last=now;data[document.querySelector('#direction').value].forEach((t,n)=>{let v=time%t.total,i=manual;if(playing){i=0;while(i<t.frames.length-1&&v>=t.frames[i].duration)v-=t.frames[i++].duration}const f=t.frames[i],card=document.querySelectorAll('.card')[n],c=card.querySelector('canvas').getContext('2d'),s=2*Number(document.querySelector('#size').value)/148;c.clearRect(0,0,368,368);c.drawImage(f.image,184-f.pivot[0]*s,350-f.pivot[1]*s,f.width*s,f.height*s);card.querySelector('small').textContent=f.key+' · frame '+(i%6)});requestAnimationFrame(draw)}requestAnimationFrame(draw)}).catch(e=>document.querySelector('#status').textContent='Load failed');</script>'''
(HERE/'index.html').write_text(html.replace('DATA',json.dumps(data)),encoding='utf-8')
out=Image.new('RGB',(960,600));draw=ImageDraw.Draw(out)
for row,(bg,h) in enumerate([((25,38,45),82),((220,225,220),82),((25,38,45),54),((220,225,220),54),((25,38,45),27),((220,225,220),27)]):
    draw.rectangle((0,row*100,960,row*100+99),fill=bg);draw.text((4,row*100+4),str(h)+'px',fill=(145,155,160))
    for col,d in enumerate(data):
        for n,index in enumerate([2,8,26]):
            f=data[d][1]['frames'][index];im=Image.open(HERE/f['file']).convert('RGBA');s=h/148
            im=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.LANCZOS)
            out.paste(im,(70+col*225+n*66-round(128*s),row*100+96-round(224*s)),im)
out.save(HERE/'gameplay-review.png')
print('Torch review: four before/after chains and82/54/27px samples')
