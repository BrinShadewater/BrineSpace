from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;B=R/'character/krusher-tablet-west-v1'
font=lambda n:ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),n)
sheet=Image.new('RGB',(1600,1100),'#272b2e');d=ImageDraw.Draw(sheet)
d.text((24,15),'KRUSHER DOM / SYSTEM ADMINISTRATOR / WEST TABLET ACTION',font=font(32),fill='white');d.text((24,55),'Selected James utility suit / matte muted cyan / complete lift read stow /5.5 seconds',font=font(24),fill='#bdcdd0')
for row,root in enumerate([B,P]):
 for col,i in enumerate([0,38,77,153]):
  im=Image.open(root/f'frames/interact-west/{i:03}.png').convert('RGBA');tile=im.resize((368,368),Image.Resampling.NEAREST);sheet.paste(tile,(col*400,row*425+70),tile);d.text((col*400+18,row*425+425),('BARE' if row==0 else 'HELMET')+f' / FRAME {i}',font=font(23),fill='white');small=im.resize((92,92),Image.Resampling.LANCZOS);sheet.paste(small,(col*400+100+row*110,915),small)
d.text((24,1030),'Below:92px display / both variants join exact canonical idle / source motion and helmet shell retained',font=font(23),fill='#bdcdd0');d.text((24,1065),'Role-action candidate / native source/frame checks passed / no station or artistic acceptance claimed',font=font(23),fill='#bdcdd0');sheet.save(P/'review/key-poses-paired.png')
sheet=Image.new('RGB',(1440,1300),'#272b2e');d=ImageDraw.Draw(sheet)
for i in range(154):
 im=Image.open(P/f'frames/interact-west/{i:03}.png').convert('RGBA').crop((70,10,140,78)).resize((98,95),Image.Resampling.NEAREST);x=i%10*144;y=i//10*86;im=im.resize((86,84),Image.Resampling.NEAREST);sheet.paste(im,(x,y),im);d.text((x+99,y+65),str(i),font=font(15),fill='white')
sheet.save(P/'review/all-helmet-tablet-poses.png')
