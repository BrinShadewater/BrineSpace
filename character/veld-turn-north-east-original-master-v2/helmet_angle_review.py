from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];H=R/'character/veld-helmet-original-turntable-v1/v3-study/shells'
board=Image.new('RGB',(6*280,2*355),'#202a30');d=ImageDraw.Draw(board)
for i in range(12):
    im=Image.open(H/f'{i:03}.png').convert('RGBA');big=im.resize((im.width*7,im.height*7),Image.Resampling.NEAREST);x=i%6*280;y=i//6*355;board.paste(big,(x+10,y+35),big);d.text((x+10,y+10),f'original whole shell{i} {im.size}',fill='white')
board.save(P/'original-shell-angle-review.png')
heads=Image.new('RGB',(6*280,320),'#202a30');d=ImageDraw.Draw(heads)
for i in range(6):
    im=Image.open(R/('character/veld-turn-north-east-original-master-v1/gather-frames/bare/000.png' if i==0 else f'character/veld-turn-north-east-original-master-v2/frames/bare/{i:03}.png')).convert('RGBA');big=im.crop((95,68,160,111)).resize((260,172),Image.Resampling.NEAREST);heads.paste(big,(i*280+10,40),big);d.text((i*280+10,10),f'actual body/head{i}',fill='white')
heads.save(P/'actual-head-angle-review.png')
print('Twelve original whole-shell views and six actual head poses prepared')
