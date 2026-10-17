"""Eight independently authored Salvage headings; registered articulated exports."""
from pathlib import Path
import hashlib,json,math,sys
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageChops
R=Path(__file__).resolve().parent;SIZE=512;FPS=30
SPECS={
 'south':dict(file='south-v1.png',cell=None,anchor=(627,650),diameter=185,grips=[(574,960),(678,960)],tip=(627,1128),lamp=(627,285),jawLength=210,jawWidth=140,fans=[(181,607,54,38),(1070,607,54,38),(357,776,21,13),(895,776,21,13)]),
 'north':dict(file='north-v1.png',cell=None,anchor=(627,565),diameter=185,grips=[(574,260),(679,260)],tip=(627,102),lamp=(627,952),jawLength=210,jawWidth=140,fans=[(171,880,65,45),(1081,880,65,45)]),
 'east':dict(file='east-west-v2.png',cell=0,anchor=(497,443),diameter=141,grips=[(711,394),(711,489)],tip=(843,443),lamp=(248,446),jawLength=160,jawWidth=110,fans=[(108,352,37,48),(108,559,37,48),(508,200,12,32),(508,691,12,32)]),
 'west':dict(file='east-west-v2.png',cell=1,anchor=(1280-887,443),diameter=141,grips=[(1060-887,394),(1060-887,489)],tip=(924-887,443),lamp=(1540-887,446),jawLength=160,jawWidth=110,fans=[(1664-887,352,37,48),(1664-887,559,37,48),(1264-887,200,12,32),(1264-887,691,12,32)]),
 'northeast':dict(file='rear-diagonals-v2.png',cell=0,anchor=(483,385),diameter=145,grips=[(599,161),(678,192)],tip=(692,69),lamp=(340,650),jawLength=190,jawWidth=125,fans=[(84,543,42,50),(699,748,51,44)]),
 'northwest':dict(file='rear-diagonals-v2.png',cell=1,anchor=(1293-887,385),diameter=145,grips=[(1078-887,191),(1166-887,160)],tip=(1081-887,65),lamp=(1437-887,650),jawLength=190,jawWidth=125,fans=[(1079-887,748,51,44),(1693-887,543,42,50)]),
 'southeast':dict(file='front-diagonals-v3.png',cell=0,anchor=(522,458),diameter=136,grips=[(594,690),(649,661)],tip=(681,792),lamp=(388,192),jawLength=180,jawWidth=98,fans=[(223,516,44,40),(777,341,31,35),(392,644,17,12),(707,489,17,12)]),
 'southwest':dict(file='front-diagonals-v3.png',cell=1,anchor=(1260-887,460),diameter=136,grips=[(1138-887,675),(1193-887,701)],tip=(1129-887,802),lamp=(1380-887,194),jawLength=180,jawWidth=98,fans=[(1005-887,366,29,33),(1570-887,502,44,38),(1081-887,516,17,12),(1363-887,656,17,12)]),
}
def save(im,path):path.parent.mkdir(parents=True,exist_ok=True);im.save(path,compress_level=3);return path.relative_to(R).as_posix()
def clean(path,cell=None):
 a=np.array(Image.open(path).convert('RGBA'))
 if cell is not None:a=a[:,cell*(a.shape[1]//2):(cell+1)*(a.shape[1]//2)]
 labels,_=ndimage.label(a[:,:,3]>128);counts=np.bincount(labels.ravel());counts[0]=0;keep=ndimage.binary_dilation(labels==counts.argmax(),iterations=2);a[:,:,3]=np.where(keep,a[:,:,3],0);return Image.fromarray(a)
south=clean(R/'sources/south-v1.png');bb=south.getbbox();SOUTH_SCALE=354/(bb[2]-bb[0]);GLASS=185*SOUTH_SCALE
scrap=Image.open(R/'layers/scrap.png').convert('RGBA')
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def rig(h,s):
 raw=clean(R/'sources'/s['file'],s['cell']);scale=GLASS/s['diameter'];offset=np.rint(np.array([256,246])-np.array(s['anchor'])*scale).astype(int)
 def point(p):return np.array(p)*scale+offset
 base=Image.new('RGBA',(SIZE,SIZE));im=raw.convert('RGBa').resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS).convert('RGBA');base.alpha_composite(im,tuple(offset))
 grips=[point(p) for p in s['grips']];center=np.mean(grips,axis=0);u=point(s['tip'])-center;u/=np.linalg.norm(u);v=np.array([-u[1],u[0]])
 Y,X=np.indices((SIZE,SIZE));along=(X-center[0])*u[0]+(Y-center[1])*u[1];across=(X-center[0])*v[0]+(Y-center[1])*v[1]
 fixed=base.copy();jaws=[]
 for pivot in grips:
  side=np.sign(np.dot(pivot-center,v));halfspan=max(abs(np.dot(p-center,v)) for p in grips)
  diagonal=len(h)>5
  width=np.minimum((s['jawWidth']+(20 if diagonal else 0))*scale,halfspan+(75 if h=='southwest' else 50)*scale+np.maximum(along,0)*.5)
  rear_margin=40 if len(h)>5 else 12
  mask=(along>=-rear_margin*scale)&(along<s['jawLength']*scale)&(across*side>0)&(abs(across)<width)
  m=Image.fromarray((mask*255).astype('uint8'));part=base.copy();part.putalpha(ImageChops.multiply(base.getchannel('A'),m));fixed.putalpha(ImageChops.multiply(fixed.getchannel('A'),ImageChops.invert(m)))
  sign=np.sign(np.dot(np.array([u[1],-u[0]]),center-pivot));jaws.append((part,tuple(pivot),sign))
 fans=[];fanmask=Image.new('L',(SIZE,SIZE))
 for cx,cy,rx,ry in s['fans']:
  x,y=point((cx,cy));rx*=scale;ry*=scale;box=(round(x-rx),round(y-ry),round(x+rx+1),round(y+ry+1));patch=base.crop(box);m=Image.new('L',patch.size);ImageDraw.Draw(m).ellipse((1,1,patch.width-2,patch.height-2),fill=255);fans.append((box,patch,m));fanmask.paste(m,box[:2])
 def body(closure,phase):
  out=fixed.copy()
  for part,pivot,sign in jaws:out.alpha_composite(part.rotate(sign*16*closure,resample=Image.Resampling.BICUBIC,center=pivot))
  alpha=out.getchannel('A')
  for box,patch,m in fans:
   rotor=patch.resize((64,64),Image.Resampling.BICUBIC).rotate(phase*6,resample=Image.Resampling.BICUBIC).resize(patch.size,Image.Resampling.LANCZOS);out.paste(Image.composite(rotor,patch,m),box[:2])
  out.putalpha(alpha)
  if closure:
   ar=np.array(out);labels,_=ndimage.label(ar[:,:,3]>128);counts=np.bincount(labels.ravel());scraps=np.isin(labels,[i for i in range(1,len(counts)) if counts[i]<80])
   ar[ndimage.binary_dilation(scraps,iterations=1),3]=0;out=Image.fromarray(ar)
  return out
 cargoPoint=point(s['tip'])-u*30*scale
 def cargo(distance=0):
  out=Image.new('RGBA',(SIZE,SIZE));p=cargoPoint+u*distance;out.alpha_composite(scrap,tuple(np.rint(p-np.array(scrap.size)/2).astype(int)));return out
 return base,body,cargo,fanmask,point(s['lamp']),dict(source=s,scale=scale,offset=offset.tolist(),grips=[p.tolist() for p in grips],axis=u.tolist(),cargoPoint=cargoPoint.tolist())
def main():
 old=json.loads((R/'manifest.json').read_text());selected=sys.argv[1:] or list(SPECS);states=[e for e in old['states'] if e['heading'] not in selected];headings=old['headings'];checks=[]
 empty=Image.new('RGBA',(SIZE,SIZE));empty_path=save(empty,R/'full/empty.png')
 for h in selected:
  base,body,cargo,fanmask,lamp,meta=rig(h,SPECS[h]);pose=save(base,R/'poses'/f'{h}.png');cache={}
  rotor_atlas=Image.new('RGBA',(SIZE*6,SIZE*10))
  for n in range(60):
   patch=body(0,n);patch.putalpha(ImageChops.multiply(patch.getchannel('A'),fanmask));rotor_atlas.paste(patch,(n%6*SIZE,n//6*SIZE))
  rp=save(rotor_atlas,R/'full/atlases'/f'rotors-{h}.png')
  headings[h]={'pose':pose,'lamp':lamp.tolist(),'rig':meta,'rotorAtlas':{'path':rp,'columns':6,'frameCount':60},'cargoPose':save(cargo(),R/'full/cargo-poses'/f'{h}.png'),'closedPose':save(body(1,0),R/'full/closed-poses'/f'{h}.png')}
  def frame(close,phase):
   key=(round(close,4),phase%60)
   if key not in cache:
    im=body(*key);bounds=im.getbbox();assert bounds and min(bounds[:2])>1 and max(bounds[2:])<SIZE-1,(h,key,bounds)
    path=save(im,R/'full/library'/h/f'{round(key[0]*10000):05}-{key[1]:02}.png');cache[key]=(path,im)
   return cache[key]
  modes=['idle','swim','reverse','carry','start','stop','power-on','power-off','charging','disabled']+(['retrieve','release','blocked'] if h in ['north','east','south','west'] else [])
  for state in modes:
   count=120 if state in ['retrieve','release','blocked'] else 60;paths=[];cp=[];phases=[];lamps=[];distances=[];atlas=Image.new('RGBA',(SIZE*6,SIZE*math.ceil(count/6)));ca=Image.new('RGBA',atlas.size)
   for n in range(count):
    t=n/30;close=1 if state=='carry' else smooth((n-30)/44) if state=='retrieve' else 1-smooth(n/44) if state=='release' else .55*(smooth((n-15)/29) if n<60 else 1-smooth((n-60)/44)) if state=='blocked' else 0
    rate=4 if state in ['swim','carry'] else -4 if state=='reverse' else 1
    phase=n*rate%60;distance=0
    if state in ['start','stop']:
     ramp=.5;speed=24;distance=24*min(t,ramp)**2+speed*max(0,t-ramp) if state=='start' else speed*min(t,ramp)-24*min(t,ramp)**2
     phase=round(distance/24*120)%60
    if state in ['charging','disabled']:phase=0
    if state=='power-on':phase=round(n*smooth(n/44))%60
    if state=='power-off':phase=round(n*(1-smooth(n/44)))%60
    path,im=frame(close,phase);paths.append(path);atlas.paste(im,(n%6*SIZE,n//6*SIZE));cargo_im=empty
    if state in ['carry','retrieve','blocked']:cargo_im=cargo()
    elif state=='release':cargo_im=cargo(26*smooth((n-44)/45))
    if cargo_im is empty:cp.append(empty_path)
    else:cp.append(save(cargo_im,R/'full/cargo'/f'{state}-{h}'/f'{n:03}.png'))
    ca.paste(cargo_im,(n%6*SIZE,n//6*SIZE));distances.append(distance)
    phases.append(('Align' if n<30 else 'Grip' if n<75 else 'Hold') if state=='retrieve' else ('Open claw' if n<45 else 'Release') if state=='release' else ('Attempt' if n<45 else 'Blocked' if n<60 else 'Recover') if state=='blocked' else state)
    lamps.append(smooth(n/44) if state=='power-on' else 1-smooth(n/44) if state=='power-off' else 1)
   states.append({'id':state+'-'+h,'state':state,'heading':h,'frameCount':count,'fps':FPS,'loop':state in ['idle','swim','reverse','carry','charging','disabled'],'holdFrame':count-1,'frameFiles':paths,'cargoFiles':cp,'phases':phases,'rootDistanceWorld':distances,'lampSamples':lamps,'lampColor':'charging' if state=='charging' else 'stopped' if state in ['blocked','disabled'] else 'operational','atlas':{'path':save(atlas,R/'full/atlases'/f'{state}-{h}.png'),'columns':6},'cargoAtlas':{'path':save(ca,R/'full/atlases'/f'{state}-{h}-cargo.png'),'columns':6}})
  checks.append({'heading':h,'clips':len(modes),'uniqueBodyFrames':len(cache),'bounds':base.getbbox()});print(h,len(modes),'clips',len(cache),'unique body frames',flush=True)
 d={**old,'id':'salvage-drone-v1','headings':headings,'states':states,'scope':'Eight-heading swimming/power, four cardinal retrieval/release/blocked actions; review only, no gameplay integration.','sourceFiles':[{'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (R/'sources').glob('*.png')]}
 (R/'manifest.json').write_text(json.dumps(d,indent=2),encoding='utf-8');(R/'review/full-build-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');print('TOTAL',len(states),'clips',flush=True)
if __name__=='__main__':main()
