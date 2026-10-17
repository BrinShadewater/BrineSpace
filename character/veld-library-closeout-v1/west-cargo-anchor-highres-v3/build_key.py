from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parents[2];src=Image.open(P/'source.png').convert('RGBA');a=np.array(src);lab,n=label(a[:,:,3]>8);counts=np.bincount(lab.ravel());keep=counts>=20;keep[0]=False;a[~keep[lab]]=0
opaque=a[:,:,3]>128;yy,xx=np.where(opaque);scale=147/(yy.max()-yy.min()+1);floor=int(yy.max());foot=opaque.copy();foot[:floor-round(45/scale)]=False;fy,fx=np.where(foot)
size=(round(src.width*scale),round(src.height*scale));offset=(148-round((int(fx.max())+1)*scale),223-round((floor+1)*scale))
scaled=Image.fromarray(a).resize(size,Image.Resampling.LANCZOS);im=Image.new('RGBA',(256,256));im.alpha_composite(scaled,offset);im.save(P/'bare.png')
master=Image.open(P.parent/'west-sample-family-v3/master-native.png').convert('RGBA');old=Image.open(R/'character/veld-unload-west-consistent-v1/frames/bare/000.png').convert('RGBA');metrics={}
for name,img in [('master',master),('candidate',im)]:
 aa=np.array(img);mask=aa[:,:,3]>128;y,x=np.where(mask);head=mask.copy();head[100:]=False;hy,hx=np.where(head);boot=mask.copy();boot[:206]=False;by,bx=np.where(boot)
 metrics[name]={'opaqueHeight':int(y.max()-y.min()+1),'floor':int(y.max()),'headTop':int(hy.min()),'headWidthAboveY100':int(hx.max()-hx.min()+1),'headLeft':int(hx.min()),'headAxis':float((hx.max()+hx.min())/2),'bootExtent':[int(bx.min()),int(bx.max())]}
board=Image.new('RGB',(768,670),'#202a30');d=ImageDraw.Draw(board)
for i,(name,img) in enumerate([('Original standing',master),('Installed cargo hold',old),('High-resolution master edit',im)]):
 board.paste(img,(i*256,30),img);d.text((i*256+5,5),name,fill='white');d.line((i*256,254,i*256+255,254),fill='#466570');crop=img.crop((90,60,170,155)).resize((160,190),Image.Resampling.NEAREST);board.paste(crop,(i*256+40,315),crop);feet=img.crop((95,195,155,225)).resize((180,90),Image.Resampling.NEAREST);board.paste(feet,(i*256+35,565),feet)
board.save(P/'comparison.png')
report={'sourceSha256':hashlib.sha256((P/'source.png').read_bytes()).hexdigest(),'sourceSize':src.size,'uniformScale':scale,'wholeKeyOffset':offset,'alphaThreshold':8,'componentMinPixels':20,'registration':'One whole authored key: source opaque span147px before Lanczos edge coverage, exported neutral148px height; near-boot heelright boundary148/floor224. No per-part/RGB adjustments. Source retained.','metrics':metrics,'scope':'Still authoring key only; no animated motion or normal admission.'};(P/'BUILD_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n');print(metrics)

# Reuse the same original rigid West shell; no new helmet design.
shellpath=R/'character/veld-helmet-original-turntable-west-v1/mixed-v5-study/shells/005.png';shell=Image.open(shellpath).convert('RGBA');bb=np.array(im);yy,xx=np.where(bb[:,:,3]>200);top=int(yy.min());hx=np.where(bb[top:top+16,:,3]>128)[1];left=int(hx.min());pos=(left-3,top-11);box=(left-2,top,left+31,top+27)
helmet=im.copy();helmet.paste((0,0,0,0),box);helmet.alpha_composite(shell,pos);helmet.save(P/'helmet.png');outside=np.ones((256,256),bool);outside[pos[1]:top+28,pos[0]:left+31]=False;assert np.array_equal(bb[outside],np.array(helmet)[outside])
assert metrics['candidate']['opaqueHeight']==148 and metrics['candidate']['floor']==223 and metrics['candidate']['headTop']==76 and metrics['candidate']['headWidthAboveY100']==27
for gear in ['bare','helmet']:
 ref='res://'+(P/f'{gear}.png').relative_to(R).as_posix();data={'name':'Veld high-resolution West standing cargo key '+gear,'status':'staged_single_key_not_gait_or_normal_admission','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'states':[{'id':'carry-west','frameFiles':[ref],'frameDurationsMs':[1000],'loop':False,'facings':['west'],'waterKinds':['carry'],'waterPoses':[False],'depthOffsets':[0.0]}]};(P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n')
board=Image.new('RGB',(1024,620),'#202a30');d=ImageDraw.Draw(board)
for i,(name,img) in enumerate([('Original standing',master),('New bare cargo key',im),('Original helmet',Image.open(R/'character/veld-idle-west-original-master-v1/blink-only-v2/helmet-original-reference.png').convert('RGBA')),('New helmet cargo key',helmet)]):
 board.paste(img,(i*256,30),img);d.text((i*256+4,5),name,fill='white');crop=img.crop((90,60,170,155)).resize((160,190),Image.Resampling.NEAREST);board.paste(crop,(i*256+40,315),crop)
board.save(P/'paired-comparison.png');report.update(checks=5,failures=0,helmetPosition=pos,helmetClearBox=box,bodyOutsideHelmetExact=True,headForwardShiftPixels=metrics['master']['headAxis']-metrics['candidate']['headAxis']);files=[Path(__file__),P/'source.png',P/'prompt.txt',P/'INPUTS.json',P/'master-right-crop.png',shellpath,P/'bare.png',P/'helmet.png',P/'bare-manifest.json',P/'helmet-manifest.json'];report['bindings']={x.relative_to(R).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in files};(P/'BUILD_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
