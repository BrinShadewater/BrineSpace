from pathlib import Path
import json,re,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OUT=ROOT/'output/bill-death-ground-station-candidate-v1';data=json.loads((OUT/'contacts.json').read_text());records=data['records'];bindings={};joins=[]
for contact,crop in [('counter',(495,520,640,665)),('aisle',(385,300,530,445))]:
 board=Image.new('RGB',(435,1320),(34,52,62));draw=ImageDraw.Draw(board)
 for row,(d,g) in enumerate((d,g) for d in ['east','west','north','south'] for g in [False,True]):
  group=[next(r for r in records if r['contact']==contact and r['direction']==d and r['gear']==g and r['phase']==phase) for phase in ['before-kneel','entry','terminal']]
  for col,r in enumerate(group):
   f=OUT/r['screenshot'];im=Image.open(f).convert('RGB').crop(crop);board.paste(im,(col*145,row*165+20));draw.text((col*145+2,row*165+2),d+(' gear ' if g else ' bare ')+r['phase'],fill='white');bindings[r['screenshot']]=hashlib.sha256(f.read_bytes()).hexdigest()
  before=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',group[0]['extent'])];after=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',group[1]['extent'])]
  joins.append({'contact':contact,'direction':d,'helmet':g,'crownRiseWorldUnits':round(before[1]-after[1],3),'scope':'alpha-crown proxy; visible standing-entry reset, not physical anatomical measurement'})
 board.save(P/f'station-{contact}-review.png')
lowered='133 checks,0 failures' in (OUT/'native.log').read_text()
report={'status':'lowered_entry_reviewed_counter_overlap_pending' if lowered else 'join_defects_found','captures':48,'sha256':bindings,'joins':joins,'scope':'actual owner galley geometry at counter/aisle; fixture-controlled facings and kneel state; lowered entry opt-in reviewed; axial crown motion is projection, not standing-height evidence; counter occlusion remains; does not certify full floor clearance'}
(P/'station-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><meta charset="utf-8"><title>Bill collapse station join audit</title><style>body{background:#152027;color:#e6eff1;font:16px system-ui;margin:24px}img{max-width:100%;vertical-align:top}p{max-width:90ch}a{color:#80d4df}</style><h1>Bill — actual galley collapse join audit</h1><p>Each row compares last kneeling pose, death entry and held terminal, using native station crops at unchanged scale. Four fixture-controlled directions and both gears. The standing entry visibly raises Bill after kneeling. Counter overlap remains a physical placement/occlusion problem. Candidates stay staged; technical checks do not certify these joins.</p><h2>Counter contact</h2><img src="station-counter-review.png"><h2>Aisle</h2><img src="station-aisle-review.png"><p><a href="/output/bill-death-ground-station-candidate-v1/contacts.json">Source capture records</a></p>'''
if lowered:html=html.replace('The standing entry visibly raises Bill after kneeling.','The opt-in lowered entry skips the standing reset. Axial screen crown motion includes authored perspective and is not a body-height invariant. Fine pose joins remain review work.')
(P/'station-review.html').write_text(html,encoding='utf-8');print('Built48 hash-bound station crops;16 lowered-entry comparison measurements')
