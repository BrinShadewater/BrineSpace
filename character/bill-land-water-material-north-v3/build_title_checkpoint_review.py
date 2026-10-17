from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-land-water-title-checkpoint-north-v1';D=P/'title-checkpoint-review';OLD=P/'fresh-checkpoint-review'
v=json.loads((O/'validation.json').read_text());assert v['passed'] and len(v['intervals'])==5;D.mkdir(exist_ok=True)
prior=json.loads((R/'output/bill-land-water-fresh-checkpoint-north-v1/records.json').read_text());byname={x['name']:x for x in prior['records']}
inputs=json.loads((P/'title-targeted-inputs.json').read_text());changes=[f for f,h in inputs.items() if hashlib.sha256((R/f).read_bytes()).hexdigest()!=h]
board=Image.new('RGB',(1050,1920),'#182932');draw=ImageDraw.Draw(board);pairs=[];hashes={};checks=0
for i,name in enumerate(['bare-81','bare-432','helmet-81','helmet-432']):
 data=json.loads((O/f'{name}-records.json').read_text());assert data['failures']==0;checks+=data['checks']
 for j,suffix in enumerate(['','-future']):
  row=next(x for x in data['records'] if x['name']==name+'-title'+suffix+'-candidate');old=byname[name+suffix+'-before-candidate']
  fields=['foot','state','direction','bridgeActive','materialWeight','materialHeadOffset']
  equal={f:row[f]==old[f] for f in fields};assert all(equal.values())
  pair={'name':name+suffix,'referenceFieldsExact':equal}
  for kind in ['room','source']:
   f=O/f'{name}-title{suffix}-candidate-{kind}.png';shutil.copy2(f,D/f.name);hashes[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
   actual=Image.open(f).convert('RGBA');reference=Image.open(OLD/f'{name}{suffix}-before-candidate-{kind}.png').convert('RGBA')
   pair[kind+'RGBAExactToPrior']=actual.size==reference.size and actual.tobytes()==reference.tobytes()
   if kind=='source':assert pair[kind+'RGBAExactToPrior']
   else:
    pair['wholeSceneRGBDifferenceBounds']=ImageChops.difference(actual.convert('RGB'),reference.convert('RGB')).getbbox()
    x=255+(row['foot'][0]-7680)*398/384;y=287+(row['foot'][1]-8064)*398/384
    box=(round(x)-120,round(y)-145,round(x)+120,round(y)+75)
    pair['registeredRoomCropRGBAExactToPrior']=actual.crop(box).tobytes()==reference.crop(box).tobytes()
    assert pair['registeredRoomCropRGBAExactToPrior']
    for col,(label,image) in enumerate([('prior fresh scene',reference),('new-process title',actual)]):
     crop=image.crop((round(x)-120,round(y)-145,round(x)+120,round(y)+75));board.paste(crop,(col*350+15,(i*2+j)*240+20));draw.text((col*350+15,(i*2+j)*240+3),name+suffix+' '+label,fill='white')
   if kind=='source':
    actual.thumbnail((220,210),Image.Resampling.LANCZOS);board.paste(actual,(720,(i*2+j)*240+20),actual);draw.text((720,(i*2+j)*240+3),'exact raw source (unregistered)',fill='white')
  pairs.append(pair)
 shutil.copy2(O/f'{name}-records.json',D/f'{name}-records.json')
 hashes[name+'.loop']=hashlib.sha256((D/f'{name}.loop').read_bytes()).hexdigest()
assert not changes,changes
board.save(D/'title-comparison.png')
e={'validation':v,'nativeChecks':checks,'comparisonPairs':pairs,'captureAndEnvelopeSHA256':hashes,'targetedPrelaunchSHA256':inputs,'targetedInputChanges':changes,
 'scope':'Four independent native processes use actual title Continue button, loading transmission/Continue button and normal main pending checksum restore. Copied current title redirects only game scene; copied main redirects only grid preload, derived staged ready hook admits checksummed transition/view. Eight native presentations;160 future ticks check survival and exact terminal normal source, not per-tick native or all per-tick trajectory fields. Eight source RGBA and recorded root/state/facing/bridge/material/head-offset fields equal prior fresh-scene endpoints. All eight240x220 native room crops at the same physical-root/camera projection byte-exact to prior. Whole-scene pixel equality to historical fixture is separately reported, not assumed. Raw source thumbnails unregistered. Staged field and fixture hooks are not production source/save admission.'}
(D/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
(D/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill title checkpoint</title><style>body{background:#182932;color:#eef;font:16px sans-serif}img{max-width:100%}</style><h1>Bill North — new-process title checkpoint</h1><p>'+e['scope']+'</p><img src="title-comparison.png">',encoding='utf-8')
print(json.dumps({'nativeChecks':checks,'independentProcesses':4,'sourceExactPairs':sum(x['sourceRGBAExactToPrior'] for x in pairs),'registeredNativeRoomCropsExact':sum(x['registeredRoomCropRGBAExactToPrior'] for x in pairs),'wholeSceneExactPairs':sum(x['roomRGBAExactToPrior'] for x in pairs),'rootMaterialExactPairs':len(pairs),'targetedInputChanges':changes}))
