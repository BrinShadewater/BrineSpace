from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,numpy as np
H=Path(__file__).resolve().parent;R=H.parents[1];P=R/'character/krusher-animation-package-v8';H.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());index=read(P/'package.json');font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),22)
fits=read(R/'character/krusher-james-motion-fit-v2/verification.json')['records']
current=Image.new('RGBA',(1536,512));original=Image.new('RGBA',(1536,512));comparison=Image.new('RGBA',(1536,1070),'#252d31');draw=ImageDraw.Draw(comparison);records=[]
for i,d in enumerate(['south','east','north','west']):
 q=index['states']['bare:idle-'+d];mp=P/q['manifest'];m=read(mp);s=next(s for s in m['states'] if s['id']=='idle-'+d);new=Image.open(mp.parent/s['frameFiles'][0]).convert('RGBA');source=next(q for q in fits if q['state']=='idle-'+d and q['frame']==0);old=Image.open(R/source['source']).convert('RGBA')
 # Fixed native crop: actual common 184px body; the two rows use identical sampling.
 box=(56,12,128,108);n=new.crop(box);o=old.crop(box)
 current.alpha_composite(n.resize((288,384),Image.Resampling.NEAREST),(i*384+48,48));original.alpha_composite(o.resize((288,384),Image.Resampling.NEAREST),(i*384+48,48))
 comparison.alpha_composite(n.resize((288,384),Image.Resampling.NEAREST),(i*384+48,60));comparison.alpha_composite(o.resize((288,384),Image.Resampling.NEAREST),(i*384+48,590));draw.text((i*384+30,20),'Current Krusher / '+d,font=font,fill='white');draw.text((i*384+30,550),'Original body style / '+d,font=font,fill='white')
 records.append({'direction':d,'current':str((mp.parent/s['frameFiles'][0]).relative_to(R)),'bodyStyleReference':source['source'],'nativeCrop':box,'reviewScale':4})
current.save(H/'current-standing-busts.png');original.save(H/'original-body-style-busts.png');comparison.save(H/'density-style-comparison.png')
(H/'diagnosis.json').write_text(json.dumps({'observations':['Current head uses binary cutout alpha and nearest export from explicitly pixel-art source sheets; body retains softer matte anti-aliased source.','Raster connectivity is not anatomical or shading continuity.','Broad gold hue mapping admits skin hues at restored collar pixels outside the inserted-head protection.'],'records':records},indent=2)+'\n')
print('Four paired native-density current/original body references saved.')
