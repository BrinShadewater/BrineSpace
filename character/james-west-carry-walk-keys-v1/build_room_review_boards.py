from pathlib import Path
from PIL import Image,ImageDraw
import sys,json
p=Path(__file__).resolve().parent/sys.argv[1];d=json.loads((p/'native-evidence.json').read_bytes())
for row in d['results']:
    files=[Path(f.removeprefix('res://')) for f in row['captures']];images=[Image.open(f).convert('RGB') for f in files];w=max(im.width for im in images);h=max(im.height for im in images);board=Image.new('RGB',(w*3,(h+24)*2),(48,59,63));draw=ImageDraw.Draw(board)
    for i,(f,im) in enumerate(zip(files,images)):
        x=i%3*w;y=i//3*(h+24);board.paste(im,(x,y+24));draw.text((x+4,y+5),f.stem,fill='white')
    board.save(p/(('helmet' if row['gear'] else 'bare')+'-room-review.png'))
print(str(len(d['results']))+' paired journey review boards built from all room captures.')
