"""Complete atlas extraction with a single standing-cell ruler; no art repairs."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent; A=P.parent; R=A.parents[1]
rawpath=P/'raw-cycle-repair-v1.png'; raw=Image.open(rawpath).convert('RGBA')
masterpath=R/'character/veld-east-held-original-master-v1/frames/bare/000.png'
master=Image.open(masterpath).convert('RGBA')
cells=[raw.crop((round(i%7*raw.width/7),round(i//7*raw.height/6),round((i%7+1)*raw.width/7),round((i//7+1)*raw.height/6))) for i in range(42)]
# Rectangular returned canvas rounded at grid boundaries; shared target plate dimensions.
def bodymask(a):
 l,k=ndimage.label(a[:,:,3]>200); counts=np.bincount(l.ravel());counts[0]=0;return l==int(counts.argmax())
cal=np.array(cells[38]); yy=np.where(bodymask(cal))[0]; estimate=round(cells[38].height*148/(yy.max()-yy.min()+1))
for delta in [0,1,-1,2,-2,3,-3]:
 h=estimate+delta; size=(h,h); ref=cells[38].resize(size,Image.Resampling.LANCZOS); ar=np.array(ref); y,x=np.where(bodymask(ar))
 if y.max()-y.min()+1==148:break
else:raise AssertionError('No common standing148 ruler')
top=int(y.min()); hx=np.where(ar[top:top+16,:,3]>128)[1]; offset=(round(123.5-(hx.min()+hx.max())/2),223-int(y.max()))
def metrics(im):
 a=np.array(im); bm=bodymask(a); y,x=np.where(bm); top=int(y.min()); hx=np.where(a[top:top+16,:,3]>128)[1]; tx=np.where(bm[top+34:top+79])[1]
 cloth=a[top+49:top+89,105:140]; rgb=cloth[:,:,:3].astype(float); m=(cloth[:,:,3]>200)&(np.ptp(rgb,axis=2)<18)&(rgb.mean(2)>20)&(rgb.mean(2)<160)
 mask=a[:,:,3]>128; edge=mask&~ndimage.binary_erosion(mask,iterations=2); v=a[:,:,:3].astype(int)
 colored=(np.ptp(v,axis=2)>85)&(v.max(2)>130)&edge
 return dict(height=int(y.max()-y.min()+1),headWidth=int(hx.max()-hx.min()+1),headTop=top,headAxis=float((hx.min()+hx.max())/2),floor=int(y.max()),upperBodyWidth=int(tx.max()-tx.min()+1),clothMedian=np.median(rgb[m],axis=0).tolist(),saturatedEdgePixels=int(colored.sum()))
frames=[]; rows=[]; bindings={}; sources=[]
for i in range(39):
 out=Image.new('RGBA',(256,256));out.alpha_composite(cells[i].resize(size,Image.Resampling.LANCZOS),offset)
 dest=P/'frames'/f'{i:03}.png'; dest.parent.mkdir(exist_ok=True);out.save(dest);frames.append(out)
 sourcepath=A/'standing-step-video-v2-native/global-standing-ruler-v1/frames'/f'{i+16:03}.png' if i<38 else masterpath
 source=Image.open(sourcepath).convert('RGBA'); sources.append(source); bindings[sourcepath.relative_to(R).as_posix()]=hashlib.sha256(sourcepath.read_bytes()).hexdigest()
 sm=np.array(source)[:,:,3]>128;om=np.array(out)[:,:,3]>128
 lowerIoU=float((sm[165:]&om[165:]).sum()/max(1,(sm[165:]|om[165:]).sum()))
 rows.append(dict(cell=i,sourceRawSlot=i+16 if i<38 else None,source=metrics(source),returned=metrics(out),lowerSilhouetteIoU=lowerIoU))
for page in range(3):
 start=page*13; board=Image.new('RGB',(768,13*280),(32,43,49));d=ImageDraw.Draw(board)
 for j in range(13):
  i=start+j
  for col,(im,label) in enumerate([(sources[i],f'Input cell{i}'),(frames[i],f'Returned cell{i}'),(master,'Original standing master')]):
   d.text((col*256+5,j*280+3),label,fill='white');board.paste(im,(col*256,j*280+20),im)
 board.save(P/f'full-comparison-{page+1}.png')
board=Image.new('RGB',(1536,700),(32,43,49));d=ImageDraw.Draw(board)
for j,(im,label) in enumerate([(master,'Original'),(frames[38],'Returned master'),(frames[0],'Returned0'),(frames[9],'Returned9'),(frames[18],'Returned18'),(frames[28],'Returned28')]):
 d.text((j*256+3,5),label,fill='white');board.paste(im,(j*256,25),im)
 crop=im.crop((98,70,170,165)).resize((216,285),Image.Resampling.NEAREST);board.paste(crop,(j*256+5,330),crop)
board.save(P/'master-detail-comparison.png')
blank=[int((np.array(cells[i])[:,:,3]>20).sum()) for i in [39,40,41]]
report=dict(rawSize=list(raw.size),grid=[7,6],occupiedCells=39,blankCellsOpaquePixels=blank,commonCellPlate=list(size),fixedOffset=list(offset),master=metrics(master),rows=rows,ranges={k:[min(r['returned'][k] for r in rows[:38]),max(r['returned'][k] for r in rows[:38])] for k in ['height','headWidth','headTop','headAxis','floor','upperBodyWidth','saturatedEdgePixels']},bindings=bindings,rawSHA256=hashlib.sha256(rawpath.read_bytes()).hexdigest(),scope='All38 motion cells and standing calibration extracted in order. Largest-component mask for MEASUREMENT ONLY prevents adjacent-row boot fragments contaminating ruler; ALL returned pixels retained in extracted artwork. One common standing148 ruler and common offset; fractional grid boundaries round to nearest pixel. No per-cell density, registration, region grading, anatomical edits or contact repair. Shape IoU and ROI grades are diagnostics, not semantic certification. V0 audit invalid because stray neighbour fragments contaminated the calibration and head/floor measurements.')
(P/'AUDIT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['rawSize','blankCellsOpaquePixels','commonCellPlate','fixedOffset','master','ranges']}))
print('Returned master:',rows[38]['returned'],'minimum lower IoU:',min(r['lowerSilhouetteIoU'] for r in rows[:38]))
