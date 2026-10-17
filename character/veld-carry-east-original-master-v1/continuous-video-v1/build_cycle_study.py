"""Paired 32-frame source study. This is not an admitted traveling gait."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent
R=P.parents[2]
shellpath=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/005.png'
shell=Image.open(shellpath).convert('RGBA')
_,sx=np.where(np.array(shell)[-4:,:,3]>160)
files={gear:[] for gear in ['bare','helmet']}
fits=[]; checks=0
for n in range(32,64):
    bare=Image.open(P/f'full-clip-frames/{n:03}.png').convert('RGBA')
    a=np.array(bare);y,x=np.where(a[:,:,3]>200);top=int(y.min())
    hx=np.where(a[top:top+16,:,3]>128)[1]
    pos=(round((hx.min()+hx.max())/2-(sx.min()+sx.max())/2),top+28-shell.height)
    clear=(int(hx.min())-3,top,int(hx.max())+4,top+27)
    helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos)
    protected=np.ones((256,256),bool)
    protected[min(top,pos[1]):max(clear[3],pos[1]+shell.height),min(pos[0],clear[0]):max(clear[2],pos[0]+shell.width)]=False
    assert np.array_equal(np.array(helmet)[protected],a[protected]);checks+=1
    fits.append({'sourceFrame':n,'position':list(pos),'bodyOutsideHeadFittingExact':True})
    for gear,im in [('bare',bare),('helmet',helmet)]:
        path=P/f'cycle-study/{gear}/{n-32:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
        z=np.array(im);assert not np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20);checks+=1
        files[gear].append(path)
durations=[round((i+1)*1000/24)-round(i*1000/24) for i in range(32)]
for gear,paths in files.items():
    frames=[Image.open(path).convert('RGBA') for path in paths]
    frames[0].save(P/f'{gear}-cycle-study.png',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=0,blend=0)
    replay=Image.open(P/f'{gear}-cycle-study.png')
    assert replay.n_frames==32
    for i,frame in enumerate(frames):
        replay.seek(i);assert np.array_equal(np.array(replay.convert('RGBA')),np.array(frame));checks+=1
board=Image.new('RGB',(1792,600),'#202a30');d=ImageDraw.Draw(board)
for row,gear in enumerate(files):
    for column,index in enumerate([0,5,10,15,20,25,31]):
        im=Image.open(files[gear][index]);board.paste(im,(column*256,row*290+25),im)
        d.text((column*256+3,row*290+3),f'{gear} raw{index+32}',fill='white')
board.save(P/'paired-cycle-study-review.png')
report={'status':'source_study_only','sourceFrames':list(range(32,64)),'frameDurationsMs':durations,'durationMs':sum(durations),'checks':checks,'failures':0,'helmetFits':fits,'bindings':{str(path.relative_to(R)).replace('\\','/'):hashlib.sha256(path.read_bytes()).hexdigest() for paths in files.values() for path in paths},'scope':'Whole original profile equipment fitted to ungraded fixed-scale video frames. 32 raw consecutive frames; no duplicated or interpolated source poses. Source pixel protection and APNG replay only. Near/far identity, loop continuity, rigid sole/world contacts, stride, native playback, start/stop and production integration remain unaccepted.'}
report['bindings'][str(shellpath.relative_to(R)).replace('\\','/')]=hashlib.sha256(shellpath.read_bytes()).hexdigest()
(P/'cycle-study-record.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['bindings','helmetFits','sourceFrames','frameDurationsMs']}))
