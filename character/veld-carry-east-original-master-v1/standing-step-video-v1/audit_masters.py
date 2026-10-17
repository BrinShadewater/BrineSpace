"""Fixed-reference whole-clip master and endpoint diagnostics, never art repair."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2]
ref=Image.open(P/'registered-reference.png').convert('RGBA');master=Image.open(R/'character/veld-east-held-original-master-v1/frames/bare/000.png').convert('RGBA')
def metrics(im):
 a=np.array(im);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];axis=float((hx.min()+hx.max())/2);tx=np.where(a[top+34:top+79,:,3]>200)[1];left=round(axis-18.5);cloth=a[top+49:top+89,left:left+35];rgb=cloth[:,:,:3].astype(float);lum=rgb.mean(2);mask=(cloth[:,:,3]>200)&(np.ptp(rgb,axis=2)<18)&(lum>20)&(lum<160);assert mask.sum()>10,'Tracked diagnostic cloth region missing'
 return {'height':int(y.max()-y.min()+1),'headWidth':int(hx.max()-hx.min()+1),'headAxis':axis,'headTop':top,'floor':int(y.max()),'upperBodyWidth':int(tx.max()-tx.min()+1),'clothMedian':np.median(rgb[mask],axis=0).tolist(),'clothMaskPixels':int(mask.sum()),'clipped':bool(np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20))}
paths=sorted((P/'full-clip-frames').glob('*.png'));assert paths
frames=[Image.open(p).convert('RGBA') for p in paths];rows=[{'frame':i,**metrics(im)} for i,im in enumerate(frames)]
rm=np.array(ref)[:,:,3]>128
endpoint=[]
for n in [0,len(frames)-1]:
 a=np.array(frames[n]);m=a[:,:,3]>128;union=m|rm;inter=m&rm
 endpoint.append({'frame':n,'silhouetteIoU':float(inter.sum()/union.sum()),'intersectionRGBMAE':float(np.abs(a[:,:,:3].astype(float)-np.array(ref)[:,:,:3].astype(float))[inter].mean()),'scope':'Encoded-source appearance/pose diagnostic against fixed registered input, not exact endpoint admission or independent contact.'})
sheet=Image.new('RGB',(1536,640),(32,43,49));d=ImageDraw.Draw(sheet)
for i,(im,label) in enumerate([(master,'Original held'),(ref,'Registered unchanged source')]+[(frames[n],f'Video frame{n}') for n in [0,len(frames)//4,len(frames)//2,len(frames)-1]]):
 sheet.paste(im,(i*256,30),im);d.text((i*256+5,10),label,fill='white');crop=im.crop((100,75,166,163)).resize((198,264),Image.Resampling.NEAREST);sheet.paste(crop,(i*256+15,320),crop)
sheet.save(P/'master-endpoint-review.png')
report={'originalMaster':metrics(master),'registeredInput':metrics(ref),'rows':rows,'endpoints':endpoint,'ranges':{key:[min(r[key] for r in rows),max(r[key] for r in rows)] for key in ['height','headWidth','headAxis','headTop','floor','upperBodyWidth']},'scope':'Every extracted frame uses one input-frozen global ruler/offset. Cloth diagnostic sampling follows measured head-axis/top at constant master-relative offsets, without altering image pixels or source registration. Earlier fixed-viewport ROI became empty as figure moved, v0 preserved INVALID for materials. Master/material/endpoint/contact diagnostics only; no motion/native/ordinary integration acceptance. No colour/geometry normalization.','bindings':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'source.mp4',P/'input-record.json',P/'prompt.txt',Path(__file__)]}}
(P/'master-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k] for k in ['originalMaster','registeredInput','ranges','endpoints']}))
