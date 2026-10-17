from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
import numpy as np
from scipy import ndimage
from scipy.spatial import ConvexHull
H=Path(__file__).resolve().parent;R=H.parents[1];B=R/'character/krusher-style-neck-bank-v1';read=lambda p:json.loads(p.read_text());idx=read(H/'audit-index.json');maps=read(R/'character/krusher-style-neck-v1/bank-mapping.json')['records'];records={q['source']:q for q in read(B/'revision.json')['records']};out=H/'pilot';out.mkdir(exist_ok=True);font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),17)
def pad(im,q):
 size=tuple(map(int,q['canvas']))
 if im.size==size:return im
 result=Image.new('RGBA',size);offset=tuple(np.array(q['pivot'],int)-[92,172]) if maps[q['source']].get('paddedCanonical') else (36,52) if im.size==(184,184) else (0,96);result.alpha_composite(im,offset);return result
def cyan(a):
 a=a.copy();r,g,b=[a[:,:,i].astype(float) for i in range(3)];m=(a[:,:,3]>0)&(r>g*.85)&(r<g*1.85)&(g>b*1.12)&(g>32);lum=(r*.2126+g*.7152+b*.0722)/145;colour=np.clip(lum[:,:,None]*[82,124,128],0,190).astype('uint8');a[m,:3]=colour[m];return a
rear=[3378,3383,3386,3395,3400]
polygons={3109:[[174,114],[180,113],[184,114],[184,123],[181,129],[177,128],[173,122]],3137:[[128,87],[141,87],[144,90],[144,99],[141,104],[131,104],[127,100],[126,91]],3207:[[121,108],[132,108],[136,112],[135,120],[131,124],[123,123],[119,118],[119,112]],3379:[[138,105],[145,105],[147,108],[146,115],[142,120],[137,118],[135,113],[135,108]]}
# Native-pixel polygons are inside the observed original visor, excluding its rim/highlights.
selected=[1355,1395,1429,1504,1526,1544,1568,3109,3137,3207,3378,3379,3383,3386,3395,3400]
results=[]
for cid in selected:
 c=idx['crops'][cid];q=records[c['sourceDrawing']];meta=maps[q['source']];a=Image.open(B/q['output']).convert('RGBA');b=np.array(a);original=pad(Image.open(R/meta['originalBody']).convert('RGBA'),q);maskpath=meta.get('mask') if cid in rear else meta['details'].get('portraitMask') or meta.get('mask');mi=Image.open(R/maskpath.removeprefix('res://')).convert('L');mask=np.array(mi)>0
 if mask.shape!=b.shape[:2]:
  expanded=Image.new('L',a.size);expanded.paste(mi,(36,52));mask=np.array(expanded)>0
 if cid in rear or cid in polygons:
  clean=cyan(np.array(original));b[mask]=clean[mask]
  if cid in polygons:
   pm=Image.new('L',a.size);ImageDraw.Draw(pm).polygon([tuple(v) for v in polygons[cid]],fill=255);ap=np.array(pm)>0;head=Image.open(R/q['newHead']).convert('RGBA')
   if cid==3379:head=Image.open(R/'character/krusher-style-neck-v1/sources/style-east-native.png').convert('RGBA')
   ha=np.array(head);r,g,bl=[ha[:,:,i].astype(float) for i in range(3)];skin=(ha[:,:,3]>150)&(r>g*1.09)&(r>bl*1.15)&(r>65);ys,xs=np.where(skin);center=np.array([xs.mean(),ys.mean()]);ys,xs=np.where(ap);target=np.array([xs.mean(),ys.mean()]);at=np.rint(target-center).astype(int);b[ap,:3]=[29,33,34];layer=Image.new('RGBA',a.size);layer.alpha_composite(head,tuple(at));merged=np.array(Image.alpha_composite(Image.fromarray(b),layer));b[ap,:3]=merged[ap,:3];mask|=ap
 else:
  raw=np.array(original);rr,gg,bb=[raw[:,:,k].astype(float) for k in range(3)];yy,xx=np.indices(mask.shape);x0,y0=q['newPaste'];hw,hh=Image.open(R/q['newHead']).size;cx=x0+hw/2
  skin=(raw[:,:,3]>120)&(rr>gg*1.06)&(rr>bb*1.1)&((rr-gg)>(gg-bb)*.75)&(rr>30)&(abs(xx-cx)<11)&(yy>=y0+8)&(yy<y0+(38 if cid==1526 else 46))
  sy,sx=np.where(skin)
  if cid in [1526,1568] and len(sx)>4:
   pts=np.array(list(zip(sx,sy)));hull=ConvexHull(pts);extra=Image.new('L',a.size);ImageDraw.Draw(extra).polygon([tuple(pts[k]) for k in hull.vertices],fill=255);mask|=ndimage.binary_dilation(np.array(extra)>0,iterations=1)
  pick={1355:('pickup-east',[165,91]),1395:('meal-west',[110,71]),1429:('prone-south',[118,134]),1504:('collapse-south',[116,95]),1526:('prone-south',[115,122]),1544:('collapse-south',[119,129]),1568:('collapse-south',[116,210])}
  name,at=pick[cid];head=Image.open(H/('integrated-'+name+'-native.png')).convert('RGBA');b[mask]=0
  layer=Image.new('RGBA',a.size);layer.alpha_composite(head,tuple(at));b=np.array(Image.alpha_composite(Image.fromarray(b),layer));mask|=np.array(layer)[:,:,3]>0
 Image.fromarray(b).save(out/f'{cid:04d}.png');results.append({'cropId':cid,'source':q['source'],'changedPixels':int(np.any(np.array(a)!=b,2).sum()),'maskPixels':int(mask.sum())})
board=Image.new('RGBA',(1400,((len(selected)+3)//4)*300),'#252d31');d=ImageDraw.Draw(board)
for j,cid in enumerate(selected):
 q=records[idx['crops'][cid]['sourceDrawing']];box=idx['crops'][cid]['cropBox'];box=(box[0]-5,box[1]-5,box[2]+5,box[3]+5)
 for col,path in enumerate([B/q['output'],out/f'{cid:04d}.png']):
  im=Image.open(path).convert('RGBA').crop(box).resize((132,140),Image.Resampling.NEAREST);x=j%4*350+col*160;y=j//4*300+35;board.alpha_composite(im,(x,y));d.text((x,y-25),str(cid)+[' before',' pilot'][col],font=font,fill='white')
board.save(H/'pilot-review.png');(H/'pilot-results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results))
