"""Locally authored breathing from the exact fitted south neutral.

No generated motion or RGB is adopted. Rigid chest hardware and seated supports
remain exact; only the outer ribs/sleeves move, at the north breathing amplitude.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.ndimage import map_coordinates
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
BASE=P.parent/'veld-seated-south-coherent-v1'
NORTH=P.parent/'veld-seated-north-breathing-source-v1/fitted-registration.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
amplitude=max(json.loads(NORTH.read_text())['sideExpansionPx'])
phase=np.array([0,.5,1,.75,.25,0]);expansion=amplitude*phase
yy,xx=np.indices((256,256),dtype=float)
allowed=(yy>130)&(yy<160)&(abs(xx-128)>12)&(abs(xx-128)<31)
vertical=np.sin(np.pi*np.clip((yy-130)/30,0,1))**2
horizontal=np.clip((abs(xx-128)-12)/14,0,1)
records=[];sequences={}
for gear in ('bare','helmet'):
 neutral_path=BASE/f'frames/{gear}/sit-down-south/005.png'
 a=np.array(Image.open(neutral_path).convert('RGBA'))
 alpha=a[:,:,3].astype(float)/255;premul=a[:,:,:3]*alpha[:,:,None]
 frames=[];files=[]
 for slot,amount in enumerate(expansion):
  result=a.copy()
  if amount:
   sx=xx-np.sign(xx-128)*amount*vertical*horizontal
   na=map_coordinates(alpha,[yy,sx],order=1,mode='constant',cval=0)
   for c in range(3):
    channel=map_coordinates(premul[:,:,c],[yy,sx],order=1,mode='constant',cval=0)
    rgb=np.divide(channel,na,out=np.zeros_like(channel),where=na>0)
    result[:,:,c][allowed]=np.rint(rgb[allowed]).clip(0,255).astype('uint8')
   result[:,:,3][allowed]=np.rint(na[allowed]*255).clip(0,255).astype('uint8')
  path=P/f'frames/{gear}/sit-idle-south/{slot:03}.png';path.parent.mkdir(parents=True,exist_ok=True)
  frame=Image.fromarray(result);frame.save(path);frames.append(frame);files.append(path.relative_to(P).as_posix())
  records.append({'gear':gear,'slot':slot,'sideExpansionPx':float(amount),'changedPixels':int(np.any(a!=result,axis=2).sum()),'neutralSha256':sha(neutral_path),'frameSha256':sha(path),'protectedExact':bool(np.array_equal(result[~allowed],a[~allowed]))})
 state={'id':'sit-idle-south','frameFiles':files,'frameDurationsMs':[600]*6,'loop':True,'facings':['south']*6,'waterPoses':[False]*6,'waterKinds':['seated']*6,'depthOffsets':[0]*6,'seatContactDepth':True}
 manifest={'name':f'Veld south locally authored seated breathing {gear}','status':'staged_candidate','precomposed':True,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','states':[state]}
 if gear=='helmet':manifest['equipment']='diving-helmet'
 (P/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 playback=[]
 for frame in frames:
  bg=Image.new('RGB',(256,256),'#202a30');bg.paste(frame,mask=frame.getchannel('A'));playback.append(bg)
 playback[0].save(P/f'{gear}-breathing.gif',save_all=True,append_images=playback[1:],duration=600,loop=0)
 sequences[gear]=frames
board=Image.new('RGB',(1536,800),'#202a30');d=ImageDraw.Draw(board)
for row,gear in enumerate(('bare','helmet')):
 for col,frame in enumerate(sequences[gear]):
  x=col*256;y=row*400;board.paste(frame,(x,y+10),frame)
  crop=frame.crop((94,122,162,168)).resize((204,138),Image.Resampling.NEAREST);board.paste(crop,(x+26,y+262),crop)
  d.text((x+6,y+2),f'{gear} {col}: {expansion[col]:.3f}px / side',fill='white')
board.save(P/'contact.png')
(P/'registration.json').write_text(json.dumps({'status':'staged locally authored breathing; no generated-body adoption','amplitudeAuthority':str(NORTH.relative_to(P.parent.parent)).replace('\\','/'),'amplitudeAuthoritySha256':sha(NORTH),'sideExpansionPx':expansion.tolist(),'affectedRegion':'y131:159, 12<abs(x-128)<31; central chest fittings/head/collar/belt/hands/lower supports exact','fixedSourceRuler':148/509,'grade':'exact final south neutral RGB; no additional grading','records':records},indent=2)+'\n')
print(json.dumps({'frames':12,'sideExpansionPx':expansion.tolist(),'protectedExact':all(r['protectedExact'] for r in records)}))
