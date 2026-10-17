from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
packs=[P.parent/'crew-runtime-matte-v1/bill',P]
clips=[];cycles=[]
for p in packs:
 m=json.loads((p/'manifest.json').read_text());s=next(s for s in m['states'] if s['id']=='walk-north');cycles.append(s.get('gaitCycles',1))
 clips.append([Image.open(p/f).convert('RGBA') for f in s['frameFiles']])
out=[]
for t in range(72):
 bg=Image.new('RGB',(650,350),'#303b40');d=ImageDraw.Draw(bg)
 for col,clip in enumerate(clips):
  f=clip[int(t/72*len(clip)/cycles[col])];x=col*325
  d.text((x+15,10),['Previous north','New north candidate'][col],fill='white')
  for h,dx,y in [(148,5,35),(82,205,35),(54,50,245),(27,200,245)]:
   sz=round(184*h/148);im=f.resize((sz,sz),Image.Resampling.BILINEAR);bg.paste(im,(x+dx,y),im)
 out.append(bg)
out[0].save(P/'old-new.gif',save_all=True,append_images=out[1:],duration=[10*(round((i+1)*150/72)-round(i*150/72)) for i in range(72)],loop=0)
page=(P/'index.html').read_text();page=page.replace('<img src="review.gif">','<h2>Previous / new north</h2><img src="old-new.gif"><h2>New north loop</h2><img src="review.gif">')
(P/'index.html').write_text(page)
print('Saved same-clock east/west comparison.')
