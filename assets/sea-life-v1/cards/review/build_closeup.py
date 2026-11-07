"""Enlarge the source frame and the actual native-rendered card for inspection."""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageFont
r=Path(__file__).resolve().parent
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',28)
small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',21)
board=Image.new('RGB',(1460,1100),'#16242c');d=ImageDraw.Draw(board)
d.text((28,20),'CARD FRAME / outer metal + inset colour',font=font,fill='#dce8e8')
frame=Image.open(r.parent/'card-frame.png').convert('RGBA').resize((600,852),Image.Resampling.NEAREST)
d.rounded_rectangle((28,90,627,941),radius=36,fill='#101a20')
board.paste(frame,(28,90),frame)
d.text((28,970),'Neutral frame source / 3x',font=small,fill='#c5dcdd')
d.text((28,1005),'Painted trim; transparent centre; 16px slice corners',font=small,fill='#c5dcdd')
metrics=json.loads((r/'native/metrics-after.json').read_text())['1600']
im=Image.open(r/'native/cards-after-1600.png').convert('RGB')
card=metrics['cards'][0];factor=1600/1920
x,y=card['screen_origin'];w,h=card['logical_size']
box=(math.floor(x*factor),math.floor(y*factor),math.ceil((x+w)*factor),math.ceil((y+h)*factor))
crop=im.crop(box);crop=crop.resize((crop.width*3,crop.height*3),Image.Resampling.NEAREST)
board.paste(crop,(755,135))
d.text((755,90),'Updated Engineering card / 3x',font=font,fill='#dce8e8')
d.text((755,890),'Neutral outer metal; department outline inside.',font=small,fill='#c5dcdd')
d.text((755,925),'Original inner stock, size and text layout retained.',font=small,fill='#c5dcdd')
board.save(r/'frame-closeup.png')
print('Frame close-up rebuilt from native capture')
