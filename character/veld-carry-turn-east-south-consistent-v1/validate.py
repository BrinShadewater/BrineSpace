from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];original=json.loads((HERE/'original-states.json').read_text());checks=0
for v in ['bare','helmet']:
 m=json.loads((HERE/f'{v}-manifest.json').read_text());assert m['pivot']==[128,224] and m['standingHeight']==148;checks+=1
 for si,d in enumerate(['east-south','south-east']):
  state=m['states'][si];assert all(state[k]==original[si][k] for k in ['id','frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']);checks+=1
  with Image.open(HERE/f'{v}-{d}-v1.gif') as gif:
   assert gif.n_frames==6;checks+=1
   for i,path in enumerate(state['frameFiles']):
    a=np.array(Image.open(HERE/path).convert('RGBA'));assert a.shape==(256,256,4);checks+=1
    alpha=a[:,:,3];assert np.any(alpha>200) and not np.any(np.concatenate([alpha[0],alpha[-1],alpha[:,0],alpha[:,-1]])>20);checks+=1
    gif.seek(i);rgb=np.array(gif.convert('RGB')).astype(int);outside=(alpha==0)&(distance_transform_edt(alpha<200)>2);assert np.abs(rgb[outside]-[32,42,48]).max()<=3;checks+=1
    if si==1:
     reverse=np.array(Image.open(HERE/m['states'][0]['frameFiles'][5-i]).convert('RGBA'));assert np.array_equal(a,reverse);checks+=1
  for i,direction in [(0,d.split('-')[0]),(5,d.split('-')[1])]:
   endpoint=np.array(Image.open(ROOT/f'character/veld-carry-{direction}-consistent-v1/frames/{v}/000.png').convert('RGBA'));frame=np.array(Image.open(HERE/state['frameFiles'][i]).convert('RGBA'));assert np.array_equal(endpoint,frame);checks+=1
(HERE/'packaging-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'original_metadata_exact':True,'endpoint_pixels_exact':True,'reverse_pixels_exact':True,'decoded_gif_frames':24},indent=2)+'\n');print(f'{checks} packaging checks, 0 failures')
