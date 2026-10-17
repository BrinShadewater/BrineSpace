from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;R=P.parents[2]
src=R/'character/veld-library-closeout-v1/west-kneel-anchor-v1/native.png'
master=R/'character/veld-library-closeout-v1/west-sample-family-v1/master-native.png'
im=Image.open(src).convert('RGBA');fr=Image.new('RGBA',(256,256));fr.paste(im,(18,5));fr.save(P/'bare.png')
a=np.array(im);b=np.array(fr)
assert np.array_equal(a[:251,:238],b[5:,18:])
assert not np.any(a[251:,:,3]) and not np.any(a[:,238:,3])
shellpath=R/'character/veld-helmet-original-turntable-west-v1/mixed-v5-study/shells/005.png'
shell=Image.open(shellpath).convert('RGBA');y,x=np.where(b[:,:,3]>200);top=int(y.min());hx=np.where(b[top:top+16,:,3]>128)[1];left=int(hx.min())
pos=(left-3,top-11);box=(left-2,top,left+31,top+27)
helmet=fr.copy();helmet.paste((0,0,0,0),box);helmet.alpha_composite(shell,pos);helmet.save(P/'helmet.png')
mask=np.ones((256,256),bool);mask[pos[1]:top+28,pos[0]:left+31]=False
assert np.array_equal(b[mask],np.array(helmet)[mask])
for gear in ['bare','helmet']:
 ref='res://'+(P/f'{gear}.png').relative_to(R).as_posix()
 data={'name':'Veld one registered West kneel key '+gear,'status':'staged_single_key_not_motion_or_normal_admission','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'states':[{'id':'kneel-west','frameFiles':[ref],'frameDurationsMs':[1000],'loop':False,'facings':['west'],'waterKinds':['repair'],'waterPoses':[False],'depthOffsets':[0.0]}]}
 (P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n')
paths=[Path(__file__),src,master,shellpath,P/'bare.png',P/'helmet.png',P/'bare-manifest.json',P/'helmet-manifest.json']
report={'mapping':'One whole key integer translation18right5down at existing native256 density; all RGBA in retained window exact, no visible pixels clipped. Fixed authoring registration, no anatomy/visible RGB/rescale edits or frame-by-frame correction.','authority':'skills/brinespace-character-pipeline/references/master-repair.md: register each by same planted boot, not changing full-body box.','registration':[18,5],'checks':3,'failures':0,'top':top,'floor':int(y.max()),'headWidth':int(hx.max()-hx.min()+1),'headAxis':float((hx.min()+hx.max())/2),'helmetPosition':pos,'helmetClearBox':box,'bindings':{x.relative_to(R).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in paths},'scope':'One fixed authored key, not accepted animated lowering/rising or physical pressure/contact proof.'}
(P/'BUILD_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
board=Image.new('RGB',(1024,580),'#202a30');d=ImageDraw.Draw(board)
for j,(label,img) in enumerate([('Original standing',Image.open(master).convert('RGBA')),('Unregistered key',im),('Registered key',fr),('Helmet key',helmet)]):
 board.paste(img,(j*256,24),img);d.text((j*256+4,4),label,fill='white')
 crop=img.crop((95,195,192,229)).resize((256,90),Image.Resampling.NEAREST);board.paste(crop,(j*256,360),crop)
 d.line((j*256+95,247,j*256+190,247),fill='#718f9b')
board.save(P/'comparison.png')
print({k:report[k] for k in ['registration','top','floor','headWidth','headAxis','checks']})
