"""Publish exact rendered route motion and before/after comparison evidence."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1];O=R/'output/bill-east-walk-join-native-v2';D=R/'character/bill-east-walk-joins-v1/native-motion-v2';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert v['engineExit']==0 and v['failures']==0 and not v['ownerChanges']
allowed={'airlock_panel.gd','crew_work_panel.gd','moonbay_panel.gd'};assert all(Path(p).name in allowed for p in v['inputChanges'])
report=json.loads((O/'report.json').read_text(encoding='utf-8'));D.mkdir(exist_ok=False)
for name in ['validation.json','report.json','inputs-before.json','inputs-after.json']:shutil.copyfile(O/name,D/name)
sequences={};records=[]
for variant in ['candidate','selected']:
 cs=[c for c in report['captures'] if c['variant']==variant];images=[Image.open(O/c['worldFile']).convert('RGBA').crop((315,270,820,425)) for c in cs];times=[];walk_i=0
 traversal=next(t for t in report['traversals'] if t['variant']==variant)
 for c in cs:
  if c['label']=='idle before':t=(c['slot']+1)*20
  elif c['label']=='idle after':t=320+round(traversal['duration']*1000)+(c['slot']+1)*20
  else:
   walk_i+=1;t=320+min(walk_i*80,round(traversal['duration']*1000))
  times.append(t)
 durations=[b-a for a,b in zip(times,times[1:])]+[80];assert all(t>0 for t in durations)
 for s in [1,4]:
  path=D/f'{variant}-{s}.png'
  images[0].save(path,save_all=True,append_images=images[1:],duration=[t*s for t in durations],loop=0,disposal=0,blend=0)
 sequences[variant]=cs
 for c,t,dt in zip(cs,times,durations):records.append(dict(c,simulationTimeMs=t,durationMs=dt,worldSha256=sha(O/c['worldFile']),sourceSha256=sha(O/c['sourceFile'])))
 assert len(images)>30
count=len(sequences['candidate']);assert count==len(sequences['selected'])
pick=[0,3,4,5,6,7,count//3,count//2,2*count//3,count-6,count-5,count-4,count-3,count-1]
pages=[]
for page,start in enumerate(range(0,len(pick),4)):
 b=Image.new('RGB',(2020,370),'#17252d');draw=ImageDraw.Draw(b)
 for col,n in enumerate(pick[start:start+4]):
  for row,variant in enumerate(['candidate','selected']):
   c=sequences[variant][n];im=Image.open(O/c['worldFile']).crop((315,270,820,425));b.paste(im,(col*505,30+row*180));draw.text((col*505+5,12+row*180),f"{variant} · {c['label']} · {c['key']} {c['slot']}",fill='white')
 path=D/f'comparison-{page}.png';b.save(path);pages.append(path.name)
# Copy endpoint/full-world evidence; other exact originals remain in isolated output.
for c in [sequences['candidate'][0],sequences['candidate'][count//2],sequences['candidate'][-1]]:shutil.copyfile(O/c['worldFile'],D/c['worldFile'])
proof={'status':'native_join_pass_visual_review_pending','scope':report['scope'],'checks':v['checks'],'failures':v['failures'],'traversals':report['traversals'],'route':report['route'],'records':records,'pages':pages,'normalAdmission':False,'fullVisualAcceptance':False,'visualReviewed':False,'inputChanges':v['inputChanges'],'ownerChanges':v['ownerChanges'],'crop':[315,270,820,425]}
(D/'review.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>Bill · eased walking joins</title><style>body{background:#17252d;color:#e8e0cf;font:16px system-ui;margin:24px}img{display:block;width:min(100%,1010px);image-rendering:pixelated}button{font:inherit;margin:8px}p{max-width:950px}</style><h1>Bill · eased walking joins</h1><p>Both versions use identical revised walking art. The upper version adds whole-figure first-step and settling poses. These are game-rendered captures. A short lead-in eases the first step; stopping settles from the current stride.</p><button id="normal">Normal speed</button><button id="slow">Quarter speed</button><h2>Eased joins</h2><img id="candidate" src="candidate-1.png"><h2>Same walk without joins</h2><img id="selected" src="selected-1.png"><p>Room crop enlarged twice. The route is prescribed for comparison; Bill’s movement, floor checks, arrival and distance-driven gait use the game code.</p><script>function speed(s){for(let id of ['candidate','selected'])document.getElementById(id).src=id+'-'+s+'.png?v='+Date.now();}document.getElementById('normal').onclick=()=>speed(1);document.getElementById('slow').onclick=()=>speed(4);</script>'''
(D/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(checks=v['checks'],captures=len(records),perSequence=count,pages=pages)))
