from pathlib import Path
import json,subprocess,hashlib
from PIL import Image,ImageDraw
import imageio_ffmpeg
H=Path(__file__).resolve().parent;R=H.parents[1];rows={}
for g in ['bare','helmet']:
 m=json.loads((H/f'{g}-manifest.json').read_text());rows[g]=[Image.open(H/f).convert('RGBA') for f in m['states'][0]['frameFiles']]
video=H/'paired-full-speed-v1.mp4'
proc=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-f','rawvideo','-vcodec','rawvideo','-s','1200x700','-pix_fmt','rgb24','-r','50','-i','-','-an','-vcodec','libx264','-pix_fmt','yuv420p','-crf','18',str(video)],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
for i in range(126):
 phase=(i//7)%6;b=Image.new('RGBA',(1200,700),'#202a30');d=ImageDraw.Draw(b)
 for j,g in enumerate(rows):
  d.text((10,j*350+10),f'{g} / phase {phase+1}/6 / 840ms / full speed',fill='white')
  for ruler,x in [(148,128),(82,360),(54,530),(27,660)]:
   s=ruler/148;im=rows[g][phase].resize((round(256*s),round(256*s)),Image.Resampling.BILINEAR);b.alpha_composite(im,(round(x-128*s),round(j*350+170-128*s)));d.text((x-45,j*350+270),f'{ruler}px ruler',fill='white')
  master=Image.open(R/f'character/veld-water-west-coherent-v1/frames/{g}/swim-west/000.png').convert('RGBA');b.alpha_composite(master,(825,j*350+42));d.text((850,j*350+270),'selected swim master',fill='white')
 proc.stdin.write(b.convert('RGB').tobytes())
proc.stdin.close();errors=proc.stderr.read();code=proc.wait();assert code==0,errors[-1000:]
(H/'motion-reel-checks.json').write_text(json.dumps(dict(fps=50,frames=126,cycles=3,durationMs=2520,slotDurationMs=140,pairedSharedClock=True,videoSha256=hashlib.sha256(video.read_bytes()).hexdigest()),indent=2)+'\n')
print('Full-speed 3-cycle paired reel saved, 126 frames / 2520ms.')
