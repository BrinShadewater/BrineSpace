"""Rebuild native review summaries from captured gameplay frames, no artwork edits."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
shots=ROOT/'native'
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',20)
board=Image.new('RGB',(1400,1080),'#101e26'); d=ImageDraw.Draw(board)
d.text((24,15),'BRINESPACE / INSTALLED SEA LIFE / NATIVE GAME REVIEW',font=font,fill='#dce8e8')
for n,subject in enumerate(['lantern','glass','veil','ribbon','tidewalker']):
    file=shots/(subject+'-after.png')
    im=Image.open(file).convert('RGB').crop((6,110,1135,585))
    im=ImageOps.contain(im,(660,260),Image.Resampling.LANCZOS)
    x=25+(n%2)*700; y=65+(n//2)*335
    board.paste(im,(x,y));d.text((x,y+268),subject,font=font,fill='#dce8e8')
overview=shots/'tidewalker-art-overview.png'
if overview.exists():
    im=Image.open(overview).convert('RGB').crop((200,150,1400,750))
    board.paste(ImageOps.contain(im,(660,260),Image.Resampling.LANCZOS),(725,735))
    d.text((725,1003),'Full assembly / native sprite renderer',font=font,fill='#dce8e8')
board.save(ROOT/'native-review.jpg',quality=95)
for subject in ['lantern','ribbon','tidewalker']:
    frames=[]
    for i in range(8):
        frames.append(Image.open(shots/(subject+'-motion-%02d.png'%i)).convert('RGB').crop((6,110,1135,585)).resize((790,332),Image.Resampling.LANCZOS))
    frames[0].save(ROOT/(subject+'-native.gif'),save_all=True,append_images=frames[1:],duration=167,loop=0)
assembly=[Image.open(shots/('tidewalker-assembly-%02d.png'%i)).convert('RGB').crop((200,150,1400,750)).resize((900,450),Image.Resampling.LANCZOS) for i in range(8)]
assembly[0].save(ROOT/'tidewalker-assembly-native.gif',save_all=True,append_images=assembly[1:],duration=167,loop=0)
print('Native contact sheet and three motion reviews rebuilt.')
