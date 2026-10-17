from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;B=R/'character/krusher-veld-cyan-test-v2'
font=lambda n:ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),n)
s=Image.new('RGB',(1600,1100),'#272b2e');d=ImageDraw.Draw(s)
d.text((24,15),'KRUSHER DOM / SYSTEM ADMINISTRATOR',font=font(34),fill='white')
d.text((24,54),'Veld body trial / AI & Robotics / matte muted cyan / bare and helmet',font=font(24),fill='#bdcdd0')
for row,root in enumerate([B,P]):
 for col,direction in enumerate(['south','east','north','west']):
  x=col*390+20;y=row*425+65;image=Image.open(root/f'frames/idle-{direction}/000.png').convert('RGBA')
  tile=image.resize((368,368),Image.Resampling.NEAREST);s.paste(tile,(x,y),tile)
  d.text((x+18,y+354),direction.upper()+' / '+('BARE' if row==0 else 'HELMET'),font=font(23),fill='white')
  small=image.resize((92,92),Image.Resampling.LANCZOS)
  s.paste(small,(col*390+105+row*110,915),small)
d.text((24,1030),'Below: 92px display references / source canvas184x184 / foot pivot(92,172) / standing ruler148px',font=font(24),fill='#bdcdd0')
d.text((24,1065),'Independent cardinal heads and original family gear shell / unselected fitting candidate',font=font(23),fill='#bdcdd0')
s.save(P/'review/cardinal-comparison.png')
records=json.loads((P/'verification.json').read_text())['records']
s=Image.new('RGB',(1200,640),'#272b2e');d=ImageDraw.Draw(s)
for col,direction in enumerate(['south','east','west']):
 record=next(t for t in records if t['state']=='idle-'+direction and t['frame']==0)
 d.text((col*400+15,8),direction+' source above / candidate below',font=font(23),fill='white')
 for row,path in enumerate([R/record['source'],P/record['output']]):
  image=Image.open(path).convert('RGBA').crop((70,17,118,55)).resize((384,304),Image.Resampling.NEAREST)
  s.paste(image,(col*400,row*310+30),image)
s.save(P/'review/profile-face-comparison.png')
