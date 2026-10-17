from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parent.parent
cases=[('master',R/'character/bill-video-south-v1/master-source.png',(350,50,680,180),(375,375,490,490)),('old-squat',P/'sources/rising-squat-v1.png',(350,180,680,320),(375,520,490,650)),('old-nearstand',P/'sources/near-standing-v1.png',(350,40,680,180),(370,405,490,540)),('new-squat',P/'sources/rising-squat-matte-v6.png',(350,270,680,390),(375,590,490,720)),('new-nearstand',P/'sources/near-standing-master-v3.png',(350,40,680,180),(370,375,490,510))]
rows=[]
for name,path,hair_roi,red_roi in cases:
 a=np.array(Image.open(path).convert('RGBA'));rgb=a[:,:,:3].astype(float);yy,xx=np.indices(a.shape[:2]);row=dict(source=name,file=path.relative_to(R).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
 for key,roi in [('hair',hair_roi),('redUnit',red_roi)]:
  x0,y0,x1,y1=roi;region=(a[:,:,3]>180)&(xx>=x0)&(xx<x1)&(yy>=y0)&(yy<y1)
  semantic=(rgb[:,:,0]>rgb[:,:,1]*1.2)&(rgb[:,:,1]>rgb[:,:,2]*1.3)&(np.ptp(rgb,axis=2)>35) if key=='hair' else (rgb[:,:,0]>rgb[:,:,1]*1.25)&(rgb[:,:,0]>rgb[:,:,2]*1.25)&(rgb[:,:,0]-rgb[:,:,1]>25)
  labs,n=label(region&semantic);c=np.bincount(labs.ravel());c[0]=0;y,x=np.where(labs==c.argmax());row[key]=dict(roi=roi,bounds=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],width=int(x.max()-x.min()+1),height=int(y.max()-y.min()+1),pixels=len(x),touchesROIEdge=bool(x.min()==x0 or x.max()==x1-1 or y.min()==y0 or y.max()==y1-1))
 neutral=(a[:,:,3]>200)&(xx>=250)&(xx<780)&(yy>=450)&(yy<1120)&(np.ptp(rgb,axis=2)<18)&(rgb.mean(axis=2)>20)&(rgb.mean(axis=2)<150);row['neutralBodyDiagnosticMedian']=float(np.median(rgb.mean(axis=2)[neutral]));rows.append(row)
review=dict(rows=rows,scope='Bounded semantic hair/red-unit diagnostics, not full hair shape/head/camera/segment or material proof. ROI-edge flags expose clipped connected components; hair height invalid when clipped. Fixed whole-source density148/1295 retained, no per-pose fit.')
(P/'anatomy-audit.json').write_text(json.dumps(review,indent=2)+'\n');board=Image.new('RGB',(1920,760),'#182932');d=ImageDraw.Draw(board)
for col,(gear,pose) in enumerate([('bare',5),('bare',6)]):
 for row,folder in enumerate([P.with_name('bill-water-exit-south-v3'),P]):
  im=Image.open(folder/f'{gear}/frames/swim-land-south/{pose:03}.png').convert('RGBA');x=col*640+row*320;board.paste(im,(x,25),im);d.text((x+5,5),f'pose{pose} '+('before' if row==0 else 'revised'),fill='white')
# Original master at fixed original density, same foot row; selected idle exact.
master=Image.open(cases[0][1]).convert('RGBA');scale=148/1295;im=master.resize((round(master.width*scale),round(master.height*scale)),Image.Resampling.LANCZOS);board.paste(im,(1280+160-round(512*scale),25+224-round(1375*scale)),im);d.text((1285,5),'original master at density',fill='white')
im=Image.open(P/'bare/frames/swim-land-south/007.png').convert('RGBA');board.paste(im,(1600,25),im);d.text((1605,5),'selected idle',fill='white')
# Bottom row repeats same shared canvases2x crops; no per-figure fit.
for i in range(6):
 crop=board.crop((i*320+95,25+60,i*320+225,25+240)).resize((260,360),Image.Resampling.NEAREST);board.paste(crop,(i*320+30,390))
board.save(P/'master-comparison.png');print(json.dumps([dict(source=x['source'],hairWidth=x['hair']['width'],redWidth=x['redUnit']['width'],neutralMedian=x['neutralBodyDiagnosticMedian']) for x in rows]))
