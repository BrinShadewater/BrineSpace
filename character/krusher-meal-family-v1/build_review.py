from pathlib import Path
import json,hashlib,math,subprocess,zipfile
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;O=P/'review';report=json.loads((O/'native/report.json').read_text());captures=report['captures'];assert all(c['bareDurationMs']==c['helmetDurationMs'] for c in captures)
ends=np.cumsum([c['bareDurationMs'] for c in captures]);duration=float(ends[-1]);video=O/'meal-preview.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','960x600','-framerate','60','-i','-','-an','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE)
images=[Image.open(O/'native'/c['file']).convert('RGB').tobytes() for c in captures]
for i in range(math.ceil(duration*60/1000)):
 n=min(int(np.searchsorted(ends,i*1000/60,side='right')),len(captures)-1);proc.stdin.write(images[n])
proc.stdin.close();assert proc.wait()==0
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(video)]));actual=float(probe['format']['duration']);assert abs(actual-duration/1000)<=1/60+0.001
audit={'sourceDurationMs':duration,'videoDurationSeconds':actual,'captures':len(captures),'videoSha256':hashlib.sha256(video.read_bytes()).hexdigest(),'scope':'48 paired native prescribed pose captures replayed with source holds at60fps; not continuous recording'};(O/'preview.json').write_text(json.dumps(audit,indent=2))
html='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krusher meals</title><style>body{max-width:1000px;margin:24px auto;padding:0 16px;background:#242c31;color:#e0ebed;font:18px system-ui}video,img{width:100%;height:auto}a{color:#93c3c6}</style><h1>Krusher Dom / meals</h1><p>System Administrator / James utility suit / matte muted cyan</p><video controls playsinline loop preload="metadata" src="meal-preview.mp4"></video><p><a href="meal-preview.mp4">Open video directly</a></p><img src="../bare-sheet.png" alt="Four-direction eating and drinking"><img src="../helmet-sheet.png" alt="Sealed helmet inspection substitutes"><p>Four-direction meals candidate. Source clocks and body motion retained; cups and foreground hands protected. Helmet uses existing tablet inspection. Preview replays native source poses with declared holds. Complete character animation work remains active.</p>'''
(O/'index.html').write_text(html)
with zipfile.ZipFile(P/'Krusher-meal-preview.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.write(video,'meal-preview.mp4');z.write(P/'bare-sheet.png','bare-sheet.png');z.write(P/'helmet-sheet.png','helmet-sheet.png');z.writestr('index.html',html.replace('../bare-sheet.png','bare-sheet.png').replace('../helmet-sheet.png','helmet-sheet.png'));z.writestr('README.txt','Krusher Dom — four-direction eating/drinking candidate. Sealed helmet substitutes inspection. Native prescribed pose replay, not continuous recording. Review only; complete animation goal remains active.\n')
with zipfile.ZipFile(P/'Krusher-meal-preview.zip') as z:assert z.testzip() is None
print(json.dumps({'videoSeconds':actual,'zipBytes':(P/'Krusher-meal-preview.zip').stat().st_size,'files':5}))
