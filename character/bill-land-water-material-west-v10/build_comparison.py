from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
BASE=ROOT/'output/bill-land-water-material-west-v9'
FIT=ROOT/'output/bill-land-water-material-west-v10'
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
  for r,(tag,cap) in enumerate([('baseline',BASE),('fitted footprint',FIT)]):
   for i,t in enumerate(ticks):
    im=Image.open(cap/f'{gear}-{t:03}-candidate-room.png').convert('RGB').crop((425,490,675,660) if family=='entry' else (275,490,525,660))
    board.paste(im,(250*i,195*r+25));draw.text((250*i+5,195*r+5),f'{tag} / {gear} {t}',fill='white')
  board.save(OUT/f'{gear}-{family}-footprint-comparison.png')
probe_pairs=[]
for gear in ['bare','helmet']:
 board=Image.new('RGB',(1750,390),(23,42,51));draw=ImageDraw.Draw(board)
 for i in range(7):
  a=Image.open(FIT/f'{gear}-swim-probe-{i}-baseline-source.png').convert('RGBA')
  b=Image.open(FIT/f'{gear}-swim-probe-{i}-fitted-source.png').convert('RGBA')
  assert a.size==b.size and a.tobytes()==b.tobytes()
  baseline=next(x for x in fit['records'] if x['name']==f'{gear}-swim-probe-{i}-baseline')
  fitted=next(x for x in fit['records'] if x['name']==f'{gear}-swim-probe-{i}-fitted')
  for key in ['foot','state','direction','materialWeight','anchor','propRect']:assert baseline[key]==fitted[key],(gear,i,key)
  for r,tag in enumerate(['baseline','fitted']):
   im=Image.open(FIT/f'{gear}-swim-probe-{i}-{tag}-room.png').convert('RGB').crop((325,490,575,660))
   board.paste(im,(250*i,195*r+25));draw.text((250*i+5,195*r+5),f'{tag} / {gear} swim{i}',fill='white')
  probe_pairs.append([gear,i])
 board.save(OUT/f'{gear}-swim-footprint-comparison.png')
report={'progressingPresentationsMatched':len(exact),'sourcePixelsExact':len(exact),'physicalRootClockWaterStateMaterialExact':len(exact),'selectedBridgeComparisonPoses':22,'controlledOrdinarySwimPairs':probe_pairs,'artworkChanged':False,'scope':'22selected bridge comparisons against V9;14same-clock controlled normal-swim pairs at water.8 with source probe override. Not natural7phase dispatch or gait endpoint fit.'}
(OUT/'comparison.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
