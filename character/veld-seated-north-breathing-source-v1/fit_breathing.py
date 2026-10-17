"""Source-contour-guided breathing of the exact graded seated neutral.

Only ribcage/sleeve support deforms; fixed skull, collar, panel and planted lower
anatomy preserve selected materials. Source RGB is not a new material authority.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import map_coordinates
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;BASE=P.parent/'veld-seated-north-coherent-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources=[np.array(Image.open(P/f'diagnostic-v2/{i:03}.png').convert('RGBA')) for i in range(6)]
# Use registered high-alpha silhouette widths; material pixel differences are excluded.
widths=[]
for a in sources:
 values=[]
 for y in range(151,173):
  xs=np.where(a[y,:,3]>180)[0];values.append(float(xs[-1]-xs[0]+1))
 widths.append(float(np.mean(values)))
# Source neutral/relaxed difference is drift, not permission to shrink the canonical pose.
measured_expansion=np.maximum(0,(np.array(widths)-widths[0])/2)
assert measured_expansion.max()>.05,('source has no resolved contour expansion',widths)
# Authored local phase curve, not a claim that the six generated figures supply
# six coherent motion samples. Rise to measured peak, longer exhale, neutral seam.
expansion=measured_expansion.max()*np.array([0,.5,1,.75,.25,0])
yy,xx=np.indices((256,256),dtype=float)
vertical=np.zeros((256,256));support=(yy>146)&(yy<178)
vertical[support]=np.sin(np.pi*(yy[support]-146)/32)**2
# Central rigid back panel is fixed; expansion grows toward the outer sleeve.
horizontal=np.clip((abs(xx-128)-10)/16,0,1)
affected=support&(abs(xx-128)>10)&(abs(xx-128)<34)
records=[];sequences={}
for gear in ('bare','helmet'):
 neutral_path=BASE/f'frames/{gear}/sit-down-north/005.png'
 neutral=Image.open(neutral_path).convert('RGBA');a=np.array(neutral)
 alpha=a[:,:,3].astype(float)/255
 premul=a[:,:,:3].astype(float)*alpha[:,:,None]
 paths=[];frames=[]
 for slot,amount in enumerate(expansion):
  result=a.copy()
  if amount>0:
   source_x=xx-np.sign(xx-128)*amount*vertical*horizontal
   new_alpha=map_coordinates(alpha,[yy,source_x],order=1,mode='constant',cval=0)
   channels=[map_coordinates(premul[:,:,c],[yy,source_x],order=1,mode='constant',cval=0) for c in range(3)]
   for c,channel in enumerate(channels):
    rgb=np.divide(channel,new_alpha,out=np.zeros_like(channel),where=new_alpha>0)
    result[:,:,c][affected]=np.rint(rgb[affected]).clip(0,255).astype('uint8')
   result[:,:,3][affected]=np.rint(new_alpha[affected]*255).clip(0,255).astype('uint8')
  frame=Image.fromarray(result);path=P/f'frames/{gear}/sit-idle-north/{slot:03}.png';path.parent.mkdir(parents=True,exist_ok=True);frame.save(path)
  files=path.relative_to(P).as_posix();paths.append(files);frames.append(frame)
  records.append({'gear':gear,'slot':slot,'sideExpansionPx':float(amount),'changedPixels':int(np.any(a!=result,axis=2).sum()),'neutralSha256':sha(neutral_path),'frameSha256':sha(path),'protectedExact':bool(np.array_equal(result[~affected],a[~affected]))})
 state={'id':'sit-idle-north','frameFiles':paths,'frameDurationsMs':[600]*6,'loop':True,'facings':['north']*6,'waterPoses':[False]*6,'waterKinds':['seated']*6,'depthOffsets':[0]*6,'seatContactDepth':True}
 manifest={'name':f'Veld north source-guided seated breath {gear}','status':'staged_candidate','precomposed':True,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','states':[state]}
 if gear=='helmet':manifest['equipment']='diving-helmet'
 (P/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 # Palette for diagnostic only, PNGs remain authoritative RGBA.
 playback=[]
 for frame in frames:
  bg=Image.new('RGB',(256,256),'#202a30');bg.paste(frame,mask=frame.getchannel('A'));playback.append(bg)
 playback[0].save(P/f'{gear}-breathing.gif',save_all=True,append_images=playback[1:],duration=600,loop=0)
 sequences[gear]=frames
board=Image.new('RGB',(1536,830),'#202a30');d=ImageDraw.Draw(board)
for row,gear in enumerate(('bare','helmet')):
 for col,frame in enumerate(sequences[gear]):
  x=col*256;y=row*415;board.paste(frame,(x,y+10),frame)
  crop=frame.crop((94,135,162,182)).resize((204,141),Image.Resampling.NEAREST);board.paste(crop,(x+26,y+268),crop)
  d.text((x+6,y+2),f'{gear} {col}: {expansion[col]:.3f}px / side',fill='white')
board.save(P/'fitted-contact.png')
report={'status':'staged source-contour-guided local breathing; no full generated-body adoption','source':'sources/breathing-v2.png','sourceSha256':sha(P/'sources/breathing-v2.png'),'fixedSourceRuler':.29306930693069305,'sourceRegisteredMeanWidths':widths,'measuredSourceSideExpansionPx':measured_expansion.tolist(),'sideExpansionPx':expansion.tolist(),'deformation':'locally authored phase curve using measured source maximum; premultiplied horizontal rib/sleeve expansion, bounded y147:177 outside rigid panel; exact current neutral pixels; no per-frame grade','records':records,'scope':'paired held-only candidate; neutral join exact, normal selection/native/motion acceptance pending'}
(P/'fitted-registration.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'frames':12,'widths':widths,'expansion':expansion.tolist(),'allProtectedExact':all(r['protectedExact'] for r in records)}))
