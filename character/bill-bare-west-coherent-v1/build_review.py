"""Review retained versus new west whole figures at equivalent foot pivots."""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
KEYS = ['interact-west','kneel-west','repair-west','stand-west']


def main():
    tracks = []
    for source,label in [(HERE/'review-before-hair','Before hair correction'),(HERE,'Brown hair west')]:
        pack = json.loads((source/'manifest.json').read_text())
        for state in pack['states']:
            if state['id'] not in KEYS:
                continue
            paths = ['../'+(source/f).resolve().relative_to(ROOT.resolve()).as_posix() for f in state['frameFiles']]
            tracks.append({'key':state['id'],'label':label,'files':paths,'durations':state['frameDurationsMs'],'width':pack['frameWidth'],'height':pack['frameHeight'],'pivot':pack['pivot']})
    tracks.sort(key=lambda t:(KEYS.index(t['key']),t['label']=='Brown hair west'))
    html = '''<!doctype html><html><head><meta charset="utf-8"><title>Bill west action review</title><style>
body{background:#152027;color:#e6eff1;font:16px system-ui;margin:20px}p{max-width:85ch;color:#bdd0d2}button,select{font:inherit;background:#29404a;color:white;border:1px solid #64828b;padding:6px}.grid{display:grid;grid-template-columns:repeat(2,minmax(270px,1fr));max-width:980px;gap:12px}.card strong{display:block;min-height:48px}.card{background:#22343e;text-align:center;padding:12px}canvas{display:block;margin:auto}.controls{position:sticky;top:0;background:#152027;padding:12px;z-index:1}small{display:block;color:#bfd0d3}</style></head><body>
<h1>Bill — bare west hair consistency</h1><p>A restrained dark-brown lift on the crown and rear hair matches the selected idle more closely. Face, body, silhouettes, timing and exact breathing-idle endpoints are preserved. Compare the prior and corrected loops or pause and step through each pose. Bare west actions are accepted and installed; this page retains the hair comparison.</p>
<div class="controls"><button id="play">Pause</button> <button id="prev">Previous frame</button> <button id="next">Next frame</button> <label>Height <select id="size"><option>155</option><option>82</option><option>54</option><option>27</option></select></label> <span id="status">Loadingâ€¦</span></div><div class="grid" id="grid"></div>
<script>const tracks=TRACKS;let playing=true,time=0,last=performance.now(),manual=0;const status=document.querySelector('#status');
for(const t of tracks){const el=document.createElement('div');el.className='card';el.innerHTML='<strong>'+t.key+' · '+t.label+'</strong><canvas width="368" height="368"></canvas><small></small>';document.querySelector('#grid').append(el);t.canvas=el.querySelector('canvas');t.info=el.querySelector('small')}
function pause(){playing=false;document.querySelector('#play').textContent='Play'}document.querySelector('#play').onclick=()=>{playing=!playing;if(!playing)manual=tracks[1].lastIndex||0;document.querySelector('#play').textContent=playing?'Pause':'Play'};document.querySelector('#prev').onclick=()=>{pause();manual=(manual+5)%6};document.querySelector('#next').onclick=()=>{pause();manual=(manual+1)%6};
Promise.all(tracks.map(async t=>{t.images=await Promise.all(t.files.map(f=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f+'?v=bill-bare-west-hair-v2'})));t.total=t.durations.reduce((a,b)=>a+b,0)})).then(()=>{status.textContent='All eight tracks loaded';function draw(now){if(playing)time+=now-last;last=now;for(const t of tracks){let i=manual;if(playing){let v=time%t.total;i=0;while(i<5&&v>=t.durations[i])v-=t.durations[i++]};t.lastIndex=i;const c=t.canvas.getContext('2d');c.clearRect(0,0,368,368);const scale=2*Number(document.querySelector('#size').value)/152;c.drawImage(t.images[i],184-t.pivot[0]*scale,350-t.pivot[1]*scale,t.width*scale,t.height*scale);t.info.textContent='Frame '+i+' / 5'}requestAnimationFrame(draw)}requestAnimationFrame(draw)}).catch(e=>status.textContent='Load failed '+e);</script></body></html>'''
    (HERE/'index.html').write_text(html.replace('TRACKS',json.dumps(tracks)),encoding='utf-8')
    print('Bare west review: eight tracks, 48 valid references')


if __name__=='__main__':
    main()


