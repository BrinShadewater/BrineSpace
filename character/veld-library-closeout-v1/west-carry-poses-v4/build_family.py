from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label

P=Path(__file__).resolve().parent;R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
anchor=P.parent/'west-cargo-anchor-highres-v3'
reg=json.loads((anchor/'BUILD_REVIEW.json').read_text());scale=reg['uniformScale'];offset=tuple(reg['wholeKeyOffset'])
sources=[P.parent/'west-carry-contact-v3/source.png',P/'down-a/source.png',P/'passing-a/source.png',P/'opposite/source.png',P/'down-b/source.png',P/'passing-b/source.png']
names=['near-contact','near-down','near-support/far-pass','far-contact','far-down','far-support/near-pass']
shellpath=R/'character/veld-helmet-original-turntable-west-v1/mixed-v5-study/shells/005.png';shell=Image.open(shellpath).convert('RGBA')
bindings={};bare=[];helmet=[];rows=[];checks=0
for i,source in enumerate(sources):
 src=Image.open(source).convert('RGBA');assert list(src.size)==reg['sourceSize']
 a=np.array(src);lab,_=label(a[:,:,3]>8);counts=np.bincount(lab.ravel());keep=counts>=20;keep[0]=False;a[~keep[lab]]=0
 scaled=Image.fromarray(a).resize((round(src.width*scale),round(src.height*scale)),Image.Resampling.LANCZOS)
 im=Image.new('RGBA',(256,256));im.alpha_composite(scaled,offset);bare.append(im)
 a=np.array(im);y,x=np.where(a[:,:,3]>128);top=int(y.min());hx=np.where(a[top:top+24,:,3]>128)[1]
 sy,sx=np.where(a[:,:,3]>200);shelltop=int(sy.min());hxs=np.where(a[shelltop:shelltop+16,:,3]>128)[1];left=int(hxs.min());pos=(left-3,shelltop-11);box=(left-2,shelltop,left+31,shelltop+27)
 out=im.copy();out.paste((0,0,0,0),box);out.alpha_composite(shell,pos);outside=np.ones((256,256),bool);outside[pos[1]:shelltop+28,pos[0]:left+31]=False;assert np.array_equal(a[outside],np.array(out)[outside]);checks+=1;helmet.append(out)
 rgb=a[:,:,:3].astype(int);blue=(a[:,:,3]>128)&(rgb[:,:,2]>rgb[:,:,0]+12)&(rgb[:,:,2]>rgb[:,:,1]+3)
 rows.append({'slot':i,'pose':names[i],'source':source.relative_to(R).as_posix(),'height':int(y.max()-y.min()+1),'headTop':top,'headWidth':int(hx.max()-hx.min()+1),'headAxis':float((hx.min()+hx.max())/2),'floorAlpha128':int(y.max()),'blueMedianRGB':np.median(rgb[blue],axis=0).tolist(),'helmetPosition':pos,'helmetClearBox':box})
 bindings[source.relative_to(R).as_posix()]=sha(source)
 for gear,img in [('bare',im),('helmet',out)]:
  f=P/f'frames/{gear}/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);img.save(f);bindings[f.relative_to(R).as_posix()]=sha(f)
for gear,frames in [('bare',bare),('helmet',helmet)]:
 refs=['res://'+(P/f'frames/{gear}/{i:03}.png').relative_to(R).as_posix() for i in range(6)]
 state={'id':'carry-west','frameFiles':refs,'frameDurationsMs':[140]*6,'loop':True,'facings':['west']*6,'waterKinds':['carry']*6,'waterPoses':[False]*6,'depthOffsets':[0.0]*6}
 data={'name':'Veld West authored whole-body carry '+gear,'status':'staged_authored_cycle_not_normal_admission','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'strideDistanceCells':{'carry-west':0.07351351351351351},'states':[state]}
 f=P/f'{gear}-manifest.json';f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf8');bindings[f.relative_to(R).as_posix()]=sha(f)
 frames[0].save(P/f'{gear}-carry.png',save_all=True,append_images=frames[1:],duration=[140]*6,loop=0,disposal=0,blend=0)
 ap=Image.open(P/f'{gear}-carry.png');assert ap.n_frames==6
 for i,im in enumerate(frames):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes();assert ap.info['duration']==140;checks+=2
 board=Image.new('RGB',(1536,610),'#202a30');d=ImageDraw.Draw(board)
 for i,im in enumerate(frames):
  d.text((i*256+4,5),str(i)+' '+names[i],fill='white');board.paste(im,(i*256,20),im);d.line((i*256,244,i*256+255,244),fill='#728792')
  crop=im.crop((90,60,170,160)).resize((160,200),Image.Resampling.NEAREST);board.paste(crop,(i*256+40,340),crop)
 board.save(P/f'{gear}-chronology.png')
 # Only image resizing for review: runtime images remain unchanged256 canvases.
 b=Image.new('RGB',(1536,580),'#202a30');d=ImageDraw.Draw(b)
 for h,y in [(47,100),(93,290),(148,540)]:
  d.line((0,y,1535,y),fill='#728792')
  for i,im in enumerate(frames):
   s=h/148;small=im.resize((round(256*s),round(256*s)),Image.Resampling.LANCZOS);b.paste(small,(round(i*256+128-128*s),round(y-224*s)),small)
 b.save(P/f'{gear}-scales.png')
bindings[shellpath.relative_to(R).as_posix()]=sha(shellpath);bindings[(anchor/'BUILD_REVIEW.json').relative_to(R).as_posix()]=sha(anchor/'BUILD_REVIEW.json')
report={'checks':checks,'failures':0,'sourcePoseOrder':names,'slotsPerGear':6,'durationMs':840,'strideDistanceCells':.07351351351351351,'fixedUniformScale':scale,'fixedWholeOffset':offset,'noPerPoseRegistrationOrGrade':True,'bodyOutsideHelmetExactFrames':6,'rows':rows,'scope':'Whole-body authored six-pose candidate; preserve accepted840ms stride contract. Source/loop/material/physical contact review separate; no normal admission.','bindings':bindings}
(P/'FAMILY_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8');print(json.dumps({'checks':checks,'rows':rows}))
