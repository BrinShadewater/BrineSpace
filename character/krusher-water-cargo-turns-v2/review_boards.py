from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent
for gear in ['bare','helmet']:
 for family in ['cargo','turn','cargo-turn']:
  states=json.load(open(P/f'{family}-{gear}-manifest.json'))['states'];board=Image.new('RGB',(2816,len(states)*300),'#242c31');d=ImageDraw.Draw(board)
  for row,s in enumerate(states):
   d.text((8,row*300+3),s['id'],fill='white')
   for col,f in enumerate(s['frameFiles']):
    im=Image.open(P/f).convert('RGBA');board.paste(im,(col*256,row*300+24),im)
  board.save(P/f'{family}-{gear}-chronology.png')
records=[q for q in json.load(open(P/'provenance.json'))['records'] if q['gear']=='bare']
for part in range((len(records)+9)//10):
 group=records[part*10:part*10+10];board=Image.new('RGB',(900,len(group)*150),'#242c31');d=ImageDraw.Draw(board)
 for row,q in enumerate(group):
  b=q['headBox'];crop=(b[0]-18,b[1]-20,b[2]+18,b[3]+20)
  for col,path in enumerate([R/q['source'],P/q['output']]):
   im=Image.open(path).convert('RGBA').crop(crop);im=im.resize((im.width*2,im.height*2));board.paste(im,(col*300,row*150+15),im)
  d.text((620,row*150+5),f"{q['state']} {q['frame']}\n{q['headBox']}",fill='white')
 board.save(P/f'head-detail-{part}.png')
