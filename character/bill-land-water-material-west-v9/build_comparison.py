from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
BASE=ROOT/'output/bill-land-water-material-west-v8'
FIT=ROOT/'output/bill-land-water-material-west-v9'
base=json.loads((BASE/'records.json').read_text())
fit=json.loads((FIT/'records.json').read_text())
lookup={x['name']:x for x in base['records']}
exact=[];changes=[]
for row in fit['records']:
 if 'tick' not in row:continue
 old=lookup[row['name']]
 for key in ['foot','clock','water','medium','state','direction','pathPoints','materialWeight']:
  assert row[key]==old[key],(row['name'],key)
 a=Image.open(BASE/(row['name']+'-source.png')).convert('RGBA')
 b=Image.open(FIT/(row['name']+'-source.png')).convert('RGBA')
 assert a.size==b.size and a.tobytes()==b.tobytes(),row['name']
 exact.append(row['name'])
for gear in ['bare','helmet']:
 for family,ticks in [('entry',[71,75,79,84,89]),('exit',[419,422,426,430,435,439])]:
  board=Image.new('RGB',(250*len(ticks),390),(23,42,51));draw=ImageDraw.Draw(board)
  for r,(tag,cap) in enumerate([('baseline',BASE),('source center',FIT)]):
   for i,t in enumerate(ticks):
    im=Image.open(cap/f'{gear}-{t:03}-candidate-room.png').convert('RGB').crop((425,490,675,660) if family=='entry' else (275,490,525,660))
    board.paste(im,(250*i,195*r+25));draw.text((250*i+5,195*r+5),f'{tag} / {gear} {t}',fill='white')
  board.save(OUT/f'{gear}-{family}-head-comparison.png')
report={'progressingPresentationsMatched':len(exact),'sourcePixelsExact':len(exact),'physicalRootClockWaterStateMaterialExact':len(exact),'selectedComparisonPoses':22,'artworkChanged':False,'scope':'Selected22current vs baseline native comparisons. No normal-swim renderer or dynamic gait endpoint center correction.'}
(OUT/'comparison.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
