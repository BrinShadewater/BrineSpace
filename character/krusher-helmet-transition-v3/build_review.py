from pathlib import Path
import json,hashlib,math,subprocess,zipfile
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;O=P/'review';report=json.loads((O/'native/report.json').read_text());captures=report['captures'];ends=np.cumsum([c['durationMs'] for c in captures]);duration=float(ends[-1]);video=O/'helmet-preview.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','960x600','-framerate','60','-i','-','-an','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
images=[Image.open(O/'native'/c['file']).convert('RGB').tobytes() for c in captures]
for i in range(math.ceil(duration*60/1000)):
 index=min(int(np.searchsorted(ends,i*1000/60,side='right')),len(captures)-1);proc.stdin.write(images[index])
proc.stdin.close();assert proc.wait()==0
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(video)]));actual=float(probe['format']['duration']);assert abs(actual-duration/1000)<=1/60+0.001
audit={'sourceDurationMs':duration,'videoDurationSeconds':actual,'captures':len(captures),'videoSha256':hashlib.sha256(video.read_bytes()).hexdigest(),'scope':'24 native prescribed pose captures replayed with manifest holds at 60fps; not an unbroken motion recording'};(O/'preview.json').write_text(json.dumps(audit,indent=2))
html='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krusher helmet on/off</title><style>body{max-width:1000px;margin:24px auto;padding:0 16px;background:#242c31;color:#e0ebed;font:18px system-ui}video,img{width:100%;height:auto}a{color:#93c3c6}</style><h1>Krusher Dom</h1><p>System Administrator / AI &amp; Robotics / James utility suit / matte muted cyan</p><video controls playsinline loop preload="metadata" src="helmet-preview.mp4"></video><p><a href="helmet-preview.mp4">Open video directly</a></p><img src="../contact-sheet.png" alt="Twelve helmet fitting poses"><p>East helmet on/off candidate. Original body motion and timing reused, exact current idle endpoints. Native pose captures replay source holds. Review pack; normal crew routing is not installed.</p>'''
(O/'index.html').write_text(html)
readme='Krusher Dom — east helmet on/off candidate\n24 frame references / 12 distinct poses. Original James body motion and clocks; muted matte cyan #527C80 and Krusher identity. Exact bare/equipped idle joins. Preview replays native pose captures, not continuous recording. Not installed.\n'
with zipfile.ZipFile(P/'Krusher-helmet-preview.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.write(video,'helmet-preview.mp4');z.write(P/'contact-sheet.png','contact-sheet.png');z.writestr('index.html',html.replace('../contact-sheet.png','contact-sheet.png'));z.writestr('README.txt',readme)
print(json.dumps({'videoSeconds':actual,'zipBytes':(P/'Krusher-helmet-preview.zip').stat().st_size,'files':4}))
