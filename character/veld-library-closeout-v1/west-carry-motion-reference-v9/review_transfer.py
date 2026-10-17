"""Preserve all transferred source frames and fixed-canvas diagnostic boards."""
from pathlib import Path
import json, subprocess, hashlib
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent
def run(args):
 r=subprocess.run(args,capture_output=True,text=True)
 if r.returncode:
  (P/'review-error.log').write_text(r.stderr,encoding='utf-8')
  raise RuntimeError(r.stderr[-800:])
 return r.stdout
assert not (P/'TRANSFER_REVIEW.json').exists(), 'Preserve previous review'
s=json.loads(run(['ffprobe','-v','error','-show_streams','-of','json',str(P/'source.mp4')]))['streams'][0]
w,h=s['width'],s['height']; a,b=map(int,s['avg_frame_rate'].split('/')); fps=a/b
assert w==h, 'Different aspect ratio requires review before fixed export'
d=P/'raw-review';d.mkdir(exist_ok=True)
run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(P/'source.mp4'),'-fps_mode','passthrough',str(d/'raw-%03d.png')])
raws=sorted(d.glob('raw-*.png')); assert len(raws)==int(s['nb_frames'])
f=P/'frames/bare';f.mkdir(parents=True,exist_ok=True)
frames=[];rows=[]
for n,p in enumerate(raws):
 rgb=np.asarray(Image.open(p).convert('RGB'))
 fg=np.max(np.abs(rgb.astype(int)-[12,18,24]),axis=2)>8
 labels,_=ndimage.label(fg);counts=np.bincount(labels.ravel());counts[0]=0;mask=fg&(counts[labels]>=20)
 arr=np.dstack([rgb,mask.astype('uint8')*255]);arr[~mask]=0
 im=Image.fromarray(arr).resize((256,256),Image.Resampling.LANCZOS);im.save(f/f'{n:03}.png');frames.append(im)
 ys,xs=np.where(np.asarray(im)[:,:,3]>200)
 top=int(ys.min());hx=np.where(np.asarray(im)[top:top+16,:,3]>128)[1]
 rows.append(dict(frame=n,height=int(ys.max()-top+1),top=top,floor=int(ys.max()),headWidth=int(hx.max()-hx.min()+1),headAxis=float((hx.min()+hx.max())/2)))
dur=[round((i+1)*1000/fps)-round(i*1000/fps) for i in range(len(frames))]
frames[0].save(P/'complete-transfer.png',save_all=True,append_images=frames[1:],duration=dur,loop=1,disposal=0,blend=0)
groups=[]
for im,hold in zip(frames,dur):
 if groups and im.tobytes()==groups[-1][0].tobytes():groups[-1]=(im,groups[-1][1]+hold)
 else:groups.append((im,hold))
replay=Image.open(P/'complete-transfer.png');assert replay.n_frames==len(groups)
for i,(im,hold) in enumerate(groups):
 replay.seek(i);assert replay.convert('RGBA').tobytes()==im.tobytes();assert round(replay.info['duration'])==hold
master=Image.open(P.parent/'west-carry-master-match-v5/frames/bare/000.png').convert('RGBA')
boards=[]
for start in range(0,len(frames),24):
 board=Image.new('RGB',(1792,1160),'#202a30');dr=ImageDraw.Draw(board)
 for j,im in enumerate(frames[start:start+24]):
  x=j%6*256;y=j//6*288;board.paste(im,(x,y+24),im);dr.text((x+4,y+4),f'{start+j} H{rows[start+j]["height"]}',fill='white')
 board.paste(master,(1536,24),master);dr.text((1540,4),'Carry identity input',fill='white')
 name=f'transfer-chronology-{start//24:02}.png';board.save(P/name);boards.append(name)
ranges={k:[min(r[k] for r in rows),max(r[k] for r in rows)] for k in ['height','top','floor','headWidth','headAxis']}
report=dict(status='Full source retained; visual review pending, no runtime admission',frameCount=len(frames),fps=fps,sourceSize=[w,h],durationMs=sum(dur),ranges=ranges,frames=rows,boards=boards,replayChecks=2*len(groups),extraction='Whole source canvas uniformly to256; dark alpha threshold8/components20; no RGB changes, per-frame registration or rescaling',sourceSha256=hashlib.sha256((P/'source.mp4').read_bytes()).hexdigest())
(P/'TRANSFER_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['frameCount','fps','sourceSize','durationMs','ranges','replayChecks']}))
