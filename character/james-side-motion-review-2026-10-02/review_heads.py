from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
rows=json.loads((P/'nine-head-package-evidence.json').read_bytes())['records']
master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(P/'east-idle-master-reference.png').convert('RGBA'),(36,52))
for page in range(3):
    board=Image.new('RGB',(768,840),'#303b40');d=ImageDraw.Draw(board)
    for j,row in enumerate(rows[page*3:page*3+3]):
        original=Image.open(R/row['source']).convert('RGBA');candidate=Image.open(P/row['candidate']).convert('RGBA')
        for col,im in enumerate([master,original,candidate]):
            at=(col*256,j*280+24);board.paste(im,at,im)
            d.text((at[0]+4,at[1]-20),['master','selected','candidate'][col]+' / '+row['key']+' '+str(row['index']),fill='white')
    board.save(P/('head-candidate-comparison-'+str(page)+'.png'))
print('Three nine-pose master/current/candidate comparison boards exported.')
preview=[]
for row in rows[:6]:
    board=Image.new('RGB',(768,280),'#303b40');d=ImageDraw.Draw(board)
    for col,im in enumerate([master,Image.open(R/row['source']).convert('RGBA'),Image.open(P/row['candidate']).convert('RGBA')]):
        at=(col*256,24);board.paste(im,at,im);d.text((col*256+4,4),['master','selected','staged head study'][col],fill='white')
    preview.append(board)
preview[0].save(P/'staged-east-carry-head-review.gif',save_all=True,append_images=preview[1:],duration=140,loop=0,optimize=False)
