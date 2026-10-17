"""Non-generative hardware highlight compression; preserve geometry and head."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent
S=P.parent/'bill-front-rear-proportions-v1'
checks=[]
for direction in ['north','south']:
 a=np.array(Image.open(S/f'{direction}-source.png').convert('RGB'));v=a.astype(float)
 key=(v[:,:,1]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,2]*1.3)&(v[:,:,1]>90)
 labels,_=ndimage.label(~key);counts=np.bincount(labels.ravel());counts[0]=0;mask=labels==counts.argmax()
 yy,xx=np.where(mask);top=yy.min();height=yy.max()-top+1
 y=np.indices(mask.shape)[0];body=mask&(y>=top+height*.18)
 # Feather neutral silver/grey selection. Saturated patches and cyan lights protected.
 neutral=np.clip((80-np.ptp(v,axis=2))/40,0,1)
 lum=v@np.array([.2126,.7152,.0722]);compressed=100+np.maximum(lum-100,0)*.52
 factor=np.minimum(1,compressed/np.maximum(lum,1))
 gain=1+(factor-1)*neutral*body
 result=np.rint(v*gain[:,:,None]).clip(0,255).astype('uint8')
 assert np.array_equal(result[~body],a[~body]);assert (result<=a).all()
 Image.fromarray(result).save(P/f'{direction}-source-matte.png')
 board=Image.new('RGB',(720,760),'#303b40');d=ImageDraw.Draw(board)
 for col,rgb8 in enumerate([a,result]):
  rgb=rgb8/255.;rgb=(rgb*.22+(np.minimum(rgb,.28)+np.maximum(rgb-.28,0)*.72)*.78)*.96
  im=Image.fromarray(np.dstack([np.rint(rgb*255).astype('uint8'),mask.astype('uint8')*255])).crop((xx.min(),top,xx.max()+1,yy.max()+1))
  base=Image.new('RGBA',(184,184));w=round(im.width*148/im.height);base.alpha_composite(im.resize((w,148),Image.Resampling.LANCZOS),((184-w)//2,24));base.save(P/f'{direction}-{col}.png')
  d.text((col*360+20,15),['Previous highlights','Softer matte fittings'][col],fill='white')
  for h,by in [(296,45),(82,425),(54,550),(27,650)]:
   sz=round(184*h/148);thumb=base.resize((sz,sz),Image.Resampling.BILINEAR);board.paste(thumb,(col*360+(360-sz)//2,by),thumb)
 board.save(P/f'{direction}-comparison.png')
 selected=body&(neutral>.9)&(lum>150)
 checks.append({'direction':direction,'headAndBackgroundUnchanged':True,'noPixelBrightened':True,'changedPixels':int(np.any(result!=a,axis=2).sum()),'highlightMedianBefore':float(np.median(lum[selected])),'highlightMedianAfter':float(np.median((result@np.array([.2126,.7152,.0722]))[selected]))})
(P/'checks.json').write_text(json.dumps(checks,indent=2))
(P/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#172226;color:#dbe4df;font:18px system-ui;max-width:900px;margin:24px auto;padding:0 16px}img{max-width:100%}</style><h1>Bill — softer matte details</h1><p>Approved proportions preserved. Bright neutral hardware highlights compressed without repainting. Head, hair and background unchanged. Same matte preview finish on both columns.</p><h2>North</h2><img src="north-comparison.png"><h2>South</h2><img src="south-comparison.png"><p>Reference candidates only; no animation or runtime replacement. No generation credits spent.</p>',encoding='utf-8')
print(json.dumps(checks))
