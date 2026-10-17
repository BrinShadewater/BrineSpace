from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;R=P.parents[1];records=json.loads((P/'turn-head-v3-package-evidence.json').read_bytes())['records']
anchor=Image.open(P/'east-family-v2/carry-east-000.png').convert('RGBA')
for page in range(2):
    board=Image.new('RGB',(1024,840),'#303b40');draw=ImageDraw.Draw(board)
    for row,record in enumerate(records[page*3:page*3+3]):
        images=[anchor,Image.open(R/record['source'][6:]).convert('RGBA'),Image.open(P/record['candidate']).convert('RGBA')]
        for col,im in enumerate(images):
            board.paste(im,(col*256,row*280+24),im);draw.text((col*256+4,row*280+4),['revised East carry','original turn','candidate turn'][col]+' / '+str(record['index']),fill='white')
        close=images[2].crop((118,64,174,116)).resize((224,208),Image.Resampling.NEAREST);board.paste(close,(768,row*280+48),close);draw.text((772,row*280+4),record['state'],fill='white')
    board.save(P/('turn-head-v3-comparison-'+str(page)+'.png'))
