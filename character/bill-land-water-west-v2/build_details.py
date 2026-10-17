from pathlib import Path
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent
old=P.parent/'bill-land-water-west-v1'
items=[('idle',old/'sources/reference-idle-native.png',(134,76,190,154)),('old crouch',old/'sources/crouch-native-v1.png',(100,114,200,192)),('new crouch',P/'sources/crouch-native-v3.png',(100,111,200,189)),('old push',old/'sources/push-native-v1.png',(85,114,185,192)),('new push',P/'sources/push-native-v2.png',(95,114,195,192)),('compact lift',old/'sources/lift-native-v2.png',(85,149,185,227))]
board=Image.new('RGB',(2400,350),'#182932')
d=ImageDraw.Draw(board)
for i,(name,path,rect) in enumerate(items):
    im=Image.open(path).convert('RGBA').crop(rect)
    im=im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST)
    board.paste(im,(i*400,30),im)
    d.text((i*400+5,5),name+' / same4x native ruler',fill='white')
board.save(P/'head-shoulder-details.png')
