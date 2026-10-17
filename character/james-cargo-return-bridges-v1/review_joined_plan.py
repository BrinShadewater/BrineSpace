from pathlib import Path
import json,re
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
branch=(r/'scripts/grid_canvas.gd').read_text().split('elif actor == "branforth":',1)[1].split('\n\t\tset(actor+',1)[0]
banks={'bare':{},'helmet':{}}
for kind,rel in re.findall(r'player\.(load_manifest|load_equipment_manifest)\([^\n]*?"res://([^"\n]+\.json)"',branch):
 path=r/rel;pack=json.loads(path.read_bytes());mode='bare' if kind=='load_manifest' else 'helmet'
 for state in pack['states']:
  if state.get('frameFiles'):banks[mode][state['id']]=[(path.parent/f).resolve() for f in state['frameFiles']]
for mode in banks:
 pack=json.loads((p/(mode+'-joined-manifest-v4.json')).read_bytes())
 banks[mode]['carry-settle-west']=[r/f.removeprefix('res://') if f.startswith('res://') else p/f for f in pack['states'][0]['frameFiles']]
report=json.loads((p/'joined-plan-v4-evidence.json').read_bytes())
plans=[]
for mode in ('bare','helmet'):
 gear='' if mode=='bare' else 'diving-helmet'
 plans.append(next(x for x in report['plans'] if x['gear']==gear and x['source']=='carry-turn-east-west' and x['sourceIndex']==10))
assert plans[0]['rows']==plans[1]['rows']
rows=plans[0]['rows'];frames=[]
for j,row in enumerate(rows):
 frame=Image.new('RGB',(512,256),'#303b40')
 for i,mode in enumerate(('bare','helmet')):
  im=Image.open(banks[mode][row['key']][row['index']]).convert('RGBA');assert im.size==(256,256)
  frame.paste(im,(i*256,0),im)
 frames.append(frame)
for part in range(2):
 subset=rows[part*5:(part+1)*5];board=Image.new('RGB',(len(subset)*256,576),'#303b40');draw=ImageDraw.Draw(board)
 for col,row in enumerate(subset):
  for i,mode in enumerate(('bare','helmet')):
   im=Image.open(banks[mode][row['key']][row['index']]).convert('RGBA');x=col*256;y=i*288
   draw.text((x+3,y+4),f"{mode} {row['key']} / {row['index']}",fill='white')
   draw.text((x+3,y+17),f"{round(row['seconds']*1000)} ms",fill='white')
   board.paste(im,(x,y+30),im);draw.line((x,y+254,x+255,y+254),fill='#929d9f')
 board.save(p/f'joined-return-v4-part{part+1}.png')
# One common palette prevents palette changes between review frames. Terminal
# hold and repeat are viewer reset behavior, not an authored loop or controller.
strip=Image.new('RGB',(512,len(frames)*256))
for i,frame in enumerate(frames):strip.paste(frame,(0,i*256))
palette=strip.quantize(colors=255)
encoded=[frame.quantize(palette=palette,dither=Image.Dither.NONE) for frame in frames]
durations=[round(row['seconds']*1000) for row in rows];durations[-1]+=700
encoded[0].save(p/'joined-return-v4-review.gif',save_all=True,append_images=encoded[1:],duration=durations,loop=0,disposal=2)
(p/'joined-return-v4-review.json').write_text(json.dumps({'rows':rows,'selected':False,'visualReviewPending':True,'scope':'Paired authored-source plan replay, exact loaded endpoint refs, registered original256/p128224/H148. Static sequence boards and GIF; no world/controller movie or seamless review reset claim.'},indent=2)+'\n')
print(f'{len(rows)}paired source slots presented across two boards and finite-source replay GIF.')
