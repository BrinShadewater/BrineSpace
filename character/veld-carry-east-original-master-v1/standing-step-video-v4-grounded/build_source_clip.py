from pathlib import Path
import copy,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2]
source_files=sorted((P/'full-clip-frames-v2').glob('*.png'));assert len(source_files)==142
shellpath=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/005.png';shell=Image.open(shellpath).convert('RGBA');_,sx=np.where(np.array(shell)[-4:,:,3]>160)
files={g:[] for g in ['bare','helmet']};checks=0;fits=[]
for n,path in enumerate(source_files):
 bare=Image.open(path).convert('RGBA');a=np.array(bare);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1]
 pos=(round((hx.min()+hx.max())/2-(sx.min()+sx.max())/2),top+28-shell.height);clear=(int(hx.min())-3,top,int(hx.max())+4,top+27)
 helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos)
 protected=np.ones((256,256),bool);protected[min(top,pos[1]):max(clear[3],pos[1]+shell.height),min(pos[0],clear[0]):max(clear[2],pos[0]+shell.width)]=False
 assert np.array_equal(np.array(helmet)[protected],a[protected]);checks+=1;fits.append({'frame':n,'position':list(pos),'bodyOutsideHeadFittingExact':True})
 for gear,im in [('bare',bare),('helmet',helmet)]:
  dest=P/f'clip-frames/{gear}/{n:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest);files[gear].append(dest)
  z=np.array(im);assert not np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20);checks+=1
durations=[round((i+1)*1000/24)-round(i*1000/24) for i in range(142)]
for gear,paths in files.items():
 frames=[Image.open(path).convert('RGBA') for path in paths]
 frames[0].save(P/f'{gear}-full-source-review.png',save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0)
 replay=Image.open(P/f'{gear}-full-source-review.png');assert replay.n_frames==142
 for i,im in enumerate(frames):replay.seek(i);assert np.array_equal(np.array(replay.convert('RGBA')),np.array(im));checks+=1
 data=json.loads((P.parent/f'{gear}-key-manifest.json').read_text(encoding='utf-8'));state=copy.deepcopy(data['states'][0]);state.update(id='source-carry-east',frameCount=142,frameFiles=['res://'+path.relative_to(R).as_posix() for path in paths],frameDurationsMs=durations,loop=False)
 for key,value in [('facings','east'),('waterKinds','carry'),('waterPoses',False),('depthOffsets',0.0)]:state[key]=[value]*142
 data.update(name='Veld grounded-prompt full source study '+gear,status='full_source_review_only',states=[state]+data['states'][1:],strideDistanceCells={})
 (P/f'{gear}-source-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1792,600),'#202a30');draw=ImageDraw.Draw(board)
for row,gear in enumerate(files):
 for col,n in enumerate([0,18,36,54,72,108,141]):
  im=Image.open(files[gear][n]);board.paste(im,(col*256,row*290+23),im);draw.text((col*256+3,row*290+3),f'{gear} raw{n}',fill='white')
board.save(P/'paired-full-source-review.png')
bound=[shellpath,P/'source.mp4',P/'prompt.txt',P/'master-input.png',P/'source-registration-v2.json',Path(__file__)]+[f for paths in files.values() for f in paths]+list(P.glob('*-source-manifest.json'))
report={'frameCountPerGear':142,'durationMs':sum(durations),'checks':checks,'failures':0,'helmetFits':fits,'bindings':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in bound},'scope':'Complete142-frame5.917s source study in both gears, original whole profile helmet, exact APNG replay; finite non-loop source manifests and exact master references. No selected gait loop, stride/start/stop/world contacts/native or normal integration acceptance.'}
(P/'full-source-record.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k not in ['bindings','helmetFits']}))
