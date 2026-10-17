from pathlib import Path
import json,hashlib,sys
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];version=int(sys.argv[1]) if len(sys.argv)>1 else 1;raw=P/f'raw-unload-v{version}.png';a=np.array(Image.open(raw).convert('RGBA'));labels,n=ndimage.label(a[:,:,3]>200);counts=np.bincount(labels.ravel());counts[0]=0
big=sorted(np.argsort(counts)[-6:],key=lambda k:float(np.where(labels==k)[1].mean()));centers=[float(np.where(labels==k)[1].mean()) for k in big];assert len(big)==6 and all(counts[k]>10000 for k in big)
boxes=[]
for k in big:
 y,x=np.where(labels==k);boxes.append([int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)])
first_h=boxes[0][3]-boxes[0][1];initial_h=round(a.shape[0]*148/first_h)
first_hi=round((boxes[0][2]+boxes[1][0])/2);first=Image.fromarray(a[:,:first_hi])
for adjust in [0,1,-1,2,-2,3,-3]:
 resize_h=initial_h+adjust;scale=resize_h/a.shape[0];test=np.array(first.resize((round(first.width*scale),resize_h),Image.Resampling.LANCZOS));ty,tx=np.where(test[:,:,3]>200)
 if int(ty.max()-ty.min()+1)==148:break
else:raise AssertionError('No common standing ruler')
# ONE atlas standing ruler and ONE floor offset. Independent columns only get whole horizontal registration.
rows=[];frames=[];floor_offset=None;board=Image.new('RGB',(1792,310),'#202a30');d=ImageDraw.Draw(board)
for i,k in enumerate(big):
 lo=0 if i==0 else round((boxes[i-1][2]+boxes[i][0])/2);hi=a.shape[1] if i==5 else round((boxes[i][2]+boxes[i+1][0])/2)
 cell=a[:,lo:hi].copy();im=Image.fromarray(cell).resize((round(cell.shape[1]*scale),resize_h),Image.Resampling.LANCZOS);z=np.array(im);mask=Image.fromarray((labels[:,lo:hi]==k).astype('uint8')*255).resize(im.size,Image.Resampling.NEAREST);m=np.array(mask)>128;ys,xs=np.where(m&(z[:,:,3]>200));top=int(ys.min());floor=int(ys.max());hx=np.where(z[top:top+16,:,3]>128)[1]
 # Sole landmarks from the connected figure, excluding the separate deposited case.
 cutoffs={1:[None,None,None,1360,1690,2026],2:[None,None,None,1290,1640,1990],3:[None,None,None,1320,1640,2015]}[version]
 right=cutoffs[i];bootmask=m.copy()
 if right is not None:bootmask[:,max(0,round((right-lo)*scale)):]=False
 fy,fx=np.where(bootmask&(z[:,:,3]>128)&(np.indices(m.shape)[0]>=floor-3));sole=(int(fx.min()),int(fx.max()));axis=(sole[0]+sole[1])/2
 if floor_offset is None:floor_offset=224-floor
 offset=(round(128-axis),floor_offset);out=Image.new('RGBA',(256,256));out.alpha_composite(im,offset);dest=P/f'diagnostic-frames-v{version}'/f'{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest);frames.append(out)
 rows.append({'pose':i,'bodyHeight':floor-top+1,'headRegionWidth':int(hx.max()-hx.min()+1),'soleSpan':sole[1]-sole[0]+1,'registeredBodyFloor':floor+floor_offset,'offset':offset,'sourceCell':[lo,0,hi,a.shape[0]],'bodySourceBox':boxes[i],'sourceFloorCaseExcludedAtX':right})
 board.paste(out,(i*256,25),out);d.text((i*256+4,4),'whole unload '+str(i),fill='white')
master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(R/'character/veld-side-foundation-v1/east-standing.png').convert('RGBA'),(36,52));board.paste(master,(1536,25),master);d.text((1540,4),'true original East empty',fill='white')
board.save(P/f'source-master-comparison-v{version}.png');(P/f'source-registration-v{version}.json').write_text(json.dumps({'sourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'sourceScale':scale,'commonFloorOffset':floor_offset,'soleContactMethod':'Bottom3 rows of complete figure, manually exclude floor case by reviewed global sourceX cutoff; diagnostic, individual boot/contact proof still required','rows':rows,'postGenerationRGBChanged':False,'status':'diagnostic; floor/boot/case/anatomy/material review before packaging'},indent=2)+'\n',encoding='utf-8');print(json.dumps({'scale':scale,'rows':rows}))
