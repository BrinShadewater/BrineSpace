"""Rigid appearance fit for diagnosis only; never changes source artwork."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage,signal
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2]
frames=[np.array(Image.open(P/f'full-clip-frames-v2/{n:03}.png').convert('RGBA')).astype(float) for n in range(142)]
windows=json.loads((P/'support-window-diagnostic.json').read_text(encoding='utf-8'))['windows']
results=[]
for role,win,first,last in [('far',windows[0],17,27),('near',windows[1],7,17)]:
 step=win['candidateConstantRootSpeedPxPerSecond']/24
 base=win['templateFrame'];x0,y0,x1,y1=win['box'];cx=(x0+x1)//2;cy=(y0+y1)//2;size=44;half=size//2
 a=frames[base];template=a[cy-half:cy+half,cx-half:cx+half,:3].copy();alpha=a[cy-half:cy+half,cx-half:cx+half,3]
 yy,xx=np.mgrid[cy-half:cy+half,cx-half:cx+half]
 mask=(alpha>220)&(xx>=x0)&(xx<x1)&(yy>=y0)&(yy<y1)&(template[:,:,0]>template[:,:,1]+3)&(template[:,:,0]>template[:,:,2]+3)&(template.mean(2)>35)&(template.mean(2)<220)
 sole=(a[max(y0,y1-2):y1,x0:x1,3]>200).any(0);soleX=np.where(sole)[0];assert len(soleX)>3
 heel=np.array([x0+soleX.min()-cx,y1-1-cy],float);toe=np.array([x0+soleX.max()-cx,y1-1-cy],float)
 rotations=[]
 for angle in range(-70,41,5):
  rgb=ndimage.rotate(template,angle,reshape=False,order=1,mode='constant',cval=0)
  m=ndimage.rotate(mask.astype(float),angle,reshape=False,order=0,mode='constant',cval=0)
  count=m.sum();mean=(rgb*m[:,:,None]).sum((0,1))/count;centered=(rgb-mean)*m[:,:,None];energy=(centered*centered).sum()
  rotations.append((angle,m,centered,count,energy))
 rows=[]
 for n in range(first,last+1):
  expectedX=round(cx-(n-base)*step);left=expectedX-half-14;top=cy-half-8
  search=frames[n][top:cy+half+9,left:expectedX+half+15,:3];assert search.shape==(61,73,3)
  candidates=[]
  for angle,m,centered,count,energy in rotations:
   numerator=sum(signal.fftconvolve(search[:,:,c],centered[::-1,::-1,c],mode='valid') for c in range(3))
   variance=np.zeros(numerator.shape)
   for c in range(3):
    sums=signal.fftconvolve(search[:,:,c],m[::-1,::-1],mode='valid');squares=signal.fftconvolve(search[:,:,c]**2,m[::-1,::-1],mode='valid');variance+=squares-sums*sums/count
   scores=numerator/np.sqrt(np.maximum(1e-8,variance*energy));py,px=np.unravel_index(np.argmax(scores),scores.shape)
   candidates.append((float(scores[py,px]),angle,left+int(px)+half,top+int(py)+half))
  score,angle,fx,fy=max(candidates)
  theta=np.deg2rad(angle);rot=np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]])
  h=rot@heel+np.array([fx,fy]);t=rot@toe+np.array([fx,fy]);root=(n-base)*step
  rows.append({'frame':n,'NCC':round(score,4),'angleDegrees':angle,'center':[fx,fy],'heelSource':h.tolist(),'toeSource':t.tolist(),'heelRootPlusSourceX':float(h[0]+root),'toeRootPlusSourceX':float(t[0]+root),'lowerProjectedEdgeY':float(max(h[1],t[1])),'rotationSearchBoundary':angle in [-70,40],'validAppearanceFitOnly':bool(score>=.8 and angle not in [-70,40])})
 board=Image.new('RGB',(1500,900),(32,43,49));d=ImageDraw.Draw(board)
 for j,row in enumerate(rows):
  im=Image.fromarray(frames[row['frame']].astype('uint8'));md=ImageDraw.Draw(im)
  for key,color in [('heelSource',(105,205,231)),('toeSource',(246,190,94))]:
   x,y=row[key];md.ellipse((x-1,y-1,x+1,y+1),outline=color,width=1)
  crop=im.crop((65,185,190,231)).resize((250,92),Image.Resampling.NEAREST);xy=((j%6)*250,(j//6)*220+30);board.paste(crop,xy,crop)
  d.text((xy[0]+3,xy[1]-20),f"{role} raw{row['frame']} angle{row['angleDegrees']}",fill='white');d.text((xy[0]+3,xy[1]+105),f"NCC{row['NCC']:.3f} {'fit' if row['validAppearanceFitOnly'] else 'UNPROVEN'}",fill='white')
 board.save(P/f'{role}-boot-roll-review.png')
 results.append({'role':role,'frames':[first,last],'templateFrame':base,'templateBox':win['box'],'soleEdgeTemplatePoints':{'heel':(heel+[cx,cy]).tolist(),'toe':(toe+[cx,cy]).tolist()},'rows':rows,'weakOrBoundaryFrames':[r['frame'] for r in rows if not r['validAppearanceFitOnly']],'scope':'Rigid rotation/translation of warm boot appearance mask only. Sole-edge anchors come from opaque two-row template bottom envelope, not validated physical pivot; envelope width avoids single bottom-row speck but does not prove sole anatomy. Separate per-role flat-window root estimate is diagnostic, not a common accepted travel speed; foot deformation/occlusion may invalidate correspondence. Inspect every overlay before interpreting contact.'})
before=json.loads((R/'output/veld-east-grounded-source-v1/inputs-after.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==sha for p,sha in before.items())
report={'roles':results,'nativeInputsStillStable':len(before),'scope':'Read-only full heel/flat/toe appearance diagnosis for both physical leg roles. No source/sprite/root/manifest changes, no full rigid contact or stride acceptance.'}
(P/'boot-roll-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'roles':[{'role':r['role'],'weakOrBoundaryFrames':r['weakOrBoundaryFrames'],'angles':[x['angleDegrees'] for x in r['rows']],'minimumNCC':min(x['NCC'] for x in r['rows'])} for r in results],'inputsStillStable':len(before)}))
