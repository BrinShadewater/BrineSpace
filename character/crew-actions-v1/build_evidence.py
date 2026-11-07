"""Review media and collision metadata from Godot-exported, fitted textures."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output'
scale=384*.17/74
data={}
for actor in ['bill','veld','branforth']:
 data[actor]={}
 for eq in ['bare','helmet']:
  bounds={}
  for state in ['salvage','swim-carry','transition']:
   for facing in ['east','south','west','north']:
    paths=list(OUT.glob(f'crew-action-{actor}-swim-*-{eq}.png')) if state=='transition' else [OUT/f'crew-action-{actor}-{state}-{facing}-{eq}.png']
    rectangles=[]
    for p in paths:
     im=Image.open(p)
     for x in range(0,im.width,128):
      box=im.crop((x,0,x+128,128)).getbbox()
      if box:rectangles.append([(v-64)*scale for v in box])
    bounds[state+'-'+facing]=[round(min(r[0] for r in rectangles),3),round(min(r[1] for r in rectangles),3),round(max(r[2] for r in rectangles),3),round(max(r[3] for r in rectangles),3)]
  data[actor][eq]=bounds
(ROOT/'character/crew-actions-v1/clearance.json').write_text(json.dumps(data,indent=2)+'\n')
clips=json.loads((OUT/'crew-action-review.json').read_text())
examples=[('salvage-east',1,'Salvage'),('swim-turn-east-west',1,'Swimming turn'),('torch-draw-east',0,'Draw torch'),('unload-east',0,'Unload'),('repair-west',0,'Repair / inspect')]
frames=[]
for step in range(30):
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
frames[0].save(OUT/'crew-actions-preview.gif',save_all=True,append_images=frames[1:],duration=70,loop=0,disposal=2)
print('Fitted clearance metadata and moving showcase exported')
