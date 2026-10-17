from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,subprocess
from matte import registered,metrics
P=Path(__file__).resolve().parent;D=P/'raw-review';D.mkdir(exist_ok=True)
generation=json.loads((P/'generation.json').read_text(encoding='utf-8'));assert generation['status'].lower()=='success'
assert hashlib.sha256((P/'master-input.png').read_bytes()).hexdigest()==generation['imageSha256']
probe=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(P/'source.mp4')],capture_output=True,text=True,check=True)
info=json.loads(probe.stdout);(D/'probe.json').write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8');stream=next(s for s in info['streams'] if s['codec_type']=='video');assert (stream['width'],stream['height'])==(768,960)
decode=subprocess.run(['ffmpeg','-y','-v','error','-i',str(P/'source.mp4'),'-fps_mode','passthrough','-threads','1',str(D/'raw-%03d.png')],capture_output=True,text=True,check=True)
files=sorted(D.glob('raw-*.png'));master=Image.open(P/'registered-reference.png').convert('RGBA');control=Image.open(P/'input-alpha-control.png').convert('RGBA');frames=[];rows=[]
for start in range(0,len(files),24):
 rawboard=Image.new('RGB',(1536,1200),(32,43,49));alphaboard=Image.new('RGB',(1792,1200),(32,43,49));rd=ImageDraw.Draw(rawboard);ad=ImageDraw.Draw(alphaboard)
 for j,file in enumerate(files[start:start+24]):
  n=start+j;raw=Image.open(file).convert('RGB');im=registered(raw);dest=P/'full-clip-frames-v2'/f'{n:03}.png';dest.parent.mkdir(exist_ok=True);im.save(dest);frames.append(im)
  a=np.array(raw);border=np.concatenate([a[:30].reshape(-1,3),a[-30:].reshape(-1,3),a[:,:30].reshape(-1,3),a[:,-30:].reshape(-1,3)]).astype(int)
  rows.append({'frame':n,**metrics(im),'backgroundMedian':np.median(border,axis=0).tolist(),'backgroundMaxDistance':int(np.abs(border-np.array([12,18,24])).max()),'backgroundBeyondToleranceFraction':float((np.abs(border-np.array([12,18,24])).max(1)>8).mean())})
  rawboard.paste(raw.resize((230,288)),((j%6)*256,(j//6)*300+12));rd.text(((j%6)*256+3,(j//6)*300),f'raw{n}',fill='white')
  alphaboard.paste(im,((j%6)*256,(j//6)*290+20),im);ad.text(((j%6)*256+3,(j//6)*290+3),f'{n} H{rows[-1]["height"]} head{rows[-1]["headWidth"]} floor{rows[-1]["floor"]}',fill='white')
 alphaboard.paste(master,(1536,20),master);ad.text((1540,3),'Original native master',fill='white');rawboard.save(D/f'chronology-{start//24:02}.png');alphaboard.save(P/f'alpha-v2-chronology-{start//24:02}.png')
num,den=map(int,stream['avg_frame_rate'].split('/'));fps=num/den;durations=[round((i+1)*1000/fps)-round(i*1000/fps) for i in range(len(frames))]
frames[0].save(P/'full-source-review-v2.png',save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0);replay=Image.open(P/'full-source-review-v2.png');assert replay.n_frames==len(frames)
for i,im in enumerate(frames):
 replay.seek(i);assert np.array_equal(np.array(replay.convert('RGBA')),np.array(im));assert round(replay.info['duration'])==durations[i]
report={'frameCount':len(files),'fps':fps,'durationMs':sum(durations),'checks':len(frames)*2,'failures':0,'videoTaskId':generation['task_id'],'sourceSHA256':hashlib.sha256((P/'source.mp4').read_bytes()).hexdigest(),'sourceScale':1/3,'fixedOffset':[0,-32],'master':metrics(master),'alphaControl':metrics(control),'rows':rows,'ranges':{k:[min(r[k] for r in rows),max(r[k] for r in rows)] for k in ['height','headWidth','headAxis','headTop','floor','upperBodyWidth']},'scope':'Complete source at frozen original-native1/3 density/offset. Fixed dark-background RGB12,18,24/tolerance8/ALL foreground components20rawpixels or larger/one-raw-pixel erosion alpha extraction only; opaque RGB untouched before whole resample. Keeps disconnected meaningful parts, based on prior dark-trial extraction lesson. No per-frame material/registration/density/anatomy edits. Replay checks prove exact pixels/timing only; visual master/contact/standing/native/runtime acceptance separate.'}
(P/'source-registration-v2.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
indices=[0,len(frames)//4,len(frames)//2,3*len(frames)//4,len(frames)-1];board=Image.new('RGB',(1792,800),(32,43,49));draw=ImageDraw.Draw(board)
for j,(im,label) in enumerate([(master,'Original native'),(control,'Input extraction control')]+[(frames[n],f'Stop source raw{n}') for n in indices]):
 draw.text((j*256+3,5),label,fill='white');board.paste(im,(j*256,25),im);crop=im.crop((98,70,170,165)).resize((216,285),Image.Resampling.NEAREST);board.paste(crop,(j*256+5,330),crop)
board.save(P/'master-source-comparison-v2.png');print(json.dumps({k:report[k] for k in ['frameCount','fps','durationMs','checks','failures','ranges']}))
