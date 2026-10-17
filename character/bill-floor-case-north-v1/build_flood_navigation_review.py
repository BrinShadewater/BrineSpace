from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-floor-case-flood-navigation-v1'
v=json.loads((O/'validation.json').read_text());assert v['passed']
data=json.loads((O/'records.json').read_text());assert data['failures']==0
rows=[r for r in data['records'] if not r['name'].endswith('-summary')]
copies=P/'flood-navigation-captures';copies.mkdir(exist_ok=True)
hashes={};native={};sources={}
metadata=json.loads((R/'output/bill-flood-source-registration-v1/metadata.json').read_text())
registration={}
for row in rows:
 name=row['name']
 for suffix in ['room','source']:
  src=O/f'{name}-{suffix}.png';dest=copies/src.name;shutil.copy2(src,dest)
  hashes[dest.name]=hashlib.sha256(dest.read_bytes()).hexdigest()
 native[name]=Image.open(copies/f'{name}-room.png').convert('RGBA').crop((235,250,675,700))
 original=Image.open(copies/f'{name}-source.png').convert('RGBA')
 digest=hashlib.sha256(original.tobytes()).hexdigest();matches=metadata[digest]
 profiles={(tuple(m['pivot']),m['standingHeight'],tuple(m['size'])) for m in matches}
 assert len(profiles)==1
 pivot,height,size=profiles.pop();assert height==148 and tuple(original.size)==size
 common=Image.new('RGBA',(512,512));common.paste(original,(round(256-pivot[0]),round(320-pivot[1])))
 bounds=common.getbbox();assert bounds and bounds[0]>=128 and bounds[1]>=128 and bounds[2]<=384 and bounds[3]<=384
 sources[name]=common.crop((128,128,384,384))
 registration[digest]={'pivot':pivot,'standingHeight':height,'size':size,'binding':'Post-run normal-loaded exact RGBA hash; source pixels unchanged, common physical root at(128,192).'}
 if name.endswith('-normal'):
  other=name.rsplit('-',1)[0]+'-candidate'
  assert sources[name].tobytes()==sources[other].tobytes()
boards=[];sections=[]
for gear in ['bare','helmet']:
 group=[r for r in rows if r['name'].startswith(gear+'-') and r['name'].endswith('-candidate')]
 group.sort(key=lambda r:r['tick']);assert len(group)==300
 # Native frames taken every2simulation ticks. 60Hz simulation,30Hz capture.
 durations=[round((i+1)*1000/30)-round(i*1000/30) for i in range(len(group))]
 for family,pictures in [('native',[native[r['name']] for r in group]),('source',[sources[r['name']] for r in group])]:
  pictures[0].save(P/f'{gear}-flood-navigation-{family}.png',save_all=True,append_images=pictures[1:],duration=durations,loop=0,disposal=0,blend=0)
  cursor=0
  with Image.open(P/f'{gear}-flood-navigation-{family}.png') as apng:
   for index in range(apng.n_frames):
    apng.seek(index);remaining=round(apng.info['duration']);decoded=apng.convert('RGBA').tobytes()
    while remaining>0:
     assert decoded==pictures[cursor].tobytes();remaining-=durations[cursor];cursor+=1
    assert remaining==0
  assert cursor==len(group) and sum(durations)==10000
 sections.append(f'<h2>{gear} — actual actor updates</h2><div><figure><img src="{gear}-flood-navigation-native.png"><figcaption>Native room · captured30Hz</figcaption></figure><figure><img src="{gear}-flood-navigation-source.png"><figcaption>Exact selected source · captured30Hz</figcaption></figure></div>')
 for boundary,indices in [('enter',[60,62,64,66,68,70,72,74]),('leave',[408,410,412,414,416,418,420,422])]:
  board=Image.new('RGB',(2048,464),'#182932');d=ImageDraw.Draw(board)
  for i,tick in enumerate(indices):
   row=next(r for r in group if r['tick']==tick);name=row['name']
   x=255+(row['foot'][0]-7680)*398/384;y=287+(row['foot'][1]-8064)*398/384
   crop=Image.open(copies/f'{name}-room.png').crop((round(x)-95,round(y)-115,round(x)+105,round(y)+25))
   board.paste(crop,(i*256+28,24));im=sources[name];board.paste(im,(i*256,170),im)
   d.text((i*256,3),f"{tick} {row['state']} {row['direction']}",fill='white');d.text((i*256,445),f"water {row['water']:.3f} {row['medium']}",fill='white')
  file=f'flood-navigation-{gear}-{boundary}-board.png';board.save(P/file);boards.append(file)
 overview=Image.new('RGB',(2048,920),'#182932');d=ImageDraw.Draw(overview)
 for i,tick in enumerate([0,60,120,180,240,300,360,420,480,540,580,598]):
  row=next(r for r in group if r['tick']==tick);x=255+(row['foot'][0]-7680)*398/384;y=287+(row['foot'][1]-8064)*398/384
  crop=Image.open(copies/f"{row['name']}-room.png").crop((round(x)-95,round(y)-115,round(x)+105,round(y)+25))
  col=i%8;line=i//8;overview.paste(crop,(col*256+28,line*460+24));im=sources[row['name']];overview.paste(im,(col*256,line*460+170),im)
  d.text((col*256,line*460+3),f"{tick} {row['state']} {row['direction']}",fill='white')
 file=f'flood-navigation-{gear}-overview.png';overview.save(P/file);boards.append(file)
(P/'flood-navigation-review.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill live flood route</title><style>body{background:#182932;color:#ddd;font:16px sans-serif;margin:24px}div{display:flex;gap:20px}figure{margin:0}</style><h1>Bill — actual movement and water joins</h1><p>Real medium/oxygen/safety/navigation/source updates at60Hz; native images captured30Hz. Room water history prescribed for ten seconds; no natural hydrology claim. Candidate renderer unselected. Pose joins require separate acceptance.</p>'+''.join(sections))
(P/'flood-navigation-evidence.json').write_text(json.dumps({'validation':v,'records':data,'captureSHA256':hashes,'boards':boards,'sourceRegistration':registration,'scope':'Actual advancing controller/source/world-medium capture; prescribed water rise/hold/drain. Native30Hz timelines, not interpolated or source-hold reconstructions. Original source panes registered from post-run loaded exact RGBA metadata; same148ruler, no pose normalization.'},indent=2)+'\n')
print(json.dumps({'presentations':len(rows),'boards':boards,'summaries':[r for r in data['records'] if r['name'].endswith('-summary')]}))
