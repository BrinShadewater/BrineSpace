from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];original=json.loads((HERE/'original-states.json').read_text());checks=0
for v in ['bare','helmet']:
 m=json.loads((HERE/f'{v}-manifest.json').read_text());assert m['pivot']==[128,224] and m['standingHeight']==148;checks+=1
 for si,d in enumerate(['north-west','west-north']):
  state=m['states'][si];assert all(state[k]==original[si][k] for k in ['id','frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']);checks+=1
  with Image.open(HERE/f'{v}-{d}-v1.gif') as gif:
   assert gif.n_frames==6;checks+=1
   for i,path in enumerate(state['frameFiles']):
    a=np.array(Image.open(HERE/path).convert('RGBA'));assert a.shape==(256,256,4);checks+=1
    alpha=a[:,:,3];assert np.any(alpha>200) and not np.any(np.concatenate([alpha[0],alpha[-1],alpha[:,0],alpha[:,-1]])>20);checks+=1
    gif.seek(i);rgb=np.array(gif.convert('RGB')).astype(int);outside=(alpha==0)&(distance_transform_edt(alpha<200)>2);assert np.abs(rgb[outside]-[32,42,48]).max()<=3;checks+=1
    if si==1:
     reverse=np.array(Image.open(HERE/m['states'][0]['frameFiles'][5-i]).convert('RGBA'));assert np.array_equal(a,reverse);checks+=1
  for path in state['frameFiles']:
   frame=np.array(Image.open(HERE/path).convert('RGBA'));yy,xx=np.where(frame[:,:,3]>200);floor=yy.max();by,bx=np.where(frame[floor-9:floor+1,:,3]>200)
   # Adjacent planted boots occupy up to41px in this reviewed west source; catch the
   # former wide split-stride endpoints without requiring a silhouette width.
   assert bx.max()-bx.min()+1<=44, 'Planted boot span too wide';checks+=1
(HERE/'packaging-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'original_metadata_exact':True,'stationary_boot_span_checked':True,'reverse_pixels_exact':True,'decoded_gif_frames':24},indent=2)+'\n');print(f'{checks} packaging checks, 0 failures')
