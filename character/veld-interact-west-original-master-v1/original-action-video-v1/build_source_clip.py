from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2]
sourcefiles=sorted((P/'full-clip-frames-uneroded-v1').glob('*.png'));assert len(sourcefiles)==142
shellpath=R/'character/veld-helmet-original-turntable-west-v1/mixed-v5-study/shells/005.png';shell=Image.open(shellpath).convert('RGBA');assert shell.size==(33,39)
master=Image.open(P/'registered-reference.png').convert('RGBA');a=np.asarray(master);top=int(np.where(a[:,:,3]>200)[0].min());hx=np.where(a[top:top+16,:,3]>128)[1];sx=np.where(np.asarray(shell)[-4:,:,3]>160)[1]
position=(round((hx.min()+hx.max())/2-(sx.min()+sx.max())/2),top+28-shell.height);clear=(int(hx.min())-3,top,int(hx.max())+4,top+27)
protected=np.ones((256,256),bool);protected[min(top,position[1]):max(clear[3],position[1]+shell.height),min(clear[0],position[0]):max(clear[2],position[0]+shell.width)]=False
def fitted(bare):
 equipped=bare.copy();equipped.paste((0,0,0,0),clear);equipped.alpha_composite(shell,position)
 assert np.array_equal(np.asarray(equipped)[protected],np.asarray(bare)[protected]);return equipped
inventory=json.loads((R/'character/veld-master-consistency-current-v2/selected-library.json').read_bytes());paths={g:[] for g in ['bare','helmet']};checks=0;bound={shellpath,P/'source.mp4',P/'master-input.png',P/'prompt.txt',P/'uneroded-source-audit.json',Path(__file__)}
for n,source in enumerate(sourcefiles):
 bare=Image.open(source).convert('RGBA');helmet=fitted(bare);checks+=1
 for gear,im in [('bare',bare),('helmet',helmet)]:
  dest=P/f'clip-frames/{gear}/{n:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest);paths[gear].append(dest);bound.add(dest)
  z=np.asarray(im);assert not np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20);checks+=1
 bound.add(source)
durations=[round((n+1)*1000/24)-round(n*1000/24) for n in range(142)]
for gear in paths:
 ref=master if gear=='bare' else fitted(master);refpath=P/f'{gear}-original-reference.png';ref.save(refpath);bound.add(refpath)
 entry=inventory['resolved'][gear]['idle-west'];selectedpath=R/entry['frameFiles'][0];assert hashlib.sha256(selectedpath.read_bytes()).hexdigest()==inventory['sourceBindings'][entry['frameFiles'][0]]
 idle=Image.open(selectedpath).convert('RGBA');plate=Image.new('RGBA',(256,256));px,py=entry['pivot'];plate.alpha_composite(idle,(128-round(px),224-round(py)));idlepath=P/f'{gear}-selected-idle.png';plate.save(idlepath);bound.update([selectedpath,idlepath])
 frames=[Image.open(path).convert('RGBA') for path in paths[gear]];frames[0].save(P/f'{gear}-full-source-review-uneroded.png',save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0)
 replay=Image.open(P/f'{gear}-full-source-review-uneroded.png');assert replay.n_frames==142
 for i,im in enumerate(frames):replay.seek(i);assert np.array_equal(np.asarray(replay.convert('RGBA')),np.asarray(im));assert round(replay.info['duration'])==durations[i];checks+=2
 def state(id,files,ds,loop):return dict(id=id,frameCount=len(files),frameFiles=['res://'+p.relative_to(R).as_posix() for p in files],frameDurationsMs=ds,loop=loop,facings=['west']*len(files),waterKinds=['interact']*len(files),waterPoses=[False]*len(files),depthOffsets=[0.0]*len(files))
 data=dict(name='Veld original West complete interaction source '+gear,status='staged_source_review_only',frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,textureFilter='linear',precomposed=True,strideDistanceCells={},states=[state('source-interact-west',paths[gear],durations,False),state('reference-west',[refpath],[1000],True),state('idle-west',[idlepath],[1000],True)])
 manifest=P/f'{gear}-source-manifest.json';manifest.write_text(json.dumps(data,indent=2)+'\n');bound.add(manifest)
b=Image.new('RGB',(1792,600),'#202a30');draw=ImageDraw.Draw(b)
for row,gear in enumerate(paths):
 for col,n in enumerate([0,18,36,54,72,108,141]):
  im=Image.open(paths[gear][n]);b.paste(im,(col*256,row*290+23),im);draw.text((col*256+3,row*290+3),f'{gear} source{n}',fill='white')
b.save(P/'paired-uneroded-source-review.png')
record=dict(frameCountPerGear=142,durationMs=sum(durations),checks=checks,failures=0,helmetSource=str(shellpath.relative_to(R)).replace('\\','/'),constantHelmetFit=dict(position=position,clearBox=clear,shellSize=shell.size,bodyOutsideFittingByteExact=True),bindings={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(bound)},scope='Complete source study both gears, fixed whole original West helmet/no pose-specific fitting. Source RGB unchanged; finite142 frame/5917ms. Native/grade/contact/idle joins/normal integration acceptance separate.')
(P/'full-source-record.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:record[k] for k in ['frameCountPerGear','durationMs','checks','failures','constantHelmetFit']}))
