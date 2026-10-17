from pathlib import Path
import json,math,hashlib,subprocess,zipfile
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;O=P/'review';r=json.loads((O/'native/report.json').read_text());ids=[a+'-'+d for d in ['north','south'] for a in ['meal-acquire','cup-acquire','meal-deposit','cup-deposit']];clips=[c for key in ids for c in r['captures'] if c['state']==key];ends=np.cumsum([c['durationMs'] for c in clips]);duration=float(ends[-1]);images={c['file']:Image.open(O/'native'/c['file']).convert('RGB').tobytes() for c in clips};video=O/'service-preview.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','960x600','-framerate','60','-i','-','-an','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
for i in range(math.ceil(duration*60/1000)):
 index=min(int(np.searchsorted(ends,i*1000/60,side='right')),len(clips)-1);proc.stdin.write(images[clips[index]['file']])
proc.stdin.close();assert proc.wait()==0
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(video)]));actual=float(probe['format']['duration']);assert abs(actual-duration/1000)<=1/60+0.001
chapters=[];start=0
for key in ids:
 total=sum(c['durationMs'] for c in clips if c['state']==key);chapters.append({'state':key,'startMs':start,'durationMs':total});start+=total
audit={'sourceDurationMs':duration,'videoDurationSeconds':actual,'chapters':chapters,'videoSha256':hashlib.sha256(video.read_bytes()).hexdigest(),'scope':'Eight service states replayed from39unique prescribed native pose captures with source holds; not unbroken recording'};(O/'preview.json').write_text(json.dumps(audit,indent=2))
html='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krusher meal service</title><style>body{max-width:1000px;margin:24px auto;padding:0 16px;background:#242c31;color:#e0ebed;font:18px system-ui}video,img{width:100%;height:auto}a{color:#93c3c6}</style><h1>Krusher Dom / pickup and deposit</h1><p>System Administrator / James utility suit / matte muted cyan</p><p id="state"></p><video controls playsinline loop preload="metadata" src="service-preview.mp4"></video><p><a href="service-preview.mp4">Open video directly</a></p><img src="../new-poses-sheet.png" alt="19 new meal service poses"><p>8acquire/deposit states +80indexed returns. Every return ends at exact canonical idle. Existing body and utensils reused, new bowing head angles. Prescribed native source poses replay source holds; shared pose captions identify source IDs. Not station prop contact or normal runtime integration.</p><script>const chapters=CHAPTERS;const video=document.querySelector('video');video.addEventListener('timeupdate',()=>{const now=video.currentTime*1000;const c=chapters.find(c=>now>=c.startMs&&now<c.startMs+c.durationMs);document.getElementById('state').textContent=c?c.state:''});</script>'''.replace('CHAPTERS',json.dumps(chapters))
(O/'index.html').write_text(html)
with zipfile.ZipFile(P/'Krusher-service-preview.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.write(video,'service-preview.mp4');z.write(P/'new-poses-sheet.png','new-poses-sheet.png');z.writestr('index.html',html.replace('../new-poses-sheet.png','new-poses-sheet.png'));z.writestr('README.txt','Krusher Dom — meal/cup service animation candidate.88states/39unique poses;80indexed returns end exactly at canonical idle. Source clocks/utensils/body preserved. Native prescribed pose replay, not continuous recording or station contact proof. Complete animation goal remains active.\n')
with zipfile.ZipFile(P/'Krusher-service-preview.zip') as z:assert z.testzip() is None
print(json.dumps({'videoSeconds':actual,'zipBytes':(P/'Krusher-service-preview.zip').stat().st_size,'files':4}))
