from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;pr=json.load(open(R/'character/krusher-complete-animation-v1/progress.json'));groups=[]
for action in ['idle','sit-idle','sleep','carry','swim','swim-carry','swim-distress','death']:
 group=[action+'-'+d for d in ['east','north','south','west'] if action+'-'+d in pr['coverage']['bare']['available']]
 if group:groups.append(group)
for page,rows in enumerate([groups[:4],groups[4:]]):
 board=Image.new('RGB',(1280,len(rows)*410),'#242c31');draw=ImageDraw.Draw(board)
 for row,group in enumerate(rows):
  for col,key in enumerate(group):
   mp=R/pr['coverage']['bare']['available'][key]['manifest'][6:];m=json.load(open(mp));s=next(v for v in m['states'] if v['id']==key);i=len(s['frameFiles'])//2;im=Image.open(mp.parent/s['frameFiles'][i]).convert('RGBA');scale=1.5;im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);pivot=m['pivot'];anchor=(col*320+160-round(pivot[0]*scale),row*410+(185 if key.startswith('swim') else 340)-round(pivot[1]*scale));board.paste(im,anchor,im);draw.text((col*320+8,row*410+8),key+' / pose'+str(i)+' / uniform1.5x',fill='white')
 board.save(P/f'full-body-review-{page}.png')
