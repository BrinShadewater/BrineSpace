from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,copy,shutil
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-idle-interact-joined-v1';P.mkdir(exist_ok=False);F=P/'frames/interact-east';F.mkdir(parents=True)
old=R/'character/bill-east-interact-master-consistency-v1';idle=R/'character/bill-east-idle-master-motion-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((old/'manifest.json').read_text());breath=json.loads((idle/'manifest.json').read_text());report={'status':'provisional_unselected','scope':'Full idle reference plus six-slot interaction. Whole-source endpoint aliases and lossless whole-canvas registration only. No new painted artwork, scaling or colour changes.','inputs':{},'frames':[],'worldVerification':None,'visualReviewed':False}
for p in [old/'manifest.json',idle/'manifest.json',R/'output/bill-east-master-world-v2/report.json',R/'output/bill-east-master-world-v2/validation.json']:report['inputs'][p.relative_to(R).as_posix()]=sha(p)
for i in range(6):
 src=idle/'frames/idle-east/000.png' if i in [0,5] else old/f'frames/interact-east/{i:03}.png';dst=F/f'{i:03}.png';a=np.asarray(Image.open(src).convert('RGBA'));report['inputs'][src.relative_to(R).as_posix()]=sha(src)
 if i==3:
  assert not a[0,:,3].any();b=np.zeros_like(a);b[:-1]=a[1:];assert np.array_equal(b[:-1],a[1:]);assert np.count_nonzero(b[:,:,3])==np.count_nonzero(a[:,:,3]);Image.fromarray(b).save(dst);operation='whole184canvas translation y=-1; surviving RGBA exact, zero opaque loss'
 else:shutil.copyfile(src,dst);operation='whole idle endpoint alias' if i in [0,5] else 'exact unchanged interaction source'
 arr=np.asarray(Image.open(dst).convert('RGBA'));ys,xs=np.where(arr[:,:,3]>127);assert int(ys.max()+1)==172
 report['frames'].append({'slot':i,'source':src.relative_to(R).as_posix(),'operation':operation,'sha256':sha(dst),'bounds':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]})
state=copy.deepcopy(source['states'][0]);state['frameFiles']=['res://'+(F/f'{i:03}.png').relative_to(R).as_posix() for i in range(6)];state['provenance']='Whole idle source0 aliases at endpoints; whole-frame lossless y-1 registration at3; exact original candidate1/2/4. join-review.json.'
manifest={k:v for k,v in source.items() if k!='states'};manifest.update(name='Bill East joined master idle and interaction',states=[copy.deepcopy(breath['states'][0]),state],status='provisional_unselected');(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
assert sum(state['frameDurationsMs'])==760
for name,mult in [('interaction-normal.png',1),('interaction-slow.png',4)]:
 frames=[Image.open(F/f'{i:03}.png').convert('RGBA') for i in range(6)];frames[0].save(P/name,save_all=True,append_images=frames[1:],duration=[x*mult for x in state['frameDurationsMs']],loop=0,disposal=0,blend=0)
 with Image.open(P/name) as im:
  assert im.n_frames==6
  for i,f in enumerate(frames):im.seek(i);assert im.convert('RGBA').tobytes()==f.tobytes()
board=Image.new('RGB',(1500,920),'#17252d');d=ImageDraw.Draw(board)
for row,(label,folder) in enumerate([('Prior interaction candidate',old/'frames/interact-east'),('Joined interaction candidate',F)]):
 d.text((18,22+row*450),label,fill='white')
 for i in range(6):
  im=Image.open(folder/f'{i:03}.png').convert('RGBA').resize((368,368),Image.Resampling.NEAREST);x=18+250*i;view=im.crop((90,0,340,368));board.paste(view,(x,60+450*row),view);d.text((x,428+450*row),f'slot {i}',fill='white')
board.save(P/'join-review.png');(P/'join-review.json').write_text(json.dumps(report,indent=2)+'\n');(P/'index.html').write_text('<html><body style="background:#17252d;color:white;font-family:sans-serif"><h1>Bill East idle / interaction join</h1><p>Provisional source registration; normal selection unchanged.</p><img src="../bill-east-idle-master-motion-v1/breathing-normal.png"><img src="interaction-normal.png"><img src="interaction-slow.png"><br><img style="max-width:100%" src="join-review.png"></body></html>');print('Six interaction slots packaged; endpoints exact idle0; slot3 losslessly registered; twelve APNG frames exact.')
