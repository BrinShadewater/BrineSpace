from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label

P=Path(__file__).resolve().parent;R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=P.parent/'west-carry-motion-reference-v9'
sources=[source/f'clean-frames/{i:03}.png' for i in range(24,48)]
names=[f'source-{i}' for i in range(24,48)]
shellpath=R/'character/veld-helmet-original-turntable-west-v1/mixed-v5-study/shells/005.png';shell=Image.open(shellpath).convert('RGBA')
holds=[round((i+1)*1000/24)-round(i*1000/24) for i in range(24)]
bindings={};bare=[];helmet=[];rows=[];checks=0
for i,source in enumerate(sources):
 im=Image.open(source).convert('RGBA');assert im.size==(256,256);bare.append(im)
 a=np.array(im);y,x=np.where(a[:,:,3]>128);top=int(y.min());hx=np.where(a[top:top+24,:,3]>128)[1]
 sy,sx=np.where(a[:,:,3]>200);shelltop=int(sy.min());hxs=np.where(a[shelltop:shelltop+16,:,3]>128)[1];left=int(hxs.min());pos=(left-3,shelltop-11);box=(left-2,shelltop,left+31,shelltop+27)
 out=im.copy();out.paste((0,0,0,0),box);out.alpha_composite(shell,pos);outside=np.ones((256,256),bool);outside[pos[1]:shelltop+28,pos[0]:left+31]=False;assert np.array_equal(a[outside],np.array(out)[outside]);checks+=1;helmet.append(out)
 rgb=a[:,:,:3].astype(int);blue=(a[:,:,3]>128)&(rgb[:,:,2]>rgb[:,:,0]+12)&(rgb[:,:,2]>rgb[:,:,1]+3)
 rows.append({'slot':i,'pose':names[i],'source':source.relative_to(R).as_posix(),'height':int(y.max()-y.min()+1),'headTop':top,'headWidth':int(hx.max()-hx.min()+1),'headAxis':float((hx.min()+hx.max())/2),'floorAlpha128':int(y.max()),'blueMedianRGB':np.median(rgb[blue],axis=0).tolist(),'helmetPosition':pos,'helmetClearBox':box})
 bindings[source.relative_to(R).as_posix()]=sha(source)
 for gear,img in [('bare',im),('helmet',out)]:
  f=P/f'frames/{gear}/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);img.save(f);bindings[f.relative_to(R).as_posix()]=sha(f)
for gear,frames in [('bare',bare),('helmet',helmet)]:
 refs=['res://'+(P/f'frames/{gear}/{i:03}.png').relative_to(R).as_posix() for i in range(24)]
 state={'id':'carry-west','frameFiles':refs,'frameDurationsMs':holds,'loop':True,'facings':['west']*24,'waterKinds':['carry']*24,'waterPoses':[False]*24,'depthOffsets':[0.0]*24}
 data={'name':'Veld West immutable-master matched carry '+gear,'status':'staged_continuous_cycle_not_normal_admission','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'strideDistanceCells':{'carry-west':0.07351351351351351},'states':[state]}
 f=P/f'{gear}-manifest.json';f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf8');bindings[f.relative_to(R).as_posix()]=sha(f)
 frames[0].save(P/f'{gear}-carry.png',save_all=True,append_images=frames[1:],duration=holds,loop=0,disposal=0,blend=0)
 ap=Image.open(P/f'{gear}-carry.png');assert ap.n_frames==24
 for i,im in enumerate(frames):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes();assert ap.info['duration']==holds[i];checks+=2
 board=Image.new('RGB',(1536,1152),'#202a30');d=ImageDraw.Draw(board)
 for i,im in enumerate(frames):
  x=i%6*256;y=i//6*288;d.text((x+4,y+4),names[i],fill='white');board.paste(im,(x,y+24),im)
 board.save(P/f'{gear}-chronology.png')
bindings[shellpath.relative_to(R).as_posix()]=sha(shellpath)
report=dict(checks=checks,failures=0,slotsPerGear=24,durationMs=1000,strideDistanceCells=.07351351351351351,bodyOutsideHelmetExactFrames=24,rows=rows,scope='Continuous consecutive source24..47; original shell. Existing stride preserved provisionally pending physical contact. No normal admission.',bindings=bindings)
(P/'FAMILY_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['checks','slotsPerGear','durationMs','bodyOutsideHelmetExactFrames']}))
