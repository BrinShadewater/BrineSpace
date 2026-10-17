from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();F=P/'frames/helmet';F.mkdir(parents=True,exist_ok=True);shellpath=R/'character/veld-helmet-original-turntable-west-v1/mixed-v5-study/shells/005.png';shell=Image.open(shellpath).convert('RGBA');bare=[Image.open(f).convert('RGBA') for f in sorted((P/'frames/bare').glob('*.png'))];helmet=[];landmarks=[];checks=0;bindings={shellpath.relative_to(R).as_posix():sha(shellpath)}
for n,im in enumerate(bare):
 a=np.array(im);rgb=a[:,:,:3].astype(int);y,x=np.where(a[:,:,3]>200);top=int(y.min());ys,xs=np.where(a[top:top+8,:,3]>128);cx=float(np.median(xs));warm=(a[:,:,3]>128)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);roi=np.zeros((256,256),bool);roi[top:top+25,max(0,round(cx-22)):min(256,round(cx+18))]=True;warm&=roi;closed=ndimage.binary_closing(warm,structure=np.ones((3,3)));lab,_=ndimage.label(closed);count=np.bincount(lab.ravel());count[0]=0;yy,xx=np.where(lab==int(count.argmax()));left=int(xx.min());pos=(left-3,top-11);box=(left-2,top,left+31,top+27)
 out=im.copy();out.paste((0,0,0,0),box);out.alpha_composite(shell,pos);mask=np.ones((256,256),bool);mask[pos[1]:top+28,pos[0]:left+31]=False;assert np.array_equal(a[mask],np.array(out)[mask]);checks+=1;f=F/f'{n:03}.png';out.save(f);bindings[f.relative_to(R).as_posix()]=sha(f);helmet.append(out);landmarks.append({'frame':n,'top':top,'headLeft':left,'helmetPosition':pos,'clearBox':box})
# Keep the full source clock here. Original selected520ms action entries are untouched.
holds=[round((n+1)*1000/24)-round(n*1000/24) for n in range(len(bare))]
for gear,ims in [('bare',bare),('helmet',helmet)]:
 states=[]
 for direction,order in [('unload',list(range(len(ims)))),('pickup',list(reversed(range(len(ims)))) )]:
  refs=['res://'+(P/f'frames/{gear}/{i:03}.png').relative_to(R).as_posix() for i in order];dur=[holds[i] for i in order];states.append({'id':'source-'+direction+'-west','frameFiles':refs,'frameDurationsMs':dur,'loop':False,'facings':['west']*len(refs),'waterKinds':[direction]*len(refs),'waterPoses':[False]*len(refs),'depthOffsets':[0.0]*len(refs)})
  frames=[ims[i] for i in order];frames[0].save(P/f'{gear}-{direction}-source.png',save_all=True,append_images=frames[1:],duration=dur,loop=0,disposal=0,blend=0)
  groups=[]
  for im,hold in zip(frames,dur):
   if groups and groups[-1][0].tobytes()==im.tobytes():groups[-1][1]+=hold
   else:groups.append([im,hold])
  ap=Image.open(P/f'{gear}-{direction}-source.png');assert ap.n_frames==len(groups)
  for i,(im,hold) in enumerate(groups):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes();assert ap.info['duration']==hold;checks+=2
 data={'name':'Veld West full source unload/reversed pickup '+gear,'status':'staged_source_clock_not_normal_action_timing_or_admission','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'states':states};f=P/f'{gear}-manifest.json';f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf8');bindings[f.relative_to(R).as_posix()]=sha(f)
 for i in range(len(ims)):f=P/f'frames/{gear}/{i:03}.png';bindings[f.relative_to(R).as_posix()]=sha(f)
for start in range(0,len(helmet),24):
 b=Image.new('RGB',(1536,760),'#202a30');d=ImageDraw.Draw(b)
 for j,im in enumerate(helmet[start:start+24]):
  x=(j%6)*256;y=(j//6)*185;top=landmarks[start+j]['top'];crop=im.crop((50,top-15,155,top+55)).resize((210,140),Image.Resampling.NEAREST);b.paste(crop,(x+20,y+24),crop);d.text((x+4,y+4),str(start+j),fill='white')
 b.save(P/f'helmet-chronology-{start//24:02}.png')
(P/'FAMILY_REVIEW.json').write_text(json.dumps({'checks':checks,'failures':0,'slotsPerState':len(bare),'durationMs':sum(holds),'pickupIsExactReversal':True,'bodyOutsideHelmetExactFrames':len(helmet),'helmetRotation':'Original rigid West shell remains upright and translates with source head; fit/neck visual review required.','landmarks':landmarks,'scope':'Full source clock 5917ms, selected520ms actions untouched. Viewer repetitions are replay only; not timed controller/gameplay/stride proof.','bindings':bindings},indent=2)+'\n',encoding='utf8');print({'checks':checks,'slots':len(bare),'durationMs':sum(holds)})
