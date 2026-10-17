from pathlib import Path
import argparse,json
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
p=argparse.ArgumentParser();p.add_argument('--start',type=int,required=True);p.add_argument('--end',type=int,required=True);p.add_argument('--name',required=True);a=p.parse_args()
nums=list(range(a.start,a.end+1));assert nums and len(nums)<=8 and all(0<=n<48 for n in nums)
bank=json.loads((OUT/'bank-assessment.json').read_text())
assert all(n in bank['frames'] for n in nums),'Segment includes absent/rejected candidate'
board=Image.new('RGB',(256*len(nums),1100),(23,42,51));d=ImageDraw.Draw(board)
for i,n in enumerate(nums):
 for row,src in enumerate([ROOT/f'character/bill-walk-west-material-v1/frames/helmet/walk-west/{n:03}.png',OUT/f'canvas-normalized-study-{n:03}.png']):
  im=Image.open(src).convert('RGBA');assert im.size==(256,256);x=i*256;y=row*330
  d.text((x+5,y+5),f'{n:03} '+('Selected' if row==0 else 'Candidate'),fill='white');board.paste(im,(x,y+25),im)
  crop=im.crop((99,65,155,122)).resize((168,171),Image.Resampling.NEAREST);y=660+row*210
  d.text((x+5,y+5),f'{n:03} helmet / collar',fill='white');board.paste(crop,(x,y+25),crop)
board.save(OUT/(a.name+'.png'))
print(json.dumps({'frames':nums,'review':a.name+'.png','scope':'Same canvas and fixed helmet/collar crops; source review only'}))
