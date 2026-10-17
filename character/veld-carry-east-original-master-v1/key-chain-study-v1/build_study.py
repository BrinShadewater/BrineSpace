"""Exact source-key chronology for independent moving-root diagnosis."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,copy,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2];A=P.parent
folders=[R/'character/veld-east-held-original-master-v1',A/'single-transition-source-v1',A/'touchdown-source-v2']
labels=['Original held','Far-foot lift','Far-heel contact (provisional)']; bindings={}
for gear in ['bare','helmet']:
 paths=[f/f'frames/{gear}/000.png' for f in folders]
 data=json.loads((folders[2]/f'{gear}-source-manifest.json').read_text(encoding='utf-8'))
 state=copy.deepcopy(data['states'][0]);state.update(id='carry-key-chain-east',frameCount=3,frameFiles=['res://'+p.relative_to(R).as_posix() for p in paths],frameDurationsMs=[180,180,180],loop=False)
 for k in ['facings','waterKinds','waterPoses','depthOffsets']:state[k]=state[k]*3
 data.update(name='Veld East sparse source-key diagnostic '+gear,status='sparse_key_diagnosis_only',states=[state]+data['states'][1:]);manifest=P/f'{gear}-source-manifest.json';manifest.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 frames=[Image.open(p).convert('RGBA') for p in paths]
 frames[0].save(P/f'{gear}-source-key-replay.png',save_all=True,append_images=frames[1:],duration=[180]*3,loop=1,disposal=0,blend=0)
 sheet=Image.new('RGB',(960,850),(32,43,49));d=ImageDraw.Draw(sheet)
 for i,im in enumerate(frames):
  d.text((i*320+15,20),labels[i],fill='white');sheet.paste(im,(i*320+32,30),im)
  crop=im.crop((98,180,182,232)).resize((252,156),Image.Resampling.NEAREST);sheet.paste(crop,(i*320+20,310),crop)
  crop=im.crop((102,75,160,163)).resize((174,264),Image.Resampling.NEAREST);sheet.paste(crop,(i*320+100,530),crop)
 sheet.save(P/f'{gear}-source-key-review.png')
 for p in paths+[manifest]:bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
bindings[Path(__file__).relative_to(R).as_posix()]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
record={'bindings':bindings,'scope':'Three exact existing independently authored whole sources; prescribed180ms holds diagnostic only. Missing prelift/recovery/intermediates; no complete animation or final identity/contact acceptance. Source registration unchanged. Root trial8 native pixels/sec is a diagnostic velocity, not final gait stride.'}
(P/'study-record.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('Paired exact three-key source chronology saved; no source alterations.')
