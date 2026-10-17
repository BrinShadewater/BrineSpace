from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent;CAP=ROOT/'output/bill-land-water-material-west-v12';BASE=ROOT/'output/bill-land-water-material-west-v12'
run=json.loads((CAP/'records.json').read_text());old={v['name']:v for v in json.loads((BASE/'records.json').read_text())['records']};changes=[];same=0;contexts={};hashes={}
for row in run['records']:
 if 'tick' not in row:continue
 if row['name'] in old:
  fields=[k for k in ['foot','clock','water','medium','state','direction','pathPoints','materialWeight'] if row[k]!=old[row['name']][k]]
  if fields:changes.append({'name':row['name'],'fields':fields})
  else:same+=1
for gear in ['bare','helmet']:
 m=json.loads((OUT/f'{gear}-walk-manifest.json').read_text());frames=[]
 for path in m['states'][0]['frameFiles']:
  q=ROOT/path.removeprefix('res://');im=Image.open(q).convert('RGBA');frames.append(im.tobytes());hashes[q.relative_to(ROOT).as_posix()]=hashlib.sha256(q.read_bytes()).hexdigest()
 for tick in [67,443,444,445]:
  q=CAP/f'{gear}-{tick:03}-candidate-source.png';im=Image.open(q).convert('RGBA');hits=[n for n,v in enumerate(frames) if im.size==(256,256) and im.tobytes()==v];assert len(hits)==1,(gear,tick,hits,im.size);contexts[gear+str(tick)]=hits[0]
 for kind,ticks in [('entry',[67,68,71,75,84,95,97]),('exit',[415,419,430,439,443,444,445])]:
  b=Image.new('RGB',(250*len(ticks),600),(23,42,51));d=ImageDraw.Draw(b)
  for i,tick in enumerate(ticks):
   name=f'{gear}-{tick:03}-candidate';q=CAP/(name+'-room.png');im=Image.open(q).convert('RGB').crop((425,490,675,660) if kind=='entry' else (275,490,525,660));b.paste(im,(250*i,30));d.text((250*i+5,5),f'{gear} {tick} native room',fill='white')
   q=CAP/(name+'-source.png');im=Image.open(q).convert('RGBA');c=Image.new('RGBA',(352,320));c.alpha_composite(im,(32,0) if im.size==(256,256) else (0,0));crop=c.crop((120,55,190,145)).resize((210,270),Image.Resampling.NEAREST);b.paste(crop,(250*i+20,260),crop);d.text((250*i+5,225),'Exact submitted source',fill='white')
  b.save(OUT/f'{gear}-{kind}-native-review.png')
report={'checks':run['checks'],'failures':run['failures'],'sameControllerRootClockWaterPathMaterialRows':same,'differences':changes,'actualNativeWalkCandidateMatches':contexts,'candidateInputSHA256':hashes,'normalAdmission':False,'fullVisualAcceptance':False,'scope':'Prescribed room hydrology and route, exact revised walk source loading/dynamic joins; isolated native fixture, not natural job/hazards/checkpoint/Continue acceptance.'};(OUT/'review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='candidateInputSHA256'}))
