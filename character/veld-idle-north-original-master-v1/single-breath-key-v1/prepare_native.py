from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;R=P.parents[2];bindings={};checks=0
shell_path=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/000.png';shell=Image.open(shell_path).convert('RGBA')
def fit(bare):
 im=bare.copy();im.paste((0,0,0,0),(115,77,143,103));im.alpha_composite(shell,(112,68));a=np.asarray(bare);b=np.asarray(im);mask=np.ones((256,256),bool);mask[68:104,112:146]=False;assert np.array_equal(a[mask],b[mask]);return im
inventory_path=R/'character/veld-master-consistency-current-v2/selected-library.json';inv=json.loads(inventory_path.read_bytes())
for gear in ['bare','helmet']:
 files=[];images=[]
 for i,p in enumerate([P.parent/'clean-idle-master.png',P/'native-inhale.png']):
  im=Image.open(p).convert('RGBA');im=im if gear=='bare' else fit(im);dest=P/f'{gear}-key-{i:03}.png';im.save(dest);files.append('res://'+dest.relative_to(R).as_posix());images.append(im)
 states=[dict(id='source-idle-north',frameCount=2,frameFiles=files,frameDurationsMs=[750,750],loop=True,facings=['north']*2,waterKinds=['idle']*2,waterPoses=[False]*2,depthOffsets=[0.0]*2)]
 for name,p in [('reference-north',P.parent/'original-idle-master.png'),('prepared-north',P.parent/'clean-idle-master.png')]:
  im=Image.open(p).convert('RGBA');im=im if gear=='bare' else fit(im);dest=P/f'{gear}-{name}.png';im.save(dest);states.append(dict(id=name,frameCount=1,frameFiles=['res://'+dest.relative_to(R).as_posix()],frameDurationsMs=[1000],loop=True))
 e=inv['resolved'][gear]['idle-north'];selected=R/e['frameFiles'][0];assert hashlib.sha256(selected.read_bytes()).hexdigest()==inv['sourceBindings'][e['frameFiles'][0]];im=Image.open(selected).convert('RGBA');plate=Image.new('RGBA',(256,256));px,py=e['pivot'];plate.alpha_composite(im,(128-round(px),224-round(py)));dest=P/f'{gear}-selected-idle.png';plate.save(dest);states.append(dict(id='idle-north',frameCount=1,frameFiles=['res://'+dest.relative_to(R).as_posix()],frameDurationsMs=[1000],loop=True))
 data=dict(name='Veld North two-real-key breathing diagnostic '+gear,status='staged_key_comparison_not_final_motion',frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,textureFilter='linear',precomposed=True,states=states);path=P/f'{gear}-native-manifest.json';path.write_text(json.dumps(data,indent=2)+'\n')
 for p in [path,selected,R/e['manifest']]:bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 for state in states:
  for ref in state['frameFiles']:
   p=R/ref[6:];bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 images[0].save(P/f'{gear}-key-study.png',save_all=True,append_images=images[1:],duration=[750,750],loop=0,disposal=0,blend=0)
for p in [P/'prepare_native.py',P/'raw-source.png',P/'prompt.txt',P/'INPUTS.json',P/'KEY_REVIEW.json',shell_path,inventory_path]:bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(P/'full-source-record.json').write_text(json.dumps(dict(bindings=bindings,scope='Two real whole-source keys, no invented/interpolated frames; diagnostic loops, no final breathing/material/join/controller acceptance.'),indent=2)+'\n')
print('Paired two-key native diagnostic prepared; whole helmet fixed/body outside exact')
