from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
H=Path(__file__).resolve().parent;R=H.parents[1];P=R/'character/krusher-animation-package-v8';O=H/'review/final';O.mkdir(exist_ok=True,parents=True)
index=json.loads((P/'package.json').read_text());cache={}
def row(g,key):
 q=index['states'][g+':'+key];mp=P/q['manifest'];m=cache.setdefault(str(mp),json.loads(mp.read_text()));s=next(s for s in m['states'] if s['id']==key);return mp,m,s
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),18)
prefixes=['idle','walk','interact','kneel','repair','stand','torch-draw','weld','torch-stow','carry','pickup','unload','sit-down','sit-idle','sit-rise','read-seated','eat','drink','lie-down','sleep','get-up','recover-air','salvage','death-ground','death-water','swim','swim-start','swim-stop','swim-carry','swim-pickup','swim-distress','tread']
records=[]
for page in range(8):
 board=Image.new('RGBA',(1200,1640),'#252e32');draw=ImageDraw.Draw(board)
 for group,prefix in enumerate(prefixes[page*4:page*4+4]):
  for gearindex,gear in enumerate(['bare','helmet']):
   for di,d in enumerate(['south','east','north','west']):
    key=prefix+'-'+d
    if gear+':'+key not in index['states']:continue
    mp,m,s=row(gear,key);i=len(s['frameFiles'])//2;im=Image.open(mp.parent/s['frameFiles'][i]).convert('RGBA');box=im.getbbox();crop=im.crop(box)
    x=di*300+20;y=(group*2+gearindex)*205+24
    # Native 1x body. Source density and tall terminal canvas remain unchanged.
    board.alpha_composite(crop,(x+(260-crop.width)//2,y));draw.text((x,y+173),gear+' / '+key,font=font,fill='white');records.append({'state':gear+':'+key,'frame':i,'board':f'family-{page:02d}.png','display':'native 1x opaque bounds crop'})
 board.save(O/f'family-{page:02d}.png')
for family in ['repair','bunk','water']:
 folder=H/'review'/family
 if not (folder/'report.json').exists():continue
 report=json.loads((folder/'report.json').read_text());rows=report.get('records',[]);selected=[]
 if family=='repair':
  for g in ['bare','helmet']:
   for d in ['east','south','west','north']:
    candidates=[q for q in rows if q['gear']==g and q['direction']==d]
    selected.extend(candidates[i] for i in [0,len(candidates)//2,len(candidates)-1])
 else:selected=rows[::max(1,len(rows)//20)][:24]
 if not selected:continue
 board=Image.new('RGBA',(1200,((len(selected)+5)//6)*230),'#252e32');draw=ImageDraw.Draw(board)
 for i,q in enumerate(selected):
  im=Image.open(folder/q['file']).convert('RGBA');foot=q.get('screenFoot');x=i%6*200;y=i//6*230
  if foot:
   fx,fy=foot
   if family=='water':crop=im.crop((round(fx)-95,round(fy)-95,round(fx)+95,round(fy)+95))
   else:crop=im.crop((round(fx)-90,round(fy)-150,round(fx)+90,round(fy)+40))
   board.alpha_composite(crop,(x+10,y))
  else:board.alpha_composite(im.resize((200,125)),(x,y+25))
  draw.text((x+3,y+195),q.get('label',q.get('key',''))[:26],font=font,fill='white')
 board.save(O/(family+'-station.png'))
(O/'review-index.json').write_text(json.dumps({'sourceSamples':records,'scope':'Every dry/life/water family, cardinal facings and both gears at native size; representative midposes. Static review is separate from complete motion/owner acceptance.'},indent=2)+'\n')
print(json.dumps({'familyBoards':8,'sourceSamples':len(records)}))


