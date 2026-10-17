"""Cross-direction audit with unchanged fitted pixels and manifest clocks."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent; R=P.parents[1]
packs={d:R/f'character/veld-seated-{d}-coherent-v1' for d in ('north','east','south','west')}
data={d:{gear:json.loads((pack/f'{gear}-manifest.json').read_text()) for gear in ('bare','helmet')} for d,pack in packs.items()}
board=Image.new('RGB',(1024,1596),'#202a30'); draw=ImageDraw.Draw(board); records=[]; bound={}
for col,(direction,pack) in enumerate(packs.items()):
 for gear_index,gear in enumerate(('bare','helmet')):
  m=data[direction][gear]; down=m['states'][0]; held=next(s for s in m['states'] if s['id']==f'sit-idle-{direction}')
  assert m['pivot']==[128,224] and m['standingHeight']==148 and sum(down['frameDurationsMs'])==800
  for pose_index,(name,file) in enumerate([('Standing',down['frameFiles'][0]),('Lowering',down['frameFiles'][2]),('Seated',held['frameFiles'][0])]):
   path=pack/file; im=Image.open(path).convert('RGBA'); assert im.size==(256,256)
   x=col*256; y=(gear_index*3+pose_index)*266; board.paste(im,(x,y+10),im); draw.text((x+5,y+2),f'{direction} / {gear} / {name}',fill='white')
   bbox=im.getchannel('A').point(lambda a:255 if a>180 else 0).getbbox()
   records.append({'direction':direction,'gear':gear,'pose':name,'occupiedOpaqueHeight':bbox[3]-bbox[1],'opaqueBounds':bbox,'source':path.relative_to(R).as_posix()})
   bound[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
board.save(P/'family-review.png')
# Eight unchanged pose lanes replay a complete lower/held/rise chain at one clock.
sequence=[(i,t) for i,t in enumerate(data['west']['bare']['states'][0]['frameDurationsMs'])]+[(5,1200)]+[(i,t) for i,t in zip(range(5,-1,-1),data['west']['bare']['states'][1]['frameDurationsMs'])]+[(0,800)]
frames=[]; durations=[]; cumulative=0; previous=0
for slot,time in sequence:
 frame=Image.new('RGB',(1024,550),'#202a30'); d=ImageDraw.Draw(frame)
 for col,(direction,pack) in enumerate(packs.items()):
  for row,gear in enumerate(('bare','helmet')):
   file=data[direction][gear]['states'][0]['frameFiles'][slot]; im=Image.open(pack/file).convert('RGBA')
   frame.paste(im,(col*256,row*275+15),im); d.text((col*256+5,row*275+2),f'{direction} / {gear} / source{slot}',fill='white')
   bound[(pack/file).relative_to(R).as_posix()]=hashlib.sha256((pack/file).read_bytes()).hexdigest()
 cumulative+=time*3; edge=round(cumulative/10)*10; durations.append(edge-previous); previous=edge; frames.append(frame)
frames[0].save(P/'family-motion.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2)
with Image.open(P/'family-motion.gif') as im:
 total=0
 for i in range(im.n_frames):im.seek(i);total+=im.info['duration']
 assert total==sum(t for _,t in sequence)*3
report={'scope':'unchanged fitted source cross-direction diagnostic, not native chair or motion acceptance','records':records,'motionRuntimeCycleMs':sum(t for _,t in sequence),'previewCycleMs':total,'bindings':bound,'reviewPending':['seated pelvis/head/seat-height comparison','complete motion and joins','native matching chair context and fresh Continue','source selection and owner acceptance']}
(P/'family-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'comparedPoses':len(records),'boundFiles':len(bound),'previewCycleMs':total,'bareSeatedHeights':{r['direction']:r['occupiedOpaqueHeight'] for r in records if r['gear']=='bare' and r['pose']=='Seated'}}))
