"""Uniform whole cargo packing, exact shared source aliases and original clocks."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label
import numpy as np,json,hashlib,copy,shutil
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-cargo-handoffs-master-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
c=json.loads((D/'selected-contract.json').read_text());protected=json.loads((D/'protected-inputs.json').read_text());assert all(sha(R/p)==h for p,h in protected.items())
def bounds(a):
 y,x=np.where(a[:,:,3]>127);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
records=[];packed_sources={};inputs={};old={};new={};states=[]
for key,s in c['states'].items():
 F=D/'frames'/key;F.mkdir(parents=True,exist_ok=True);old[key]=[];new[key]=[]
 for slot,pose in enumerate(s['poseMapping']):
  source=Image.open(R/s['files'][slot]).convert('RGBA');old[key].append(source);dst=F/f'{slot:03}.png'
  if pose in packed_sources:
   shutil.copy2(packed_sources[pose],dst);im=Image.open(dst).convert('RGBA');records.append(dict(key=key,slot=slot,aliasOf=pose,frameSha256=sha(dst)))
  else:
   P=D/pose;raw=P/'raw.png';refs=json.loads((P/'references.json').read_text());receipt=json.loads((P/'receipt.json').read_text());assert sha(Path(receipt['path']))==sha(raw)
   assert all(sha(Path(r['path']))==r['sha256'] and sha(Path(r['source']))==r['sourceSha256'] for r in refs)
   rawim=Image.open(raw).convert('RGBA');assert rawim.width==rawim.height
   a=np.asarray(rawim).copy();a[a[:,:,3]==0,:3]=0;a=np.asarray(Image.fromarray(a).resize((256,256),Image.Resampling.LANCZOS)).copy();components,count=label(a[:,:,3]>0);removed=0
   for k in range(1,count+1):
    mask=components==k
    if mask.sum()<=3 and a[:,:,3][mask].max()<=1:removed+=int(mask.sum());a[mask]=0
   b=bounds(a);original=bounds(np.asarray(source));dy=original[3]-b[3];packed=np.zeros_like(a)
   if dy>0:assert not a[-dy:,:,3].any();packed[dy:]=a[:-dy]
   elif dy<0:assert not a[:-dy,:,3].any();packed[:dy]=a[-dy:]
   else:packed=a.copy()
   assert np.count_nonzero(packed[:,:,3])==np.count_nonzero(a[:,:,3]);im=Image.fromarray(packed);bb=bounds(packed)
   rec=dict(key=key,slot=slot,pose=pose,rawSize=rawim.size,bounds=bb,selectedBounds=original,heightDelta=(bb[3]-bb[1])-(original[3]-original[1]),soleDelta=bb[3]-original[3],wholeShiftY=dy,removedDisconnectedAlpha1Pixels=removed,rawSha256=sha(raw),promptSha256=sha(P/'prompt.txt'),references=refs,receipt=receipt)
   assert abs(rec['heightDelta'])<=3 and rec['soleDelta']==0,rec
   im.save(dst);rec['frameSha256']=sha(dst);records.append(rec);packed_sources[pose]=dst;(P/'provenance.json').write_text(json.dumps(rec,indent=2)+'\n')
   for p in [raw,P/'prompt.txt',P/'references.json',P/'receipt.json']:inputs[p.relative_to(R).as_posix()]=sha(p)
  inputs[dst.relative_to(R).as_posix()]=sha(dst);new[key].append(im)
 state=copy.deepcopy(s['state']);state['frameFiles']=[f'res://character/bill-east-cargo-handoffs-master-v1/frames/{key}/{i:03}.png' for i in range(len(new[key]))];state['provenance']='Whole built-in image edits preserving original cargo pose and520ms action; identical original endpoints share one repaired whole source.';states.append(state)
assert new['pickup-east'][0].tobytes()==new['unload-east'][5].tobytes();assert new['pickup-east'][10].tobytes()==new['unload-east'][0].tobytes()
m=json.loads((R/c['manifest']).read_text());m.update(name='Bill East master pickup/unload',status='provisional_unselected',states=states,strideDistanceCells={},textureFilter='linear');(D/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
movies=[]
def movie(name,frames,times,rate):
 p=D/f'{name}-{rate}.png';dur=[t*rate for t in times];frames[0].save(p,save_all=True,append_images=frames[1:],duration=dur,loop=0,disposal=0,blend=0);expected=[]
 for im,t in zip(frames,dur):
  if expected and expected[-1][0].tobytes()==im.tobytes():expected[-1][1]+=t
  else:expected.append([im,t])
 decoded=Image.open(p);assert decoded.n_frames==len(expected)
 for i,(im,t) in enumerate(expected):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==im.tobytes() and decoded.info['duration']==t
 movies.append(dict(file=p.name,sourceSlots=len(frames),decodedFrames=decoded.n_frames,durationMs=sum(dur),sha256=sha(p)))
for key,s in c['states'].items():
 for kind,frames in [('selected',old[key]),('candidate',new[key])]:
  for rate in [1,4]:movie(key+'-'+kind,frames,s['state']['frameDurationsMs'],rate)
 rows=(len(new[key])+5)//6;board=Image.new('RGBA',(1536,rows*550),'#17252d');draw=ImageDraw.Draw(board)
 for slot in range(len(new[key])):
  for row,(name,im) in enumerate([('Previous',old[key][slot]),('Master repair',new[key][slot])]):
   x=slot%6*256;y=slot//6*550+row*275;draw.text((x+8,y+8),f'{key} / {slot}: {name}',fill='white');board.alpha_composite(im,(x,y+18))
 board.save(D/(key+'-comparison.png'))
cm=json.loads((R/'character/bill-east-carry-master-v1/manifest.json').read_text());cs=next(s for s in cm['states'] if s['id']=='carry-east');carryfiles=[p.replace('res://','') for p in cs['frameFiles']];carry=[Image.open(R/p).convert('RGBA') for p in carryfiles]
for p in carryfiles:protected[p]=sha(R/p)
protected['character/bill-east-carry-master-v1/manifest.json']=sha(R/'character/bill-east-carry-master-v1/manifest.json')
chain=[new['pickup-east'][0]]+new['pickup-east']+carry*3+new['unload-east']+[new['unload-east'][5]];times=[600]+states[0]['frameDurationsMs']+cs['frameDurationsMs']*3+states[1]['frameDurationsMs']+[600]
for rate in [1,4]:movie('full-sequence',chain,times,rate)
sources={s['id']:dict(manifest='character/bill-east-cargo-handoffs-master-v1/manifest.json',files=[p.replace('res://','') for p in s['frameFiles']],durations=s['frameDurationsMs'],loop=s['loop']) for s in states};sources['carry-east']=dict(manifest='character/bill-east-carry-master-v1/manifest.json',files=carryfiles,durations=cs['frameDurationsMs'],loop=True)
review=dict(records=records,inputs=inputs,protectedInputs=protected,sources=sources,movies=movies,frameCount=17,newWholeSources=15,sharedAliasSlots=2,processing='Uniform raw-square to256 LANCZOS; remove only disconnected <=3px/maxalpha1; wholeY registration to original complete figure bottom. Bent silhouettes retain own height; no stretching, body/face/crate stamping or grading masks. Shared original endpoint slots reuse same whole repaired source.',visualReviewed=False,nativeTested=False,normalAdmission=False)
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
cards=''.join(f'<div class="card">{key} · {kind}<br><img class="sprite motion" data-name="{key}-{kind}" src="{key}-{kind}-1.png"></div>' for key in c['states'] for kind in ['selected','candidate'])
html='''<!doctype html><html lang="en"><meta charset="utf-8"><title>Bill East pickup and unload</title><style>body{background:#17252d;color:#dbe5e9;font:16px system-ui;margin:20px}h1{margin:12px 0}h2{margin:12px 0}p{max-width:1050px;line-height:1.4}.row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.card{background:#20313b;padding:10px}img{max-width:100%}.sprite{width:100%;height:190px;object-fit:contain}button{padding:10px;margin:8px;background:#34515f;color:white;border:0}</style><h1>Bill East: pickup and unload</h1><p>Fifteen whole poses restore the matte quilted suit and warmer face. Original11-slot pickup and6-slot unload, both520ms, retain their crouches and crate handling. Two matching original endpoints remain exact shared whole sources. Review candidate.</p><button id="speed">Quarter speed</button><h2>Pickup → carry → unload</h2><div class="card">Full material and pose review<br><img class="sprite motion" data-name="full-sequence" src="full-sequence-1.png"></div><h2>Previous and repaired</h2><div class="row">'''+cards+'</div>'+''.join(f'<h2>{key}: every source</h2><img src="{key}-comparison.png">' for key in c['states'])+'''<p>Stationary browser preview compares material and joins. Carry gait is shown without world movement. Normal gameplay selection remains unchanged; actual cargo lifecycle, moving feet and gear/save acceptance remain to verify.</p><script>let slow=false;document.querySelector('#speed').onclick=()=>{slow=!slow;document.querySelectorAll('.motion').forEach(im=>im.src=im.dataset.name+'-'+(slow?4:1)+'.png');document.querySelector('#speed').textContent=slow?'Normal speed':'Quarter speed'}</script></html>''';(D/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(frames=17,uniqueWholeSources=15,exactSharedAliases=2,heightDeltas=[r['heightDelta'] for r in records if 'heightDelta'in r],wholeY=[r['wholeShiftY'] for r in records if 'wholeShiftY'in r],movies=len(movies),decodedFrames=sum(v['decodedFrames'] for v in movies),protected=len(protected))))
