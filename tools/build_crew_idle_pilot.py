"""Extract a full idle trial at fixed registration; never installs runtime art."""
from pathlib import Path
import argparse
import json
import numpy as np
from PIL import Image, ImageDraw
import imageio.v2 as iio
from scipy import ndimage

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True)
args = parser.parse_args()
p = args.source

def mask(a):
    rgb = np.asarray(a, dtype=float)
    green = (rgb[:, :, 1] > rgb[:, :, 0] * 1.3) & (rgb[:, :, 1] > rgb[:, :, 2] * 1.3) & (rgb[:, :, 1] > 90)
    labels, _ = ndimage.label(~green)
    counts = np.bincount(labels.ravel())
    counts[0] = 0
    return labels == counts.argmax()

ref = np.array(Image.open(p / 'master-input.png').convert('RGB'))
ys, xs = np.where(mask(ref))
scale = 148 / (ys.max() - ys.min() + 1)
offset = (92 - round((xs.min() + xs.max()) * .5 * scale), 172 - round((ys.max() + 1) * scale))
reader = iio.get_reader(p / 'source.mp4')
fps = reader.get_meta_data()['fps']
dest = p / 'frames'
dest.mkdir(exist_ok=True)
frames = []
bounds = []
for n, a in enumerate(reader):
    alpha = mask(a)
    im = Image.fromarray(np.dstack([a, alpha.astype('uint8') * 255]))
    out = Image.new('RGBA', (184, 184))
    out.alpha_composite(im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS), offset)
    out.save(dest / f'{n:03}.png')
    frames.append(out)
    bounds.append(out.getbbox())
reader.close()
sheet = Image.new('RGB', (1104, 440), '#303b40')
draw = ImageDraw.Draw(sheet)
for j, n in enumerate(np.linspace(0, len(frames) - 1, 12).astype(int)):
    sheet.paste(frames[n], (j % 6 * 184, j // 6 * 220 + 20), frames[n])
    draw.text((j % 6 * 184 + 4, j // 6 * 220 + 3), str(n), fill='white')
sheet.save(p / 'contact.png')
(p / 'checks.json').write_text(json.dumps({'frames': len(frames), 'fps': fps, 'fixedScale': scale, 'offset': offset, 'bounds': bounds, 'additionalGrade': False, 'loopSelected': False, 'installed': False}, indent=2))
html = '''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bill breathing idle pilot</title><style>body{background:#253137;color:#eee;font:17px system-ui;max-width:1150px;margin:24px auto;padding:12px}canvas{max-width:100%;background:#303b40}video,img{max-width:100%}button{padding:10px}</style>
<h1>Bill — subtle breathing idle</h1><p>Left: locked idle. Right: new full source trial. Preview only; installed animations remain locked. Sizes: 148 / 82 / 54 / 27 px.</p>
<button id="pause">Pause</button> <span id="status">Loading frames…</span><br><canvas width="1080" height="235"></canvas>
<p>This is the full clip, not a selected seamless loop. Check breathing, face, matte suit and planted feet.</p><video src="source.mp4" controls loop></video><img src="contact.png">
<script>const count=COUNT,fps=FPS;const frames=[],ref=new Image();ref.src='locked-reference.png';
const canvas=document.querySelector('canvas'),ctx=canvas.getContext('2d');let paused=false,elapsed=0,last=performance.now();
document.querySelector('button').onclick=()=>{paused=!paused;document.querySelector('button').textContent=paused?'Play':'Pause'};
Promise.all([new Promise(r=>ref.onload=r),...Array.from({length:count},(_,i)=>new Promise((resolve,reject)=>{let im=new Image();frames.push(im);im.onload=resolve;im.onerror=reject;im.src=`frames/${String(i).padStart(3,'0')}.png`}))]).then(()=>{function tick(now){if(!paused)elapsed+=now-last;last=now;const index=Math.floor(elapsed*fps/1000)%count;ctx.clearRect(0,0,1080,235);let x=10;for(const h of [148,82,54,27]){const s=184*h/148;ctx.fillStyle='#eee';ctx.fillText(`${h}px — locked / pilot`,x,20);ctx.drawImage(ref,x,35,s,s);ctx.drawImage(frames[index],x+s+8,35,s,s);x+=s*2+35;}document.querySelector('#status').textContent=`Frame ${index+1}/${count}`;requestAnimationFrame(tick)}requestAnimationFrame(tick)}).catch(()=>document.querySelector('#status').textContent='Frame load failed');</script>'''
(p / 'index.html').write_text(html.replace('COUNT', str(len(frames))).replace('FPS', str(fps)), encoding='utf-8')
print(json.dumps({'frames': len(frames), 'fps': fps, 'fixedScale': scale, 'preview': str(p / 'index.html')}))
