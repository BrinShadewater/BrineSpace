from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent
records=json.load(open(P/'provenance.json'))['records']
for gear in ['bare','helmet']:
 states=json.load(open(P/(gear+'-manifest.json')))['states']
 for part in range(3):
  group=states[part*5:part*5+5];board=Image.new('RGB',(1792,1400),(35,42,48));d=ImageDraw.Draw(board)
  for row,s in enumerate(group):
   d.text((8,row*280+4),s['id'],fill='white')
   for col,f in enumerate(s['frameFiles']):
    im=Image.open(P/f).convert('RGBA');board.paste(im,(col*256,row*280+24),im)
  board.save(P/f'{gear}-chronology-{part}.png')
sel=[q for q in records if q['gear']=='bare']
for part in range(5):
 group=sel[part*10:part*10+10];board=Image.new('RGB',(900,len(group)*170),(35,42,48));d=ImageDraw.Draw(board)
 for row,q in enumerate(group):
  box=q['headBox'];crop=(box[0]-18,box[1]-22,box[2]+28,box[3]+25)
  for col,path in enumerate([R/q['source'],P/q['output']]):
   im=Image.open(path).convert('RGBA').crop(crop);im=im.resize((im.width*2,im.height*2));board.paste(im,(col*300,row*170+16),im)
  d.text((610,row*170+10),f"{q['state']} {q['frame']}\nbox {box}\nneck {q['neck']}\npaste {q['headPaste']}",fill='white')
 board.save(P/f'tracking-detail-{part}.png')
