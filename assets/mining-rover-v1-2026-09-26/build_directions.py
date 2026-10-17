"""Independent directional source registration and grounded rover motion."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageChops,ImageFont
from build_pilot import R,SIZE,FPS,save
SPECS={
 'north':dict(file='north-v2.png',cell=None,grid=(1,1),hubs=[(242,328),(1008,328),(237,964),(1007,964)],diagonals=[(0,3),(1,2)],axis=(0,-1),radii=(130,64),partRadii=(170,107),lamp=(626,911),bit=(587,130,669,251),shaft=(610,252,647,268)),
 'east':dict(file='east-west-v2.png',cell=0,grid=(2,1),hubs=[(140,193),(682,194),(140,693),(681,693)],diagonals=[(0,3),(1,2)],axis=(1,0),radii=(88,43),partRadii=(126,73),lamp=(160,444),bit=(756,410,839,478),shaft=(739,425,757,461)),
 'west':dict(file='east-west-v2.png',cell=1,grid=(2,1),hubs=[(195,194),(735,194),(195,693),(735,693)],diagonals=[(0,3),(1,2)],axis=(-1,0),radii=(88,43),partRadii=(126,73),lamp=(725,444),bit=(42,410,133,478),shaft=(132,425,152,460)),
 'northeast':dict(file='diagonals-v3-selective.png',cell=0,grid=(2,2),hubs=[(300,167),(129,396),(513,381),(344,553)],diagonals=[(0,3),(1,2)],axis=(.70710678,-.70710678),radii=(59,31),partRadii=(94,62),lamp=(201,462)),
 'southeast':dict(file='diagonals-v2-extra-tools-rejected.png',cell=1,grid=(2,2),hubs=[(309,174),(119,394),(520,438),(309,551)],diagonals=[(0,3),(1,2)],axis=(.70710678,.70710678),radii=(59,31),partRadii=(94,62),lamp=(181,242)),
 'southwest':dict(file='diagonals-v2-extra-tools-rejected.png',cell=2,grid=(2,2),hubs=[(344,137),(132,383),(519,324),(343,511)],diagonals=[(0,3),(1,2)],axis=(-.70710678,.70710678),radii=(59,31),partRadii=(94,62),lamp=(460,209)),
 'northwest':dict(file='diagonals-v3-selective.png',cell=3,grid=(2,2),hubs=[(342,146),(121,334),(525,382),(319,515)],diagonals=[(0,3),(1,2)],axis=(-.70710678,-.70710678),radii=(59,31),partRadii=(94,62),lamp=(439,430)),
}
Y,X=np.indices((SIZE,SIZE),dtype=float)
for heading in ['northeast','southeast','southwest','northwest']:
 SPECS[heading]['file']='diagonals-v5-polished.png'
def setup(h,s):
 raw=Image.open(R/'sources'/s['file']).convert('RGBA')
 if s['cell'] is not None:
  c=s['cell'];cols,rows=s['grid'];pixels=np.array(raw);labels,_=ndimage.label(pixels[:,:,3]>200);counts=np.bincount(labels.ravel());counts[0]=0
  largest=np.argsort(counts)[-cols*rows:];expected=np.array([(c%cols+.5)*raw.width/cols,(c//cols+.5)*raw.height/rows]);centres=ndimage.center_of_mass(pixels[:,:,3]>200,labels,largest)
  selected=min(zip(largest,centres),key=lambda item:np.linalg.norm(np.array(item[1][::-1])-expected))[0]
  keep=ndimage.binary_dilation(labels==selected,iterations=2);pixels[:,:,3]=np.where(keep,pixels[:,:,3],0);raw=Image.fromarray(pixels)
  # Generated poses can cross nominal cell boundaries. Separate by alpha
  # component before slicing; retain the full selected tyre silhouette.
  ox=round(c%cols*raw.width/cols);oy=round(c//cols*raw.height/rows);raw=raw.crop((ox,oy,raw.width,raw.height))
 a=np.array(raw);labels,_=ndimage.label(a[:,:,3]>200);counts=np.bincount(labels.ravel());counts[0]=0;keep=ndimage.binary_dilation(labels==counts.argmax(),iterations=2);a[:,:,3]=np.where(keep,a[:,:,3],0);raw=Image.fromarray(a)
 diagonal=np.mean([np.linalg.norm(np.subtract(s['hubs'][a],s['hubs'][b])) for a,b in s['diagonals']]);scale=(190 if len(h)>5 else 244)/diagonal;anchor=np.mean(s['hubs'],axis=0);offset=np.round(224-anchor*scale).astype(int);small=raw.convert('RGBa').resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS).convert('RGBA');base=Image.new('RGBA',(SIZE,SIZE));base.alpha_composite(small,tuple(offset))
 def pt(p):return tuple(np.array(p)*scale+offset)
 hubs=[pt(p) for p in s['hubs']];u=np.array(s['axis']);v=np.array([-u[1],u[0]]);L,W=np.array(s['radii'])*scale;PL,PW=np.array(s['partRadii'])*scale;mask=np.zeros((SIZE,SIZE),bool);front=sorted(range(4),key=lambda i:np.dot(np.subtract(hubs[i],(224,224)),u),reverse=True)[:2]
 rigs=[]
 for i,(cx,cy) in enumerate(hubs):
  du=(X-cx)*u[0]+(Y-cy)*u[1];dv=(X-cx)*v[0]+(Y-cy)*v[1];weight=np.clip(np.minimum(L-np.abs(du),W-np.abs(dv))/2,0,1);weight*=np.array(base)[:,:,3]>245;mask|=weight>0
  pm=Image.new('L',(SIZE,SIZE));poly=[tuple(np.array([cx,cy])+u*a*PL+v*b*PW) for a,b in [(-1,-1),(-1,1),(1,1),(1,-1)]];ImageDraw.Draw(pm).polygon(poly,fill=255);rigs.append((du,dv,weight,pm,(cx,cy)))
 return base,pt,scale,offset,rigs,front,mask

def main():
 import sys
 selected=sys.argv[1:] or list(SPECS)
 data=json.loads((R/'manifest.json').read_text());data['states']=[s for s in data['states'] if s['heading'] not in selected];checks=[]
 for h,s in SPECS.items():
  if h not in selected:continue
  base,pt,scale,offset,rigs,front,wheelmask=setup(h,s);a=np.array(base);u=np.array(s['axis']);v=np.array([-u[1],u[0]]);L=s['radii'][0]*scale
  def roll(phase):
   out=a.copy()
   for du,dv,w,pm,(cx,cy) in rigs:
    sampleu=(du-phase*2*L+L)%(2*L)-L;sx=cx+sampleu*u[0]+dv*v[0];sy=cy+sampleu*u[1]+dv*v[1]
    for c in range(3):
     moved=ndimage.map_coordinates(a[:,:,c].astype(float),[sy,sx],order=1,mode='nearest');out[:,:,c]=np.clip(out[:,:,c]*(1-w)+moved*w,0,255).astype('uint8')
   return Image.fromarray(out)
  def steer(im,angle):
   out=im.copy()
   for i in front:
    pm=rigs[i][3];part=im.copy();part.putalpha(ImageChops.multiply(im.getchannel('A'),pm));out.putalpha(ImageChops.multiply(out.getchannel('A'),ImageChops.invert(pm)));out.alpha_composite(part.rotate(angle,resample=Image.Resampling.BICUBIC,center=rigs[i][4]))
   return out
  if 'bit' in s:
   b=tuple(round(x) for x in (*pt(s['bit'][:2]),*pt(s['bit'][2:])));bm=Image.new('L',(SIZE,SIZE));ImageDraw.Draw(bm).rectangle(b,fill=255);bit=base.copy();bit.putalpha(ImageChops.multiply(base.getchannel('A'),bm));fixed=base.copy();fixed.putalpha(ImageChops.multiply(base.getchannel('A'),ImageChops.invert(bm)));sb=tuple(round(x) for x in (*pt(s['shaft'][:2]),*pt(s['shaft'][2:])));shaft=base.crop(sb)
   bitbase=np.array([(b[0]+b[2])/2,(b[1]+b[3])/2])-u*((b[2]-b[0]) if h in ['east','west'] else (b[3]-b[1]))/2
   tip=np.array([(b[0]+b[2])/2,(b[1]+b[3])/2])+u*((b[2]-b[0]) if h in ['east','west'] else (b[3]-b[1]))/2
  def mine(n):
   phase='Brace' if n<15 else 'Deploy' if n<45 else 'Mine' if n<135 else 'Retract' if n<165 else 'Ready';t=0 if n<15 else min(1,(n-15)/29) if n<45 else 1 if n<135 else max(0,1-(n-135)/29) if n<165 else 0;t=t*t*(3-2*t);ext=round(28*t);delta=np.round(u*ext).astype(int);out=fixed.copy();moving=bit.copy()
   if phase=='Mine':
    ar=np.array(moving)
    # Rotate the authored screw shading around its axis, not its silhouette.
    if h in ['east','west']:
     for x in range(b[0],b[2]):
      ys=np.where(ar[:,x,3]>64)[0]
      if len(ys)>3:lo,hi=ys[0],ys[-1]+1;ar[lo:hi,x,:3]=np.roll(ar[lo:hi,x,:3],round(3*math.sin(n*.8+x*.35)),axis=0)
    else:
     for y in range(b[1],b[3]):
      xs=np.where(ar[y,:,3]>64)[0]
      if len(xs)>3:lo,hi=xs[0],xs[-1]+1;ar[y,lo:hi,:3]=np.roll(ar[y,lo:hi,:3],round(3*math.sin(n*.8+y*.35)),axis=0)
    moving=Image.fromarray(ar)
   if ext:
    length=ext+4
    if h in ['east','west']:
     bridge=shaft.resize((length,shaft.height),Image.Resampling.BICUBIC);start=(round(bitbase[0]-2 if h=='east' else bitbase[0]-ext-2),round(bitbase[1]-shaft.height/2))
    else:
     bridge=shaft.resize((shaft.width,length),Image.Resampling.BICUBIC);start=(round(bitbase[0]-shaft.width/2),round(bitbase[1]-ext-2))
    out.alpha_composite(bridge,start)
   out.alpha_composite(moving,tuple(delta));fx=Image.new('RGBA',(SIZE,SIZE));d=ImageDraw.Draw(fx)
   if phase=='Mine':
    for j in range(12):
     p=(n/30*1.2+j/12)%1;at=tip+delta+v*math.sin(j*11.3)*p*19+u*p*10;x,y=at;d.ellipse((x-1,y-1,x+1,y+1),fill=(135,139,125,round(150*(1-p))))
   return out,fx,phase
  methods=[('idle',60),('drive',60),('reverse',60),('steer-left',60),('steer-right',60)]+([('mine',180)] if 'bit' in s else [])
  lamp=[round(x) for x in pt(s['lamp'])];posepath=save(base,R/'poses'/f'{h}.png');data['headings'][h]={'pose':posepath,'lamp':lamp,'source':s,'scale':scale,'offset':offset.tolist(),'wheelHubs':[list(r[-1]) for r in rigs],'frontWheelIndices':front}
  for state,count in methods:
   paths=[];effects=[];phases=[];atlas=Image.new('RGBA',(SIZE*6,SIZE*math.ceil(count/6)));fxatlas=Image.new('RGBA',atlas.size)
   for n in range(count):
    fx=Image.new('RGBA',(SIZE,SIZE));phase=state
    if state=='mine':im,fx,phase=mine(n)
    elif state=='idle':im=base.copy()
    else:
     im=roll((-1 if state=='reverse' else 1)*n/60)
     if state.startswith('steer'):im=steer(im,(-1 if state.endswith('left') else 1)*8*math.sin(math.pi*n/59)**2)
    bounds=im.getbbox();assert bounds and min(bounds[:2])>0 and max(bounds[2:])<SIZE,(h,state,n,bounds)
    if state in ['drive','reverse']:
     ar=np.array(im);assert np.array_equal(ar[:,:,3],a[:,:,3]);assert np.array_equal(ar[~wheelmask],a[~wheelmask])
    paths.append(save(im,R/'frames'/f'{state}-{h}'/f'{n:03}.png'));effects.append(save(fx,R/'effects'/f'{state}-{h}'/f'{n:03}.png'));phases.append(phase);atlas.paste(im,(n%6*SIZE,n//6*SIZE));fxatlas.paste(fx,(n%6*SIZE,n//6*SIZE))
   if state=='mine':assert Image.open(R/paths[0]).tobytes()==Image.open(R/paths[-1]).tobytes()==base.tobytes()
   data['states'].append({'id':state+'-'+h,'state':state,'heading':h,'frameFiles':paths,'effectFiles':effects,'frameCount':count,'fps':FPS,'loop':state!='mine','holdFrame':count-1 if state=='mine' else None,'phases':phases,'atlas':{'path':save(atlas,R/'atlases'/f'{state}-{h}.png'),'columns':6},'effectAtlas':{'path':save(fxatlas,R/'atlases'/f'{state}-{h}-effects.png'),'columns':6},'travelWorldUnitsPerSecond':22 if state not in ['idle','mine'] else 0})
  checks.append({'heading':h,'wheelDiagonalLibraryPixels':190 if len(h)>5 else 244,'scale':scale,'clips':len(methods),'geometryAndTravelInvariance':'pass'});print(h,'complete',flush=True)
 data['scope']='Review only. Eight independently authored headings, grounded idle/drive/reverse/steering; four cardinal mining deploy/work/retract jobs. No game integration.';data['sourceFiles']=[{'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (R/'sources').glob('*.png')];temp=R/'manifest.tmp.json';temp.write_text(json.dumps(data,indent=2));temp.replace(R/'manifest.json');(R/'review/directional-checks.json').write_text(json.dumps(checks,indent=2));print(len(data['states']),'clips delivered')
if __name__=='__main__':main()
