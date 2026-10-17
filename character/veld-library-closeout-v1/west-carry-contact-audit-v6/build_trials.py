from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
import numpy as np
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parents[2]
registration=json.loads((P.parent/'west-cargo-anchor-highres-v3/BUILD_REVIEW.json').read_text())
scale=registration['uniformScale'];offset=tuple(registration['wholeKeyOffset'])
control=Image.open(P.parent/'west-carry-master-match-v5/frames/bare/005.png').convert('RGBA')
shellpath=R/'character/veld-helmet-original-turntable-west-v1/mixed-v5-study/shells/005.png';shell=Image.open(shellpath).convert('RGBA')
rows=[];images=[control];bindings={}
for folder in [P,P/'retry']:
 if not (folder/'source.png').exists():continue
 src=Image.open(folder/'source.png').convert('RGBA')
 if list(src.size)!=registration['sourceSize']:
  rows.append({'trial':folder.relative_to(P).as_posix(),'sourceSize':src.size,'rejectedBeforePackaging':True,'reason':'Source canvas changed; whole stance boot still too far right on source review. No compensating rescale/registration applied.'})
  for name in ['source.png','prompt.txt']:
   path=folder/name;bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
  continue
 a=np.array(src);lab,_=label(a[:,:,3]>8);count=np.bincount(lab.ravel());keep=count>=20;keep[0]=False;a[~keep[lab]]=0
 small=Image.fromarray(a).resize((round(src.width*scale),round(src.height*scale)),Image.Resampling.LANCZOS)
 im=Image.new('RGBA',(256,256));im.alpha_composite(small,offset);im.save(folder/'bare.png');images.append(im)
 a=np.array(im);y,x=np.where(a[:,:,3]>128);top=int(y.min());hx=np.where(a[top:top+24,:,3]>128)[1];sy,sx=np.where(a[:,:,3]>200);st=int(sy.min());left=int(np.where(a[st:st+16,:,3]>128)[1].min());pos=(left-3,st-11);box=(left-2,st,left+31,st+27)
 out=im.copy();out.paste((0,0,0,0),box);out.alpha_composite(shell,pos);outside=np.ones((256,256),bool);outside[pos[1]:st+28,pos[0]:left+31]=False;assert np.array_equal(a[outside],np.array(out)[outside]);out.save(folder/'helmet.png')
 # Broad bottom window only valid after visual confirmation the far foot is flat.
 fy,fx=np.where(a[219:228,120:165,3]>128);assert len(fx)
 rows.append({'trial':folder.relative_to(P).as_posix(),'headTop':top,'headWidth':int(hx.max()-hx.min()+1),'headAxis':float((hx.min()+hx.max())/2),'floor':int(y.max()),'stanceHeelRightContourX':int(fx.max()+120),'bodyOutsideHelmetExact':True})
 for name in ['source.png','bare.png','helmet.png','prompt.txt']:
  path=folder/name;bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
board=Image.new('RGB',(len(images)*256,660),'#202a30');d=ImageDraw.Draw(board)
for i,im in enumerate(images):
 title='V5 retained pose' if i==0 else f'Trial {i}';d.text((i*256+5,6),title,fill='white');board.paste(im,(i*256,25),im);d.line((i*256,249,i*256+255,249),fill='#728792')
 crop=im.crop((85,190,170,230)).resize((255,120),Image.Resampling.NEAREST);board.paste(crop,(i*256,310),crop)
 for height,y in [(47,520),(93,640)]:
  s=height/148;small=im.resize((round(256*s),round(256*s)),Image.Resampling.LANCZOS);board.paste(small,(round(i*256+128-128*s),round(y-224*s)),small)
board.save(P/'trial-comparison.png')
(P/'TRIAL_REVIEW.json').write_text(json.dumps({'fixedUniformScale':scale,'fixedWholeOffset':offset,'noPerPoseRegistrationOrGrade':True,'rows':rows,'normalAdmission':False,'bindings':bindings},indent=2)+'\n',encoding='utf8')
print(json.dumps(rows))
