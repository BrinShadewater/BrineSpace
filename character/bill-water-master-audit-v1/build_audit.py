from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent
banks={
 'east':{'entry':{'bare':'character/bill-land-water-east-v3/manifest.json','helmet':'character/bill-land-water-helmet-east-v1/manifest.json'},'exit':{'bare':'character/bill-water-exit-east-v2/manifest.json','helmet':'character/bill-water-exit-helmet-east-v1/manifest.json'}},
 'west':{'entry':{'bare':'character/bill-land-water-west-v4/bare/manifest.json','helmet':'character/bill-land-water-west-v4/helmet/manifest.json'},'exit':{'bare':'character/bill-water-exit-west-v1/bare/manifest.json','helmet':'character/bill-water-exit-west-v1/helmet/manifest.json'}},
 'north':{'entry':{'bare':'character/bill-land-water-north-v3/bare/manifest.json','helmet':'character/bill-land-water-north-v3/helmet/manifest.json'},'exit':{'bare':'character/bill-water-exit-north-v1/bare/manifest.json','helmet':'character/bill-water-exit-north-v1/helmet/manifest.json'}},
 'south':{'entry':{'bare':'character/bill-land-water-south-v2/bare/manifest.json','helmet':'character/bill-land-water-south-v2/helmet/manifest.json'},'exit':{'bare':'character/bill-water-exit-south-v4/bare/manifest.json','helmet':'character/bill-water-exit-south-v4/helmet/manifest.json'}}}
masters={'east':('character/bill-land-water-east-v3/master-relative-review.png',(0,25,320,345),'Original side sheet east at148/956; existing registered reference crop'), 'west':('character/bill-land-water-west-v4/master-comparison.png',(0,25,320,345),'Original side sheet west at148/956; existing registered reference crop'), 'north':('character/bill-video-north-v5/master-standing.png',None,'Original rear v5 prepared standing184canvas,p92/172,H148,148/976 density'), 'south':('character/bill-water-exit-south-v4/master-comparison.png',(1280,25,1600,345),'Original frontal master at148/1295; existing registered reference crop')}
inputs={};rows=[];frameCount=0
def read(path):
 f=R/path;inputs[path]=hashlib.sha256(f.read_bytes()).hexdigest();return Image.open(f).convert('RGBA')
def canvas(im,pivot,height):
 factor=148/height;im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(320,352));out.alpha_composite(im,(round(160-pivot[0]*factor),round(224-pivot[1]*factor)));return out
normal={}
for gear,file in [('bare','character/crew-runtime-matte-v1/bill/manifest.json'),('helmet','character/bill-shared-helmet-runtime-v2/manifest.json')]:
 f=R/file;inputs[file]=hashlib.sha256(f.read_bytes()).hexdigest();m=json.loads(f.read_text(encoding='utf-8'))
 for direction in banks:
  state=next(s for s in m['states'] if s['id']=='idle-'+direction)
  path=(f.parent/state['frameFiles'][0]).relative_to(R).as_posix();normal[gear,direction]=(canvas(read(path),m['pivot'],m['standingHeight']),path)
for direction,phases in banks.items():
 file,box,scope=masters[direction];im=read(file)
 if box:master=canvas(im.crop(box),[160,224],148)
 else:master=canvas(im,[92,172],148)
 board=Image.new('RGB',(1980,900),'#182932');d=ImageDraw.Draw(board);d.text((10,8),direction.upper()+' - common H148 / foot224; no per-pose fit; bare master repeated for identity only',fill='white')
 for ri,(phase,gear) in enumerate([(p,g) for p in ['entry','exit'] for g in ['bare','helmet']]):
  y=35+ri*215;file=phases[phase][gear];f=R/file;inputs[file]=hashlib.sha256(f.read_bytes()).hexdigest();m=json.loads(f.read_text(encoding='utf-8'));key=('land-swim-' if phase=='entry' else 'swim-land-')+direction;state=next(s for s in m['states'] if s['id']==key)
  frames=[];paths=[]
  for rel in state['frameFiles']:
   path=(f.parent/rel).relative_to(R).as_posix();frames.append(canvas(read(path),m['pivot'],m['standingHeight']));paths.append(path)
  frameCount+=len(frames);r=dict(direction=direction,phase=phase,gear=gear,manifest=file,key=key,frameFiles=paths,sourcePivot=m['pivot'],sourceHeight=m['standingHeight'],normalIdleSource=normal[gear,direction][1],masterReference=masters[direction][0],masterScope=scope);rows.append(r)
  for ci,(label,im) in enumerate([('bare master',master),(gear+' normal idle',normal[gear,direction][0])]+[(phase+' '+str(i),im) for i,im in enumerate(frames)]):
   tile=im.resize((180,198),Image.Resampling.LANCZOS);board.paste(tile,(ci*180,y+16),tile);d.text((ci*180+3,y),label,fill='white');d.line((ci*180,y+16+round(224*180/320),ci*180+179,y+16+round(224*180/320)),fill='#416165')
 board.save(P/(direction+'-audit.png'))
report=dict(frameSlots=frameCount,rows=rows,inputsSHA256=inputs,scope='Static source cross-family audit; directional master references and actual current normal idle manifests; shared physicalH148 canvas320x352,p160/224. No per-pose fitting, mirroring, grading or source mutation. Master reference board crops retain prior registrations. Bare master is repeated for identity, not helmet shape proof. No new native/profile interval or full visual acceptance.',visualReview='Pending all4direction board inspection.')
(P/'audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html='<!doctype html><meta charset="utf-8"><title>Bill water master audit</title><style>body{background:#182932;color:#eef;font:17px sans-serif;margin:24px}img{max-width:100%}a{color:#9cd5e4;margin-right:20px}</style><h1>Bill water transitions - master consistency</h1><p>Shared physical scale and foot registration. Each row compares the bare master, current normal idle and the complete transition. Art and runtime selections unchanged; source review only.</p><nav>'
for direction in banks:html+=f'<a href="#{direction}">{direction.capitalize()}</a>'
html+='</nav>'
for direction in banks:html+=f'<h2 id="{direction}">{direction.capitalize()}</h2><img src="{direction}-audit.png" alt="{direction} master idle entry exit comparison">'
(P/'index.html').write_text(html,encoding='utf-8');print(json.dumps(dict(frameSlots=frameCount,rows=len(rows),frozenInputs=len(inputs))))
