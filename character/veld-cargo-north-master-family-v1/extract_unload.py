"""Single standing source ruler, whole bodies, physical boot contact; diagnostics only."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.ndimage import label,binary_dilation,find_objects
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];rawpath=P/'raw-unload-v1.png';raw=Image.open(rawpath).convert('RGBA');a=np.array(raw)
occupied=(a[:,:,3]>200).any(0);bounds=[0]
for i in range(1,6):
 nominal=round(i*raw.width/6);lo=max(0,nominal-45);hi=min(raw.width,nominal+46);possible=np.where(~occupied[lo:hi])[0]+lo;assert len(possible),('No gutter',i);bounds.append(int(possible[np.argmin(abs(possible-nominal))]))
bounds.append(raw.width);cells=[a[:,bounds[i]:bounds[i+1]].copy() for i in range(6)]
ys,xs=np.where(cells[0][:,:,3]>200);scale=148/(ys.max()-ys.min()+1);O=P/'ungraded-unload';O.mkdir(exist_ok=True);rows=[];board=Image.new('RGB',(1536,860),'#202a30');d=ImageDraw.Draw(board)
for i,cell in enumerate(cells):
 labels,n=label(cell[:,:,3]>200);sizes=np.bincount(labels.ravel());sizes[0]=0;bodyid=int(sizes.argmax());body=labels==bodyid;yy,xx=np.where(body);floor=int(yy.max())
 footmask=body[max(0,floor-7):floor+1].copy()
 # North case projects between/farther than boots; boot bottom remains body contact.
 by,bx=np.where(footmask);center=(bx.min()+bx.max())/2
 clean=cell.copy();clean[~binary_dilation(body,iterations=2)]=0
 offset=(round(128-center*scale),round(224-floor*scale));im=Image.fromarray(clean);frame=Image.new('RGBA',(256,256));frame.alpha_composite(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS),offset);frame.save(O/f'{i:03}.png')
 fa=np.array(frame);fy,fx=np.where(fa[:,:,3]>200);top=int(fy.min());_,headx=np.where(fa[top:top+20,:,3]>128)
 rows.append({'phase':i,'sourceCell':[bounds[i],0,bounds[i+1],raw.height],'bodyComponent':bodyid,'sourceBootFloor':floor,'sourceBootCenter':float(center),'bootRightExclusionFraction':None,'offset':offset,'headTop':top,'top20WidthProxy':int(headx.max()-headx.min()+1),'sourceRightEdgeOpaquePixels':int((cell[:,-1,3]>200).sum())})
 for y,(name,f) in enumerate([('Current action',Image.open(R/f'character/veld-unload-north-consistent-v1/frames/bare/{i:03}.png').convert('RGBA')),('New whole source',frame)]):
  d.text((i*256+4,y*290+4),name+' '+str(i),fill='white');board.paste(f,(i*256,y*290+24),f)
 detail=frame.crop((85,66,198,166)).resize((248,219),Image.Resampling.NEAREST);board.paste(detail,(i*256+4,620),detail)
board.save(P/'unload-source-comparison.png')
(P/'unload-extraction.json').write_text(json.dumps({'source':rawpath.name,'sourceSHA256':hashlib.sha256(rawpath.read_bytes()).hexdigest(),'scale':scale,'gutterBounds':bounds,'rows':rows,'floorCase':'retained inside whole authored source; independent prop binding pending','scope':'Whole authored action source single first-standing148 ruler; original generated source registration diagnostics; no package/adoption/motion acceptance.','visualReview':'pending'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'sourceDimensions':raw.size,'scale':scale,'gutters':bounds,'headWidths':[r['top20WidthProxy'] for r in rows],'floors':[r['sourceBootFloor'] for r in rows],'edgePixels':[r['sourceRightEdgeOpaquePixels'] for r in rows],'floorCase':'whole-source contact retained'}))
