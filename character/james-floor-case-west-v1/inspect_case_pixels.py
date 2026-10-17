from pathlib import Path
import json
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
board=Image.new('RGB',(900,350),'#303b40');d=ImageDraw.Draw(board)
for n,i in enumerate([4,5]):
    path=r/f'character/james-cargo-material-joined-v1/frames/bare/unload-west/{i:03d}.png'
    image=Image.open(path).convert('RGBA');roi=image.crop((70,190,170,230)).resize((800,320),Image.Resampling.NEAREST)
    small=roi.resize((400,160),Image.Resampling.NEAREST);board.paste(small,(n*450,30),small)
    d.text((n*450+5,5),f'Original {i}: x70..170/y190..230, 4x',fill='white')
    for rect,color in [((74,195,120,223),'red'),((74,196,119,223),'yellow')]:
        box=((rect[0]-70)*4+n*450,(rect[1]-190)*4+30,(rect[2]-70)*4+n*450,(rect[3]-190)*4+30);d.rectangle(box,outline=color)
board.save(p/'original-case-pixel-review.png')
print('Original case/boot boundaries enlarged without modifying source files.')
