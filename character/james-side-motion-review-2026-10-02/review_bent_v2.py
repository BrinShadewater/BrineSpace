from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
rows=json.loads((P/'bent-v2-package-evidence.json').read_bytes())['records']
master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(P/'east-idle-master-reference.png').convert('RGBA'),(36,52))
board=Image.new('RGB',(1024,840),'#303b40');d=ImageDraw.Draw(board)
for j,row in enumerate(rows):
    old=P/'head-candidates'/Path(row['candidate']).name
    images=[master,Image.open(R/row['source']).convert('RGBA'),Image.open(old).convert('RGBA'),Image.open(P/row['candidate']).convert('RGBA')]
    for col,im in enumerate(images):
        at=(col*256,j*280+24);board.paste(im,at,im)
        d.text((col*256+4,j*280+4),['master','selected','head study v1','bent revision v2'][col]+' / '+str(row['index']),fill='white')
board.save(P/'bent-v2-comparison.png')
print('Three bent source poses compared with master and prior study.')
