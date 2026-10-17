from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent
frames=[Image.open(P/f'frames/land-swim-east/{i:03}.png').convert('RGBA') for i in range(6)]
for name,expected in [('source-enter.png',frames),('source-leave.png',list(reversed(frames)))]:
 with Image.open(P/name) as apng:
  assert apng.n_frames==6
  for i,im in enumerate(expected):
   apng.seek(i);assert apng.convert('RGBA').tobytes()==im.tobytes()
  assert sum(apng.seek(i) or apng.info['duration'] for i in range(6))==500
raw=np.array(Image.open(R/'crew-side-masters-v1/bill-side-master-01.png').convert('RGBA'))
labs,_=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());ids=np.argsort(counts[1:])[-2:]+1
n=min(ids,key=lambda x:np.where(labs==x)[1].min());mask=binary_dilation(labs==n,iterations=3)&(raw[:,:,3]>0)
y,x=np.where(mask);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
pixels=raw.copy();pixels[~mask]=0;crop=Image.fromarray(pixels).crop(box)
scale=148/956.0;crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
master=Image.new('RGBA',(320,320));master.alpha_composite(crop,(round(160-(480-box[0])*scale),round(224-(977-box[1])*scale)))
board=Image.new('RGB',(2240,340),'#182932');d=ImageDraw.Draw(board)
for i,(name,im) in enumerate(zip(['Original side master','Selected idle','Interior 1','Interior 2','Interior 3','Interior 4','Selected swim'],[master]+frames)):
 board.paste(im,(i*320,20),im);d.text((i*320+5,4),name,fill='white')
board.save(P/'master-relative-review.png')
game=Image.new('RGB',(1152,460),'#182932');d=ImageDraw.Draw(game)
for j,height in enumerate([82,54,27]):
 ratio=height/148
 for i,im in enumerate(frames):
  small=im.resize((round(320*ratio),round(320*ratio)),Image.Resampling.LANCZOS)
  game.paste(small,(i*192+(192-small.width)//2,j*150+20),small)
 d.text((5,j*150+3),f'{height}px standing ruler',fill='white')
game.save(P/'gameplay-review.png')
(P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill land/water East source study</title><style>body{background:#182932;color:#ddd;font:16px sans-serif;margin:24px}img{max-width:100%}div{display:flex;gap:30px}</style><h1>Bill East — new land/water interiors</h1><p>Source study only. Four authored poses, original endpoints, fixed anatomical scale/material curve. Reverse exit is derived. Helmet, moving-gait entrance, world collision/support, interruption/Continue and native motion still pending.</p><img src="master-relative-review.png"><img src="gameplay-review.png"><div><figure><img src="source-enter.png"><figcaption>500ms entrance</figcaption></figure><figure><img src="source-leave.png"><figcaption>Derived reverse exit</figcaption></figure></div>',encoding='utf-8')
e=json.loads((P/'source-evidence.json').read_text());e.update({'APNGDecodeExact':True,'timelineMs':500,'masterReference':'character/crew-side-masters-v1/bill-side-master-01.png','masterCrop':box,'masterSourceScale':scale,'masterStandingRuler':'956 original pixels to148; no per-pose stature fitting','scope':'Static registered source/master/game-density review. No continuous/native/controller acceptance.'})
(P/'source-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
print('Exact source/endpoints/timelines verified; original-master and82/54/27px review boards prepared.')
