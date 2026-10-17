from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];original=json.loads((HERE/'original-states.json').read_text());refs=json.loads((HERE/'provenance.json').read_text());checks=0
for v in ['bare','helmet']:
 m=json.loads((HERE/f'{v}-manifest.json').read_text());assert m['pivot']==[128,224] and m['standingHeight']==148;checks+=1
 for state in m['states']:
  base=next(s for s in original if s['id']==state['id']);assert all(state[k]==base[k] for k in ['id','frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']);checks+=1
  direction=state['id'].removeprefix('carry-turn-');frames=[]
  with Image.open(HERE/f'{v}-{direction}-v1.gif') as gif:
   # The identical seam poses may coalesce into one decoded GIF frame.
   assert 11<=gif.n_frames<=12;checks+=1
   for path in state['frameFiles']:
    a=np.array(Image.open(HERE/path).convert('RGBA'));assert a.shape==(256,256,4);checks+=1
    alpha=a[:,:,3];assert np.any(alpha>200) and not np.any(np.concatenate([alpha[0],alpha[-1],alpha[:,0],alpha[:,-1]])>20);checks+=1
    source=np.array(Image.open(ROOT/refs[path]['source']).convert('RGBA'));assert np.array_equal(a,source);checks+=1;frames.append(a)
   assert np.array_equal(frames[5],frames[6]);checks+=1
   # GIF encoder merges adjacent identical pixels; verify each decoded exterior
   # against its closest source frame, preserving transparent boundary evidence.
   for i in range(gif.n_frames):
    gif.seek(i);rgb=np.array(gif.convert('RGB')).astype(int);errors=[]
    for a in frames:
     outside=(a[:,:,3]==0)&(distance_transform_edt(a[:,:,3]<200)>2);errors.append(np.abs(rgb[outside]-[32,42,48]).max())
    assert min(errors)<=3;checks+=1
for repair in (HERE/'helmet-head-repairs').glob('*.png'):
 base=np.array(Image.open(ROOT/'character/veld-carry-turn-north-east-consistent-v1/frames/helmet/carry-turn-north-east'/repair.name).convert('RGBA'));fixed=np.array(Image.open(repair).convert('RGBA'));outside=np.ones((256,256),bool);outside[68:105,100:157]=False;assert np.array_equal(base[outside],fixed[outside]);checks+=1
(HERE/'packaging-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'exact_recorded_source_pixels':True,'body_outside_head_repair_exact':True,'shared_joint_pixels':True,'original_metadata_exact':True},indent=2)+'\n');print(f'{checks} packaging checks, 0 failures')
