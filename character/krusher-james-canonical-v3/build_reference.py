from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
font=lambda n:ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),n)
b=Image.new('RGB',(1600,1450),'#272b2e');d=ImageDraw.Draw(b)
d.text((24,15),'KRUSHER DOM / SYSTEM ADMINISTRATOR',font=font(36),fill='white')
d.text((24,62),'AI & Robotics / matte muted cyan #527C80 / selected James utility suit',font=font(25),fill='#bdcdd0')
for row,(gear,action) in enumerate([('bare',False),('helmet',False),('bare',True),('helmet',True)]):
 m=json.loads((P/(gear+'-manifest.json')).read_text())
 for col,direction in enumerate(['south','east','north','west']):
  s=next(s for s in m['states'] if s['id']==('interact-' if action else 'idle-')+direction)
  elapsed=0;i=0
  if action:
   for i,hold in enumerate(s['frameDurationsMs']):
    elapsed+=hold
    if elapsed>2750:break
  im=Image.open(P/s['frameFiles'][i]).convert('RGBA');tile=im.resize((276,276),Image.Resampling.NEAREST);x=col*400+30;y=row*320+125;b.paste(tile,(x,y),tile)
  d.text((x,y+270),gear.upper()+' / '+s['id'],font=font(22),fill='white');small=im.resize((92,92),Image.Resampling.LANCZOS);b.paste(small,(x+285,y+115),small)
d.text((24,1410),'184px source canvas / foot (92,172) / standing ruler148 / 92px gameplay-scale samples',font=font(23),fill='#bdcdd0');(P/'review').mkdir(exist_ok=True);b.save(P/'review/character-sheet.png')
print('Saved four-direction paired idle/action reference sheet.')
