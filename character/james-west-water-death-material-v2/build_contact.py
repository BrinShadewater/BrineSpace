from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
rows=[]
for folder in [P.parent/'james-west-water-death-polish-v1',P]:
 for mode in ['bare','helmet']:
  for i in range(6):
   a=np.array(Image.open(folder/f'frames/{mode}/{i:03d}.png').convert('RGBA'))[198:283,150:230];rgb=a[:,:,:3].astype(float);mask=(a[:,:,3]>192)&(np.ptp(rgb,axis=2)<30);px=rgb[mask]
   rows.append({'version':folder.name,'mode':mode,'index':i,'neutralPixels':len(px),'P90RGB':np.percentile(px,90,axis=0).tolist(),'meanAbove100Fraction':float((px.mean(axis=1)>100).mean())})
(P/'material-diagnostic.json').write_text(json.dumps({'rows':rows,'scope':'Same broad registered rear ROI as source motion review, original256x360 coordinates. Includes pose-dependent boots/hardware; not semantic material/physical lighting proof.'},indent=2)+'\n')
for version in ['james-west-water-death-polish-v1',P.name]:
 rs=[r for r in rows if r['version']==version and r['mode']=='bare'];print(version,'P90',np.mean([r['P90RGB'] for r in rs],axis=0).round(1).tolist(),'above100',round(np.mean([r['meanAbove100Fraction'] for r in rs]),3))
for tag in ['native-staged-behaviour','native-installed-behaviour']:
 fs=list((P/(tag+'-captures')).glob('*.png'))
 if not fs:continue
 board=Image.new('RGB',(1200,440),'#303b40');d=ImageDraw.Draw(board)
 for row,mode in enumerate(['bare','helmet']):
  for i,f in enumerate(sorted(p for p in fs if p.name.startswith(mode+'-water-west-'))):
   im=Image.open(f).convert('RGB');x,y=im.width//2,im.height//2;crop=im.crop((x-90,y-85,x+90,y+100));board.paste(crop,(i*200,row*220+25));d.text((i*200+3,row*220+3),f.stem,fill='white')
 board.save(P/(tag+'-contact.png'))
