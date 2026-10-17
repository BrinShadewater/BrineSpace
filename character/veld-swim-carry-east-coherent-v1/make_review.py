from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
data={gear:json.loads((H/f'{gear}-manifest.json').read_text()) for gear in ['bare','helmet']}
board=Image.new('RGBA',(1024,600),'#202a30');d=ImageDraw.Draw(board)
for row,gear in enumerate(data):
 paths=[R/f'character/dr-veld-v2/frames/{gear}/swim-carry-east/000.png',H/f'frames/{gear}/swim-carry-east/000.png',R/f'character/veld-water-east-coherent-v1/frames/{gear}/swim-east/000.png',R/f'character/veld-carry-east-consistent-v1/frames/{gear}/000.png']
 for col,p in enumerate(paths):
  im=Image.open(p).convert('RGBA');board.alpha_composite(im,(col*256,row*300+25));d.text((col*256+4,row*300+4),gear+' / '+['selected old cargo','new staged cargo','selected prone master','accepted dry case'][col],fill='white')
board.save(H/'master-comparison-v1.png')
html='''<!doctype html><meta charset="utf-8"><title>Veld east water cargo master repair</title>
<style>body{background:#202a30;color:#e5ebed;font:16px sans-serif;margin:24px}canvas{max-width:100%;height:auto}a{color:#8cc6e7}button,select,input{margin:8px}img{max-width:100%}</style>
<h1>Veld — east water cargo</h1><p>New authored cargo loop staged beside the selected swimming and dry cargo masters. Shared graphite/skin/blue grade, fixed anatomical ruler and original 840ms loop. Same closed swimming helmet component in every phase. Runtime selection unchanged. Complete journey and remaining directions still need work.</p>
<button id="play">Pause</button><label>Frame <input aria-label="Frame" id="phase" type="range" min="0" max="5" value="0"></label><label>Speed <select id="speed"><option value="1">Full speed</option><option value="0.3333333333">One-third speed</option></select></label><label>Background <select id="bg"><option value="#202a30">Dark</option><option value="#a7afb2">Light</option></select></label><span id="clock"></span>
<canvas id="canvas" width="1024" height="720"></canvas>
<p><a href="paired-full-speed-v1.mp4">Full-speed paired three-cycle reel beside the swim master</a></p><h2>Selected old cargo / staged cargo / selected swim / accepted dry case</h2><img src="master-comparison-v1.png"><p><a href="paired-contact-v1.png">All paired poses</a> · <a href="native-paired-v1.png">Native player at 148/82/54</a> · <a href="source-provenance.json">Source and exact prompt provenance</a></p>
<script>const manifests=DATA;let running=true,phase=0,elapsed=0,last=performance.now();const ctx=canvas.getContext('2d');const imgs={};async function init(){for(const g of ['bare','helmet']){imgs[g]=await Promise.all(manifests[g].states[0].frameFiles.map(url=>new Promise(resolve=>{const im=new Image();im.onload=()=>resolve(im);im.src=url})));}requestAnimationFrame(tick)}
function draw(){ctx.fillStyle=bg.value;ctx.fillRect(0,0,1024,720);ctx.fillStyle='#e5ebed';ctx.font='16px sans-serif';for(let j=0;j<2;j++){const gear=j?'helmet':'bare';ctx.fillText(gear+' — shared phase '+phase,8,j*350+20);for(const [height,x,y] of [[148,128,180],[82,365,180],[54,535,180],[27,665,180]]){const s=height/148;ctx.drawImage(imgs[gear][phase],x-128*s,j*350+y-128*s,256*s,256*s);ctx.fillText(height+'px ruler',x-50,j*350+285)}const im=imgs[gear][phase];ctx.drawImage(im,120,87,63,70,775,j*350+50,189,210);ctx.fillText('head / grip detail',770,j*350+285)}clock.textContent='Phase '+(phase+1)+' / 6 · '+Math.round(elapsed)+'ms / 840ms';document.getElementById('phase').value=phase;}
function tick(t){if(running){elapsed=(elapsed+(t-last)*Number(speed.value))%840;let e=elapsed;phase=0;for(let i=0;i<6;i++){if(e<manifests.bare.states[0].frameDurationsMs[i]){phase=i;break}e-=manifests.bare.states[0].frameDurationsMs[i]}}last=t;draw();requestAnimationFrame(tick)}play.onclick=()=>{running=!running;play.textContent=running?'Pause':'Play'};document.getElementById('phase').oninput=e=>{running=false;play.textContent='Play';phase=Number(e.target.value);elapsed=phase*140;draw()};init();</script>'''
(H/'index.html').write_text(html.replace('DATA',json.dumps(data)),encoding='utf-8')
sources=[]
for version,original,refs in [('v1','exec-0e2cdd4d-56c3-4974-a7db-beca670e7361.png',['character/veld-water-east-coherent-v1/swim-source-v1.png','character/veld-carry-east-consistent-v1/motion-source-v9.png']),('v2','exec-d9834424-51d6-43de-b38e-caa4728c7284.png',['character/veld-swim-carry-east-coherent-v1/source-v1.png'])]:
 p=H/f'source-{version}.png';im=Image.open(p);prompt=H/f'source-prompt-{version}.txt'
 sources.append(dict(source=p.relative_to(R).as_posix(),sha256=sha(p),dimensions=list(im.size),mode=im.mode,prompt=prompt.relative_to(R).as_posix(),promptSha256=sha(prompt),builtinOriginal='C:/Users/Alex/.codex/generated_images/01a0ef89-9984-7e73-99c2-84cdd8b28b14/'+original,references=[dict(path=x,sha256=sha(R/x)) for x in refs],selection='selected' if version=='v2' else 'superseded kick jump; retained identity source'))
(H/'source-provenance.json').write_text(json.dumps(dict(method='built-in imagegen',installed=False,sources=sources),indent=2)+'\n')
print('Paired shared-clock review, master comparison and exact source provenance saved.')
