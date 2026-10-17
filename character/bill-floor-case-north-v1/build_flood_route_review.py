from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-floor-case-flood-route-v1'
v=json.loads((O/'validation.json').read_text());assert v['passed']
data=json.loads((O/'records.json').read_text());assert data['failures']==0
rows=[r for r in data['records'] if not r['name'].endswith('-summary')]
copies=P/'flood-route-captures';copies.mkdir(exist_ok=True)
hashes={};native={};sources={}
for row in rows:
 name=row['name']
 for suffix in ['room','source']:
  src=O/f'{name}-{suffix}.png';dest=copies/src.name;shutil.copy2(src,dest)
  hashes[dest.name]=hashlib.sha256(dest.read_bytes()).hexdigest()
 native[name]=Image.open(copies/f'{name}-room.png').convert('RGBA').crop((235,250,675,700))
 sources[name]=Image.open(copies/f'{name}-source.png').convert('RGBA')
 if name.endswith('-normal'):
  other=name.rsplit('-',1)[0]+'-candidate'
  assert sources[name].tobytes()==sources[other].tobytes()
boards=[];sections=[]
for gear in ['bare','helmet']:
 group=[r for r in rows if r['name'].startswith(gear+'-') and r['name'].endswith('-candidate')]
 group.sort(key=lambda r:r['tick']);assert len(group)==300
 # Native frames taken every2simulation ticks. 60Hz simulation,30Hz capture.
 durations=[1000/30]*len(group)
 for family,pictures in [('native',[native[r['name']] for r in group]),('source',[sources[r['name']] for r in group])]:
  pictures[0].save(P/f'{gear}-flood-route-{family}.png',save_all=True,append_images=pictures[1:],duration=durations,loop=0,disposal=0,blend=0)
 sections.append(f'<h2>{gear} — actual actor updates</h2><div><figure><img src="{gear}-flood-route-native.png"><figcaption>Native room · captured30Hz</figcaption></figure><figure><img src="{gear}-flood-route-source.png"><figcaption>Exact selected source · captured30Hz</figcaption></figure></div>')
 for boundary,indices in [('enter',[60,62,64,66,68,70,72,74]),('leave',[408,410,412,414,416,418,420,422])]:
  board=Image.new('RGB',(1600,340),'#182932');d=ImageDraw.Draw(board)
  for i,tick in enumerate(indices):
   row=next(r for r in group if r['tick']==tick);name=row['name']
   x=255+(row['foot'][0]-7680)*398/384;y=287+(row['foot'][1]-8064)*398/384
   crop=Image.open(copies/f'{name}-room.png').crop((round(x)-95,round(y)-115,round(x)+105,round(y)+25))
   board.paste(crop,(i*200,24));im=sources[name];board.paste(im,(i*200,170),im)
   d.text((i*200,3),f"{tick} {row['state']} {row['direction']}",fill='white');d.text((i*200,320),f"water {row['water']:.3f} {row['medium']}",fill='white')
  file=f'flood-route-{gear}-{boundary}-board.png';board.save(P/file);boards.append(file)
 overview=Image.new('RGB',(1600,640),'#182932');d=ImageDraw.Draw(overview)
 for i,tick in enumerate([0,60,120,180,240,300,360,420,480,540,580,598]):
  row=next(r for r in group if r['tick']==tick);x=255+(row['foot'][0]-7680)*398/384;y=287+(row['foot'][1]-8064)*398/384
  crop=Image.open(copies/f"{row['name']}-room.png").crop((round(x)-95,round(y)-115,round(x)+105,round(y)+25))
  col=i%8;line=i//8;overview.paste(crop,(col*200,line*320+24));im=sources[row['name']];overview.paste(im,(col*200,line*320+170),im)
  d.text((col*200,line*320+3),f"{tick} {row['state']} {row['direction']}",fill='white')
 file=f'flood-route-{gear}-overview.png';overview.save(P/file);boards.append(file)
(P/'flood-route-review.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill live flood route</title><style>body{background:#182932;color:#ddd;font:16px sans-serif;margin:24px}div{display:flex;gap:20px}figure{margin:0}</style><h1>Bill — actual movement and water joins</h1><p>Real medium/oxygen/safety/navigation/source updates at60Hz; native images captured30Hz. Room water history prescribed for ten seconds; no natural hydrology claim. Candidate renderer unselected. Pose joins require separate acceptance.</p>'+''.join(sections))
(P/'flood-route-evidence.json').write_text(json.dumps({'validation':v,'records':data,'captureSHA256':hashes,'boards':boards,'scope':'Actual advancing controller/source/world-medium capture; prescribed water rise/hold/drain. Native30Hz timelines, not interpolated or source-hold reconstructions.'},indent=2)+'\n')
print(json.dumps({'presentations':len(rows),'boards':boards,'summaries':[r for r in data['records'] if r['name'].endswith('-summary')]}))
