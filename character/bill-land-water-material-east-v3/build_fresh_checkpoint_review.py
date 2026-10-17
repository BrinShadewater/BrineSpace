from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-land-water-fresh-checkpoint-east-v1';D=P/'fresh-checkpoint-review';D.mkdir(exist_ok=True)
v=json.loads((O/'validation.json').read_text());data=json.loads((O/'records.json').read_text())
restores=[x for x in data['records'] if x['name'].endswith('-fresh-restore')];assert len(restores)==4
inputs=json.loads((P/'fresh-targeted-inputs.json').read_text());changes=[f for f,h in inputs.items() if hashlib.sha256((R/f).read_bytes()).hexdigest()!=h]
board=Image.new('RGB',(1000,1920),'#182932');draw=ImageDraw.Draw(board);pairs=[];hashes={}
for i,record in enumerate(restores):
 stem=record['name'].removesuffix('-fresh-restore')
 for j,suffix in enumerate(['','-future']):
  name=stem+suffix;rows=[next(x for x in data['records'] if x['name']==name+'-'+tag+'-candidate') for tag in ['before','after']]
  pair={'name':name}
  for kind in ['room','source']:
   images=[]
   for col,tag in enumerate(['before','after']):
    f=O/f'{name}-{tag}-candidate-{kind}.png';shutil.copy2(f,D/f.name);hashes[f.name]=hashlib.sha256(f.read_bytes()).hexdigest();images.append(Image.open(f).convert('RGBA'))
    if kind=='room':
     row=rows[col];x=255+(row['foot'][0]-7680)*398/384;y=287+(row['foot'][1]-8064)*398/384
     crop=images[-1].crop((round(x)-120,round(y)-145,round(x)+120,round(y)+75));board.paste(crop,(col*500+20,(i*2+j)*240+20));draw.text((col*500+20,(i*2+j)*240+3),name+' '+tag,fill='white')
   pair[kind+'Exact']=images[0].size==images[1].size and images[0].tobytes()==images[1].tobytes()
   pair[kind+'RGBDifferenceBounds']=ImageChops.difference(images[0].convert('RGB'),images[1].convert('RGB')).getbbox()
  pairs.append(pair)
 for f in [O/f'{stem}-bridge.bin',Path(v['scratchAPPDATA'])/'Godot/app_userdata/BrineSpace'/f'bill-water-{stem}.loop']:
  assert f.exists();shutil.copy2(f,D/f.name);hashes[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
board.save(D/'fresh-before-after.png')
e={'validation':v,'checks':data['checks'],'failures':data['failures'],'freshRestores':restores,'nativeSourcePairs':pairs,'captureAndDiskSHA256':hashes,'targetedPrelaunchSHA256':inputs,'targetedInputChanges':changes,
 'scope':'Four same-process fresh scenes/normal actors/worlds restored through actual normal checksum RunSave write/read/restore_staged, then staged bridge sidecar.160 future60Hz ticks compare foot/facing/state/medium/needs/oxygen/source/material/head offset/bridge activity; sixteen native endpoint presentations. Not native capture of every future tick, natural hydrology/jobs, Title Continue/new-process or normal bridge admission.'}
(D/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
(D/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill fresh water checkpoint</title><style>body{background:#182932;color:#eef;font:16px sans-serif}img{max-width:100%}</style><h1>Bill East — fresh scene water checkpoint</h1><p>'+e['scope']+'</p><p>Checks '+str(e['checks'])+'; failures '+str(e['failures'])+'</p><img src="fresh-before-after.png">',encoding='utf-8')
print(json.dumps({'checks':e['checks'],'failures':e['failures'],'exactNativePairs':sum(x['roomExact'] for x in pairs),'exactSourcePairs':sum(x['sourceExact'] for x in pairs),'targetedInputChanges':changes}))
