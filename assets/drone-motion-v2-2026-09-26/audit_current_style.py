from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
R=Path('assets/drone-motion-v2-2026-09-26'); m=json.loads((R/'manifest.json').read_text()); lock=json.loads(Path('docs/BRINESPACE_ART_REFERENCE_LOCK_2026-09-26.json').read_text()); f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
names=['north','northeast','east','southeast','south','southwest','west','northwest']; report={'worldUnitsPerPixel':m['worldUnitsPerPixel'],'pixelsPerWorldUnit':1/m['worldUnitsPerPixel'],'poses':{},'referenceHashes':{}}
refs=[]
for key in ['sp-engineering-extra3-3','sp-science-extra11-2']:
 e=next(a for a in lock['assets'] if a['id']==key); p=Path(lock['local_root'])/e['native']['path']; ok=hashlib.sha256(p.read_bytes()).hexdigest()==e['native']['sha256']; assert ok; report['referenceHashes'][key]=ok; refs.append((key,Image.open(p).convert('RGBA')))
for theme,bg,fg in [('dark','#192930','#d9e5e9'),('light','#d7dde0','#20323a')]:
 b=Image.new('RGB',(1120,1120),bg); d=ImageDraw.Draw(b); d.text((15,10),'CURRENT DRONE / unscaled 256px exports; lower inset at 0.34 display scale',font=f,fill=fg)
 for i,h in enumerate(names):
  im=Image.open(R/m['headings'][h]['pose']).convert('RGBA'); x=(i%4)*280;y=40+(i//4)*340;d.text((x+12,y),h,font=f,fill=fg);b.paste(im,(x+12,y+20),im);sm=im.resize((87,87),Image.Resampling.LANCZOS);b.paste(sm,(x+96,y+254),sm)
  box=im.getchannel('A').point(lambda a:255 if a>64 else 0).getbbox();report['poses'][h]={'canvas':im.size,'silhouetteBounds':box,'silhouetteWidthPx':box[2]-box[0]}
 d.text((15,735),'Locked machinery at native library pixels / material reference, not equal physical size',font=f,fill=fg)
 for i,(key,im) in enumerate(refs):
  x=15+i*390;d.text((x,767),key,font=f,fill=fg);b.paste(im,(x,795),im)
 a=Image.open('assets/drone-npc-pilot-2026-09-26/sources/construction-approved-v10.png').convert('RGBA');a=a.crop(a.getbbox());a=a.resize((203,round(a.height*203/a.width)),Image.Resampling.LANCZOS);d.text((805,767),'Accepted v10 / 203px wide',font=f,fill=fg);b.paste(a,(825,795),a)
 b.save(R/f'review/current-style-audit-{theme}.png')
(R/'review/current-style-metrics.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
