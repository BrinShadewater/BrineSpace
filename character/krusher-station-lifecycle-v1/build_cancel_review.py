from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess
p=Path('character/krusher-station-lifecycle-v1');o=p/'review/cancel';r=json.load(open(o/'native-indexed-evidence.json'));f=o/'video-frames';f.mkdir(exist_ok=True);font=ImageFont.truetype('assets/fonts/BarlowSemiCondensed-Regular.ttf',22);pairs=[];clock=0.
with (o/'frames.txt').open('w') as listing:
 for j in r['journeys']:
  for q in j['contactSamples']:
   source=Path(q['source']);native=Path(q['native']);im=Image.open(native).convert('RGB');src=Image.open(source).convert('RGBA');b=Image.new('RGB',(1000,600),'#242c31');d=ImageDraw.Draw(b);d.text((18,12),'KRUSHER DOM / EXTERIOR PICKUP RECALL / HELMET',font=font,fill='white');d.text((18,43),q['label']+' / '+q['state']+' / '+q['direction'],font=font,fill='#bcd6d8')
   # Native scene and source canvases at original1x; no body fit resize.
   scaled=im.resize((im.width,im.height),Image.Resampling.NEAREST);assert scaled.width<=560 and scaled.height<=500;b.paste(scaled,(20+(560-scaled.width)//2,88+(500-scaled.height)//2))
   scaled=src.resize((src.width,src.height),Image.Resampling.NEAREST);bg=Image.new('RGBA',scaled.size,'#242c31');bg.alpha_composite(scaled);b.paste(bg.convert('RGB'),(650,170));d.text((620,100),'Selected source pose / native1x',font=font,fill='#bcd6d8')
   name=f'{len(pairs):03d}.png';b.save(f/name);listing.write(f"file 'video-frames/{name}'\noption framerate 1000\nduration 0.200000000\n");pairs.append({'label':q['label'],'native':str(native),'source':str(source),'clock':q['actionElapsed'],'direction':q['direction']});clock+=.2
 listing.write(f"file 'video-frames/{name}'\noption framerate 1000\n")
with (o/'media.log').open('w') as log:subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(o/'frames.txt'),'-t',str(clock),'-vf','fps=60','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(o/'station-cancel-review.mp4')],stdout=log,stderr=log,check=True)
encoded=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(o/'station-cancel-review.mp4')],text=True));assert abs(encoded-clock)<=1/60
(o/'media.json').write_text(json.dumps({'seconds':clock,'encodedSeconds':encoded,'samples':pairs,'scope':'Four real helmet recall journeys, selected before/after-cancel actual native scene crops alongside original selected source texture. Native scene1x/source1x, each snapshot200ms; pose gallery, not continuous motion or original hold replay.'},indent=2)+'\n')
(o/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krusher recall review</title><body style="background:#242c31;color:#cadcde;font:18px sans-serif;max-width:1000px;margin:24px auto"><h1>Krusher Dom - underwater pickup recall</h1><video controls playsinline style="width:100%" src="station-cancel-review.mp4"></video><p>Selected native pose gallery from four actual trips. Each snapshot displays200ms.</p></body>')
print(json.dumps({'seconds':clock,'encodedSeconds':encoded,'samples':len(pairs)}))
