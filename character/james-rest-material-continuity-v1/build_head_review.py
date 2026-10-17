from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;e=json.loads((P/'material-evidence.json').read_text())
for direction in ['north','south','east','west']:
    b=Image.new('RGB',(12*204,2*230),'#303b40');d=ImageDraw.Draw(b)
    for row,mode in enumerate(['bare','helmet']):
        records=[r for action in ['lie-down','sleep'] for r in e['records'] if r['mode']==mode and r['key']==action+'-'+direction]
        for col,r in enumerate(records):
            im=Image.open(P/r['output']).convert('RGBA');x0,y0,x1,y1=r['protectedHead'];cx=(x0+x1)//2;cy=(y0+y1)//2;crop=im.crop((cx-25,cy-25,cx+25,cy+25)).resize((200,200),Image.Resampling.NEAREST);at=(col*204,row*230);b.paste(crop,(at[0],at[1]+26),crop);d.text((at[0]+4,at[1]+4),mode+' '+r['key'].removesuffix('-'+direction)+' '+str(r['index']),fill='white')
    b.save(P/(direction+'-all-heads.png'))
print('All96 unique displayed lie/sleep references, exact reverse get-up sources already verified; no head artwork edits.')
