from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-land-water-material-west-v2'
v=json.loads((O/'validation.json').read_text());assert v['passed']
data=json.loads((O/'records.json').read_text());assert data['failures']==0
rows=[x for x in data['records'] if x['name'].endswith('-candidate') and 'tick' in x]
normal=json.loads((R/'output/bill-flood-source-registration-v1/metadata.json').read_text());candidate={}
# Historical flood inventory predates the selected West material walking bank.
# Identify captured pixels against current manifests; do not infer registration
# from dimensions or transfer historical source-stability evidence.
current_manifest_hashes={}
for relative in ['character/bill-walk-west-material-v1/manifest.json','character/bill-walk-west-material-v1/helmet-manifest.json']:
 manifest=R/relative; bank=json.loads(manifest.read_text(encoding='utf-8'))
 current_manifest_hashes[relative]=hashlib.sha256(manifest.read_bytes()).hexdigest()
 for state in bank['states']:
  for index,path in enumerate(state['frameFiles']):
   file=R/path[6:] if path.startswith('res://') else manifest.parent/path
   im=Image.open(file).convert('RGBA');sha=hashlib.sha256(im.tobytes()).hexdigest()
   normal.setdefault(sha,[]).append(dict(pivot=bank['pivot'],standingHeight=bank['standingHeight'],size=list(im.size),manifest=relative,path=str(file.relative_to(R)),index=index,key=state['id']))
for study in ['bill-land-water-west-v4/bare','bill-land-water-west-v4/helmet']:
 for file in (R/'character'/study/'frames').rglob('*.png'):
  im=Image.open(file).convert('RGBA');sha=hashlib.sha256(im.tobytes()).hexdigest();candidate[sha]=dict(size=im.size,pivot=[160,224],standingHeight=148,study=study)
dest=P/'captures';dest.mkdir(exist_ok=True);inputs={};sources={};native={};registered={}
for row in rows:
 name=row['name']
 for kind in ['source','room']:
  f=O/f'{name}-{kind}.png';shutil.copy2(f,dest/f.name);inputs[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
 im=Image.open(dest/f'{name}-source.png').convert('RGBA');sha=hashlib.sha256(im.tobytes()).hexdigest()
 if sha in candidate:m=candidate[sha]
 else:
  profiles={(tuple(x['pivot']),x['standingHeight'],tuple(x['size'])) for x in normal[sha]};assert len(profiles)==1
  pivot,h,size=profiles.pop();m=dict(pivot=pivot,standingHeight=h,size=size,normalMatches=normal[sha])
 assert m['standingHeight']==148 and tuple(m['size'])==im.size
 out=Image.new('RGBA',(320,320));out.alpha_composite(im,(round(160-m['pivot'][0]),round(224-m['pivot'][1])));sources[name]=out;registered[sha]=m
 native[name]=Image.open(dest/f'{name}-room.png').convert('RGBA').crop((235,250,675,700))
sections=[];boards=[];decoded=0
for gear in ['bare','helmet']:
 for phase,low,high in [('enter',60,105)]:
  group=sorted([x for x in rows if x['name'].startswith(gear+'-') and low<=x['tick']<high],key=lambda x:x['tick']);assert len(group)==high-low
  board=Image.new('RGB',(2000,((len(group)+9)//10)*425),'#182932');d=ImageDraw.Draw(board)
  durations=[round((i+1)*1000/60)-round(i*1000/60) for i in range(len(group))]
  for i,row in enumerate(group):
   x=255+(row['foot'][0]-7680)*398/384;y=287+(row['foot'][1]-8064)*398/384
   room=Image.open(dest/f"{row['name']}-room.png").crop((round(x)-100,round(y)-130,round(x)+100,round(y)+70))
   col=i%10;line=i//10;board.paste(room,(col*200,line*425+20))
   im=sources[row['name']];ratio=65.28/148*398/384;small=im.resize((round(320*ratio),round(320*ratio)),Image.Resampling.LANCZOS)
   board.paste(small,(col*200+round(100-160*ratio),line*425+225+round(130-224*ratio)),small)
   d.text((col*200+3,line*425+3),f"{row['tick']} {row['state']} bridge={row['bridgeActive']}",fill='white')
   d.text((col*200+3,line*425+407),f"water {row['water']:.3f}",fill='white')
  file=f'{gear}-{phase}-all-frames.png';board.save(P/file);boards.append(file)
  for kind,pictures in [('native',[native[x['name']] for x in group]),('source',[sources[x['name']] for x in group])]:
   f=P/f'{gear}-{phase}-{kind}.png';pictures[0].save(f,save_all=True,append_images=pictures[1:],duration=durations,loop=0,disposal=0,blend=0)
   cursor=0
   with Image.open(f) as apng:
    for index in range(apng.n_frames):
     apng.seek(index);left=round(apng.info['duration']);a=apng.convert('RGBA').tobytes()
     while left>0:assert a==pictures[cursor].tobytes();left-=durations[cursor];cursor+=1;decoded+=1
     assert left==0
   assert cursor==len(group)
  sections.append(f'<h2>{gear} {phase}</h2><div><img src="{gear}-{phase}-native.png"><img src="{gear}-{phase}-source.png"></div><img src="{file}">')
(P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill live land-water bridge</title><style>body{background:#182932;color:#ddd;font:16px sans-serif;margin:24px}img{max-width:100%}div{display:flex}</style><h1>Bill West — staged moving land/water bridge</h1><p>Actual normal actor navigation/needs/safety, fixture bridge and water treatment. Simulation60Hz; native capture every boundary tick, camera/room retained. Dynamic exact outgoing/incoming phases and combined pose envelope guard. Prescribed water/path, no natural hydrology or normal production admission. Synthetic interruption guards reviewed separately. West exit remains normal source; checkpoints/Continue and continuous motion/master material acceptance pending.</p>'+''.join(sections),encoding='utf-8')
(P/'review.json').write_text(json.dumps(dict(validation=v,checks=data['checks'],captureFilesSHA256=inputs,sourceRegistration=registered,boards=boards,decodedCaptureIntervals=decoded,events=[x for x in data['records'] if x['name'].endswith('-bridge-events')],scope='90 advancing60Hz entry boundary presentations/180original source-room files;4APNGs verify180decoded capture intervals. Same physical root/H148. Fixture source bridge, prescribed route/water. Native visual acceptance separate.'),indent=2)+'\n',encoding='utf-8')
e=json.loads((P/'review.json').read_text(encoding='utf-8'))
e['supplementalCurrentManifestSHA256']=current_manifest_hashes
e['normalInventoryScope']='Historical flood inventory supplemented by current selected West walking manifests and exact captured RGBA matches. Supplemental walking artwork was not included in the prelaunch 26-input freeze; these matches do not establish whole normal-bank pre/post stability.'
(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'presentations':len(rows),'originalSourceRoomFiles':len(inputs),'decodedIntervals':decoded,'boards':boards,'events':[x for x in data['records'] if x['name'].endswith('-bridge-events')]}))
