from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
CAP=ROOT/'output/bill-land-water-material-west-v8'
for gear in ['bare','helmet']:
 for family,ticks in [('entry',[67,71,75,79,84,89,94,97]),('exit',[415,419,422,426,430,435,439,444])]:
  if not all((CAP/f'{gear}-{t:03}-candidate-room.png').exists() for t in ticks):continue
  board=Image.new('RGB',(1000,390),(23,42,51));draw=ImageDraw.Draw(board)
  for i,t in enumerate(ticks):
   im=Image.open(CAP/f'{gear}-{t:03}-candidate-room.png').convert('RGB').crop((425,490,675,660) if family=='entry' else (275,490,525,660))
   x=(i%4)*250;y=(i//4)*195
   board.paste(im,(x,y+25));draw.text((x+4,y+5),f'{gear} {family} tick{t} / native crop',fill='white')
  board.save(OUT/f'{gear}-{family}-native-review.png')
print('Available native crop boards saved; original screenshots remain in interval output.')
