"""Representative native-size repair; preserve the actual body outside head/contact masks."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,math
H=Path(__file__).resolve().parent;R=H.parents[1];P=R/'character/krusher-animation-package-v8';read=lambda p:json.loads(p.read_text());idx=read(P/'package.json');(H/'pilot').mkdir(exist_ok=True)
fits={(q['state'],q['frame']):q for q in read(R/'character/krusher-james-motion-fit-v2/verification.json')['records']};canon={(q['state'],q['index']):q for q in read(R/'character/krusher-james-canonical-v9/revision.json')['records'] if q['gear']=='bare'}
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def neck(h):
 y,x=np.indices(h.shape[:2]);r,g,b=[h[:,:,k].astype(float) for k in range(3)];m=(h[:,:,3]>120)&(y>=h.shape[0]-5)&(r>g*1.055)&(r>b*1.09)&(r>60)
 yy,xx=np.where(m)
 if not len(xx):yy,xx=np.where((h[:,:,3]>120)&(y>=h.shape[0]-4))
 bottom=int(yy.max());xs=xx[yy>=bottom-2];return np.array([float(xs.mean()),float(bottom)])
jobs=[]
for d in ['south','east','north','west']:
 key='idle-'+d;c=canon[key,0];jobs.append({'state':key,'index':0,'direction':d,'oldHead':R/f'character/krusher-head-fit-v5/sources/clean-bare-{d}-native.png','paste':c['headPaste'],'original':R/fits[key,0]['source'],'axis':[0,1]})
for family,state,frame,d in [('repair-family-v5','kneel-east',1,'east'),('rest-family-v6','get-up-west',3,'west')]:
 root=R/('character/krusher-'+family);q=next(q for q in read(root/'revision.json')['records'] if q['gear']=='bare' and q['state']==state and q['frame']==frame);det=q['details'];jobs.append({'state':state,'index':frame,'direction':d,'oldHead':R/det['headSource'][6:],'paste':det['paste'],'original':R/q['originalBody'][6:],'axis':det.get('bodyAxis',[0,1]),'targetNeck':det.get('neck')})
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),19);board=Image.new('RGBA',(1200,len(jobs)*250),'#252d31');draw=ImageDraw.Draw(board);records=[]
for row,q in enumerate(jobs):
 mp=P/idx['states']['bare:'+q['state']]['manifest'];m=read(mp);s=next(s for s in m['states'] if s['id']==q['state']);a=arr(mp.parent/s['frameFiles'][q['index']]);original=arr(q['original']);old=Image.open(q['oldHead']).convert('RGBA');layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.alpha_composite(old,tuple(q['paste']));oldlayer=np.array(layer)
 visible=(oldlayer[:,:,3]>0)&np.all(a==oldlayer,2);clean=a.copy();clean[visible]=0
 head=Image.open(H/'sources'/('style-'+q['direction']+'-native.png')).convert('RGBA');new=np.array(head);oldneck=neck(np.array(old));target=np.array(q['targetNeck']) if q.get('targetNeck') else np.array(q['paste'])+oldneck;anchor=neck(new);paste=np.rint(target-anchor).astype(int)
 yy,xx=np.indices(a.shape[:2]);dx=xx-target[0];dy=yy-target[1];axis=np.array(q['axis']);projection=dx*axis[0]+dy*axis[1];cross=dx*axis[1]-dy*axis[0];contact=(projection>=-5)&(projection<=7)&(abs(cross)<=6)
 r,g,b=[original[:,:,k].astype(float) for k in range(3)];skin=(original[:,:,3]>120)&(r>g*1.09)&(r>b*1.15)&((r-g)>(g-b)*.65)&(r>32)
 restore=skin&contact;clean[restore]=original[restore]
 # Composite antialiased head over the body, then retain the real collar lip.
 layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.alpha_composite(head,tuple(paste));hn=np.array(layer);out=np.array(Image.alpha_composite(Image.fromarray(clean),layer));collar=contact&~skin&(original[:,:,3]>180)&(a[:,:,3]>180)&~visible
 out[collar]=a[collar];mask=visible|restore|(hn[:,:,3]>0);mask|=collar
 assert np.array_equal(a[~mask],out[~mask]);targetpath=H/'pilot'/f"{q['state']}-{q['index']:03d}.png";Image.fromarray(out).save(targetpath)
 cx,cy=target;box=(round(cx)-35,round(cy)-43,round(cx)+35,round(cy)+17);before=Image.fromarray(a).crop(box);after=Image.fromarray(out).crop(box);y=row*250+25;board.alpha_composite(before.resize((280,240),Image.Resampling.NEAREST),(10,y));board.alpha_composite(after.resize((280,240),Image.Resampling.NEAREST),(320,y));draw.text((10,y-23),q['state']+' / BEFORE',font=font,fill='white');draw.text((320,y-23),'NEW / same native density',font=font,fill='white')
 # Whole unchanged canvas at native size, alongside enlarged join diagnosis.
 board.alpha_composite(Image.fromarray(a),(650,y));board.alpha_composite(Image.fromarray(out),(900,y));draw.text((650,y-23),'native before',font=font,fill='white');draw.text((900,y-23),'native candidate',font=font,fill='white')
 records.append({'state':q['state'],'frame':q['index'],'source':str((mp.parent/s['frameFiles'][q['index']]).resolve().relative_to(R)),'originalBody':str(q['original'].relative_to(R)),'output':targetpath.relative_to(H).as_posix(),'oldPaste':q['paste'],'newPaste':paste.tolist(),'bodyNeckTarget':target.tolist(),'restoredOriginalSkinPixels':int(restore.sum()),'protectedBodyOutsideMaskExact':True})
board.save(H/'pilot-before-after.png');(H/'pilot-verification.json').write_text(json.dumps({'scope':'Six representative native pose candidates; no full-bank propagation or native admission','records':records},indent=2)+'\n');print(json.dumps({'pilotPoses':len(records),'protectedBodyChecks':len(records)}))
