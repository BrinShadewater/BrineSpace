"""One whole-video standing ruler; all poses share one resample and offset."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;S=P.parent;R=S.parents[2]
masterpath=R/'character/veld-east-held-original-master-v1/frames/bare/000.png';master=Image.open(masterpath).convert('RGBA')
rawfiles=sorted((S/'raw-review').glob('raw-*.png'));assert len(rawfiles)==142
def extract(file):
 rgb=np.array(Image.open(file).convert('RGB'));v=rgb.astype(int);white=(v.min(2)>=238)&(np.ptp(v,axis=2)<12)
 labels,k=ndimage.label(~white);counts=np.bincount(labels.ravel());counts[0]=0;mask=ndimage.binary_erosion(labels==int(counts.argmax()),iterations=1)
 rgba=np.dstack((rgb,mask.astype('uint8')*255));rgba[~mask]=0;return Image.fromarray(rgba)
first=extract(rawfiles[0]);a=np.array(first);y,x=np.where(a[:,:,3]>200);estimate=round(first.height*148/(y.max()-y.min()+1))
for delta in [0,1,-1,2,-2,3,-3]:
 h=estimate+delta;size=(round(first.width*h/first.height),h);image=first.resize(size,Image.Resampling.LANCZOS);a=np.array(image);y,x=np.where(a[:,:,3]>200)
 if y.max()-y.min()+1==148:break
else:raise AssertionError('No single global148 standing ruler')
top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];offset=(round(123.5-(hx.min()+hx.max())/2),223-int(y.max()))
def metrics(image):
 a=np.array(image);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];tx=np.where(a[top+34:top+79,:,3]>200)[1]
 cloth=a[top+49:top+89,105:140];rgb=cloth[:,:,:3].astype(float);m=(cloth[:,:,3]>200)&(np.ptp(rgb,axis=2)<18)&(rgb.mean(2)>20)&(rgb.mean(2)<160)
 return {'height':int(y.max()-y.min()+1),'headWidth':int(hx.max()-hx.min()+1),'headTop':top,'headAxis':float((hx.min()+hx.max())/2),'floor':int(y.max()),'upperBodyWidth':int(tx.max()-tx.min()+1),'clothMedian':np.median(rgb[m],axis=0).tolist(),'clipped':bool(np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20))}
rows=[];files=[]
for n,file in enumerate(rawfiles):
 source=extract(file);assert source.size==first.size
 image=source.resize(size,Image.Resampling.LANCZOS);out=Image.new('RGBA',(256,256));out.alpha_composite(image,offset)
 dest=P/'frames'/f'{n:03}.png';dest.parent.mkdir(exist_ok=True);out.save(dest);files.append(dest);rows.append({'frame':n,**metrics(out)})
report={'sourceTaskId':'448578329612795','sourceVideoSHA256':hashlib.sha256((S/'source.mp4').read_bytes()).hexdigest(),'rawFrameCount':len(files),'firstRawOpaqueHeight':int(np.where(np.array(first)[:,:,3]>200)[0].max()-np.where(np.array(first)[:,:,3]>200)[0].min()+1),'wholeResampledPlateSize':list(size),'scale':h/first.height,'fixedOffset':list(offset),'master':metrics(master),'rows':rows,'ranges':{key:[min(r[key] for r in rows),max(r[key] for r in rows)] for key in ['height','headWidth','headTop','headAxis','floor','upperBodyWidth']},'scope':'Alternative ONE global source ruler calibrated from encoded first standing frame to original148. Applied unchanged to ALL142whole raw frames, same alpha extraction. No per-frame/region scale, RGB grading, anatomical repair, position correction or pose deletion. Original input-frozen1/3 result preserved separately. This corrects a shared source-density discrepancy, cannot establish physical foot support/master art/standing joins.'}
(P/'source-registration.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1536,800),(32,43,49));d=ImageDraw.Draw(board)
images=[(master,'Original master'),(Image.open(S/'full-clip-frames/000.png').convert('RGBA'),'Prior fixed input ruler')]+[(Image.open(files[n]).convert('RGBA'),f'Global ruler raw{n}') for n in [0,36,53,141]]
for j,(im,label) in enumerate(images):
 board.paste(im,(j*256,30),im);d.text((j*256+3,8),label,fill='white');crop=im.crop((98,70,170,165)).resize((216,285),Image.Resampling.NEAREST);board.paste(crop,(j*256+5,330),crop)
board.save(P/'master-ruler-comparison.png')
print(json.dumps({'first':rows[0],'last':rows[-1],'ranges':report['ranges'],'scale':report['scale'],'offset':offset}))
