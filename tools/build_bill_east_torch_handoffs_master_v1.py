"""Whole-source torch transitions with exact current idle/weld joins."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label
import numpy as np,json,hashlib,copy
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-torch-handoffs-master-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
contract=json.loads((D/'selected-contract.json').read_text());protected=json.loads((D/'protected-inputs.json').read_text())
assert all(sha(R/p)==h for p,h in protected.items())
def bounds(a):
 y,x=np.where(a[:,:,3]>127);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
idle=Image.open(D/'idle-endpoint.png').convert('RGBA');torch=Image.open(R/'character/bill-east-torch-master-v1/frames/000.png').convert('RGBA')
old={};new={};records=[];states=[];inputs={}
for key,c in contract['states'].items():
 F=D/'frames'/key;F.mkdir(parents=True,exist_ok=True);old[key]=[];new[key]=[]
 for slot in range(6):
  source=Image.open(R/c['files'][slot]).convert('RGBA');old[key].append(source);dst=F/f'{slot:03}.png'
  if slot in [0,5]:
   endpoint='idle' if (key=='torch-draw-east' and slot==0) or (key=='torch-stow-east' and slot==5) else 'torch'
   im=idle.copy() if endpoint=='idle' else torch.copy();im.save(dst)
   rec=dict(key=key,slot=slot,endpoint=endpoint,processing='Exact current whole-figure endpoint pixels; idle only padded36,52 into256.',frameSha256=sha(dst),bounds=bounds(np.asarray(im)))
  else:
   S=D/key/f'pose-{slot:03}';raw=S/'raw.png';refs=json.loads((S/'references.json').read_text());receipt=json.loads((S/'receipt.json').read_text())
   assert all(sha(Path(r['path']))==r['sha256'] and sha(Path(r['source']))==r['sourceSha256'] for r in refs)
   assert sha(Path(receipt['path']))==sha(raw)
   rawim=Image.open(raw).convert('RGBA');assert rawim.width==rawim.height
   a=np.asarray(rawim).copy();a[a[:,:,3]==0,:3]=0;a=np.asarray(Image.fromarray(a).resize((256,256),Image.Resampling.LANCZOS)).copy()
   components,count=label(a[:,:,3]>0);removed=0
   for k in range(1,count+1):
    mask=components==k
    if mask.sum()<=3 and a[:,:,3][mask].max()<=1:removed+=int(mask.sum());a[mask]=0
   b=bounds(a);original=bounds(np.asarray(source));dy=original[3]-b[3];packed=np.zeros_like(a)
   if dy>0:assert not a[-dy:,:,3].any();packed[dy:]=a[:-dy]
   elif dy<0:assert not a[:-dy,:,3].any();packed[:dy]=a[-dy:]
   else:packed=a.copy()
   assert np.count_nonzero(packed[:,:,3])==np.count_nonzero(a[:,:,3])
   im=Image.fromarray(packed);im.save(dst);bb=bounds(packed)
   rec=dict(key=key,slot=slot,rawSize=rawim.size,bounds=bb,selectedBounds=original,heightDelta=(bb[3]-bb[1])-(original[3]-original[1]),soleDelta=bb[3]-original[3],wholeShiftY=dy,removedDisconnectedAlpha1Pixels=removed,rawSha256=sha(raw),frameSha256=sha(dst),promptSha256=sha(S/'prompt.txt'),referenceHashes=refs,receipt=receipt)
   assert abs(rec['heightDelta'])<=3 and rec['soleDelta']==0,rec
   (S/'provenance.json').write_text(json.dumps(rec,indent=2)+'\n')
   for p in [raw,S/'prompt.txt',S/'references.json',S/'receipt.json']:inputs[p.relative_to(R).as_posix()]=sha(p)
  inputs[dst.relative_to(R).as_posix()]=sha(dst);records.append(rec);new[key].append(im)
 s=copy.deepcopy(c['state']);s['frameFiles']=[f'res://character/bill-east-torch-handoffs-master-v1/frames/{key}/{slot:03}.png' for slot in range(6)]
 s['provenance']='Four whole built-in image edits; exact current idle/weld endpoint pixels. Original intermediate sole, uniform raw-square scale and selected520ms timing.';states.append(s)
m=json.loads((R/contract['manifest']).read_text());m.update(name='Bill East master torch draw/stow',status='provisional_unselected',states=states,frameSize=[256,256],pivot=[128,224],standingHeight=148,textureFilter='linear',strideDistanceCells={})
(D/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
assert new['torch-draw-east'][0].tobytes()==new['torch-stow-east'][5].tobytes()==idle.tobytes()
assert new['torch-draw-east'][5].tobytes()==new['torch-stow-east'][0].tobytes()==torch.tobytes()
movies=[]
def movie(name,frames,times,rate):
 p=D/f'{name}-{rate}.png';dur=[t*rate for t in times];frames[0].save(p,save_all=True,append_images=frames[1:],duration=dur,loop=0,disposal=0,blend=0)
 expected=[]
 for im,t in zip(frames,dur):
  if expected and expected[-1][0].tobytes()==im.tobytes():expected[-1][1]+=t
  else:expected.append([im,t])
 decoded=Image.open(p);assert decoded.n_frames==len(expected)
 for i,(im,t) in enumerate(expected):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==im.tobytes() and decoded.info['duration']==t
 movies.append(dict(file=p.name,sourceSlots=len(frames),decodedFrames=decoded.n_frames,durationMs=sum(dur),sha256=sha(p)))
for key,c in contract['states'].items():
 for kind,frames in [('selected',old[key]),('candidate',new[key])]:
  for rate in [1,4]:movie(key+'-'+kind,frames,c['state']['frameDurationsMs'],rate)
 board=Image.new('RGBA',(1536,825),'#17252d');draw=ImageDraw.Draw(board)
 for slot in range(6):
  for row,(name,im) in enumerate([('Previous selected',old[key][slot]),('Master repair',new[key][slot]),('Current idle',idle)]):
   draw.text((slot*256+8,row*275+8),f'{slot}: {name}',fill='white');board.alpha_composite(im,(slot*256,row*275+18))
 board.save(D/(key+'-comparison.png'))
weldm=json.loads((R/'character/bill-east-torch-master-v1/manifest.json').read_text());welds=next(s for s in weldm['states'] if s['id']=='weld-east')
weldfiles=[p.replace('res://','') for p in welds['frameFiles']];weld=[Image.open(R/p).convert('RGBA') for p in weldfiles]
for p in weldfiles:protected[p]=sha(R/p)
protected['character/bill-east-torch-master-v1/manifest.json']=sha(R/'character/bill-east-torch-master-v1/manifest.json')
chain=[idle]+new['torch-draw-east']+weld*3+new['torch-stow-east']+[idle]
times=[600]+states[0]['frameDurationsMs']+welds['frameDurationsMs']*3+states[1]['frameDurationsMs']+[600]
for rate in [1,4]:movie('full-sequence',chain,times,rate)
sources={}
for s in states:sources[s['id']]=dict(manifest='character/bill-east-torch-handoffs-master-v1/manifest.json',files=[p.replace('res://','') for p in s['frameFiles']],durations=s['frameDurationsMs'],loop=s['loop'])
sources['weld-east']=dict(manifest='character/bill-east-torch-master-v1/manifest.json',files=weldfiles,durations=welds['frameDurationsMs'],loop=True)
review=dict(records=records,inputs=inputs,protectedInputs=protected,sources=sources,movies=movies,frameCount=12,newWholeSources=8,exactEndpointSlots=4,processing='Uniform raw-square to256 LANCZOS; only disconnected <=3px/maxalpha1 cleanup; wholeY to original intermediate sole. Exact current whole endpoints. No part stamping, per-pose stretching or local tone masks.',visualReviewed=False,nativeTested=False,normalAdmission=False)
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
cards=''
for key in sources:
 if key=='weld-east':continue
 for kind in ['selected','candidate']:cards+=f'<div class="card">{key} · {kind}<br><img class="sprite motion" data-name="{key}-{kind}" src="{key}-{kind}-1.png"></div>'
html='''<!doctype html><html lang="en"><meta charset="utf-8"><title>Bill East torch draw and stow</title><style>body{background:#17252d;color:#dbe5e9;font:16px system-ui;margin:24px}p{max-width:1000px;line-height:1.5}.row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.card{background:#20313b;padding:12px}img{max-width:100%}.sprite{width:100%;height:230px;object-fit:contain}button{padding:10px;margin:8px;background:#34515f;color:white;border:0}</style><h1>Bill East: torch draw and stow</h1><p>Eight intermediate whole figures restored to the current matte suit and warm face. Four endpoint slots reuse the current idle or welding pose exactly. Both original520ms transitions preserved. Review candidate.</p><button id="speed">Quarter speed</button><h2>Full repaired sequence</h2><div class="card">Idle → draw → weld → stow → idle<br><img class="sprite motion" data-name="full-sequence" src="full-sequence-1.png"></div><h2>Previous and repaired handoffs</h2><div class="row">'''+cards+'</div>'+''.join(f'<h2>{key}: every source</h2><img src="{key}-comparison.png">' for key in contract['states'])+'''<p>Preview sequence compares material and endpoint registration. Normal gameplay selection remains unchanged; this does not certify autonomous job completion, other directions or equipment variants.</p><script>let slow=false;document.querySelector('#speed').onclick=()=>{slow=!slow;document.querySelectorAll('.motion').forEach(im=>im.src=im.dataset.name+'-'+(slow?4:1)+'.png');document.querySelector('#speed').textContent=slow?'Normal speed':'Quarter speed'}</script></html>'''
(D/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(frames=12,newSources=8,exactEndpoints=4,heightDeltas=[r['heightDelta'] for r in records if 'heightDelta'in r],wholeY=[r['wholeShiftY'] for r in records if 'wholeShiftY'in r],movies=len(movies),decodedFrames=sum(v['decodedFrames'] for v in movies),protected=len(protected))))
