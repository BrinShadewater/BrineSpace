"""Independent side breathing from exact fitted neutrals, without new anatomy."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.ndimage import map_coordinates
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
AUTH=P.parent/'veld-seated-north-breathing-source-v1/fitted-registration.json'
PHASE=[0,.5,1,.75,.25,0]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def region(direction,a):
 yy,xx=np.indices((256,256),dtype=float)
 low,high,center,sign=(85,104,104,-1) if direction=='east' else (150,174,150,1)
 allowed=(yy>149)&(yy<163)&(xx>low)&(xx<high)
 # Protect the actual science patch, including its lower blue fringe.
 rgb=a[:,:,:3].astype(float)
 blue=(rgb[:,:,2]>rgb[:,:,0]*1.15)&(rgb[:,:,2]>rgb[:,:,1]*1.05)
 allowed &= ~blue
 vertical=np.sin(np.pi*np.clip((yy-149)/14,0,1))**2
 horizontal=np.clip(abs(xx-center)/18,0,1)
 return allowed,yy,xx,sign*vertical*horizontal
amp=max(json.loads(AUTH.read_text(encoding='utf-8'))['sideExpansionPx'])
records=[];sequences={};source_bindings={}
for gear in ('bare','helmet'):
 states=[]
 for direction in ('east','west'):
  base=P.parent/f'veld-seated-{direction}-coherent-v1'
  neutral=base/f'frames/{gear}/sit-down-{direction}/005.png'
  a=np.array(Image.open(neutral).convert('RGBA'))
  # Both gears share the exact same lower-body mask authority.
  mask_source=np.array(Image.open(base/f'frames/bare/sit-down-{direction}/005.png').convert('RGBA'))
  allowed,yy,xx,offset=region(direction,mask_source)
  alpha=a[:,:,3].astype(float)/255;premul=a[:,:,:3]*alpha[:,:,None]
  files=[];frames=[]
  for slot,phase in enumerate(PHASE):
   b=a.copy();amount=amp*phase
   if amount:
    sx=xx-amount*offset
    na=map_coordinates(alpha,[yy,sx],order=1,mode='constant',cval=0)
    for c in range(3):
     channel=map_coordinates(premul[:,:,c],[yy,sx],order=1,mode='constant',cval=0)
     rgb=np.divide(channel,na,out=np.zeros_like(channel),where=na>0)
     b[:,:,c][allowed]=np.rint(rgb[allowed]).clip(0,255).astype('uint8')
    b[:,:,3][allowed]=np.rint(na[allowed]*255).clip(0,255).astype('uint8')
   path=P/f'frames/{gear}/sit-idle-{direction}/{slot:03}.png'
   path.parent.mkdir(parents=True,exist_ok=True);im=Image.fromarray(b);im.save(path)
   frames.append(im);files.append(path.relative_to(P).as_posix())
   records.append({'gear':gear,'direction':direction,'slot':slot,'expansionPx':amount,'changedPixels':int(np.any(a!=b,axis=2).sum()),'frameSha256':sha(path),'protectedExact':bool(np.array_equal(a[~allowed],b[~allowed]))})
  source_bindings[neutral.relative_to(P.parents[1]).as_posix()]=sha(neutral)
  states.append({'id':f'sit-idle-{direction}','frameFiles':files,'frameDurationsMs':[600]*6,'loop':True,'facings':[direction]*6,'waterPoses':[False]*6,'waterKinds':['seated']*6,'depthOffsets':[0]*6,'seatContactDepth':True})
  sequences[gear,direction]=frames
  playback=[]
  for frame in frames:
   bg=Image.new('RGB',(256,256),'#202a30');bg.paste(frame,mask=frame.getchannel('A'));playback.append(bg)
  playback[0].save(P/f'{gear}-{direction}-breathing.gif',save_all=True,append_images=playback[1:],duration=600,loop=0)
 m={'name':f'Veld independent side seated breathing {gear}','status':'staged_candidate','precomposed':True,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','states':states}
 if gear=='helmet':m['equipment']='diving-helmet'
 (P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1536,1440),'#202a30');draw=ImageDraw.Draw(board)
for row,((gear,direction),frames) in enumerate(sequences.items()):
 for slot,im in enumerate(frames):
  x=slot*256;y=row*360
  board.paste(im,(x,y+10),im)
  crop=im.crop((80,140,180,170)).resize((240,72),Image.Resampling.NEAREST)
  board.paste(crop,(x+8,y+270),crop)
  draw.text((x+4,y+2),f'{gear} {direction} {slot}: {amp*PHASE[slot]:.3f}px',fill='white')
board.save(P/'contact.png')
(P/'registration.json').write_text(json.dumps({'authoring':'bounded local breathing, independent East/West source bodies; no generation, mirroring, scaling or regrading','amplitudeAuthority':AUTH.relative_to(P.parents[1]).as_posix(),'amplitudeAuthoritySha256':sha(AUTH),'amplitudePx':amp,'phase':PHASE,'sourceBindings':source_bindings,'affectedRegion':'rear lower sleeve/rib y150:162; East x86:103, West x151:173; actual blue patch pixels excluded','protected':'head/hair/helmet/collar/science patch/chest fittings/cuffs/hands/belt/pelvis/knees/boots','records':records},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frames':24,'states':4,'amplitudePx':amp,'protectedExact':all(r['protectedExact'] for r in records)}))
