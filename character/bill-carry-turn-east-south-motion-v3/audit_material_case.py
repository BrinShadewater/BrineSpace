from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
Y,X=np.indices((256,256))
def skin(a):
 rgb=a[:,:,:3].astype(float)
 return (a[:,:,3]>180)&(Y<110)&(X>100)&(X<160)&(rgb[:,:,0]>rgb[:,:,1]+12)&(rgb[:,:,0]>rgb[:,:,2]+15)&(rgb.mean(2)>70)
rows=[];board=Image.new('RGB',(1536,768),(34,52,62));draw=ImageDraw.Draw(board)
for i in range(6):
 im=Image.open(P/f'frames/bare/carry-turn-east-south/{i:03}.png').convert('RGBA');a=np.array(im);mask=skin(a)
 rows.append({'phase':i,'skinPixels':int(mask.sum()),'skinMedianRGB':np.median(a[:,:,:3][mask],axis=0).tolist(),'skinMeanRGB':np.mean(a[:,:,:3][mask],axis=0).tolist()})
 for row,box in enumerate([(100,68,160,112),(93,121,172,172)]):
  crop=im.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3),Image.Resampling.NEAREST);board.paste(crop,(i*256+8,row*300+45),crop)
 draw.text((i*256+8,12),'phase'+str(i)+(' master' if i in [0,5] else ' candidate'),fill='white')
 draw.text((i*256+8,260),'skin median '+str(rows[-1]['skinMedianRGB']),fill='white')
target=np.median(np.concatenate([np.array(Image.open(P/f'frames/bare/carry-turn-east-south/{i:03}.png'))[:,:,:3][skin(np.array(Image.open(P/f'frames/bare/carry-turn-east-south/{i:03}.png')))] for i in [0,5]]),axis=0)
source=np.median(np.concatenate([np.array(Image.open(P/f'frames/bare/carry-turn-east-south/{i:03}.png'))[:,:,:3][skin(np.array(Image.open(P/f'frames/bare/carry-turn-east-south/{i:03}.png')))] for i in [1,2,3,4]]),axis=0)
report={'scope':'Opaque warm skin material statistics and native3xface/case crops; no proof of anatomy or material acceptance','skinRows':rows,'pooledEndpointSkinMedian':target.tolist(),'pooledInteriorSkinMedian':source.tolist(),'suggestedSharedSkinCorrection':(target/source).tolist(),'caseScope':'Visual crop only; aggregate arm/case silhouette is not object size measurement.'}
(P/'material-case-audit.json').write_text(json.dumps(report,indent=2)+'\n');board.save(P/'material-case-review.png');print(json.dumps(report))
