from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
for mode in ['bare','helmet']:
    board=Image.new('RGB',(1560,2160),'#303b40');d=ImageDraw.Draw(board)
    for row,direction in enumerate(['east','south','west','north']):
        files=sorted((P/'arrival-captures').glob(mode+'-dry-'+direction+'-*.png'))
        assert len(files)==3,(mode,direction,len(files))
        for col,path in enumerate(files):
            im=Image.open(path).convert('RGB');assert im.width<=520 and im.height<=507,im.size
            x=col*520;y=row*540+28;board.paste(im,(x,y));d.text((x+4,y-22),path.stem,fill='white')
    board.save(P/(mode+'-route-review.png'))
print('24 actual room captures packaged without image scaling.')
