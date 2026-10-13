"""Publish full-canvas sources and registered native comparison crops."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'output/marsh-animation-audit/cardinal-continue-v1-2026-10-03'
dst=ROOT/'character/marsh-cardinal-continue-v1';dst.mkdir(exist_ok=True)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((src/'report.json').read_text());assert r['failures']==0 and len(r['cases'])==6
changes={}
for kind in ['owner','inputs']:
 a=json.loads((src/(kind+'-before.json')).read_text());b=json.loads((src/(kind+'-after.json')).read_text())
 changes[kind]={'beforeCount':len(a),'afterCount':len(b),'changed':[k for k in sorted(a.keys()|b.keys()) if a.get(k)!=b.get(k)]}
assert not changes['owner']['changed'],changes['owner']
boards=[];copies=[]
for i,case in enumerate(r['cases']):
 board=Image.new('RGB',(1120,332),'#20292e');draw=ImageDraw.Draw(board)
 for j,idx in enumerate([i,i+6]):
  c=r['captures'][idx];im=Image.open(src/c['file']).convert('RGB');x,y=map(round,c['canvasPosition'])
  board.paste(im.crop((x-140,y-260,x+140,y+40)),(j*280,32))
  draw.text((j*280+8,10),('Saved' if j==0 else 'Continued')+' '+case['label'],fill='white')
  art=Image.open(src/c['sourceFile']).convert('RGBA');assert art.width<=280 and art.height<=300
  board.paste(art,(560+j*280+(280-art.width)//2,32+(300-art.height)),art)
  draw.text((568+j*280,10),('Saved source' if j==0 else 'Continued source'),fill='white')
  for name in [c['file'],c['sourceFile']]:
   shutil.copyfile(src/name,dst/name);copies.append({'path':name,'sha256':h(dst/name),'actualPngSize':list(Image.open(dst/name).size)})
 assert Image.open(src/r['captures'][i]['sourceFile']).tobytes()==Image.open(src/r['captures'][i+6]['sourceFile']).tobytes()
 name=case['label']+'-continue.png';board.save(dst/name);boards.append({'path':name,'sha256':h(dst/name),'visualReviewed':False})
receipt={'checks':r['checks'],'failures':r['failures'],'cases':r['cases'],'fingerprints':changes,'reportPath':(src/'report.json').relative_to(ROOT).as_posix(),'reportSha256':h(src/'report.json'),'boards':boards,'captures':copies,'scope':'Six actual normal-route checkpoints restored through fresh Title Continue. Registered held crops plus source parity; not continuously watched cadence, every phase, or every room.'}
(dst/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'checks':r['checks'],'failures':r['failures'],'fingerprints':changes,'boards':len(boards),'captures':len(copies)}))
