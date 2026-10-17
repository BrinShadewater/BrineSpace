from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
board=Image.new('RGB',(1024,1024),'#303b40');draw=ImageDraw.Draw(board);records=[]
for row,mode in enumerate(['bare','helmet']):
    for col,index in enumerate([4,5]):
        source=r/('character/james-cargo-material-joined-v1/frames/'+mode+'/unload-west/%03d.png'%index)
        sprite=Image.open(source).convert('RGBA');assert sprite.size==(256,256)
        sprite=sprite.resize((512,512),Image.Resampling.NEAREST)
        board.paste(sprite,(col*512,row*512),sprite)
        draw.text((col*512+6,row*512+6),mode+' / original unload-west %03d'%index,fill='white')
        records.append({'source':str(source.relative_to(r)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'index':index,'gear':mode})
board.save(p/'rise-reference.png')
(p/'rise-reference-evidence.json').write_text(json.dumps({'scope':'Exact original unload4 and5 shown2x nearest-neighbor in paired endpoint presentation. No source mutation; shared canvas256/p128224/H148.','sources':records},indent=2)+'\n')
print('Four original paired crouch/standing endpoints registered;source hashes retained.')
