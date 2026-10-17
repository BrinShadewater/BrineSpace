"""Reference-only comparison; deterministic key, registration and matte curve."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

P=Path(__file__).resolve().parent
R=P.parent
sources={'south':['bill-front-rear-matte-v2/south-source-matte.png','bill-face-readability-v1/south-source.png','bill-front-rear-matte-v2/south-source-matte.png']}
checks=[]
for who,paths in sources.items():
    board=Image.new('RGB',(600,760),'#303b40'); d=ImageDraw.Draw(board)
    for col,path in enumerate(paths[:2]):
        a=np.array(Image.open(R/path).convert('RGB')); v=a.astype(float)
        key=(v[:,:,1]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,2]*1.3)&(v[:,:,1]>90)
        labels,_=ndimage.label(~key); counts=np.bincount(labels.ravel()); counts[0]=0
        mask=labels==counts.argmax(); ys,xs=np.where(mask)
        # Same approved shader RGB curve, evaluated deterministically in byte space.
        rgb=v/255.; rgb=(rgb*.22+(np.minimum(rgb,.28)+np.maximum(rgb-.28,0)*.72)*.78)*.96
        rgba=np.dstack([np.rint(rgb*255).clip(0,255).astype('uint8'),mask.astype('uint8')*255])
        crop=Image.fromarray(rgba).crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
        base=Image.new('RGBA',(184,184)); w=round(crop.width*148/crop.height)
        small=crop.resize((w,148),Image.Resampling.LANCZOS);base.alpha_composite(small,((184-w)//2,24))
        base.save(P/f'{who}-{col}.png')
        x=col*300
        d.text((x+20,15),['Current face','Subtle face contrast'][col],fill='white')
        for height,y in [(296,50),(82,425),(54,550),(27,650)]:
            display=base.resize((round(184*height/148),)*2,Image.Resampling.BILINEAR)
            board.paste(display,(x+(300-display.width)//2,y),display)
        checks.append(dict(character=who,source=path,sourceBounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],normalizedHeight=148,clipped=bool(w>=184)))
    board.save(P/f'{who}-comparison.png')
assert not any(c['clipped'] for c in checks)
(P/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
html='<meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#172226;color:#dbe4df;font:18px system-ui;max-width:850px;margin:25px auto}img{max-width:100%}</style><h1>Bill face readability</h1><p>Current face / subtle face contrast. Suit, hair, proportions and background are unchanged. Same matte finish and smooth sampling in both columns.</p><img src="south-comparison.png"><p>Enlarged view and approximate 82, 54 and 27px heights. Reference-only candidate; no new animation or credits spent.</p>'
(P/'index.html').write_text(html,encoding='utf-8')
