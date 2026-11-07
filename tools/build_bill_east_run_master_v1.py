"""Uniform whole-source packing, original run contract and reproducible review exports."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-run-master-v1';F=D/'frames';F.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=json.loads((D/'protected-inputs.json').read_text(encoding='utf-8'));assert all(sha(R/p)==s for p,s in protected.items())
contract=json.loads((D/'selected-contract.json').read_text(encoding='utf-8'))
def bounds(a):
 y,x=np.where(a[:,:,3]>127);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
records=[];old=[];new=[];inputs={};board=Image.new('RGBA',(1536,860),'#17252d');draw=ImageDraw.Draw(board)
idle=Image.new('RGBA',(256,256));idle.alpha_composite(Image.open(R/'character/bill-east-idle-master-motion-v1/frames/idle-east/000.png').convert('RGBA'),(36,52))
for slot in range(6):
 S=D/f'pose-{slot:03}';raw=S/'raw.png';refs=json.loads((S/'references.json').read_text(encoding='utf-8'))
 assert all(sha(Path(r['path']))==r['sha256'] and sha(Path(r['source']))==r['sourceSha256'] for r in refs)
 receipt=json.loads((S/'receipt.json').read_text(encoding='utf-8'));assert sha(Path(receipt['path']))==sha(raw)
 source=Image.open(R/contract['files'][slot]).convert('RGBA');old.append(source)
 a=np.asarray(Image.open(raw).convert('RGBA')).copy();a[a[:,:,3]==0,:3]=0
 a=np.asarray(Image.fromarray(a).resize((256,256),Image.Resampling.LANCZOS)).copy()
 components,count=label(a[:,:,3]>0);removed=0
 for k in range(1,count+1):
  mask=components==k
  if mask.sum()<=3 and a[:,:,3][mask].max()<=1:removed+=int(mask.sum());a[mask]=0
 b=bounds(a);original=bounds(np.asarray(source));dy=original[3]-b[3]
 packed=np.zeros_like(a)
 if dy>0:assert not a[-dy:,:,3].any();packed[dy:]=a[:-dy]
 elif dy<0:assert not a[:-dy,:,3].any();packed[:dy]=a[-dy:]
 else:packed=a.copy()
 assert np.count_nonzero(packed[:,:,3])==np.count_nonzero(a[:,:,3])
 im=Image.fromarray(packed);dst=F/f'{slot:03}.png';im.save(dst);new.append(im);bb=bounds(packed)
 rec=dict(slot=slot,rawSize=Image.open(raw).size,bounds=bb,selectedBounds=original,heightDelta=(bb[3]-bb[1])-(original[3]-original[1]),soleDelta=bb[3]-original[3],wholeShiftY=dy,removedDisconnectedAlpha1Pixels=removed,rawSha256=sha(raw),frameSha256=sha(dst),promptSha256=sha(S/'prompt.txt'),referenceHashes=refs,receipt=receipt)
 assert abs(rec['heightDelta'])<=3 and rec['soleDelta']==0
 records.append(rec);(S/'provenance.json').write_text(json.dumps(rec,indent=2)+'\n',encoding='utf-8')
 for p in [raw,S/'prompt.txt',S/'references.json',S/'receipt.json',dst]:inputs[p.relative_to(R).as_posix()]=sha(p)
 for row,(name,im2) in enumerate([('Selected run',source),('Master repair',im),('Current idle',idle)]):
  draw.text((slot*256+8,row*275+8),f'{slot}: {name}',fill='white');board.alpha_composite(im2,(slot*256,row*275+18))
board.save(D/'whole-comparison.png')
m=json.loads((R/contract['manifest']).read_text(encoding='utf-8'));state=next(s for s in m['states'] if s['id']=='run-east');state['frameFiles']=[f'res://character/bill-east-run-master-v1/frames/{i:03}.png' for i in range(6)]
m.update(name='Bill East whole master run repair',status='provisional_unselected',states=[state],strideDistanceCells={'run-east':m['strideDistanceCells']['run-east']})
(D/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
movies=[]
for name,frames in [('selected',old),('candidate',new)]:
 for rate in [1,4]:
  p=D/f'{name}-{rate}.png';times=[d*rate for d in contract['timing']];frames[0].save(p,save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=0,blend=0)
  decoded=Image.open(p);assert decoded.n_frames==6
  for i,frame in enumerate(frames):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==frame.tobytes() and decoded.info['duration']==times[i]
  movies.append(dict(file=p.name,frames=6,durationMs=sum(times),sha256=sha(p)))
review=dict(records=records,inputs=inputs,protectedInputs=protected,movies=movies,frameCount=6,cycleMs=sum(contract['timing']),strideDistanceCells=m['strideDistanceCells'],processing='One uniform raw-square to256 resample for every pose; remove only disconnected components <=3px/maxalpha1; whole Y registration to each original pose sole. No per-pose size fitting, local grading, body-part splicing or interpolation.',visualReviewed=False,normalAdmission=False,nativeTested=False)
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><html lang="en"><meta charset="utf-8"><title>Bill East run master repair</title><style>body{background:#17252d;color:#dbe5e9;font:16px system-ui;max-width:1536px;margin:24px auto}p{max-width:950px;line-height:1.5}.row{display:flex;gap:16px;flex-wrap:wrap}.card{background:#20313b;padding:12px}img{max-width:100%}button{padding:10px;margin:8px;color:#dbe5e9;background:#34515f;border:0}a{color:#82d3df}.sprite{width:384px;height:384px;image-rendering:auto}</style><h1>Bill East: master-matched running</h1><p>All six running poses rebuilt as whole figures to restore the matte quilted suit, hardware and warm face. Original six-frame order, 540ms loop and stride setting retained. Review candidate; normal selection unchanged.</p><div><button id="speed">Quarter speed</button><button id="pause">Pause</button></div><div class="row"><div class="card">Current master idle<br><img class="sprite" src="idle-reference.png"></div><div class="card">Selected running<br><img class="sprite" id="old" src="selected-1.png"></div><div class="card">Master repair<br><img class="sprite" id="new" src="candidate-1.png"></div></div><h2>Every pose beside the current idle</h2><img src="whole-comparison.png"><p>Whole figures share H148/p128224 registration. Running naturally leans and changes height; no independent pose stretching. This preview does not establish moving feet, autonomous transitions or normal game admission.</p><script>let slow=false,paused=false;document.querySelector('#speed').onclick=()=>{slow=!slow;for(let [id,name] of [['old','selected'],['new','candidate']])document.querySelector('#'+id).src=name+'-'+(slow?4:1)+'.png';document.querySelector('#speed').textContent=slow?'Normal speed':'Quarter speed'};document.querySelector('#pause').onclick=()=>{paused=!paused;for(let [id,name] of [['old','selected'],['new','candidate']])document.querySelector('#'+id).src=paused?(id==='old'?'../bill-run-head-locked-v1/frames/run-east/000.png':'frames/000.png'):name+'-'+(slow?4:1)+'.png';document.querySelector('#pause').textContent=paused?'Play':'Pause'};</script></html>'''
(D/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(frames=6,heights=[r['heightDelta'] for r in records],wholeY=[r['wholeShiftY'] for r in records],duration=sum(contract['timing']),decodedMovieFrames=24,protectedInputsUnchanged=len(protected))))
