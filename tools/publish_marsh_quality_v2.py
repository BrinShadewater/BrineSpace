"""Publish the second full-set quality pass and its selected registration fix."""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-quality-pass-v2'
def main():
    before=json.loads((BASE/'baseline-contract.json').read_text())['states']['tread-north']
    after=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
    for label,files in [('before',before['files']),('after',after['tread-north']['files'])]:
        frames=[]
        for f in files:
            im=Image.open(ROOT/f).convert('RGBA');bg=Image.new('RGB',(368,440),'#293b40')
            im=im.resize((368,368),Image.Resampling.NEAREST);bg.paste(im,(0,22),im)
            ImageDraw.Draw(bg).text((8,8),label+' / north tread',fill='white');frames.append(bg)
        frames[0].save(BASE/('tread-north-'+label+'.gif'),save_all=True,append_images=frames[1:],duration=before['durations'],loop=0)
    data={'states':after}
    html='''<!doctype html><meta charset="utf-8"><title>Marsh / second quality pass</title>
<style>body{background:#17252a;color:#dce7e8;font:16px system-ui;max-width:1152px;margin:30px auto;padding:18px}p{line-height:1.6;max-width:1000px}a{color:#b7ddcc}button,select{font:inherit;padding:8px;margin:4px;background:#293b40;color:inherit;border:1px solid #647c80}canvas,img{max-width:100%;image-rendering:pixelated}.pair{display:flex;gap:15px;flex-wrap:wrap}details{margin:12px 0}h1{font-size:28px}</style>
<h1>Marsh / second full-set quality pass</h1>
<p>Reviewed 200 current states and 1,026 frame slots across identity, material colour, perspective, proportions, source density, spatial detail, registration, loop seams and action joins. Marsh retains his clean-shaven blond face, fitted ivory/slate suit, muted sage shoulders, graphite equipment and anatomical right temple implant. White synthetic fluid remains tied to physical injury.</p>
<h2>Installed corrections</h2>
<p><b>Walk / run continuity:</b> Marsh now preserves gait phase when changing speed, removing the forced frame-zero restart. Facing changes, pause and Continue retain phase; teleports and new actions reset it. This is an explicit Marsh-only manifest option.</p>
<p><b>North floating loop:</b> two poses were aligned by their lowest boot despite changing leg bend. Their torso jumped 15px at source size. Registration now keeps a natural 2px head bob while preserving every visible colour, alpha pixel and leg pose. Timing and density stay unchanged.</p>
<div class="pair"><img src="tread-north-before.gif" alt="Previous north tread registration"><img src="tread-north-after.gif" alt="Corrected north tread registration"></div>
<h2>Current motion viewer</h2><p>Choose any current clip. Check source, station and distant scale with the same pivot. Nonlooping actions repeat here for review; the game still plays them once. Idle holds and sparse authored poses are intentional. The viewer uses authored frame timing; travel in the game advances by distance.</p>
<select id="state"></select><select id="size"><option value="148">Source size</option><option value="65.28">Station size</option><option value="27">Distant view</option></select><select id="speed"><option value="1">Normal speed</option><option value="0.5">Half speed</option><option value="2">Double speed</option></select><button id="pause">Pause</button><button id="restart">Restart</button><canvas id="view" width="1000" height="410"></canvas><p id="caption"></p>
<h2>Verification and limits</h2><p>Actual player checks: 21,968 continuous playback, gait switch, pause/Continue and registration checks, zero failures. Native full-set review: 200 states, 1,026 source/elapsed checks and 416 captures, zero failures. Material protection: three tests pass. Colour lock: 8,627 paths, 1,031 approved corrections, zero errors. All four translated exports reproduce exactly; all canvases retain margin. Source density is consistently 148px per 65.28 world units, about 2.27 source pixels per world unit.</p>
<p>The run retains its current six authored poses. Two replacement source candidates were rejected for repeated stride poses or style/background drift; they are preserved with prompts and are not installed. No new global tint, blur, rescaling, palette simplification or interpolated frames were added. The technical playback checks do not certify subjective smoothness; current timed clips and native phase samples provide the visual evidence. The short pose cadence remains visible at close zoom.</p>
<p><a href="../marsh-consistency-review-v1/index.html">Current transition chains and native samples</a> | <a href="../marsh-gameplay-review-v1/index.html">Station gameplay review</a> | <a href="audit.json">Per-state audit</a></p>
<h2>Complete pose boards</h2>'''
    for p in sorted(BASE.glob('*-contact.png')):
        html+=f'<details><summary>{p.stem[:-8]}</summary><img loading="lazy" src="{p.name}" alt="All authored {p.stem[:-8]} poses"></details>'
    html+='''<script>const DATA=__DATA__;const images={};for(const s of Object.values(DATA.states))for(const f of s.files){if(images[f])continue;const im=new Image();im.src='../'+f.slice('character/'.length);images[f]=im}const choose=document.querySelector('#state'),size=document.querySelector('#size'),speed=document.querySelector('#speed'),canvas=document.querySelector('#view'),ctx=canvas.getContext('2d');Object.keys(DATA.states).sort().forEach(k=>choose.add(new Option(k,k)));choose.value='tread-north';let time=0,last=performance.now(),paused=false;document.querySelector('#pause').onclick=()=>{paused=!paused;document.querySelector('#pause').textContent=paused?'Play':'Pause'};const restart=()=>time=0;choose.onchange=restart;document.querySelector('#restart').onclick=restart;function render(now){if(!paused)time+=(now-last)*Number(speed.value);last=now;const key=choose.value,s=DATA.states[key],duration=s.durations.reduce((a,b)=>a+b,0);let cursor=time%(duration+(s.loop?0:500)),slot=0;while(slot<s.durations.length-1&&cursor>=s.durations[slot]){cursor-=s.durations[slot];slot++}ctx.fillStyle='#293b40';ctx.fillRect(0,0,1000,410);ctx.fillStyle='#dce7e8';ctx.font='17px system-ui';ctx.fillText(key+' / pose '+slot+' / '+s.durations[slot]+'ms',24,32);ctx.imageSmoothingEnabled=false;for(let i=0;i<2;i++){const height=i?65.28:Number(size.value),scale=height/s.standingHeight,x=i?760:300,im=images[s.files[slot]];ctx.strokeStyle='#647c80';ctx.beginPath();ctx.moveTo(x-170,350);ctx.lineTo(x+170,350);ctx.stroke();ctx.fillText(i?'Station reference':height+'px standing calibration',x-125,75);if(im.complete&&im.naturalWidth)ctx.drawImage(im,x-s.pivot[0]*scale,350-s.pivot[1]*scale,im.width*scale,im.height*scale)}document.querySelector('#caption').textContent=s.loop?'Looping clip':'Nonlooping action; final pose held for review';requestAnimationFrame(render)}requestAnimationFrame(render);</script>'''
    html=html.replace('__DATA__',json.dumps(data));(BASE/'index.html').write_text(html,encoding='utf8')
    script=re.search(r'<script>(.*?)</script>',html,re.S).group(1);(ROOT/'output/marsh-animation-audit/quality-v2-review.js').write_text(script,encoding='utf8')
    marker=b'<h2>Second full-set quality pass</h2>';section=marker+b'<p>Current review adds continuous walk/run gait phase and corrected north tread registration. <a href="../marsh-quality-pass-v2/index.html">Open the latest visual and motion review</a>.</p>'
    for name in ('marsh-consistency-review-v1','marsh-run-carry-review-v1','marsh-gameplay-review-v1'):
        p=ROOT/'character'/name/'index.html';text=p.read_bytes()
        if marker not in text:
            anchor=b'<script>' if b'<script>' in text else b'<h1>'
            text=text.replace(anchor,section+anchor,1);p.write_bytes(text)
    assert all((BASE/x).exists() for x in re.findall(r'<(?:a|img)[^>]+(?:src|href)="([^"]+)"',html))
    print('Latest quality review: 200 timed clips, 59 complete-pose boards, before/after, links resolve')
if __name__=='__main__':main()
