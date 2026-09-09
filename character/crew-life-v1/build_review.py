"""Build local motion review and conservative pose bounds from native exports."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output'
clips=json.loads((OUT/'crew-life-review.json').read_text())
template=(ROOT/'character/crew-actions-v1/build_review.py').read_text()
template=template.replace('crew-action-review.json','crew-life-review.json').replace('crew-actions-review.html','crew-life-review.html').replace('Crew actions','Crew life').replace('Salvage, swimming transitions, torch handling, cargo, and directional work.','Sitting, meals, sleep, oxygen distress, pickups, reading, carrying turns and directional deaths. All three architects. Native fitted sprites; visual acceptance pending.')
start=template.index('const titles=');end=template.index(';',start)
titles={k:k.replace('-',' ').capitalize() for k in ['sit-down','sit-idle','sit-rise','eat','drink','lie-down','sleep','get-up','swim-distress','recover-air','pickup','swim-pickup','read-seated','inspect','carry-turn','swim-carry-turn','death-ground','death-water']}
template=template[:start]+'const titles='+json.dumps(titles)+template[end:]
template=template.replace("clip.key.startsWith('swim-turn-')?'swim-turn':clip.key.slice(0,clip.key.lastIndexOf('-'))","clip.key.includes('-turn-')?clip.key.slice(0,clip.key.indexOf('-turn-')+5):clip.key.slice(0,clip.key.lastIndexOf('-'))")
exec(compile(template,str(__file__),'exec'))
examples=[('sit-down-west',0,'Sit down'),('eat-east',0,'Eat'),('sleep-east',0,'Sleep'),('swim-pickup-west',1,'Pick up cargo'),('carry-turn-north-west',0,'Carry turn')]
frames=[]
for step in range(48):
 canvas=Image.new('RGB',(800,495),'#17262d');draw=ImageDraw.Draw(canvas)
 for col,(_,_,label) in enumerate(examples):draw.text((col*160+14,12),label,fill='#c0e6df')
 for row,actor in enumerate(['bill','veld','branforth']):
  draw.text((12,42+row*150),{'bill':'Major Bill','veld':'Dr. Veld','branforth':'Chief Branforth'}[actor],fill='white')
  for col,(key,equipment,_) in enumerate(examples):
   clip=next(c for c in clips[actor] if c['key']==key)
   t=(step*70)%(sum(clip['durations'])+(0 if clip['loop'] else 500));index=0
   while index<len(clip['durations'])-1 and t>=clip['durations'][index]:t-=clip['durations'][index];index+=1
   im=Image.open(OUT/clip['files'][equipment]).crop((index*128,0,(index+1)*128,128))
   canvas.paste(im,(col*160+16,row*150+62),im)
 frames.append(canvas)
frames[0].save(OUT/'crew-life-preview.gif',save_all=True,append_images=frames[1:],duration=70,loop=0,disposal=2)
scale=384*.17/74
data={}
for actor in clips:
 data[actor]={}
 for eq in ['bare','helmet']:
  bounds={}
  for state in ['swim-distress','cargo-turn']:
   for facing in ['east','south','west','north']:
    paths=list(OUT.glob(f'crew-life-{actor}-swim-carry-turn-*-{eq}.png')) if state=='cargo-turn' else [OUT/f'crew-life-{actor}-{state}-{facing}-{eq}.png']
    rectangles=[]
    for path in paths:
     im=Image.open(path)
     for x in range(0,im.width,128):
      box=im.crop((x,0,x+128,128)).getbbox()
      if box:rectangles.append([(v-64)*scale for v in box])
    bounds[state+'-'+facing]=[round(min(r[0] for r in rectangles),3),round(min(r[1] for r in rectangles),3),round(max(r[2] for r in rectangles),3),round(max(r[3] for r in rectangles),3)]
  data[actor][eq]=bounds
(ROOT/'character/crew-life-v1/clearance.json').write_text(json.dumps(data,indent=2)+'\n')
print('Life showcase and fitted collision bounds exported')
