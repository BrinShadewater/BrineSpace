from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'bill-land-water-runtime-east-v1'
s=(OLD/'build_review.py').read_text().replace('bill-land-water-runtime-east-v1','bill-land-water-material-east-v2')
exec(compile(s,str(P/'build_review.py'),'exec'),{'__file__':str(P/'build_review.py')})
data=json.loads((R/'output/bill-land-water-material-east-v2/records.json').read_text());prior=json.loads((R/'output/bill-land-water-runtime-east-v1/records.json').read_text())
oldrows={x['name']:x for x in prior['records'] if x['name'].endswith('-candidate')};rows=[x for x in data['records'] if x['name'].endswith('-candidate')]
for row in rows:
 old=oldrows[row['name']];assert row['foot']==old['foot'] and row['water']==old['water'] and row['state']==old['state'] and row['direction']==old['direction']
 assert Image.open(P/'captures'/f"{row['name']}-source.png").convert('RGBA').tobytes()==Image.open(OLD/'captures'/f"{row['name']}-source.png").convert('RGBA').tobytes()
board=Image.new('RGB',(1600,900),'#182932');d=ImageDraw.Draw(board)
for line,(gear,ticks) in enumerate([('bare',[69,70,76,82]),('helmet',[69,70,76,82]),('bare',[420,421,440,442]),('helmet',[420,421,440,442])]):
 for col,tick in enumerate(ticks):
  row=next(x for x in rows if x['name']==f'{gear}-{tick:03}-candidate');x=255+(row['foot'][0]-7680)*398/384;y=287+(row['foot'][1]-8064)*398/384
  box=(round(x)-100,round(y)-130,round(x)+100,round(y)+70)
  for offset,root in [(0,OLD),(200,P)]:
   im=Image.open(root/'captures'/f"{row['name']}-room.png").crop(box);board.paste(im,(col*400+offset,line*225+20))
  d.text((col*400+4,line*225+3),f'{gear} {tick}: old | blended',fill='white')
board.save(P/'material-comparison.png')
e=json.loads((P/'review.json').read_text());e.update(sourceArtRGBAExactToPrior=True,all190WorldPositionsWaterStatesExactToPrior=True,materialParameters=[{k:x[k] for k in ['name','materialWeight','materialHeadOffset','water','bridgeActive']} for x in rows],scope='Actual same190source/world/water boundary presentations, with per-instance continuous material blend and pose-registered head highlight.8APNG380decoded intervals. Normal outside-bridge renderer/art unchanged; native visual acceptance separate.');(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
html=(P/'index.html').read_text(encoding='utf-8').replace('Bill East — staged moving land/water bridge','Bill East — continuous transition water treatment').replace('<h2>bare enter','<img src="material-comparison.png"><h2>bare enter',1);(P/'index.html').write_text(html,encoding='utf-8')
print('All190source RGBA/world positions/water/states exact to prior; before/after native material comparison prepared.')
