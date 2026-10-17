from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent
for pair in ['east-south','south-west','west-north','north-east']:
 p=P.parent/('james-water-cargo-turn-'+pair+'-v1'); board=Image.new('RGB',(2700,450),'#303b40'); d=ImageDraw.Draw(board)
 for i in range(6):
  im=Image.open(p/'source-crops'/f'{i:03d}.png').convert('RGBA'); board.paste(im,(i*450,35),im)
  d.text((i*450+5,5),pair+' / crop '+str(i),fill='white')
  for x in range(0,450,40):d.line((i*450+x,30,i*450+x,435),fill='#596166');d.text((i*450+x+2,20),str(x),fill='white')
  for y in range(0,400,40):d.line((i*450,35+y,i*450+440,35+y),fill='#596166');d.text((i*450+2,35+y),str(y),fill='white')
 board.save(p/'head-rulers.png')
