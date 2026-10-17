from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
JOINT=ROOT/'character/bill-west-water-joint-continuity-v1'
board=Image.new('RGB',(1920,560),(31,35,40));draw=ImageDraw.Draw(board);rows=[]
for n,key in enumerate(['bare-ready','helmet-ready','bare-rise','helmet-rise']):
    job=json.loads((JOINT/f'generation-job-{key}-v1.json').read_text(encoding='utf-8'))
    old=Image.open(job['sourcePath']).convert('RGBA');new=Image.open(JOINT/f'{key}-candidate.png').convert('RGBA')
    rec={'key':key,'footPivotY':224,'alphaBootBottomExclusive':{}}
    for j,(label,im) in enumerate([('original',old),('candidate',new)]):
        a=np.asarray(im)[:,:,3];rec['alphaBootBottomExclusive'][label]={}
        for threshold in [32,127,224]:
            ys,xs=np.where(a[185:240,110:225]>threshold)
            rec['alphaBootBottomExclusive'][label][str(threshold)]=int(ys.max()+186) if len(ys) else None
        x=n*480+10;y=j*270+35
        crop=im.crop((110,185,225,240)).resize((460,220),Image.Resampling.NEAREST)
        board.paste(crop,(x,y),crop);draw.text((x,j*270+10),key+' '+label,fill='white')
        draw.line((x,y+39*4,x+460,y+39*4),fill=(70,185,195))
    rows.append(rec)
draw.text((10,540),'Fixed source boot windows x4. Cyan = pivot row224; alpha edge bands are raster diagnostics, not proof of anatomical floor contact.',fill='white')
board.save(OUT/'source-boot-contact-review.png')
(OUT/'source-contact-review.json').write_text(json.dumps({'poses':rows,'physicalVisualAcceptance':False},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'poses':len(rows),'physicalVisualAcceptance':False}))
