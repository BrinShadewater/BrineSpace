from pathlib import Path
from PIL import Image,ImageDraw
import sys
P=Path(__file__).resolve().parent;installed='--installed' in sys.argv
for mode in ['bare','helmet']:
 board=Image.new('RGB',(1320,8*180),'#303b40');draw=ImageDraw.Draw(board)
 for row,(d,action) in enumerate((d,a) for d in ['east','south','west','north'] for a in ['distress','recovery']):
  for col in range(6):
   label=mode+'-'+action+'-'+d+'-'+str(col).zfill(3);im=Image.open(P/('installed-behaviour-captures' if installed else 'route-captures')/(label+'.png')).convert('RGB');x,y=im.width//2,im.height//2;crop=im.crop((x-105,y-100,x+105,y+50));at=(col*220,row*180+25);board.paste(crop,at);draw.text((at[0]+3,row*180+3),label,fill='white')
 board.save(P/('native-'+('installed-' if installed else '')+'behaviour-'+mode+'.png'))
print('Two actual state/clock capture boards,96 native captures')
