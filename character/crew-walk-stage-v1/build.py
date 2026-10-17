from pathlib import Path
import json,hashlib,os
import numpy as np
from PIL import Image,ImageDraw

P=Path(__file__).resolve().parent;C=P.parent
directions=['south','east','north','west']
folders={'bill':['bill-video-south-v2','bill-video-east-v1','bill-video-north-v1','bill-video-west-v1'],
 'branforth':['branforth-video-south-v1','branforth-video-east-v2','branforth-video-north-v2','branforth-video-west-v1']}
cycles={'bill':[3,1,1,2],'branforth':[3,2,1,2]}
clips={};checks=[];hashes={}
def neutral(im):
 a=np.array(im);v=a[:,:,:3].astype(float);mask=(a[:,:,3]>=128)&(np.ptp(v,axis=2)<24)&(v.mean(axis=2)>25)&(v.mean(axis=2)<145)
 return np.median(v[mask],axis=0)
def load(root,state):return [Image.open(root/f).convert('RGBA') for f in state['frameFiles']]
def metrics(frames):
 heights=[];soles=[];col=[];clipped=0
 for im in frames:
  a=np.array(im);ys,xs=np.where(a[:,:,3]>=128);heights.append(int(ys.max()-ys.min()+1));soles.append(int(ys.max()+1));col.append(neutral(im));clipped+=int(xs.min()==0 or ys.min()==0 or xs.max()==183 or ys.max()==183)
 return dict(heightRange=[min(heights),max(heights)],soleRange=[min(soles),max(soles)],neutralMedianRange=[np.min(col,axis=0).tolist(),np.max(col,axis=0).tolist()],clippedFrames=clipped)
for who,roots in folders.items():
 dst=P/who;dst.mkdir(parents=True,exist_ok=True);states=[]
 for j,(direction,folder) in enumerate(zip(directions,roots)):
  root=C/folder;m=json.loads((root/'manifest.json').read_text());s=dict(m['states'][0]);frames=load(root,s)
  for f in s['frameFiles']:hashes[str((root/f).relative_to(C))]=hashlib.sha256((root/f).read_bytes()).hexdigest()
  s['frameFiles']=[os.path.relpath(root/f,dst).replace('\\','/') for f in s['frameFiles']];s['gaitCycles']=cycles[who][j];states.append(s)
  master=root/'master-standing.png'
  if not master.exists():master=C/f'{who}-video-{direction}-v1/master-standing.png'
  idle=Image.open(master).convert('RGBA');target=np.median([neutral(f) for f in frames],axis=0);base=neutral(idle);gain=np.minimum(1,target/base)
  a=np.array(idle);v=a[:,:,:3].astype(float);value=v.mean(axis=2);weight=np.clip((40-np.ptp(v,axis=2))/16,0,1)*np.clip((160-value)/35,0,1)*np.clip(value/25,0,1)
  a[:,:,:3]=np.rint(v+(v*gain-v)*weight[:,:,None]).clip(0,255).astype('uint8');idle=Image.fromarray(a);idle.save(dst/f'idle-{direction}.png')
  states.append(dict(id=f'idle-{direction}',frameCount=1,frameFiles=[f'idle-{direction}.png'],frameDurationsMs=[1000],loop=True,provenance=dict(source=str(master.relative_to(C)),neutralGain=gain.tolist(),method='Static approved-reference hold; darkening only, no synthetic motion')))
  clips[(who,direction)]=(frames,s['frameDurationsMs'],[idle],[1000])
  checks.append(dict(character=who,direction=direction,source=folder,frames=len(frames),durationMs=sum(s['frameDurationsMs']),gaitCycles=cycles[who][j],cycleMs=sum(s['frameDurationsMs'])/cycles[who][j],idleNeutralBefore=base.tolist(),idleNeutralAfter=neutral(idle).tolist(),idleGain=gain.tolist(),**metrics(frames)))
 (dst/'manifest.json').write_text(json.dumps(dict(name=f'{who} staged accepted walks and matching idle holds',status='staged_not_installed',frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,precomposed=True,states=states),indent=2))
root=C/'veld-runtime-walk-v1';m=json.loads((root/'manifest.json').read_text());states={s['id']:s for s in m['states']}
for direction in directions:
 s=states[f'walk-{direction}'];idle=states[f'idle-{direction}'];frames=load(root,s);clips[('veld',direction)]=(frames,s['frameDurationsMs'],load(root,idle),idle['frameDurationsMs'])
 checks.append(dict(character='veld',direction=direction,source=root.name,frames=len(frames),durationMs=sum(s['frameDurationsMs']),gaitCycles=1,cycleMs=sum(s['frameDurationsMs']),**metrics(frames)))
def at(frames,durations,t):
 t=t%sum(durations);n=0
 while n<len(durations)-1 and t>=durations[n]:t-=durations[n];n+=1
 return frames[n]
def review(transition=False):
 out=[]
 for tick in range(144):
  bg=Image.new('RGB',(828,1016),'#263139');draw=ImageDraw.Draw(bg)
  for col,who in enumerate(['bill','veld','branforth']):
   for row,direction in enumerate(directions):
    frames,durations,idles,idleDur=clips[(who,direction)];t=tick*1000/24;label='WALK'
    if transition and (t<1000 or t>=4500):im=at(idles,idleDur,t);label='IDLE'
    else:im=at(frames,durations,t-(1000 if transition else 0))
    x=col*276;y=row*254;draw.text((x+8,y+5),f'{who.upper()} {direction.upper()} / {label}',fill='white')
    large=im.resize((230,230),Image.Resampling.NEAREST);bg.paste(large,(x+8,y+22),large)
    small=im.resize((64,64),Image.Resampling.LANCZOS);bg.paste(small,(x+208,y+176),small)
  out.append(bg)
 name='idle-walk-review.gif' if transition else 'cast-walk-review.gif'
 out[0].save(P/name,save_all=True,append_images=out[1:],duration=[40,40,50]*48,loop=0,optimize=False)
review();review(True)
(P/'checks.json').write_text(json.dumps(checks,indent=2));(P/'accepted-frame-hashes.json').write_text(json.dumps(hashes,indent=2))
for f,h in hashes.items():assert hashlib.sha256((C/f).read_bytes()).hexdigest()==h
print(json.dumps(dict(clips=len(clips),newIdleHolds=8,acceptedFramesUnchanged=len(hashes),clippedFrames=sum(c['clippedFrames'] for c in checks))))
