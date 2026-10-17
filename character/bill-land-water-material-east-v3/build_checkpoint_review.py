from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib, shutil
P=Path(__file__).resolve().parent;R=P.parent.parent
O=R/'output/bill-land-water-checkpoint-east-v1';D=P/'checkpoint-review';D.mkdir(exist_ok=True)
v=json.loads((O/'validation.json').read_text());data=json.loads((O/'records.json').read_text())
assert v['passed'] and data['failures']==0
disk=[x for x in data['records'] if x['name'].endswith('-checkpoint')];assert len(disk)==4
rows=[x for x in data['records'] if 'tick' in x and x['name'].endswith('-candidate')];assert len(rows)==190
equal={'source':0,'room':0}
for row in rows:
 for kind in equal:
  new=Image.open(O/f"{row['name']}-{kind}.png").convert('RGBA')
  old=Image.open(P/'captures'/f"{row['name']}-{kind}.png").convert('RGBA')
  equal[kind]+=new.size==old.size and new.tobytes()==old.tobytes()
board=Image.new('RGB',(900,1000),'#182932');draw=ImageDraw.Draw(board);hashes={}
for i,record in enumerate(disk):
 stem=record['name'].removesuffix('-checkpoint')
 before=Image.open(O/f'{stem}-before-candidate-room.png').convert('RGBA');after=Image.open(O/f'{stem}-after-candidate-room.png').convert('RGBA')
 assert before.tobytes()==after.tobytes()
 row=next(x for x in data['records'] if x['name']==stem+'-before-candidate')
 x=255+(row['foot'][0]-7680)*398/384;y=287+(row['foot'][1]-8064)*398/384
 for col,label in enumerate(['before','after']):
  for kind in ['room','source']:
   f=O/f'{stem}-{label}-candidate-{kind}.png';shutil.copy2(f,D/f.name);hashes[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
  im=Image.open(O/f'{stem}-{label}-candidate-room.png').crop((round(x)-120,round(y)-155,round(x)+120,round(y)+65))
  board.paste(im,(col*450+20,i*250+25));draw.text((col*450+20,i*250+5),stem+' '+label,fill='white')
 f=O/f'{stem}.bin';shutil.copy2(f,D/f.name);hashes[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
board.save(D/'disk-roundtrip.png')
e={'validation':v,'checks':data['checks'],'diskCheckpoints':disk,'advancingImagesExactToV3':equal,'snapshotSHA256':hashes,
 'scope':'Four actual live East entry/exit bridges/both gears stored as resource-free Variant and decoded from disk, restored into cleared same live grid/player with original actor/world/clock. Eight native before/after presentations exact. Not fresh actor, RunSave extension, Title Continue, normal admission or other cardinals. Signature rgba fields hash hex-encoded bytes, not raw RGBA directly.'}
(D/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
(D/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill water checkpoint</title><style>body{background:#182932;color:#eef;font:16px sans-serif}img{max-width:100%}</style><h1>Bill East water checkpoint — staged disk round-trip</h1><p>'+e['scope']+'</p><img src="disk-roundtrip.png">',encoding='utf-8')
print(json.dumps({'checks':data['checks'],'diskCheckpoints':len(disk),'advancingExact':equal}))
