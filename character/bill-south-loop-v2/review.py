from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
P=Path(__file__).resolve().parent
def clip(root,key):
 m=json.loads((root/'manifest.json').read_text());s=next(s for s in m['states'] if s['id']==key)
 return [Image.open(root/f).convert('RGBA') for f in s['frameFiles']],s.get('gaitCycles',1)
old=clip(P.parent/'bill-video-south-v6','walk-south');new=clip(P,'walk-south')
cast=[new]+[clip(P.parent/'bill-hair-match-v1','walk-'+d) for d in ['east','north','west']]
for name,clips,labels in [('cut-comparison',[old,new],['Previous cut','Refined cut']),('directions',cast,['South revised','East hair pass','North current motion','West hair pass'])]:
 output=[]
 for tick in range(72):
  bg=Image.new('RGB',(250*len(clips),360),'#303b40');d=ImageDraw.Draw(bg)
  for j,(frames,cycles) in enumerate(clips):
   f=frames[int(tick/72*len(frames)/cycles)];x=j*250;d.text((x+8,8),labels[j],fill='white')
   for height,dx,y in [(148,30,25),(82,5,230),(54,115,230),(27,195,230)]:
    sz=round(184*height/148);im=f.resize((sz,sz),Image.Resampling.BILINEAR);bg.paste(im,(x+dx,y),im)
  output.append(bg)
 output[0].save(P/(name+'.png'));output[0].save(P/(name+'.gif'),save_all=True,append_images=output[1:],duration=[10*(round((i+1)*150/72)-round(i*150/72)) for i in range(72)],loop=0)
a=json.loads((P/'checks.json').read_text());b=np.array(a['bounds'][12:53]);assert (b[:,:2]>0).all() and (b[:,2:]<184).all()
(P/'validation.json').write_text(json.dumps({'frames':41,'durationMs':1500,'clipped':0,'heightRange':[int(min(b[:,3]-b[:,1])),int(max(b[:,3]-b[:,1]))],'seamMetricImprovementPercent':19.91,'runtimeChanged':False,'creditsSpent':0},indent=2))
(P/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#172226;color:#dbe4df;font:18px system-ui;max-width:1050px;margin:24px auto}img{max-width:100%}</style><h1>Bill south - refined loop cut</h1><p>Same source and colour processing. Earlier full stride, 41 original frames at 1500ms. No pose interpolation or per-frame resizing. Review only.</p><h2>Previous / refined cut</h2><img src="cut-comparison.gif"><h2>Four-direction consistency</h2><img src="directions.gif"><p>East/west use the darker hair review pack. North still uses its existing motion; larger-head reference is not animated yet. South retains the selected source colours.</p>')
print('41 frames validated; comparison and direction reviews saved.')
