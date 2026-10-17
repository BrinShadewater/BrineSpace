from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;old=json.loads((P.parent/'bill-carry-stow-west-north-v1/replay.json').read_text());new=json.loads((P/'replay.json').read_text());cases=[]
for gear in ['bare','helmet']:
 for kind,rows in [('before',old),('after',new)]:
  c=next(c for c in rows if c['gear']==gear);c=dict(c);c['kind']=kind;cases.append(c)
html='''<!doctype html><meta charset="utf-8"><title>Bill — north unload rise</title><style>body{background:#182932;color:#dde8e9;font:16px system-ui;margin:24px}canvas{background:#22343e;border:1px solid #4c626d;max-width:100%}img{max-width:100%}label,button{margin:8px}h2{font-size:20px}</style><h1>Bill — north unload rise</h1><p>Two intermediate poses replace the abrupt rise. The original master head, helmet, upper-body detail and standing endpoint are retained.</p><label>Size <select id="size"><option>82</option><option selected>148</option></select></label><label>Review <select id="mode"><option value="rise">Rise comparison</option><option value="full">Full stop and stow</option></select></label><button id="play">Pause</button><p id="clock"></p><h2>Bare · before / after</h2><canvas id="bare" width="480" height="270"></canvas><h2>Helmet · before / after</h2><canvas id="helmet" width="480" height="270"></canvas><p>Source choices replay at recorded room timestamps. The room check preserves Bill's destination, the original two-second unload and his normal needs. Wider posture, foot contact and cargo placement still need review.</p><h2>Actual workshop · bare</h2><img src="bare-unload-native-review.png"><h2>Actual workshop · helmet</h2><img src="helmet-unload-native-review.png"><script>const cases=CASES,images=new Map();for(const c of cases)for(const p of Object.values(c.sources)){if(images.has(p))continue;let a=new Image();a.src=p;images.set(p,a)}let playing=true,elapsed=0,last=performance.now();document.querySelector('#mode').onchange=()=>elapsed=0;document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play'};function tick(now){if(playing)elapsed+=(now-last)/1000;last=now;const rise=document.querySelector('#mode').value==='rise',t=rise?2.09+elapsed%1.2:elapsed%4.2,scale=Number(document.querySelector('#size').value)/148;for(const gear of ['bare','helmet']){let ctx=document.querySelector('#'+gear).getContext('2d');ctx.clearRect(0,0,480,270);for(const c of cases.filter(c=>c.gear===gear)){let row=0;for(const r of c.timeline){if(r.time>t)break;row=r.row}const a=images.get(c.sources[String(row)]);if(a&&a.complete&&a.naturalWidth){let px=a.width===256?128:92,py=a.width===256?224:172;ctx.drawImage(a,(c.kind==='before'?120:360)-px*scale,240-py*scale,a.width*scale,a.height*scale)}}}document.querySelector('#clock').textContent=rise?(t<2.32?'Rising':'Standing'):t.toFixed(2)+'s';requestAnimationFrame(tick)}requestAnimationFrame(tick)</script>'''
(P/'index.html').write_text(html.replace('CASES',json.dumps(cases)),encoding='utf-8');(P/'comparison-replay.json').write_text(json.dumps(cases,indent=2)+'\n')
frames=[]
for tick in range(60):
 t=2.09+tick*.02;b=Image.new('RGB',(480,400),'#22343e');draw=ImageDraw.Draw(b)
 for c in cases:
  row=0
  for r in c['timeline']:
   if r['time']>t:break
   row=r['row']
  im=Image.open(P/c['sources'][str(row)]).convert('RGBA');px,py=(128,224) if im.width==256 else (92,172);col=0 if c['kind']=='before' else 1;line=0 if c['gear']=='bare' else 1;b.paste(im,(120+240*col-px,190+200*line-py),im);draw.text((col*240+12,line*200+12),c['gear']+' / '+c['kind'],fill='white')
 frames.append(b)
atlas=Image.new('RGB',(480*len(frames),400))
for i,f in enumerate(frames):atlas.paste(f,(i*480,0))
palette=atlas.quantize(colors=255);q=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames];q[0].save(P/'rise-before-after.gif',save_all=True,append_images=q[1:],duration=20,loop=0,optimize=False);frames[7].save(P/'rise-before-after.png');print('Before/after recorded-source-clock comparison and20ms GIF preview saved')
