"""Fit bounded authored arms/tablet onto exact seated bodies for both gears."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent; R=P.parents[1]; B=R/'character/veld-seated-south-coherent-v1'
source=P/'sources/reading-v1.png'; raw=np.array(Image.open(source).convert('RGBA')); base_reg=json.loads((B/'bare-registration.json').read_text()); ruler=base_reg['fixedRuler']
labs,n=label(raw[:,:,3]>180); counts=np.bincount(labs.ravel()); counts[0]=0
parts=sorted(np.argsort(counts)[-6:],key=lambda k:(int(np.where(labs==k)[0].mean())//512,int(np.where(labs==k)[1].mean())//512))
assert len(parts)==6 and all(counts[k]>20000 for k in parts)
# Reuse the frozen seated material curves; head and upper-body output are discarded.
rgb=raw[:,:,:3].astype(float); solid=raw[:,:,3]>200; yy,xx=np.indices(raw.shape[:2]); head=np.zeros(raw.shape[:2],bool)
for k in parts:
 y,x=np.where(labs==k); top=y.min();head|=(labs==k)&(yy<top+110)
cyan=solid&~head&(rgb[:,:,1]>1.4*rgb[:,:,0])&(rgb[:,:,2]>1.3*rgb[:,:,0])&(rgb[:,:,1]>.72*rgb[:,:,2])
science=solid&~head&~cyan&(rgb[:,:,2]>1.3*rgb[:,:,0])&(rgb[:,:,2]>1.10*rgb[:,:,1])
neutral=solid&~head&~cyan&~science&(np.ptp(rgb,axis=2)<45)
masks={'cloth':neutral&(rgb.mean(2)<=95),'metal':neutral&(rgb.mean(2)>95),'science':science,'cyan':cyan}; graded=raw.copy()
for name,mask in masks.items():
 curve=base_reg['curves'][name]; lum=rgb[mask].mean(1)
 for c in range(3): graded[mask,c]=np.interp(lum,curve['knots'],np.array(curve['targets'])[:,c]).clip(0,255).astype('uint8')
assert np.array_equal(graded[:,:,3],raw[:,:,3]); generated=[]; records=[]
for slot,k in enumerate(parts):
 y,x=np.where(labs==k);floor=int(y.max());foot=float(x[y>=floor-8].mean());box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
 pixels=graded.copy(); pixels[~(binary_dilation(labs==k,iterations=3)&(raw[:,:,3]>0))]=0
 crop=Image.fromarray(pixels).crop(box);size=[round(crop.width*ruler),round(crop.height*ruler)];pos=[round(128-(foot-box[0])*ruler),round(223-(floor-box[1])*ruler)]
 frame=Image.new('RGBA',(256,256));frame.alpha_composite(crop.resize(size,Image.Resampling.LANCZOS),pos);generated.append(np.array(frame))
 records.append({'slot':slot,'rawBox':box,'floor':floor,'foot':foot,'size':size,'position':pos})
# Fixed lower forearm/glove/lap/tablet band, excluding face/hair/collar/badges,
# upper chest fittings, knees/shins/boots. Deliberate source insertion, not warping.
region=[105,148,151,185]; mask=np.zeros((256,256),bool);mask[region[1]:region[3],region[0]:region[2]]=True
frames_by_gear={}; files_by_gear={}
entry=[0,1,2,3];entry_ms=[80,120,140,140];hold=[3,5,4,3,5,3];hold_ms=[1840]*6;exit=[3,2,1,0];exit_ms=[140,140,120,80]
def state(key,indices,times,loop,files):return {'id':key,'frameFiles':[files[i] for i in indices],'frameDurationsMs':times,'loop':loop,'facings':['south']*len(indices),'waterPoses':[False]*len(indices),'waterKinds':['seated']*len(indices),'depthOffsets':[0]*len(indices),'seatContactDepth':True}
for gear in ('bare','helmet'):
 base_path=B/f'frames/{gear}/sit-down-south/005.png'; base=np.array(Image.open(base_path).convert('RGBA'));frames=[Image.fromarray(base)];files=[]
 for slot in range(1,6):
  out=base.copy();out[mask]=generated[slot][mask];assert np.array_equal(out[~mask],base[~mask]);frames.append(Image.fromarray(out))
 for slot,frame in enumerate(frames):
  path=P/f'frames/{gear}/read-seated-south/{slot:03}.png';path.parent.mkdir(parents=True,exist_ok=True);frame.save(path);files.append(path.relative_to(P).as_posix())
 m={'name':f'Veld South bounded tablet {gear} candidate','status':'staged_candidate','precomposed':True,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','states':[state('read-seated-south',entry+hold+exit,entry_ms+hold_ms+exit_ms,False,files),state('read-seated-enter-south',entry,entry_ms,False,files),state('read-seated-exit-south',exit,exit_ms,False,files),state('read-seated-hold-south',hold,hold_ms,True,files)]}
 if gear=='helmet':m['equipment']='diving-helmet'
 (P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n');frames_by_gear[gear]=frames;files_by_gear[gear]=files
report={'executionId':'62bbed37-780e-44c9-a0e8-d6ad9baad405','source':'sources/reading-v1.png','sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'fixedRuler':ruler,'gradeAuthority':'character/veld-seated-south-coherent-v1/bare-registration.json','gradeAuthoritySha256':hashlib.sha256((B/'bare-registration.json').read_bytes()).hexdigest(),'bodyAuthority':{g:{'path':f'character/veld-seated-south-coherent-v1/frames/{g}/sit-down-south/005.png','sha256':hashlib.sha256((B/f'frames/{g}/sit-down-south/005.png').read_bytes()).hexdigest()} for g in ('bare','helmet')},'insertRegion':region,'frames':records,'fullReadDurationMs':12000,'scope':'bounded generated arm/tablet source on exact common seated body; staged, finite12s read includes draw/hold/stow; interrupted reading/room/Continue/acceptance pending'}
(P/'registration.json').write_text(json.dumps(report,indent=2)+'\n')
board=Image.new('RGB',(1536,1010),'#202a30');d=ImageDraw.Draw(board)
for row,gear in enumerate(('bare','helmet')):
 for slot,frame in enumerate(frames_by_gear[gear]):
  x=slot*256;y=row*505;board.paste(frame,(x,y+10),frame);d.text((x+4,y+2),gear+f' {slot}',fill='white')
  detail=frame.crop((95,130,162,195)).resize((201,195),Image.Resampling.NEAREST);board.paste(detail,(x+28,y+270),detail)
board.save(P/'paired-contact.png')
print(json.dumps({'exports':12,'states':8,'readCycleMs':12000,'region':region,'normalSelection':False}))
