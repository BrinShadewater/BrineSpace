from pathlib import Path
from PIL import Image
import json,hashlib
H=Path(__file__).resolve().parent;R=H.parents[1]
originals={'tread':'exec-750c0723-eeb2-47f7-a774-c2fec1aee1f6.png','swim':'exec-37b1ee9e-ece1-40cf-8e32-ad9e4ee8cf5f.png','transition':'exec-b76063c2-7e2e-47bb-b518-0b9631a0c982.png'}
records=[]
for kind,name in originals.items():
    p=H/f'{kind}-source-v1.png';im=Image.open(p)
    refs=['character/veld-video-walk-v1/master-input.png']
    if kind!='tread':refs.append('character/veld-water-west-coherent-v1/tread-source-v1.png')
    if kind=='transition':refs.append('character/veld-water-west-coherent-v1/swim-source-v1.png')
    records.append({'source':p.relative_to(R).as_posix(),'builtinOriginal':'C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/'+name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'dimensions':list(im.size),'mode':im.mode,'promptFile':f'{kind}-source-prompt-v1.txt','references':[{'path':ref,'sha256':hashlib.sha256((R/ref).read_bytes()).hexdigest()} for ref in refs]})
(H/'source-provenance.json').write_text(json.dumps({'method':'built-in imagegen','status':'saved raw sources; staged not installed','records':records},indent=2)+'\n')
for variant in ['bare','helmet']:
    m=json.loads((H/f'{variant}-manifest.json').read_text());states={s['id']:s for s in m['states']}
    chain=[]
    for key in ['tread-west','swim-start-west','swim-west','swim-stop-west']:
        for file in states[key]['frameFiles']:
            im=Image.open(H/file).convert('RGBA');canvas=Image.new('RGBA',im.size,'#202a30');canvas.alpha_composite(im);chain.append(canvas.convert('RGB'))
    chain[0].save(H/f'{variant}-chain-preview.gif',save_all=True,append_images=chain[1:],duration=240,loop=0,disposal=2)
html='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Veld coherent west water</title><style>body{background:#202a30;color:#e1e7eb;font:16px system-ui;margin:24px}p{max-width:80ch}img{max-width:100%;height:auto}.row{display:flex;gap:20px;flex-wrap:wrap}a{color:#8cc6e7}canvas{display:block}button{background:#344b57;color:#fff;border:1px solid #647f8e;padding:6px;border-radius:4px;font:inherit}input{width:200px}</style><h1>Veld — coherent west water family</h1><p>Independent west master-derived tread, swim and lean sources. Near hip scanner retained; far hip cylinders partially hidden. One frozen anatomy scale per atlas from selected west16px face ruler, shared material curves and exact native west helmet. Eight paired states,48frames. Staged; runtime selection remains unchanged. Preview is slowed.</p><h2>Complete paired motion</h2><div class="row"><div>Bare<br><img src="bare-chain-preview.gif" width="256"><img src="bare-chain-preview.gif" width="161"><img src="bare-chain-preview.gif" width="81"></div><div>Helmet<br><img src="helmet-chain-preview.gif" width="256"><img src="helmet-chain-preview.gif" width="161"><img src="helmet-chain-preview.gif" width="81"></div></div><h2>Selected-master anatomy trials</h2><img src="physical-scale-trials-v1.png" alt="Fixed source scales compared to selected148px idle"><h2>All paired loop poses</h2><img src="paired-loop-trials-v1.png" alt="Six tread and swim poses both equipment modes"><h2>Launch and exact reverse return</h2><img src="paired-launch-v1.png" alt="Six launch frames"><p><a href="../veld-water-east-coherent-v1/">East family review</a> · <a href="../veld-water-material-v2/cross-direction-audit-v6.html">Earlier master audit</a></p>'''
tracks={}
for variant in ['bare','helmet']:
    manifest=json.loads((H/f'{variant}-manifest.json').read_text());states={s['id']:s for s in manifest['states']};track=[]
    for key in ['tread-west','swim-start-west','swim-west','swim-stop-west']:
        state=states[key]
        for slot,(file,duration) in enumerate(zip(state['frameFiles'],state['frameDurationsMs'])):track.append({'file':file,'duration':duration,'key':key,'slot':slot})
    tracks[variant]=track
assert [f['duration'] for f in tracks['bare']]==[f['duration'] for f in tracks['helmet']]
begin=html.index('<h2>Complete paired motion</h2>');end=html.index('<h2>Selected-master anatomy trials</h2>')
html=html[:begin]+'''<h2>Synchronized paired motion</h2><button id="play">Pause</button><label>Frame <input id="slot" type="range" min="0" max="23" value="0"></label><span id="status">Loading</span><div class="row"><div>Bare<canvas id="bare" width="256" height="256"></canvas></div><div>Helmet<canvas id="helmet" width="256" height="256"></canvas></div></div><canvas id="station" width="500" height="200"></canvas><p>Original timing at one-third speed. Both equipment modes share the same clock; scrub to compare the exact same pose.</p>'''+html[end:]
html+='<script>const tracks='+json.dumps(tracks)+';'+'''const images={};let playing=true,t=0,last=performance.now();const durations=tracks.bare.map(f=>f.duration),total=durations.reduce((a,b)=>a+b,0),slider=document.getElementById('slot'),button=document.getElementById('play');let loaded=0;for(const variant of ['bare','helmet'])images[variant]=tracks[variant].map(f=>{const im=new Image();im.onload=()=>loaded++;im.src=f.file;return im;});function atTime(){let edge=0;for(let i=0;i<durations.length;i++){edge+=durations[i];if(t<edge)return i;}return 0;}function draw(i){for(const v of ['bare','helmet']){const c=document.getElementById(v).getContext('2d');c.fillStyle='#202a30';c.fillRect(0,0,256,256);c.drawImage(images[v][i],0,0);}const c=document.getElementById('station').getContext('2d');c.fillStyle='#202a30';c.fillRect(0,0,500,200);c.fillStyle='#e1e7eb';c.fillText('93px /47px physical standing scale',5,14);for(const [col,v] of ['bare','helmet'].entries()){for(const [row,h] of [93,47].entries()){const s=h/148;c.drawImage(images[v][i],col*240+120-128*s,55+row*90-128*s,256*s,256*s);}}document.getElementById('status').textContent=tracks.bare[i].key+' /slot '+tracks.bare[i].slot;slider.value=i;}button.onclick=()=>{playing=!playing;button.textContent=playing?'Pause':'Play';};slider.oninput=()=>{playing=false;button.textContent='Play';t=durations.slice(0,Number(slider.value)).reduce((a,b)=>a+b,0);draw(Number(slider.value));};function tick(now){if(loaded===48){if(playing)t=(t+(now-last)/3)%total;draw(atTime());}last=now;requestAnimationFrame(tick);}requestAnimationFrame(tick);</script>'''
(H/'index.html').write_text(html,encoding='utf-8')
print('3 hashed raw sources/reference hashes and paired chain review saved.')
