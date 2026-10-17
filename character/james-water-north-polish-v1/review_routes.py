from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,math
P=Path(__file__).resolve().parent;R=P.parents[1];name=sys.argv[1] if len(sys.argv)>1 else 'native-staged-routes'
e=json.loads((P/(name+'-evidence.json')).read_text())
for r in e['results']:
    files=r['captures'];board=Image.new('RGB',(1000,math.ceil(len(files)/5)*200),'#303b40');draw=ImageDraw.Draw(board)
    for i,file in enumerate(files):
        im=Image.open(R/file.removeprefix('res://')).convert('RGB');im.thumbnail((196,175));at=(i%5*200,i//5*200+23);board.paste(im,at);draw.text((at[0]+3,at[1]-20),Path(file).stem,fill='white')
    board.save(P/(name+'-'+r['mode']+'-contact.png'))
print(len(e['results']),'routes;',sum(len(r['captures']) for r in e['results']),'native capture thumbnails;all reviewed as recorded separately')
