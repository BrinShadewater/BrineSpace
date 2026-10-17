from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
inputs=json.loads((p/'inputs.json').read_bytes());assert all(hashlib.sha256((r/f).read_bytes()).hexdigest()==v for f,v in inputs['preLaunchSha256'].items())
validation=json.loads((p/'edge-study-validation.json').read_bytes());assert validation['exitCode']==0 and validation['realProfileUnchanged']
evidence=json.loads((p/'native-evidence.json').read_bytes());assert evidence['failures']==0 and len(evidence['records'])==18
contract=json.loads((p/'source-contract.json').read_bytes());records=[]
for row in evidence['records']:
 a=np.array(Image.open(r/row['source'][6:]).convert('RGBA'));b=np.array(Image.open(r/row['candidate'][6:]).convert('RGBA'));rgb=a[:,:,:3].astype(int);red,green,blue=rgb.transpose(2,0,1);alpha=a[:,:,3];solid=alpha>0;inside=solid.copy()
 for dy in [-1,0,1]:
  for dx in [-1,0,1]:
   if dy==dx==0:continue
   shifted=np.zeros_like(solid);y0=max(0,dy);y1=min(184,184+dy);x0=max(0,dx);x1=min(184,184+dx);shifted[y0:y1,x0:x1]=solid[y0-dy:y1-dy,x0-dx:x1-dx];inside &= shifted
 mask=solid&(10*green>13*red)&(10*green>13*blue)&(green>20)&((alpha<128)|~inside)
 assert int(mask.sum())==row['selectedPixels']
 assert np.array_equal(a[:,:,0],b[:,:,0]) and np.array_equal(a[:,:,2:],b[:,:,2:]) and np.array_equal(a[~mask],b[~mask])
 assert (b[:,:,1][mask]<=a[:,:,1][mask]).all()
 records.append(dict(**row,alphaRedBlueExact=True,outsideEdgeAdmissionExact=True))
for direction in ['south','north','west']:
 for mode in ['bare','helmet']:
  rows=[x for x in evidence['records'] if x['direction']==direction and x['mode']==mode]
  board=Image.new('RGBA',(1104,1176),(48,59,63,255));draw=ImageDraw.Draw(board)
  for j,row in enumerate(rows):
   item=next(x for x in contract['records'] if x['direction']==direction and x['mode']==mode and x['slot']==row['slot'])
   for col,(file,label) in enumerate([(item['master'],'idle master'),(row['source'],'selected '+str(row['slot'])),(row['candidate'],'edge study '+str(row['slot']))]):
    im=Image.open(r/file[6:]).convert('RGBA');board.alpha_composite(im.resize((368,368),Image.Resampling.NEAREST),(col*368,j*392+24));draw.text((col*368+4,j*392+5),label,fill='white')
  board.convert('RGB').save(p/f'{mode}-{direction}-comparison.png')
(p/'package-review.json').write_text(json.dumps(dict(records=records,sourceFrames=18,originalAlphaRedBlueExact=True,outsideEdgeAdmissionExact=True,frozenInputsStable=True,
    realProfileUnchanged=True,visualReviewPending=True,sourceAcceptance=False,normalChanged=False,scope='Representative source-native edge-material samples only. No864frame expansion,normal adoption or semantic segmentation inferred.'),indent=2)+'\n')
print('All18 candidates preserve exact alpha/R/B/outside edge mask. Six comparison boards prepared.')
