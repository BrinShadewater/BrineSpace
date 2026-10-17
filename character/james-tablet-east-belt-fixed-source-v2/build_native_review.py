from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;e=json.loads((P/'native-arrival-continue-evidence.json').read_text());board=Image.new('RGB',(3*340,len(e['results'])*240),'#303b40');d=ImageDraw.Draw(board)
for row,r in enumerate(e['results']):
    for col,path in enumerate(r['captures']):
        im=Image.open(P.parents[1]/path.removeprefix('res://')).convert('RGB');x=col*340;y=row*240
        w,h=im.size;crop=im.crop((w//2-90,h//2-145,w//2+90,h//2+15))
        board.paste(crop,(x,y+30));scene=im.copy();scene.thumbnail((150,190));board.paste(scene,(x+185,y+30));d.text((x+5,y+5),Path(path).stem,fill='white')
board.save(P/'native-arrival-continue-review.png');print('24 original native scene views with fixed center details; no pose interpolation.')
