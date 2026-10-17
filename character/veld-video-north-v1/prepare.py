from pathlib import Path
import sys,json
import numpy as np
from PIL import Image
from scipy import ndimage
P=Path(__file__).resolve().parent
root=P.parent/'veld-animation-pilot-v12'
sys.path.insert(0,str(root))
from brightness import match
from materials import apply as materials
targets=json.loads((root/'brightness-checks.json').read_text())['targets']
for direction in ['north','south']:
 out=P.parent/f'veld-video-{direction}-v1';out.mkdir(exist_ok=True)
 im=Image.open(root/'sources'/f'idle-{direction}-01.png').convert('RGBA'); a=np.array(im)
 mask=a[:,:,3]>=128
 if direction=='north':mask=~((a[:,:,0]>180)&(a[:,:,1]<110)&(a[:,:,2]>180))
 # First top-left pose only, identified by source sheet cell.
 mask[im.height//2:]=False;mask[:,im.width//3:]=False
 lab,n=ndimage.label(mask);sz=np.bincount(lab.ravel());sz[0]=0;mask=lab==sz.argmax();ys,xs=np.where(mask)
 im.putalpha(Image.fromarray(mask.astype('uint8')*255));im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
 im,_=match(im,targets,'north' if direction=='north' else None)
 im,_,_=materials(im,'north' if direction=='north' else 'east',reference_match=False)
 # Remove magenta contamination along keyed edges without changing anatomy.
 arr=np.array(im);rgb=arr[:,:,:3].astype(float);spill=(arr[:,:,3]>0)&(rgb[:,:,0]>rgb[:,:,1]*1.2)&(rgb[:,:,2]>rgb[:,:,1]*1.2)
 valid=(arr[:,:,3]>0)&~spill
 _,near=ndimage.distance_transform_edt(~valid,return_indices=True);arr[spill,:3]=arr[near[0][spill],near[1][spill],:3];im=Image.fromarray(arr)
 im.save(out/'reference-cutout.png')
 # Fit original pixels into square rather than upscale the master.
 canvas=round(im.height/0.889);bg=Image.new('RGB',(canvas,canvas),(48,190,72));bg.paste(im,((canvas-im.width)//2,round(canvas*.054)),im);bg.save(out/'master-input.png')
 print(direction,im.size,canvas)
