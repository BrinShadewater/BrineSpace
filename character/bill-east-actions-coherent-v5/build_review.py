"""Build a review with playback and individual frame controls."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    tracks = []
    for root,label in [(HERE/'review-before-shoulder-fit','v5 · before shoulder fit'),(HERE,'v5 · shoulder fit + darker shell')]:
        data = json.loads((root/'manifest.json').read_text())
        for state in data['states']:
            tracks.append({'state':state['id'],'label':label,'files':['../'+(root/f).relative_to(ROOT).as_posix() for f in state['frameFiles']],'durations':state['frameDurationsMs']})
    tracks.sort(key=lambda t: (['interact-east','kneel-east','repair-east','stand-east'].index(t['state']),t['label']))
    html = '''<!doctype html><html><head><meta charset="utf-8"><title>Bill east actions v5</title><style>
body{background:#152027;color:#e6eff1;font:16px system-ui;margin:20px}p{max-width:85ch;color:#bacecf}button,select{font:inherit;background:#29404a;color:white;border:1px solid #64828b;padding:6px}.grid{display:grid;grid-template-columns:repeat(2,minmax(270px,1fr));max-width:980px;gap:12px}.card{background:#22343e;text-align:center;padding:12px}canvas{display:block;margin:auto}.controls{position:sticky;top:0;background:#152027;padding:12px;z-index:1}small{display:block;color:#bfd0d3}</style></head><body>
<h1>Bill — east interaction shoulder and helmet fit</h1><p>The approved helmet follows the authored head position, while the moving shoulder now stays entirely from the action pose. The graphite shell is 8% darker; staged idle endpoints use the same shell grade. Face, visor, bright silver trim and lamp are retained. Body motion below the collar is unchanged. No runtime installation.</p>
<div class="controls"><button id="play">Pause</button> <button id="prev">Previous frame</button> <button id="next">Next frame</button> <label>Height <select id="size"><option>155</option><option>82</option><option>54</option><option>27</option></select></label> <span id="status">Loading…</span></div><div class="grid" id="grid"></div>
<script>const tracks=TRACKS;let playing=true,time=0,last=performance.now(),manual=0;const status=document.querySelector('#status');
for(const t of tracks){const el=document.createElement('div');el.className='card';el.innerHTML='<strong>'+t.state+' · '+t.label+'</strong><canvas width="368" height="368"></canvas><small></small>';document.querySelector('#grid').append(el);t.canvas=el.querySelector('canvas');t.info=el.querySelector('small')}
function pause(){playing=false;document.querySelector('#play').textContent='Play'}document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play'};document.querySelector('#prev').onclick=()=>{pause();manual=(manual+5)%6};document.querySelector('#next').onclick=()=>{pause();manual=(manual+1)%6};
Promise.all(tracks.map(async t=>{t.images=await Promise.all(t.files.map(f=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=reject;im.src=f+'?v=coherent-v5-shoulder-fit-v2'})));t.total=t.durations.reduce((a,b)=>a+b,0)})).then(()=>{status.textContent='Loaded';function draw(now){if(playing)time+=now-last;last=now;for(const t of tracks){let i=manual;if(playing){let v=time%t.total;i=0;while(i<5&&v>=t.durations[i])v-=t.durations[i++]};const c=t.canvas.getContext('2d');c.clearRect(0,0,368,368);const scale=2*Number(document.querySelector('#size').value)/155;c.drawImage(t.images[i],184-92*scale,360-175*scale,184*scale,184*scale);t.info.textContent='Frame '+i+' / 5'}requestAnimationFrame(draw)}requestAnimationFrame(draw)}).catch(e=>status.textContent='Load failed '+e);</script></body></html>'''
    (HERE/'index.html').write_text(html.replace('TRACKS',json.dumps(tracks)),encoding='utf-8')
    print('Review: 8 tracks / 48 frame references; playback and frame stepping')


if __name__ == '__main__':
    main()





