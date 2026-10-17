from pathlib import Path
import json,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-carry-north-station-v1'
configs=[]
for gear in ['bare','helmet']:
 s=json.loads((P/f'{gear}-manifest.json').read_text())['states'][0];configs.append({'gear':gear,'master':f'../bill-cargo-north-master-head-v1/frames/{gear}/pickup-north/011.png','frames':[f.removeprefix('res://character/bill-carry-north-gait-v1/') for f in s['frameFiles']]})
frames=[]
for slot in range(6):
 b=Image.new('RGB',(512,560),'#22343e');d=ImageDraw.Draw(b)
 for row,c in enumerate(configs):
  for col,f in enumerate([P/c['master'],P/c['frames'][slot]]):
   a=Image.open(f).convert('RGBA');b.paste(a,(col*256,row*280),a)
  d.text((8,row*280+260),c['gear']+' master / phase'+str(slot),fill='white')
 frames.append(b)
palette=Image.new('RGB',(512,560*6))
for i,f in enumerate(frames):palette.paste(f,(0,560*i))
palette=palette.quantize(colors=255);quant=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames];quant[0].save(P/'master-loop.gif',save_all=True,append_images=quant[1:],duration=140,loop=0)
html="""<!doctype html><meta charset="utf-8"><title>Bill North carrying gait</title><style>body{background:#182932;color:#dde8e9;font:16px system-ui;margin:24px}canvas{background:#22343e;border:1px solid #4c626d;max-width:100%}img{max-width:100%}label,button{margin:8px}</style><h1>Bill — North carrying gait</h1><p>Both legs share the work. Original master head, helmet, torso, hands and cargo stay consistent.</p><label>Size <select id="size"><option>82</option><option>148</option></select></label><button id="play">Pause</button><p id="clock"></p><h2>Bare · master / gait</h2><canvas width="512" height="270"></canvas><h2>Helmet · master / gait</h2><canvas width="512" height="270"></canvas><p>840ms source loop. Room checks use a prescribed clear North lane; first step, natural routing and saved transitions remain separate work.</p><h2>Source poses</h2><img src="candidate-review.png"><h2>Actual room comparisons</h2>BOARDS<script>const configs=CONFIGS,imgs=new Map();for(const c of configs)for(const f of [c.master,...c.frames]){let a=new Image();a.src=f;imgs.set(f,a)}let playing=true,t=0,last=performance.now();document.querySelector('#play').onclick=()=>{playing=!playing;document.querySelector('#play').textContent=playing?'Pause':'Play'};function tick(now){if(playing)t+=now-last;last=now;let slot=Math.floor(t%840/140),scale=Number(document.querySelector('#size').value)/148;document.querySelectorAll('canvas').forEach((canvas,row)=>{const ctx=canvas.getContext('2d');ctx.clearRect(0,0,512,270);[configs[row].master,configs[row].frames[slot]].forEach((f,col)=>{const a=imgs.get(f);if(a.complete&&a.naturalWidth)ctx.drawImage(a,128+col*256-128*scale,240-224*scale,256*scale,256*scale)})});document.querySelector('#clock').textContent='Phase '+slot+' · '+Math.round(t%840)+'ms';requestAnimationFrame(tick)}requestAnimationFrame(tick)</script>"""
boards=[];exact=0;total=0
if (O/'validation.json').exists() and json.loads((O/'validation.json').read_text())['passed']:
 d=json.loads((O/'journeys.json').read_text());v=json.loads((O/'validation.json').read_text())
 for j in d['journeys']:
  tag=('staged' if j['candidate'] else 'normal')+('-helmet' if j['helmet'] else '-bare');rows=j['captures'];b=Image.new('RGB',(960,240*math.ceil(len(rows)/6)),'#22343e');dr=ImageDraw.Draw(b)
  for i,c in enumerate(rows):
   x0=(i%6)*160;y0=(i//6)*240;room=Image.open(O/c['room']).convert('RGB');x=255+(c['foot'][0]-7680)*398/384;y=287+(c['foot'][1]-8064)*398/384;b.paste(room.crop((round(x)-75,round(y)-130,round(x)+75,round(y)+35)),(x0+5,y0));src=Image.open(O/c['source']).convert('RGBA');total+=1
   if j['candidate'] and c['slot']>=0:
    f=P/configs[1 if j['helmet'] else 0]['frames'][c['slot']];expect=Image.open(f).convert('RGBA');assert src.size==expect.size and src.tobytes()==expect.tobytes();exact+=1
   px,py=(128,224) if src.width==256 else (92,172);scale=82/148;src=src.resize((round(src.width*scale),round(src.height*scale)),Image.Resampling.LANCZOS);b.paste(src,(round(x0+80-px*scale),round(y0+225-py*scale)),src);dr.text((x0+3,y0+227),str(c['slot'])+' / '+str(round(c['time'],2))+'s',fill='white')
  name=tag+'-native-review.png';b.save(P/name);boards.append(name)
 evidence={'validation':v,'nativeChecks':d['checks'],'nativeFailures':d['failures'],'scope':d['scope'],'nativeSourceSamples':total,'stagedGaitSourcesExactRGBA':exact,'packageValidation':json.loads((P/'validation.json').read_text()),'normalSelectionChanged':False,'limits':['Not continuous native footage or anatomical stance-lock proof','Natural chooser/path, first step/arrival, gear/hazard interruptions and Continue untested']};(P/'runtime-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
(P/'index.html').write_text(html.replace('CONFIGS',json.dumps(configs)).replace('BOARDS',''.join('<h3>'+f+'</h3><img src="'+f+'">' for f in boards)),encoding='utf-8');print('Saved source loop/review;',total,'native/source samples;',exact,'staged exact-source captures')

