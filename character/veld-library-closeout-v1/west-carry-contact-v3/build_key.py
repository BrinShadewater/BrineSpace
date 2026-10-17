from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label

P=Path(__file__).resolve().parent
R=P.parents[2]
anchor=P.parent/'west-cargo-anchor-highres-v3'
registration=json.loads((anchor/'BUILD_REVIEW.json').read_text())
scale=registration['uniformScale']; offset=registration['wholeKeyOffset']
source=Image.open(P/'source.png').convert('RGBA')
assert list(source.size)==registration['sourceSize'], 'New canvas requires explicit registration review'
a=np.array(source);lab,_=label(a[:,:,3]>8);counts=np.bincount(lab.ravel());keep=counts>=20;keep[0]=False;a[~keep[lab]]=0
scaled=Image.fromarray(a).resize((round(source.width*scale),round(source.height*scale)),Image.Resampling.LANCZOS)
candidate=Image.new('RGBA',(256,256));candidate.alpha_composite(scaled,tuple(offset));candidate.save(P/'bare.png')
shellpath=R/'character/veld-helmet-original-turntable-west-v1/mixed-v5-study/shells/005.png'
shell=Image.open(shellpath).convert('RGBA');bb=np.array(candidate);yy,xx=np.where(bb[:,:,3]>200);top=int(yy.min());hx=np.where(bb[top:top+16,:,3]>128)[1];left=int(hx.min());pos=(left-3,top-11);box=(left-2,top,left+31,top+27)
helmet=candidate.copy();helmet.paste((0,0,0,0),box);helmet.alpha_composite(shell,pos);helmet.save(P/'helmet.png')
outside=np.ones((256,256),bool);outside[pos[1]:top+28,pos[0]:left+31]=False;assert np.array_equal(bb[outside],np.array(helmet)[outside])
control=Image.open(anchor/'bare.png').convert('RGBA')
master=Image.open(P.parent/'west-sample-family-v3/master-native.png').convert('RGBA')
old=Image.open(R/'character/veld-carry-west-consistent-v1/frames/bare/000.png').convert('RGBA')
def metrics(im):
 a=np.array(im);mask=a[:,:,3]>128;y,x=np.where(mask);head=mask.copy();head[100:]=False;hy,hx=np.where(head);boot=mask.copy();boot[:206]=False;by,bx=np.where(boot)
 return {'height':int(y.max()-y.min()+1),'floor':int(y.max()),'headTop':int(hy.min()),'headWidth':int(hx.max()-hx.min()+1),'headAxis':float((hx.max()+hx.min())/2),'bootExtent':[int(bx.min()),int(bx.max())]}
board=Image.new('RGB',(1024,790),'#202a30');d=ImageDraw.Draw(board)
for j,(title,im) in enumerate([('Original standing',master),('Matched cargo control',control),('Authored contact',candidate),('Installed carry contact',old)]):
 d.text((j*256+4,5),title,fill='white');board.paste(im,(j*256,20),im);d.line((j*256,244,j*256+255,244),fill='#728792')
 for h,y in [(47,385),(93,520),(148,735)]:
  s=h/148;small=im.resize((round(256*s),round(256*s)),Image.Resampling.LANCZOS);x=round(j*256+128-128*s);top=round(y-224*s);board.paste(small,(x,top),small);d.line((j*256,y,j*256+255,y),fill='#728792')
board.save(P/'comparison.png')
paired=Image.new('RGB',(1024,620),'#202a30');pd=ImageDraw.Draw(paired)
for j,(title,im) in enumerate([('Bare cargo control',control),('Bare contact key',candidate),('Helmet cargo control',Image.open(anchor/'helmet.png').convert('RGBA')),('Helmet contact key',helmet)]):
 pd.text((j*256+4,5),title,fill='white');paired.paste(im,(j*256,20),im);crop=im.crop((90,60,170,160)).resize((160,200),Image.Resampling.NEAREST);paired.paste(crop,(j*256+45,315),crop)
paired.save(P/'paired-comparison.png')
files=[Path(__file__),P/'source.png',P/'prompt.txt',P/'INPUTS.json',anchor/'BUILD_REVIEW.json',anchor/'bare.png',P/'bare.png',P/'helmet.png',shellpath]
report={'scope':'One authored near-leg-leading contact key, not a complete gait, opposite-contact success or normal admission','fixedMasterUniformScale':scale,'fixedMasterWholeOffset':offset,'noPoseSpecificRegistrationChange':True,'alphaThreshold':8,'componentMinPixels':20,'sourceSize':source.size,'metrics':{'control':metrics(control),'candidate':metrics(candidate),'originalStanding':metrics(master)},'bindings':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
report.update(bodyOutsideHelmetExact=True,helmetPosition=pos,helmetClearBox=box)
(P/'BUILD_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8');print(json.dumps(report['metrics']))
