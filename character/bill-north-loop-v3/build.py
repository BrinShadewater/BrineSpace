"""Select an intact gait from approved direct v2; never regenerates or recolours."""
from pathlib import Path
import bisect
import hashlib
import json
import shutil

import numpy as np
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
SOURCE = P.parent / 'bill-north-direct-v2'
RUNTIME = P.parent / 'crew-runtime-matte-v1/bill'
INDICES = list(range(91, 121))
DURATION = 1500


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_frames(root, state):
    return [Image.open(root / f).convert('RGBA') for f in state['frameFiles']]


out = P / 'frames/walk-north'
out.mkdir(parents=True, exist_ok=True)
hashes = {}
for j, n in enumerate(INDICES):
    src = SOURCE / f'frames/walk-north/{n:03}.png'
    dst = out / f'{j:03}.png'
    shutil.copy2(src, dst)
    assert digest(src) == digest(dst)
    hashes[dst.relative_to(P).as_posix()] = digest(dst)

state = dict(id='walk-north', frameCount=len(INDICES),
             frameFiles=list(hashes), frameDurationsMs=[50]*30,
             sourceFrames=INDICES, loop=True, gaitCycles=1, mirrored=False,
             provenance=dict(source='../bill-north-direct-v2/source.mp4',
                             sourceSha256=digest(SOURCE/'source.mp4'),
                             method='Exact copies of reviewed matte frames; complete alternating stride. No extra colour/geometry processing.',
                             sourceCycleDurationMs=1250, playbackCycleDurationMs=DURATION))
manifest = dict(name='Bill north direct v2 selected loop', status='candidate_not_installed',
                frameWidth=184, frameHeight=184, pivot=[92,172], standingHeight=148,
                textureFilter='linear', precomposed=True,
                strideDistanceCells={'walk-north':69/384}, states=[state])
(P/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
(P/'frame-hashes.json').write_text(json.dumps(hashes, indent=2)+'\n')
frames = read_frames(P, state)
arrays = [np.asarray(f).astype(float) for f in frames]
bounds = [f.getbbox() for f in frames]
def distance(a,b):
    aa=a/255; bb=b/255
    aa=np.concatenate((aa[:,:,:3]*aa[:,:,3:4],aa[:,:,3:4]),axis=2)
    bb=np.concatenate((bb[:,:,:3]*bb[:,:,3:4],bb[:,:,3:4]),axis=2)
    mask=np.maximum(aa[:,:,3],bb[:,:,3])>.05
    return float(np.mean((aa-bb)[mask]**2))
adjacent=[distance(arrays[i],arrays[i+1]) for i in range(29)]
seam=distance(arrays[-1],arrays[0])
report=dict(sourceFrames=INDICES,frameCount=30,durationMs=DURATION,
            allCopiedFramesExact=True,clippedFrames=sum(b[0]<=0 or b[1]<=0 or b[2]>=184 or b[3]>=184 for b in bounds),
            seamForegroundMSE=seam,medianAdjacentForegroundMSE=float(np.median(adjacent)),
            maxAdjacentForegroundMSE=max(adjacent),
            sourceOwnerFeedback='looks good, lets keep going',
            limits=['Pixel seam metrics are supporting evidence, not temporal gait acceptance.',
                    'No runtime change; loop and direction transition review remains pending.'])
checks=json.loads((SOURCE/'checks.json').read_text())
heights=[checks['bounds'][n][3]-checks['bounds'][n][1] for n in INDICES]
medians=np.array([checks['neutralMedians'][n] for n in INDICES])
report.update(processedHeightRange=[min(heights),max(heights)],
              neutralMedianRange=[medians.min(0).tolist(),medians.max(0).tolist()])
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n')

sheet=Image.new('RGB',(184*10,208*3),'#303b40');draw=ImageDraw.Draw(sheet)
for i,im in enumerate(frames):
    x=i%10*184;y=i//10*208;sheet.paste(im,(x,y+20),im)
    draw.text((x+8,y+3),f'{i} / source {INDICES[i]}',fill='white')
sheet.save(P/'contact.png')
review=[]
for i,im in enumerate(frames):
    bg=Image.new('RGB',(552,260),'#303b40');d=ImageDraw.Draw(bg)
    for height,x in [(148,0),(82,225),(54,355),(27,465)]:
        side=round(184*height/148);small=im.resize((side,side),Image.Resampling.BILINEAR)
        bg.paste(small,(x,35),small)
    d.text((8,8),f'Bill north / frame {i} / 1500ms full cycle',fill='white');review.append(bg)
review[0].save(P/'review.gif',save_all=True,append_images=review[1:],duration=50,loop=0)

runtime=json.loads((RUNTIME/'manifest.json').read_text())
tracks=[]
for direction in ['south','east','north','west']:
    s=state if direction=='north' else next(s for s in runtime['states'] if s['id']=='walk-'+direction)
    prefix='' if direction=='north' else '../crew-runtime-matte-v1/bill/'
    tracks.append(dict(label=direction.title()+(' - new loop' if direction=='north' else ' - installed'),
                       files=[prefix+f for f in s['frameFiles']],durations=s['frameDurationsMs']))
old=next(s for s in runtime['states'] if s['id']=='walk-north')
tracks.append(dict(label='North - installed v5',files=['../crew-runtime-matte-v1/bill/'+f for f in old['frameFiles']],durations=old['frameDurationsMs']))
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bill north - selected loop</title><style>body{background:#172226;color:#dbe4df;font:17px system-ui;max-width:1150px;margin:24px auto;padding:16px}canvas{display:block;width:100%;height:auto;background:#303b40}img,video{max-width:100%}button,select,input{font:inherit;padding:6px}a{color:#91d6d1}.controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center}small{color:#b8c6c8}</style><h1>Bill north - selected walk loop</h1><p>Approved direct v2 take, source frames 91-120: 30 original poses, both alternating steps, timed to the existing 1.5-second cycle. Matte colours and geometry are unchanged. Candidate only; runtime still uses the previous north walk.</p><div class="controls"><button id="toggle">Pause</button><label>Speed <select id="speed"><option value="1">Normal</option><option value="0.5">Half</option></select></label><label>Phase <input id="phase" type="range" min="0" max="1499" value="0"></label><span id="status">Loading frames...</span></div><h2>Direction consistency and previous north</h2><p>Rows show 148px inspection height, then the three approximate gameplay sizes: 82 / 54 / 27px. All directions share the same cycle time.</p><canvas id="board" width="1050" height="540"></canvas><h2>Selected loop</h2><img src="review.gif"><h2>Full approved source</h2><video src="../bill-north-direct-v2/source.mp4" controls loop muted playsinline></video><h2>Every selected pose</h2><img src="contact.png"><p><a href="../bill-north-direct-v2/">Full source comparison</a></p><script>const tracks=TRACKS;let loaded=false,playing=true,t=0,last=0;const canvas=document.getElementById('board'),ctx=canvas.getContext('2d'),phase=document.getElementById('phase'),status=document.getElementById('status');Promise.all(tracks.map(async s=>{s.images=await Promise.all(s.files.map(src=>new Promise((resolve,reject)=>{const im=new Image;im.onload=()=>resolve(im);im.onerror=()=>reject(src);im.src=src})));s.total=s.durations.reduce((a,b)=>a+b,0)})).then(()=>{loaded=true;status.textContent='All frames loaded'}).catch(e=>status.textContent='Image failed: '+e);document.getElementById('toggle').onclick=e=>{playing=!playing;e.target.textContent=playing?'Pause':'Play'};phase.oninput=()=>{t=Number(phase.value);playing=false;document.getElementById('toggle').textContent='Play'};function draw(now){if(last&&playing)t=(t+(now-last)*Number(document.getElementById('speed').value))%1500;last=now;if(loaded){ctx.clearRect(0,0,1050,540);ctx.imageSmoothingEnabled=true;tracks.forEach((s,c)=>{let local=t%s.total,i=0;while(i<s.images.length-1&&local>=s.durations[i]){local-=s.durations[i++]}ctx.fillStyle='#dbe4df';ctx.font='14px system-ui';ctx.fillText(s.label,c*210+8,22);[148,82,54,27].forEach((height,row)=>{const side=184*height/148;const y=[38,245,368,457][row];ctx.drawImage(s.images[i],c*210+(210-side)/2,y,side,side)})});phase.value=Math.floor(t)}requestAnimationFrame(draw)}requestAnimationFrame(draw);</script></html>'''
(P/'index.html').write_text(html.replace('TRACKS',json.dumps(tracks)),encoding='utf-8')
print(json.dumps(report))
