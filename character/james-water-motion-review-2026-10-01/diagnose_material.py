from pathlib import Path
import json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;rows=[]
for mode in ['body','equipment']:
 for key in ['swim-west','death-water-west']:
  for i in range(6):
   # Shared registered rear-body region; broad diagnostic, not semantic material mask.
   a=np.array(Image.open(P/f'{mode}-{key}-{i:03d}.png').convert('RGBA'))[80:165,150:230]
   rgb=a[:,:,:3].astype(float);opaque=a[:,:,3]>192;neutral=opaque&(np.ptp(rgb,2)<30);px=rgb[neutral]
   rows.append({'mode':mode,'key':key,'index':i,'roi':[150,80,230,165],'opaquePixels':int(opaque.sum()),'neutralPixels':len(px),'neutralMedianRGB':np.median(px,axis=0).tolist(),'neutralP90RGB':np.percentile(px,90,axis=0).tolist(),'neutralMeanAbove100Fraction':float((px.mean(axis=1)>100).mean()),'neutralMeanAbove130Fraction':float((px.mean(axis=1)>130).mean())})
(P/'material-diagnostic.json').write_text(json.dumps({'rows':rows,'scope':'Fixed registered rear-body ROI with alpha>192 and RGB spread<30. Broad colour/intensity diagnostic can include boots, hardware and pose-dependent coverage; not semantic matte certification or physical lighting measurement.'},indent=2)+'\n')
for mode in ['body','equipment']:
 for key in ['swim-west','death-water-west']:
  rs=[r for r in rows if r['mode']==mode and r['key']==key];print(mode,key,'P90',np.mean([r['neutralP90RGB'] for r in rs],axis=0).round(1).tolist(),'above100',round(np.mean([r['neutralMeanAbove100Fraction'] for r in rs]),3))
