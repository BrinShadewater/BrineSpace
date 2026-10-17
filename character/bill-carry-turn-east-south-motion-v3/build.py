from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation,binary_fill_holes
P=Path(__file__).resolve().parent;R=P.parents[1];f=json.loads((P/'frozen-bindings.json').read_text())
raws={g:np.array(Image.open(P/('sources/bare-v7.png' if g=='bare' else 'sources/helmet-components-v3.png')).convert('RGBA')) for g in ['bare','helmet']};bodies=[];heads=[];records=[]
yaw=np.array(Image.open(P/'sources/bare-v8.png').convert('RGBA'));assert yaw.shape==raws['bare'].shape
raws['bare'][:,768:1152]=yaw[:,768:1152]
# This independently regenerated strip changed source density. Calibrate once
# from its complete first figure, then retain the same ruler for every pose.
body_cal=raws['bare'][:,:384];labs,_=label(body_cal[:,:,3]>180);n=np.bincount(labs.ravel());n[0]=0;cy,cx=np.where(labs==n.argmax());body_height=int(cy.max()-cy.min()+1);scale=148/body_height
# Independent isolated-head sheet: one complete first-head calibration, shared
# by every angle. Never normalize individual helmets to fit their body pose.
master_head_paths=['character/bill-cargo-east-master-head-v1/sources/helmet-master-head.png','character/bill-cargo-south-master-head-v1/sources/helmet-master-head.png']
master_head_heights=[Image.open(R/file).height for file in master_head_paths];target_head_height=float(np.median(master_head_heights))
cal=raws['helmet'][:,:384];labs,_=label(cal[:,:,3]>180);n=np.bincount(labs.ravel());n[0]=0;cy,cx=np.where(labs==n.argmax());head_height=int(cy.max()-cy.min()+1);helmet_scale=target_head_height/head_height
for i in range(4):
 a=raws['bare'][:,i*384:(i+1)*384].copy();labs,_=label(a[:,:,3]>180);n=np.bincount(labs.ravel());n[0]=0;body=labs==n.argmax();y,x=np.indices(body.shape);by,bx=np.where(body);top=int(by.min());bottom=int(by.max());height=bottom-top+1
 assert top>10 and bottom<1010 and bx.min()>3 and bx.max()<380,'Unclipped complete source'
 assert abs(height*scale-148)<2,'Common ruler stature drift must remain below2native pixels'
 band=body&(y>top+height*.75)&(y<top+height*.88);ly,lx=np.where(band);axis=float((lx.min()+lx.max())/2);mask=binary_dilation(body,iterations=1)&(a[:,:,3]>80);a[~mask]=0;yy,xx=np.where(mask);box=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);aa=np.array(im);oy,ox=np.where(aa[:,:,3]>180);pos=[round(128-(axis-box[0])*scale),224-int(oy.max())];plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,tuple(pos));bodies.append(plane)
 h=raws['helmet'][:,i*384:(i+1)*384].copy();labs,_=label(h[:,:,3]>180);n=np.bincount(labs.ravel());n[0]=0;body=labs==n.argmax();hy,hx=np.where(body);htop=int(hy.min());cy,cx=np.where(body&(y<htop+12));haxis=float((cx.min()+cx.max())/2);mask=binary_dilation(body,iterations=1)&(h[:,:,3]>80);hy,hx=np.where(mask);hbox=[int(hx.min()),int(hy.min()),int(hx.max()+1),int(hy.max()+1)];assert hbox[0]>3 and hbox[2]<380 and hbox[1]>10 and hbox[3]<1010;h[~mask]=0;im=Image.fromarray(h).crop(hbox);im=im.resize((round(im.width*helmet_scale),round(im.height*helmet_scale)),Image.Resampling.LANCZOS);heads.append(im)
 records.append({'bodySource':'sources/bare-v8.png' if i==2 else 'sources/bare-v7.png','sourceCell':i,'frame':i+1,'scale':scale,'helmetScale':helmet_scale,'sourceBox':box,'opaqueSourceHeight':height,'axis':axis,'bodyPosition':pos,'helmetSourceBox':hbox,'helmetAxis':(haxis-hbox[0])*helmet_scale})
Y,X=np.indices((256,256));masters={g:[np.array(Image.open(R/f['endpoints'][g][d][6:]).convert('RGBA')) for d in ['east','south']] for g in ['bare','helmet']}
def material(a,kind,head=False):
 rgb=a[:,:,:3].astype(float);y,x=np.indices(a.shape[:2]);opaque=a[:,:,3]>180;top=int(np.where(opaque)[0].min());roi=opaque&(y<top+30) if head else opaque&(y<110)&(x>100)&(x<160)
 if kind=='skin':return roi&(rgb[:,:,0]>rgb[:,:,1]+12)&(rgb[:,:,0]>rgb[:,:,2]+15)&(rgb.mean(2)>70)
 if kind=='hair':return roi&(y<top+14)&(rgb[:,:,0]>rgb[:,:,2]*1.05)&(rgb.mean(2)<100)
 if kind=='burgundy':return opaque&(y>top+18)&(rgb[:,:,2]>rgb[:,:,1]*.85)&(rgb[:,:,0]>rgb[:,:,1]*1.5)&(rgb[:,:,0]>rgb[:,:,2]*1.35)&(rgb.mean(2)>30)
 if kind=='shell':return opaque&(rgb.max(2)-rgb.min(2)<25)&(y<top+45)&(True if head else (x>100)&(x<160))
 if kind=='visor':return roi&(rgb[:,:,2]>rgb[:,:,0]+15)&(rgb[:,:,2]>rgb[:,:,1]+8)
 return opaque&(rgb.max(2)-rgb.min(2)<25)&(True if head else y>110)
gains=json.loads((P/'sources/material-grade-skin-v9.json').read_text())['fixedGains']
case_fits=json.loads((P/'case-fit-diagnostic.json').read_text())['frames']
outputs={'bare':[],'helmet':[]}
for i in range(6):
 for gear in outputs:
  if i in [0,5]:out=Image.open(R/f['endpoints'][gear]['east' if i==0 else 'south'][6:]).convert('RGBA')
  else:
   a=np.array(bodies[i-1]);rgb=a[:,:,:3].astype(float)
   for k in ['fabric','burgundy','hair','skin']:
    mask=material(a,k);a[mask,:3]=np.clip(rgb[mask]*gains[k],0,255).astype('uint8')
   out=Image.fromarray(a)
   if i<4:
    casefit=case_fits[i-1];assert casefit['scale']==scale
    out.paste(Image.open(P/casefit['component']).convert('RGBA'),tuple(casefit['nativeFitBox'][:2]));a=np.array(out)
    records[i-1]['caseFit']=casefit
   if gear=='helmet':
    h=np.array(heads[i-1]);rgb=h[:,:,:3].astype(float)
    for k in ['shell','visor','sealed_skin']:
     mask=material(h,'skin' if k=='sealed_skin' else k,True);h[mask,:3]=np.clip(rgb[mask]*gains[k],0,255).astype('uint8')
    head=Image.fromarray(h);rgb=a[:,:,:3].astype(float);top=int(np.where(a[:,:,3]>180)[0].min());cy,cx=np.where((a[:,:,3]>180)&(Y<top+8));axis=float((cx.min()+cx.max())/2);warm=(a[:,:,3]>0)&(X>axis-20)&(X<axis+20)&(Y<top+32)&(rgb[:,:,0]>rgb[:,:,1]*1.035)&(rgb[:,:,0]>rgb[:,:,2]*1.05);erase=(binary_dilation(binary_fill_holes(warm),iterations=1)|((Y>=top-2)&(Y<top+14)))&(a[:,:,3]>0)&(X>axis-20)&(X<axis+20)&(Y>=top-2)&(Y<top+32);erase&=~((rgb.max(2)-rgb.min(2)<12)&(Y>=top+14));neck=int(np.where(warm&(a[:,:,3]>180))[0].max());hy,hx=np.where(h[:,:,3]>180);pos=[round(axis-records[i-1]['helmetAxis']),neck+5-int(hy.max())];base=a.copy();base[erase]=0;out=Image.fromarray(base);out.alpha_composite(head,tuple(pos));records[i-1]['helmetPosition']=pos;head.save(P/f'sources/component-helmet-{i:03}.png');Image.fromarray(erase.astype('uint8')*255).save(P/f'sources/erase-{i:03}.png')
  file=P/f'frames/{gear}/carry-turn-east-south/{i:03}.png';file.parent.mkdir(parents=True,exist_ok=True);out.save(file);outputs[gear].append('res://'+file.relative_to(R).as_posix())
for gear in outputs:
 original=json.loads((R/f['turn'][gear]['manifest']).read_text());m={k:v for k,v in original.items() if k!='states'};m.update(name='Bill East/South authored progressive whole pivot candidate',status='staged_visual_review',states=[])
 for key,files in [('carry-turn-east-south',outputs[gear]),('carry-turn-south-east',outputs[gear][::-1])]:
  s=copy.deepcopy(next(s for s in original['states'] if s['id']==key));s['frameFiles']=files;s['provenance']='New whole authored body/head progression;onecompletebare-v7bodyruler;onepooledmasterisolatedhelmetruler;exact current held endpoints;helmet component over identical new bare body;original800ms/reverse';m['states'].append(s)
 (P/('bare-manifest.json' if gear=='bare' else 'helmet-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
(P/'registration.json').write_text(json.dumps({'scale':scale,'ruler':'complete bare-v7 strip0 ->148native;one common body ruler;independent isolated helmet sheet uses one complete first-head ruler','bodyCalibration':{'source':'sources/bare-v7.png','cell':0,'opaqueSourceHeight':body_height,'targetNativeHeight':148,'scale':scale}, 'helmetCalibration':{'source':'sources/helmet-components-v3.png','cell':0,'opaqueSourceHeight':head_height,'targetNativeHeight':target_head_height,'scale':helmet_scale,'masterPaths':master_head_paths,'masterHeights':master_head_heights,'master':'fixed pooled median of exact current east/south complete helmet components'},'frames':records},indent=2)+'\n');(P/'material-grade.json').write_text(json.dumps({'fixedGains':gains,'scope':'Frozen pooled v7 gains with one shared bare skin correction from skin-v9 recipe;all4interiors same;never perpose exposure'},indent=2)+'\n')
board=Image.new('RGB',(1536,1024),(34,52,62));draw=ImageDraw.Draw(board)
for row,g in enumerate(outputs):
 for i,file in enumerate(outputs[g]):
  im=Image.open(R/file[6:]);board.paste(im,(i*256,row*512),im);crop=im.crop((96,65,166,135)).resize((210,210),Image.Resampling.NEAREST);board.paste(crop,(i*256,row*512+260),crop);draw.text((i*256+3,row*512+480),g+' phase'+str(i),fill='white')
board.save(P/'candidate-review.png');print('Staged progressive full-body quarter, paired12unique poses;unselected')
