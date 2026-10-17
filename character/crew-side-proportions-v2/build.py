"""Reference-only comparison; deterministic key, registration and matte curve."""
from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

P=Path(__file__).resolve().parent
R=P.parent
sources={
 'bill': ['bill-video-east-v1/master-input.png','crew-side-proportions-v2/bill-east-source.png','bill-front-proportion-v4/master-input.png'],
 'branforth':['branforth-video-east-v2/master-input.png','crew-side-proportions-v2/branforth-east-source.png','branforth-video-south-v1/master-input.png']}
checks=[]
for who,paths in sources.items():
    board=Image.new('RGB',(900,760),'#303b40'); d=ImageDraw.Draw(board)
    for col,path in enumerate(paths):
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
        d.text((x+20,15),['Existing side','Revised side - candidate','Front proportion reference'][col],fill='white')
        for height,y in [(296,50),(82,425),(54,550),(27,650)]:
            display=base.resize((round(184*height/148),)*2,Image.Resampling.BILINEAR)
            board.paste(display,(x+(300-display.width)//2,y),display)
        checks.append(dict(character=who,source=path,sourceBounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],normalizedHeight=148,clipped=bool(w>=184)))
    board.save(P/f'{who}-comparison.png')
assert not any(c['clipped'] for c in checks)
(P/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
html='''<!doctype html><meta name="viewport" content="width=device-width, initial-scale=1"><title>Crew side proportions</title><style>body{background:#172226;color:#dbe4df;font:17px system-ui;margin:24px auto;max-width:960px;padding:0 15px}img{display:block;max-width:100%;margin:16px 0 36px}p{line-height:1.6}h1{font-size:28px}</style><h1>Side head proportions · reference candidates</h1><p>Existing side / revised side / front reference. Top row enlarged; lower rows approximate 82, 54 and 27px character heights at full image size. All references share the matte colour curve and smooth sampling. No animation replacements installed.</p><h2>Major Alexander Bill</h2><img src="bill-comparison.png"><h2>Lt. James Branforth</h2><img src="branforth-comparison.png"><p>These are regenerated reference candidates: detail can change beyond the head. Motion, gait and Bill’s south-facing style still need separate work. No Higgsfield credits spent.</p>'''
(P/'index.html').write_text(html,encoding='utf-8')
print('Built 6 registered reference exports and 2 comparison boards; no clipping.')

