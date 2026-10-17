"""Whole original-canvas extraction and complete walk source review; no admission."""
from pathlib import Path
import subprocess,json,hashlib,numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent;R=P.parents[2];W=P/'walk-source-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def run(args):
 result=subprocess.run(args,capture_output=True,text=True)
 if result.returncode:
  (W/'extraction-error.log').write_text(result.stderr,encoding='utf-8');raise RuntimeError(result.stderr[-800:])
 return result.stdout
def extract(im):
 rgb=np.array(im.convert('RGB'));foreground=np.max(np.abs(rgb.astype(int)-[12,18,24]),axis=2)>8
 labels,_=ndimage.label(foreground);counts=np.bincount(labels.ravel());counts[0]=0;mask=foreground&(counts[labels]>=20)
 a=np.dstack([rgb,mask.astype('uint8')*255]);a[~mask]=0
 return Image.fromarray(a).resize((256,256),Image.Resampling.LANCZOS)
def metrics(im):
 a=np.asarray(im);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1]
 return dict(height=int(y.max()-y.min()+1),top=top,floor=int(y.max()),left=int(x.min()),right=int(x.max()),headWidth=int(hx.max()-hx.min()+1),headAxis=float((hx.min()+hx.max())/2))
assert not (W/'SOURCE_REVIEW.json').exists(),'Preserve prior review'
probe=json.loads(run(['ffprobe','-v','error','-show_streams','-of','json',str(W/'source.mp4')]))['streams'][0]
assert (probe['width'],probe['height'],probe['avg_frame_rate'])==(768,768,'24/1')
D=W/'raw-review';D.mkdir(exist_ok=True)
run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(W/'source.mp4'),'-fps_mode','passthrough',str(D/'raw-%03d.png')])
raws=sorted(D.glob('raw-*.png'));assert len(raws)==int(probe['nb_frames'])
master=Image.open(W/'original-idle-master.png').convert('RGBA');control=extract(Image.open(W/'master-input.png'));control.save(W/'input-alpha-control.png')
frames=[];rows=[];bindings={str((W/name).relative_to(R).as_posix()):sha(W/name) for name in ['source.mp4','generation.json','master-input.png','original-idle-master.png','prompt.txt']}
F=W/'frames/bare';F.mkdir(parents=True,exist_ok=True)
for n,path in enumerate(raws):
 im=extract(Image.open(path));dest=F/f'{n:03}.png';im.save(dest);frames.append(im);rows.append(dict(frame=n,**metrics(im)));bindings[dest.relative_to(R).as_posix()]=sha(dest)
durations=[round((n+1)*1000/24)-round(n*1000/24) for n in range(len(frames))]
frames[0].save(W/'complete-walk-source.png',save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0)
# Encoders may coalesce byte-identical adjacent poses. Verify grouped pixels/holds.
groups=[]
for im,hold in zip(frames,durations):
 if groups and im.tobytes()==groups[-1][0].tobytes():groups[-1]=(im,groups[-1][1]+hold)
 else:groups.append((im,hold))
replay=Image.open(W/'complete-walk-source.png');assert replay.n_frames==len(groups)
for i,(im,hold) in enumerate(groups):
 replay.seek(i);assert replay.convert('RGBA').tobytes()==im.tobytes();assert round(replay.info['duration'])==hold
boards=[]
for start in range(0,len(frames),24):
 board=Image.new('RGB',(1792,1160),'#202a30');draw=ImageDraw.Draw(board)
 for j,im in enumerate(frames[start:start+24]):
  x=(j%6)*256;y=(j//6)*288;board.paste(im,(x,y+24),im);m=rows[start+j];draw.text((x+4,y+4),f'{start+j} H{m["height"]} head{m["headWidth"]}',fill='white')
 board.paste(master,(1536,24),master);draw.text((1540,4),'Original master',fill='white');name=f'walk-chronology-{start//24:02}.png';board.save(W/name);boards.append(name)
ranges={key:[min(row[key] for row in rows),max(row[key] for row in rows)] for key in ['height','top','floor','headWidth','headAxis']}
report=dict(status='Full source extracted, visual/stride/loop review pending; no runtime manifest',frameCount=len(frames),durationMs=sum(durations),fps=24,allSourceFramesRetained=True,extraction='Fixed whole768-to256 mapping/offset0; dark-background alpha8/components20/no erosion/no RGB changes; no pose-bound rescale/recenter/refloor.',master=metrics(master),control=metrics(control),ranges=ranges,frames=rows,boards=boards,replayGroups=len(groups),replayChecks=2*len(groups),bindings=bindings)
(W/'SOURCE_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k] for k in ['frameCount','durationMs','ranges','replayChecks','status']}))
