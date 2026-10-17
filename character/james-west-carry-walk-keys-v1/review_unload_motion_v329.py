from pathlib import Path
from PIL import Image, ImageDraw
from scipy import ndimage
import numpy as np
import subprocess,json,hashlib

p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-coherent-motion-v329'
def run(args):
    result=subprocess.run(args,capture_output=True,text=True)
    if result.returncode:
        (o/'extraction-error.log').write_text(result.stderr)
        raise RuntimeError(result.stderr[-1500:])
    return result.stdout
probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(o/'source.mp4')]))
stream=next(s for s in probe['streams'] if s['codec_type']=='video')
assert (stream['width'],stream['height'])==(768,768)
fps=float(stream['avg_frame_rate'].split('/')[0])/float(stream['avg_frame_rate'].split('/')[1])
rawdir=o/'raw-review';rawdir.mkdir(exist_ok=True)
run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(o/'source.mp4'),'-fps_mode','passthrough',str(rawdir/'raw-%03d.png')])
raws=sorted(rawdir.glob('raw-*.png'));assert len(raws)==int(stream['nb_frames'])
def extract(im):
    rgb=np.array(im.convert('RGB'));fg=np.max(np.abs(rgb.astype(int)-[48,59,64]),axis=2)>8
    labels,_=ndimage.label(fg);counts=np.bincount(labels.ravel());counts[0]=0
    mask=fg&(counts[labels]>=20);rgba=np.dstack([rgb,mask.astype('uint8')*255]);rgba[~mask]=0
    return Image.fromarray(rgba).resize((256,256),Image.Resampling.LANCZOS)
def metrics(im):
    a=np.asarray(im);y,x=np.where(a[:,:,3]>200);top=int(y.min())
    foot_y,foot_x=np.where(a[210:230,:,3]>200)
    hx=np.where(a[top:top+16,:,3]>128)[1]
    return dict(top=top,floor=int(y.max()),height=int(y.max()-y.min()+1),left=int(x.min()),right=int(x.max()),headWidth=int(hx.max()-hx.min()+1),headAxis=float((hx.min()+hx.max())/2),footBandLeft=int(foot_x.min()) if len(foot_x) else None,footBandRight=int(foot_x.max()) if len(foot_x) else None)
frames=[];rows=[]
fd=o/'frames/bare';fd.mkdir(parents=True,exist_ok=True)
for i,path in enumerate(raws):
    frame=extract(Image.open(path));frame.save(fd/f'{i:03}.png');frames.append(frame);rows.append(dict(frame=i,**metrics(frame)))
first=extract(Image.open(o/'first.png'));last=extract(Image.open(o/'last.png'))
first.save(o/'first-alpha-control.png');last.save(o/'last-alpha-control.png')
duration=[round((i+1)*1000/fps)-round(i*1000/fps) for i in range(len(frames))]
frames[0].save(o/'full-source.png',save_all=True,append_images=frames[1:],duration=duration,loop=1,disposal=0,blend=0)
decoded=Image.open(o/'full-source.png');checks=0;semantic=0
for i in range(decoded.n_frames):
    decoded.seek(i);pixels=decoded.convert('RGBA').tobytes();ms=0
    while semantic<len(frames) and frames[semantic].tobytes()==pixels:
        ms+=duration[semantic];semantic+=1;checks+=1
    assert ms==round(decoded.info['duration']);checks+=1
assert semantic==len(frames)
for start in range(0,len(frames),24):
    for kind in ['raw','alpha']:
        board=Image.new('RGB',(1792,1120),(48,59,64));d=ImageDraw.Draw(board)
        for j,im in enumerate(frames[start:start+24]):
            xy=((j%6)*256,(j//6)*280)
            image=Image.open(raws[start+j]).resize((256,256),Image.Resampling.LANCZOS) if kind=='raw' else im
            board.paste(image,(xy[0],xy[1]+20),image if kind=='alpha' else None)
            m=rows[start+j];d.text((xy[0]+5,xy[1]+2),f'{start+j} top{m["top"]} floor{m["floor"]} head{m["headWidth"]}',fill='white')
        for im,label,y in [(first,'First control',20),(last,'Last control',300)]:
            board.paste(im,(1536,y),im);d.text((1540,y-18),label,fill='white')
        board.save(o/f'{kind}-chronology-{start//24:02}.png')
state=dict(id='unload-north-source',frameCount=len(frames),frameFiles=[f'res://{(fd/f"{i:03}.png").relative_to(r).as_posix()}' for i in range(len(frames))],frameDurationsMs=duration,loop=False,facings=['north']*len(frames),waterKinds=['interact']*len(frames),waterPoses=[False]*len(frames),depthOffsets=[0.0]*len(frames))
(o/'bare-source-manifest.json').write_text(json.dumps(dict(name='James whole North unload source study',frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',status='provisional_not_selected_full_source',states=[state]),indent=2)+'\n')
report=dict(frameCount=len(frames),fps=fps,durationMs=sum(duration),decodedFrames=decoded.n_frames,checks=checks,failures=0,normalChanged=False,selected=False,fullGoalComplete=False,firstControl=metrics(first),lastControl=metrics(last),ranges={k:[min(row[k] for row in rows if row[k] is not None),max(row[k] for row in rows if row[k] is not None)] for k in metrics(first)},rows=rows,sourceSha256=hashlib.sha256((o/'source.mp4').read_bytes()).hexdigest(),registration=dict(scale=1/3,offset=[0,0]),alpha='Uniform background48,59,64 tolerance8; components>=20raw; no RGB correction/erosion/body fitting. Raw chronology remains authority for motion and extraction defects.',nativeRun=False)
(o/'source-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['frameCount','fps','durationMs','checks','ranges']}))
