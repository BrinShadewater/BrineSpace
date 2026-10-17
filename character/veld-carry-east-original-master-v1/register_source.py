from pathlib import Path
import sys,json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];version=sys.argv[1];raw=P/f'raw-gait-v{version}.png';original=Image.open(raw).convert('RGBA');cells=[];bounds=[];cols,grid_rows=(4,3) if version=='1' else (6,1)
if version!='1':
 whole=np.array(original);labels,n=ndimage.label(whole[:,:,3]>200);sizes=np.bincount(labels.ravel());sizes[0]=0;keys=sorted(np.argsort(sizes)[-6:],key=lambda k:np.where(labels==k)[1].mean());complete=[]
 for k in keys:
  yy,xx=np.where(labels==k);complete.append([int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)])
for row in range(grid_rows):
 for col in range(cols):
  box=(round(col*original.width/cols),round(row*original.height/grid_rows),round((col+1)*original.width/cols),round((row+1)*original.height/grid_rows)) if version=='1' else (0 if col==0 else round((complete[col-1][2]+complete[col][0])/2),0,original.width if col==5 else round((complete[col][2]+complete[col+1][0])/2),original.height)
  a=np.array(original.crop(box));labels,n=ndimage.label(a[:,:,3]>200);sizes=np.bincount(labels.ravel());sizes[0]=0;keep=np.isin(labels,np.where(sizes>=50)[0]);a[~ndimage.binary_dilation(keep,iterations=3)]=0;cells.append(Image.fromarray(a));bounds.append(box)
first=np.array(cells[0]);y,x=np.where(first[:,:,3]>200);estimate=round(cells[0].height*148/(y.max()-y.min()+1))
for delta in [0,1,-1,2,-2,3,-3]:
 h=estimate+delta;scale=h/cells[0].height;test=cells[0].resize((round(cells[0].width*scale),h),Image.Resampling.LANCZOS);y,x=np.where(np.array(test)[:,:,3]>200)
 if int(y.max()-y.min()+1)==148:break
else:raise AssertionError('No common original148 standing ruler')
common_y=223-int(y.max());master=Image.open(R/'character/veld-east-held-original-master-v1/frames/bare/000.png').convert('RGBA');m=np.array(master);my,mx=np.where(m[:,:,3]>200);mh=np.where(m[int(my.min()):int(my.min())+16,:,3]>128)[1];target_head=(mh.min()+mh.max())/2;rows=[];board=Image.new('RGB',((cols+1)*256,grid_rows*300+50),'#202a30');d=ImageDraw.Draw(board)
for i,cell in enumerate(cells):
 im=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS);a=np.array(im);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];offset=(round(target_head-(hx.min()+hx.max())/2),common_y);out=Image.new('RGBA',(256,256));out.alpha_composite(im,offset);path=P/f'diagnostic-frames-v{version}/{i:03}.png';path.parent.mkdir(exist_ok=True);out.save(path);z=np.array(out);yy,xx=np.where(z[:,:,3]>200);sole_y=int(yy.max());sy,sx=np.where(z[sole_y-1:sole_y+1,:,3]>200);near_mean=float(sx.mean());clip=int(np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20));rows.append({'pose':i,'height':int(yy.max()-yy.min()+1),'headRegionWidth':int(hx.max()-hx.min()+1),'floor':sole_y,'soleBottomMeanX':near_mean,'soleBottomBoundsX':[int(sx.min()),int(sx.max()+1)],'cell':list(bounds[i]),'offset':list(offset),'clipped':bool(clip)})
 board.paste(out,((i%cols)*256,(i//cols)*300+20),out);d.text(((i%cols)*256+4,(i//cols)*300+3),f'{i} H{rows[-1]["height"]} head{rows[-1]["headRegionWidth"]} floor{sole_y}',fill='white')
board.paste(master,(cols*256,20),master);d.text((cols*256+4,3),'exact held master',fill='white');board.save(P/f'source-master-review-v{version}.png')
report={'rawSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'sourceSize':list(original.size),'grid':[cols,grid_rows],'sourceScale':scale,'commonYOffset':common_y,'targetHeadCenterX':float(target_head),'rows':rows,'clippingCount':sum(r['clipped'] for r in rows),'headWidths':[r['headRegionWidth'] for r in rows],'heights':[r['height'] for r in rows],'floorSpan':max(r['floor'] for r in rows)-min(r['floor'] for r in rows),'scope':'Complete fixed-grid cells, ONE actual first-pose148ruler/sharedY, wholeX registration to head axis. Diagnostic sources only; identity/case/stride/anatomical contacts/native acceptance separate.'};(P/f'source-registration-v{version}.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='rows'}))
