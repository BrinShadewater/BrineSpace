from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;R=P.parent.parent
font=lambda n:ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),n)
s=Image.new('RGB',(1600,1100),'#272b2e');d=ImageDraw.Draw(s)
d.text((24,15),'KRUSHER DOM / SYSTEM ADMINISTRATOR',font=font(34),fill='white')
d.text((24,54),'Selected James utility suit / AI & Robotics / matte muted cyan / bare and helmet',font=font(24),fill='#bdcdd0')
for row,gear in enumerate(['bare','helmet']):
 for col,direction in enumerate(['south','east','north','west']):
  x=col*390+20;y=row*425+65;im=Image.open(P/f'frames/{gear}/idle-{direction}/000.png').convert('RGBA');tile=im.resize((368,368),Image.Resampling.NEAREST);s.paste(tile,(x,y),tile);d.text((x+18,y+354),direction.upper()+' / '+gear.upper(),font=font(23),fill='white');small=im.resize((92,92),Image.Resampling.LANCZOS);s.paste(small,(col*390+105+row*110,915),small)
d.text((24,1030),'Below:92px display / source canvas184x184 / foot pivot92,172 / standing ruler148px',font=font(24),fill='#bdcdd0')
d.text((24,1065),'Base chosen October3,2026 / original family gait retained / role actions in development',font=font(23),fill='#bdcdd0');s.save(P/'review/character-sheet.png')
