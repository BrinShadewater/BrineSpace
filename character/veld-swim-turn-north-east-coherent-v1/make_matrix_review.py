"""Same-clock review and physical-scale contact boards for all staged quarters."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1];tracks={};families=['east-south','south-west','west-north','north-east']
for family in families:
 folder='veld-swim-turn-'+family+'-coherent-v1';source=R/'character'/folder
 for variant in ['bare','helmet']:
  m=json.loads((source/f'{variant}-manifest.json').read_text())
  for turn in m['states']:
   direction=turn['id'].removeprefix('swim-turn-');track=[]
   for d in direction.split('-'):
    loop=next(s for s in json.loads((R/f'character/veld-water-{d}-coherent-v1/{variant}-manifest.json').read_text())['states'] if s['id']=='swim-'+d);files=['../veld-water-'+d+'-coherent-v1/'+p for p in loop['frameFiles']]
    if not track:
     track.extend(dict(file=p,duration=t,key=loop['id'],slot=i) for i,(p,t) in enumerate(zip(files,loop['frameDurationsMs'])))
     track.extend(dict(file='../'+folder+'/'+p,duration=t,key=turn['id'],slot=i) for i,(p,t) in enumerate(zip(turn['frameFiles'],turn['frameDurationsMs'])))
    else:
     track.extend(dict(file=p,duration=t,key=loop['id'],slot=i) for i,(p,t) in enumerate(zip(files,loop['frameDurationsMs'])))
     track.append(dict(file=files[0],duration=1,key='destination frame0 hold',slot=0))
   tracks.setdefault(direction,{})[variant]=track
for direction,pair in tracks.items():assert len(pair['bare'])==len(pair['helmet'])==19 and all(b['duration']==e['duration'] for b,e in zip(pair['bare'],pair['helmet']))
for variant in ['bare','helmet']:
 board=Image.new('RGBA',(1536,1120),'#202a30');draw=ImageDraw.Draw(board)
 for row,family in enumerate(families):
  source=R/'character'/('veld-swim-turn-'+family+'-coherent-v1');m=json.loads((source/f'{variant}-manifest.json').read_text());state=next(s for s in m['states'] if s['id']=='swim-turn-'+family)
  for i,p in enumerate(state['frameFiles']):board.alpha_composite(Image.open(source/p).convert('RGBA'),(i*256,row*280+24))
  draw.text((4,row*280+4),variant+' '+family+' / exact loop0 endpoints; authored interiors',fill='white')
 board.save(H/f'all-quarter-{variant}-contact-v1.png')
html=(H/'review-template.html').read_text(encoding='utf-8');start=html.index('<select id="direction">');end=html.index('</select>',start)+len('</select>');html=html[:start]+'<select id="direction">'+''.join('<option>'+d+'</option>' for d in tracks)+'</select>'+html[end:]
html=html.replace('Veld north/east swim turn','Veld swimming quarter turns').replace('Veld — north/east swimming turn','Veld — swimming quarter turns').replace('Four authored body/helmet angles join the exact selected water loops. Shared source-family cloth, skin and science-patch grade; protected brown hair/silver streak. Bare and helmet share one clock. Staged; runtime bindings unchanged. Runtime turn520ms; review at one-third speed.','Eight quarter-turn directions join the selected swimming loops. Bare and helmet share one clock. Staged for the full proportions and motion review; playback at one-third speed.').replace('bare-turn-contact-v1.png','all-quarter-bare-contact-v1.png').replace('helmet-fit-contact-v1.png','all-quarter-helmet-contact-v1.png').replace('Head and collar detail','All helmet poses').replace('TRACKS',json.dumps(tracks,separators=(',',':')))
(H/'quarter-matrix.html').write_text(html,encoding='utf-8');(H/'quarter-review-checks.json').write_text(json.dumps(dict(directions=len(tracks),states=len(tracks)*2,turnReferences=len(tracks)*2*6,pairedClocks=True,installed=False),indent=2)+'\n');print('8 paired directions/16 states/96 turn refs; finite matrix review and2 contact boards generated')
