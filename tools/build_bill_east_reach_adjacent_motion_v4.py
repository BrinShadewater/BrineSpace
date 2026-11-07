"""Stage full revised reach with lossless whole-frame contact registration."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
import hashlib,json,copy,shutil,ast
R=Path(__file__).resolve().parents[1];OLD=R/'character/bill-east-reach-adjacent-motion-v1';P=R/'character/bill-east-reach-adjacent-motion-v2';F=P/'frames/interact-east';F.mkdir(parents=True,exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
idle=R/'character/bill-east-idle-master-motion-v1/frames/idle-east/000.png'
report=dict(status='provisional_unselected',frames=[],inputs={str(idle):sha(idle)},normalAdmission=False,nativeTested=False,visualReviewed=False)
for slot in range(6):
 dst=F/f'{slot:03}.png'
 if slot in [0,5]:shutil.copyfile(idle,dst);method='exact whole idle0 endpoint alias'
 else:
  folder=OLD/'extension-register-003-v3' if slot==3 else OLD/'recovery-direct-004-v3' if slot==4 else OLD/'sources'
  raw=folder/f'raw-{slot:03}.png';receipt_path=folder/'provenance.json' if slot in [3,4] else OLD/f'provenance/{slot:03}.json'
  receipt=json.loads(receipt_path.read_text(encoding='utf-8'));assert sha(raw)==receipt['rawSha256']
  im=Image.open(raw).convert('RGBA').resize((352,352),Image.Resampling.LANCZOS);mask=np.asarray(im)[:,:,3]>127
  outside=mask.copy();outside[52:236,68:252]=False;assert not outside.any()
  packed=np.asarray(im.crop((68,52,252,236))).copy()
  if slot==3:
   shift=6;assert not packed[:shift,:,3].any();moved=np.zeros_like(packed);moved[:-shift]=packed[shift:]
   assert np.array_equal(moved[:-shift],packed[shift:]) and np.count_nonzero(moved[:,:,3])==np.count_nonzero(packed[:,:,3]);packed=moved
  Image.fromarray(packed).save(dst);method='builtin whole pose, uniform352canvas/crop184'+('; lossless whole y-6 sole registration' if slot==3 else '')
  report['inputs'].update({str(raw):sha(raw),str(receipt_path):sha(receipt_path)})
 pixels=np.asarray(Image.open(dst).convert('RGBA'));y,x=np.where(pixels[:,:,3]>127)
 report['frames'].append(dict(slot=slot,bounds=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],height=int(y.max()+1-y.min()),soleEdge=int(y.max()+1),method=method,sha256=sha(dst)))
assert all(x['soleEdge']==172 for x in report['frames'])
assert [x['height'] for x in report['frames']]==[148,148,149,149,149,148]
manifest=json.loads((OLD/'manifest.json').read_text(encoding='utf-8'));state=next(s for s in manifest['states'] if s['id']=='interact-east')
state['frameFiles']=['res://'+(F/f'{i:03}.png').relative_to(R).as_posix() for i in range(6)]
state['provenance']='Original donor poses1/2, revised whole extension3 and direct recovery4; exact idle endpoints. family-review.json.'
manifest['name']='Bill East full reach stature refinement';(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
frames=[Image.open(F/f'{i:03}.png').convert('RGBA') for i in range(6)]
for name,mult in [('interaction-normal.png',1),('interaction-slow.png',4)]:
 frames[0].save(P/name,save_all=True,append_images=frames[1:],duration=[t*mult for t in state['frameDurationsMs']],loop=0,disposal=0,blend=0)
 with Image.open(P/name) as media:
  assert media.n_frames==6
  for i,expected in enumerate(frames):media.seek(i);assert media.convert('RGBA').tobytes()==expected.tobytes()
board=Image.new('RGB',(1680,850),'#17252d');draw=ImageDraw.Draw(board)
for row,(label,folder) in enumerate([('Prior detailed reach',OLD/'frames/interact-east'),('Revised stature / recovery',F)]):
 draw.text((15,row*425+12),label,fill='white')
 for n in range(6):
  im=Image.open(folder/f'{n:03}.png').convert('RGBA').resize((368,368),Image.Resampling.NEAREST);view=im.crop((80,0,348,368));board.paste(view,(n*280+6,row*425+40),view);draw.text((n*280+12,row*425+402),f'slot{n}',fill='white')
board.save(P/'family-review.png');report['heights']=[r['height'] for r in report['frames']];report['openIssues']=['One-pixel crown/stature variation remains; shoulder/face and arm arc require full temporal review.','Native V4 covers prior bank only. Natural dispatch/gear/full run Continue and normal selection unverified.']
(P/'family-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
timeline=[];inputs={};elapsed=0
for label,key in [('Idle before','idle-east'),('Reach','interact-east'),('Idle return','idle-east')]:
 s=next(s for s in manifest['states'] if s['id']==key)
 for slot,(resource,duration) in enumerate(zip(s['frameFiles'],s['frameDurationsMs'])):
  source=R/resource.removeprefix('res://');name=source.relative_to(R).as_posix();inputs[name]=sha(source);timeline.append(dict(state=label,key=key,slot=slot,path='/'+name,startMs=elapsed,durationMs=duration));elapsed+=duration
assert len(timeline)==150 and len(inputs)==78 and elapsed==6760
(P/'timeline.json').write_text(json.dumps(dict(durationMs=elapsed,frames=timeline,inputs=inputs),indent=2)+'\n',encoding='utf-8')
html=(OLD/'motion.html').read_text(encoding='utf-8').replace('Late-pose head rise still needs polish.','Stature variation reduced to one source pixel; pose and motion polish remains.').replace('Source and actual station comparisons','Source comparisons')
(P/'motion.html').write_text(html,encoding='utf-8')
(P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill reach refinement</title><body style="background:#17252d;color:#d7e0df;font:16px system-ui"><h1>Bill East reach refinement</h1><p>Provisional source revision. Height drift reduced; native runtime validation pending.</p><a href="motion.html">Idle, reach and return</a><p><img src="family-review.png" style="max-width:100%"></p>',encoding='utf-8')
print('Six original slots/timings; heights148/148/149/149/149/148, soles172;12APNG frames exact;150timeline slots6760ms.')
