"""Retain current phase/contact/guard evidence alongside original native captures."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
P=Path(__file__).resolve().parent;O=P.parent.parent/'output/bill-land-water-material-west-v7'
data=json.loads((O/'records.json').read_text());r=json.loads((P/'review.json').read_text());assert r['validation']['passed']
inventory=json.loads((P/'source-inventory.json').read_text());rows=[v for v in data['records'] if '-guard-' in v['name'] and v['name'].endswith('-candidate')];assert len(rows)==32
b=Image.new('RGB',(1600,920),'#182932');d=ImageDraw.Draw(b);files={};matches={}
for i,v in enumerate(rows):
 for kind in ['source','room']:
  f=O/(v['name']+'-'+kind+'.png');shutil.copy2(f,P/'captures'/f.name);files[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
 im=Image.open(O/(v['name']+'-source.png')).convert('RGBA');sha=hashlib.sha256(im.tobytes()).hexdigest();assert sha in inventory;matches[v['name']]=inventory[sha]
 x=255+(v['foot'][0]-7680)*398/384;y=287+(v['foot'][1]-8064)*398/384
 room=Image.open(O/(v['name']+'-room.png')).crop((round(x)-100,round(y)-130,round(x)+100,round(y)+70));col=i%8;row=i//8;b.paste(room,(col*200,row*230+25));d.text((col*200+3,row*230+3),v['name'].replace('-candidate','').replace('guard-',''),fill='white')
b.save(P/'native-guards.png')
holds={}
for v in data['records']:
 if v['name'].endswith('-support-holds'):
  samples=v['samples'];assert len({str(s['foot']) for s in samples})==1
  holds[v['name']]={'samples':len(samples),'firstClock':samples[0]['clock'],'lastClock':samples[-1]['clock'],'foot':str(samples[0]['foot']),'hungerFirst':samples[0]['needs']['hunger'],'hungerLast':samples[-1]['needs']['hunger']}
r.update(guardPresentations=32,guardFilesSHA256=files,guardSourceMatches=matches,supportHolds=holds,targetedInputsStable=r['validation']['targetedInputCount'],targetedChanges=r['validation']['targetedChanges'])
(P/'review.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
html=(P/'index.html').read_text(encoding='utf-8')
if 'native-guards.png' not in html:html+='<h2>Priority interruption checks</h2><img src="native-guards.png" alt="32 current interruption presentations">'
(P/'index.html').write_text(html,encoding='utf-8')
print(json.dumps({'checks':data['checks'],'guards':32,'sourceRoomFiles':len(files)+len(r['captureFilesSHA256']),'holds':holds,'stableInputs':r['validation']['targetedInputCount']}))
