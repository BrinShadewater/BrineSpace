"""Compose master-joined bare yaw candidate; no installed bindings."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
from fit_material_trials import masks,curves
H=Path(__file__).resolve().parent;R=H.parents[1]
raw=Image.open(H/'bare-yaw72-source-v3.png').convert('RGBA');a=np.array(raw);lab,n=label(a[:,:,3]>160);sizes=np.bincount(lab.ravel());k=1+np.argmax(sizes[1:]);y,x=np.where(lab==k);box=[int(x.min())-2,int(y.min())-2,int(x.max())+3,int(y.max())+3];assert min(box[:2])>=0 and box[2]<=a.shape[1] and box[3]<=a.shape[0];cut=a.copy();cut[~binary_dilation(lab==k,iterations=2)]=0;raw=Image.fromarray(cut).crop(box);raw.save(H/'source-crops/yaw72-v3.png');a=np.array(raw);v=a[:,:,:3].astype(float);m,fb,head=masks(a);before=a.copy()
for key,mask in m.items():
 for c in range(3):a[mask,c]=np.interp(v[mask].mean(1),curves[key]['knots'],np.array(curves[key]['targets'])[:,c]).clip(0,255).astype('uint8')
assert np.array_equal(before[:,:,3],a[:,:,3]);assert np.array_equal(before[head&~m['skin']],a[head&~m['skin']]);union=m['skin']|m['cloth']|m['patch'];assert np.array_equal(before[~union],a[~union])
scale=.125;target=np.array([133,150]);face=np.array([(fb[0]+fb[2])/2,fb[3]]);pos=np.rint(target-face*scale).astype(int);pose=Image.fromarray(a).resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS);late=Image.new('RGBA',(256,256));late.alpha_composite(pose,tuple(pos));late.save(H/'graded-trials/003.png')
e=Image.open(R/'character/veld-water-east-coherent-v1/frames/bare/swim-east/000.png').convert('RGBA');s=Image.open(R/'character/veld-water-south-coherent-v1/frames/bare/swim-south/000.png').convert('RGBA');images=[e]+[Image.open(H/f'graded-trials/{i:03}.png').convert('RGBA') for i in range(3)]+[late,s];cov=json.loads((R/'character/veld-consistency-audit-v3/coverage.json').read_text());states=[];checks=4
for direction,row in [('east-south',images),('south-east',list(reversed(images)))]:
 rec=cov['selected']['bare']['swim-turn-'+direction];old=json.loads((R/rec['manifest']).read_text());state=next(x for x in old['states'] if x['id']=='swim-turn-'+direction).copy();assert len(state['frameDurationsMs'])==len(row);files=[]
 for i,im in enumerate(row):
  ar=np.array(im);assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1;file=f'frames/bare/swim-turn-{direction}/{i:03}.png';(H/file).parent.mkdir(parents=True,exist_ok=True);im.save(H/file);files.append(file)
 state.update(frameFiles=files);states.append(state)
manifest=json.loads((R/'character/veld-water-east-coherent-v1/bare-manifest.json').read_text());manifest.update(name='Veld coherent east south ordinary swim turns bare',states=states,status='staged_bare_yaw_pending_helmet_motion_native_review');(H/'bare-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
board=Image.new('RGBA',(1536,560),'#202a30');d=ImageDraw.Draw(board)
for row in range(2):
 for i,im in enumerate(images):
  if row==0:board.alpha_composite(im,(i*256,24))
  else:board.alpha_composite(im.resize((142,142),Image.Resampling.LANCZOS),(i*256+57,304));board.alpha_composite(im.resize((93,93),Image.Resampling.LANCZOS),(i*256+82,459))
  d.text((i*256+4,row*280+4),str(i)+(' exact selected loop' if i in [0,5] else ' authored yaw'),fill='white')
board.save(H/'bare-turn-contact-v1.png');(H/'bare-fit-v1.json').write_text(json.dumps({'checks':checks,'failures':0,'atlasScale':.24,'correctedSourceScale':scale,'lateSourceBox':box,'lateFaceBox':fb,'latePosition':pos.tolist(),'correctedScaleRule':'independent high-density source: projected skull about170 maps21px; shoulder about312 maps39px; one.125 scale','exactEndpointPixels':True,'grade':'frozen first-three source family curve applied to fourth, no per-pose exposure','installed':False},indent=2)+'\n');print(f'{checks} corrected material/family border checks PASS;2 bare states12refs staged')
