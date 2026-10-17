from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;O=P.parents[1]/'output/veld-bunk-death-east-v1'
for group in range(2):
    board=Image.new('RGB',(1440,1080),'#202a30');draw=ImageDraw.Draw(board)
    for row,rotation in enumerate(range(group*2,group*2+2)):
        for g,gear in enumerate(['bare','helmet']):
            y=(row*2+g)*270
            name=f'rotation{rotation}-{gear}'
            for col,(suffix,label) in enumerate([('live','Live sleeping'),('pose1','Relaxation'),('pose2','Still'),('pose2-terminal-restored','Restored corpse')]):
                im=Image.open(O/f'{name}-{suffix}-room.png').convert('RGB').crop((275,305,635,535))
                board.paste(im,(col*360,y+35));draw.text((col*360+8,y+10),f'R{rotation} {gear}: {label}',fill='white')
    board.save(P/f'native-contact-{group+1}.png')
print('Two boards: all8cases,32unmodified native room crops')
