from pathlib import Path
import subprocess,json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[3]
def run(args):
 result=subprocess.run(args,capture_output=True,text=True)
 if result.returncode:
  (P/'extraction-error.log').write_text(result.stderr,encoding='utf-8')
  raise RuntimeError(result.stderr[-1200:])
 return result.stdout
probe=json.loads(run(['ffprobe','-v','error','-show_streams','-of','json',str(P/'source.mp4')]))['streams'][0]
assert (probe['width'],probe['height'],probe['avg_frame_rate'])==(768,768,'24/1')
D=P/'raw-review';D.mkdir(exist_ok=True)
run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(P/'source.mp4'),'-fps_mode','passthrough',str(D/'raw-%03d.png')])
raws=sorted(D.glob('raw-*.png'));assert len(raws)==int(probe['nb_frames'])
def extract(im):
 rgb=np.array(im.convert('RGB'));foreground=np.max(np.abs(rgb.astype(int)-[12,18,24]),axis=2)>8
 labels,_=ndimage.label(foreground);counts=np.bincount(labels.ravel());counts[0]=0;mask=foreground&(counts[labels]>=20)
 a=np.dstack([rgb,mask.astype('uint8')*255]);a[~mask]=0
 return Image.fromarray(a).resize((256,256),Image.Resampling.LANCZOS)
def metrics(im):
 a=np.asarray(im);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];tx=np.where(a[top+34:top+79,:,3]>200)[1]
 return dict(height=int(y.max()-y.min()+1),top=top,floor=int(y.max()),left=int(x.min()),right=int(x.max()),headWidth=int(hx.max()-hx.min()+1),headAxis=float((hx.min()+hx.max())/2),upperWidth=int(tx.max()-tx.min()+1))
master=Image.open(P/'prepared-idle-master.png').convert('RGBA');control=extract(Image.open(P/'master-input.png'));control.save(P/'input-alpha-control.png')
shell_path=R/'character/veld-shared-helmet-south-v1/fitted-helmet.png';shell=Image.open(shell_path).convert('RGBA');assert shell.size==(35,39)
def fitted(bare):
 helmet=bare.copy();helmet.paste((0,0,0,0),(111,77,143,102));helmet.alpha_composite(shell,(110,69))
 a=np.array(bare);b=np.array(helmet);protected=np.ones((256,256),bool);protected[69:108,110:145]=False
 assert np.array_equal(a[protected],b[protected]);return helmet
frames=[];helmets=[];rows=[];checks=0;bound={P/'source.mp4',P/'master-input.png',P/'prompt.txt',P/'prepared-idle-master.png',P/'original-idle-master.png',P/'INPUTS.json',shell_path,Path(__file__)}
for n,path in enumerate(raws):
 im=extract(Image.open(path));helm=fitted(im);checks+=1;frames.append(im);helmets.append(helm);rows.append(dict(frame=n,**metrics(im)))
 for gear,source in [('bare',im),('helmet',helm)]:
  dest=P/f'frames/{gear}/{n:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);source.save(dest);bound.add(dest)
durations=[round((n+1)*1000/24)-round(n*1000/24) for n in range(len(frames))]
for gear,sources in [('bare',frames),('helmet',helmets)]:
 replaypath=P/f'{gear}-full-source.png';sources[0].save(replaypath,save_all=True,append_images=sources[1:],duration=durations,loop=1,disposal=0,blend=0)
 # PNG encoder coalesces exact consecutive real source poses. Preserve every authored
 # slot in manifests and verify the equivalent timed replay without pixel perturbation.
 runs=[]
 for i,source in enumerate(sources):
  if runs and source.tobytes()==sources[runs[-1][0]].tobytes():runs[-1][1]+=durations[i];runs[-1][2].append(i)
  else:runs.append([i,durations[i],[i]])
 replay=Image.open(replaypath);assert replay.n_frames==len(runs)
 for j,(first,hold,slots) in enumerate(runs):
  replay.seek(j);assert round(replay.info['duration'])==hold;checks+=1
  for i in slots:assert replay.convert('RGBA').tobytes()==sources[i].tobytes();checks+=1
 (P/f'{gear}-replay-source-runs.json').write_text(json.dumps(dict(authoredSlots=len(sources),encodedFrames=len(runs),runs=runs,scope='Exact consecutive source poses coalesced by PNG encoder, summed actual durations; every original slot retained in manifests.'),indent=2)+'\n',encoding='utf-8')
 ref=master if gear=='bare' else fitted(master);ref.save(P/f'{gear}-original-reference.png')
 for start in range(0,len(sources),24):
  board=Image.new('RGB',(1792,1160),'#202a30');draw=ImageDraw.Draw(board)
  for j,im in enumerate(sources[start:start+24]):
   xy=((j%6)*256,(j//6)*288);board.paste(im,(xy[0],xy[1]+24),im);draw.text((xy[0]+4,xy[1]+4),f'{gear} {start+j} H{rows[start+j]["height"]} head{rows[start+j]["headWidth"]}',fill='white')
  board.paste(ref,(1536,24),ref);draw.text((1540,4),'Original master',fill='white');board.save(P/f'{gear}-chronology-{start//24:02}.png')
 state=dict(id='source-draw-south',frameCount=len(sources),frameFiles=[f'res://character/veld-interact-south-original-master-v1/scanner-held-key-v3-square/draw-video-v1/frames/{gear}/{i:03}.png' for i in range(len(sources))],frameDurationsMs=durations,loop=False,facings=['south']*len(sources),waterKinds=['interact']*len(sources),waterPoses=[False]*len(sources),depthOffsets=[0.0]*len(sources))
 (P/f'{gear}-source-manifest.json').write_text(json.dumps(dict(name='Veld original-guided South scanner '+gear,status='staged_full_source_review_only',frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,textureFilter='linear',precomposed=True,states=[state]),indent=2)+'\n')
for start in range(0,len(raws),24):
 board=Image.new('RGB',(1536,1160),'#202a30');draw=ImageDraw.Draw(board)
 for j,path in enumerate(raws[start:start+24]):
  im=Image.open(path).resize((256,256),Image.Resampling.LANCZOS);xy=((j%6)*256,(j//6)*288);board.paste(im,(xy[0],xy[1]+24));draw.text((xy[0]+4,xy[1]+4),f'Raw source {start+j}',fill='white')
 board.save(P/f'raw-chronology-{start//24:02}.png')
ims=[Image.open(P/'original-idle-master.png').convert('RGBA'),master,control]+[frames[i] for i in [0,35,71,106,len(frames)-1]]
board=Image.new('RGB',(2048,560),'#202a30');draw=ImageDraw.Draw(board)
for j,im in enumerate(ims):
 board.paste(im,(j*256,24),im);draw.text((j*256+3,3),['Original','Prepared master','Input control','Source0','Source35','Source71','Source106','Source last'][j],fill='white')
 detail=im.crop((100,60,164,124)).resize((256,256),Image.Resampling.NEAREST);board.paste(detail,(j*256,288),detail)
board.save(P/'master-control-source-comparison.png')
record=dict(frameCount=len(frames),durationMs=sum(durations),checks=checks,failures=0,master=metrics(master),control=metrics(control),rows=rows,ranges={k:[min(r[k] for r in rows),max(r[k] for r in rows)] for k in metrics(master)},helmetFit=dict(source=shell_path.relative_to(R).as_posix(),position=[110,69],clear=[111,77,143,102],bodyOutsideFitExact=True),registration=dict(scale=1/3,offset=[0,0]),alpha='Uniform dark12/18/24,tolerance8,components>=20raw,no erosion; no RGB correction.',bindings={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(bound)},scope='Complete finite source both gears; loop/continuous source/native/idle-action/controller/full-library acceptance remains separate.')
(P/'SOURCE_REVIEW.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:record[k] for k in ['frameCount','durationMs','checks','master','control','ranges']}))
