from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;P=R/'character/krusher-animation-package-v3'
read=lambda p:json.loads(p.read_text())
rows=read(H/'shoulder-palette-proposals.json');groups=read(H/'shoulder-palette-review-groups.json');selected=read(H/'shoulder-palette-selection.json')['selectedGroups'];mapping={q['source']:q['output'] for q in read(P/'palette-revision.json')['records']}
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),20)
for start in range(0,len(selected),48):
 out=Image.new('RGBA',(1600,1200),'#252b2e');draw=ImageDraw.Draw(out)
 for j,gid in enumerate(selected[start:start+48]):
  q=rows[groups[gid]['representative']];im=Image.open(P/mapping[q['file']]).convert('RGBA');x0,y0,x1,y1=q['box'];crop=im.crop((x0-10,y0-10,x1+10,y1+18));crop=crop.resize((crop.width*3,crop.height*3),Image.Resampling.NEAREST);x=j%8*200+8;y=j//8*200+28;out.alpha_composite(crop,(x,y));draw.text((x,y-25),'G'+str(gid),font=font,fill='white')
 out.save(H/('shoulder-after-%02d.png'%(start//48)))
index=read(P/'package.json');keys=['carry-turn-north-west','carry-turn-south-west','read-seated-west'];out=Image.new('RGBA',(900,850),'#252b2e');draw=ImageDraw.Draw(out);font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24)
draw.text((18,10),'KRUSHER DOM / MUTED CYAN SHOULDER PASS',font=font,fill='white')
for row,gear in enumerate(['bare','helmet']):
 for col,key in enumerate(keys):
  q=index['states'][gear+':'+key];mp=P/q['manifest'];s=next(s for s in read(mp)['states'] if s['id']==key);im=Image.open(mp.parent/s['frameFiles'][len(s['frameFiles'])//2]).convert('RGBA');im=im.crop(im.getbbox());im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);x=col*300+(300-im.width)//2;y=row*390+90;out.alpha_composite(im,(x,y));draw.text((col*300+20,y-30),gear+' / '+key.replace('carry-turn-',''),font=font,fill='white')
out.save(H/'shoulder-palette-mobile.png');print('Refreshed12final shoulder review boards and mobile six-pose sheet.')
