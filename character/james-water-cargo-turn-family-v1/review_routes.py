from pathlib import Path
from PIL import Image,ImageDraw
import json,sys
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1];installed='--installed' in sys.argv
report=json.loads((P/('installed-route-evidence.json' if installed else 'route-evidence.json')).read_bytes())
for mode in ['bare','helmet']:
 for kind,count in [('quarters',6),('halves',11)]:
  rows=[s for s in report['results'] if s['mode']==mode and s.get('completed') and len(s['seenSlots'])==count]
  board=Image.new('RGB',(1320,len(rows)*180),'#303b40');draw=ImageDraw.Draw(board)
  for row,s in enumerate(rows):
   for col,index in enumerate(np.linspace(0,len(s['captures'])-1,6).round().astype(int)):
    file=R/s['captures'][index].removeprefix('res://');im=Image.open(file).convert('RGB');x=im.width//2;y=im.height//2;crop=im.crop((x-105,y-72,x+105,y+78));board.paste(crop,(col*220,row*180+25));draw.text((col*220+3,row*180+4),s['clip'].replace('swim-carry-turn-','')+' '+str(index),fill='white')
  board.save(P/('native-'+('installed-' if installed else '')+'route-'+mode+'-'+kind+'.png'))
print('Four actual-frame route contacts generated from authoritative report capture lists')
