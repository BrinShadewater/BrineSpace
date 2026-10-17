"""Grounded rover pilot: authored tyre texture, local steering and tool articulation."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageChops,ImageFont
R=Path(__file__).resolve().parent;SIZE=448;PIVOT=224;FPS=30

def save(im,path):path.parent.mkdir(parents=True,exist_ok=True);im.save(path,compress_level=3);return path.relative_to(R).as_posix()
def main():
 source=Image.open(R/'sources/south-v4.png').convert('RGBA');bbox=source.getchannel('A').point(lambda a:255 if a>64 else 0).getbbox();scale=246/(bbox[2]-bbox[0]);offset=(round(PIVOT-640*scale),)*2
 small=source.convert('RGBa').resize((round(source.width*scale),round(source.height*scale)),Image.Resampling.LANCZOS).convert('RGBA');base=Image.new('RGBA',(SIZE,SIZE));base.alpha_composite(small,offset)
 def pt(x,y):return (round(offset[0]+x*scale),round(offset[1]+y*scale))
 def box(b):return (*pt(*b[:2]),*pt(*b[2:]))
 tyres=[box(b) for b in [(174,195,319,470),(934,195,1080,470),(151,875,306,1126),(957,875,1107,1126)]]
 wheelparts=[box(b) for b in [(109,842,328,1144),(919,842,1145,1144)]]
 bitbox=box((585,966,674,1082));bitmask=Image.new('L',(SIZE,SIZE));ImageDraw.Draw(bitmask).rectangle(bitbox,fill=255)
 bit=base.copy();bit.putalpha(ImageChops.multiply(base.getchannel('A'),bitmask));chassis=base.copy();chassis.putalpha(ImageChops.multiply(base.getchannel('A'),ImageChops.invert(bitmask)))
 shaft=base.crop(box((613,943,651,967)))
 lamp=pt(624,251);drillcontact=pt(628,1082);a=np.array(base);tyremasks=[]
 for x0,y0,x1,y1 in tyres:
  yy,xx=np.indices((y1-y0,x1-x0));edge=np.minimum.reduce([xx,yy,x1-x0-1-xx,y1-y0-1-yy]);tyremasks.append(np.clip(edge/3,0,1))
 def roll(phase):
  out=a.copy()
  for bounds,w in zip(tyres,tyremasks):
   x0,y0,x1,y1=bounds;patch=a[y0:y1,x0:x1,:3];shift=phase*(y1-y0);yy,xx=np.indices(patch.shape[:2],dtype=float);yy=(yy-shift)%(y1-y0)
   moved=np.stack([ndimage.map_coordinates(patch[:,:,c].astype(float),[yy,xx],order=1,mode='wrap') for c in range(3)],axis=2)
   out[y0:y1,x0:x1,:3]=np.clip(patch*(1-w[:,:,None])+moved*w[:,:,None],0,255).astype('uint8')
  return Image.fromarray(out)
 def steer(im,angle):
  out=im.copy()
  for b in wheelparts:
   m=Image.new('L',(SIZE,SIZE));ImageDraw.Draw(m).rectangle(b,fill=255);part=im.copy();part.putalpha(ImageChops.multiply(im.getchannel('A'),m));out.putalpha(ImageChops.multiply(out.getchannel('A'),ImageChops.invert(m)));out.alpha_composite(part.rotate(angle,resample=Image.Resampling.BICUBIC,center=((b[0]+b[2])/2,(b[1]+b[3])/2)))
  return out
 def mining(n):
  phase='Brace' if n<15 else 'Deploy' if n<45 else 'Mine' if n<135 else 'Retract' if n<165 else 'Ready'
  t=0 if n<15 else min(1,(n-15)/29) if n<45 else 1 if n<135 else max(0,1-(n-135)/29) if n<165 else 0
  t=t*t*(3-2*t);extension=round(28*t);out=chassis.copy();moving=bit.copy()
  if phase=='Mine':
   ar=np.array(moving);x0,y0,x1,y1=bitbox
   for y in range(y0,y1):
    xs=np.where(ar[y,:,3]>64)[0]
    if len(xs)>3:
     left,right=xs[0],xs[-1]+1;ar[y,left:right,:3]=np.roll(ar[y,left:right,:3],round(3*math.sin(n*.8+y*.35)),axis=0)
   moving=Image.fromarray(ar)
  if extension:
   x=round((bitbox[0]+bitbox[2]-shaft.width)/2);out.alpha_composite(shaft.resize((shaft.width,extension+4),Image.Resampling.BICUBIC),(x,bitbox[1]-2))
  out.alpha_composite(moving,(0,extension));fx=Image.new('RGBA',(SIZE,SIZE));d=ImageDraw.Draw(fx)
  if phase=='Mine':
   for j in range(12):
    p=(n/30*1.2+j/12)%1;dx=math.sin(j*11.3)*p*19;dy=p*10
    x=drillcontact[0]+dx;y=drillcontact[1]+extension+dy;d.ellipse((x-1,y-1,x+1,y+1),fill=(135,139,125,round(150*(1-p))))
  return out,fx,phase
 clips=[]
 for state,count in [('idle',60),('drive',60),('reverse',60),('steer-left',60),('steer-right',60),('mine',180)]:
  paths=[];fxpaths=[];phases=[];maskchanges=0
  for n in range(count):
   fx=Image.new('RGBA',(SIZE,SIZE));phase=state
   if state=='mine':im,fx,phase=mining(n)
   elif state=='idle':im=base.copy()
   else:
    im=roll((-1 if state=='reverse' else 1)*n/60)
    if state.startswith('steer'):im=steer(im,(-1 if state.endswith('left') else 1)*8*math.sin(math.pi*n/59)**2)
   bounds=im.getbbox();assert bounds and min(bounds[:2])>0 and max(bounds[2:])<SIZE,(state,n,bounds)
   if state in ['idle','drive','reverse']:assert np.array_equal(np.array(im)[:,:,3],a[:,:,3])
   paths.append(save(im,R/'frames'/f'{state}-south'/f'{n:03}.png'));fxpaths.append(save(fx,R/'effects'/f'{state}-south'/f'{n:03}.png'));phases.append(phase)
  columns=6;atlas=Image.new('RGBA',(columns*SIZE,math.ceil(count/columns)*SIZE));effect=Image.new('RGBA',atlas.size)
  for n,(p,f) in enumerate(zip(paths,fxpaths)):atlas.paste(Image.open(R/p),(n%columns*SIZE,n//columns*SIZE));effect.paste(Image.open(R/f),(n%columns*SIZE,n//columns*SIZE))
  clips.append({'id':state+'-south','state':state,'heading':'south','frameFiles':paths,'effectFiles':fxpaths,'frameCount':count,'fps':FPS,'loop':state!='mine','holdFrame':count-1 if state=='mine' else None,'phases':phases,'atlas':{'path':save(atlas,R/'atlases'/f'{state}-south.png'),'columns':columns},'effectAtlas':{'path':save(effect,R/'atlases'/f'{state}-south-effects.png'),'columns':columns},'travelWorldUnitsPerSecond':22 if state not in ['idle','mine'] else 0})
 assert Image.open(R/clips[-1]['frameFiles'][0]).tobytes()==base.tobytes()
 assert Image.open(R/clips[-1]['frameFiles'][-1]).tobytes()==base.tobytes()
 manifest={'id':'mining-rover-v1','frameWidth':SIZE,'frameHeight':SIZE,'pivot':[PIVOT,PIVOT],'worldUnitsPerPixel':.34,'nominalWidthWorld':83.64,'fps':FPS,'headings':{'south':{'pose':save(base,R/'poses/south.png'),'lamp':lamp,'tyreBounds':tyres,'steeringParts':wheelparts,'toolBounds':bitbox,'toolContact':drillcontact,'scale':scale,'offset':offset}},'states':clips,'lamp':{'periodSeconds':.85,'colors':{'operational':'#309bff','stopped':'#ff302e','charging':'#ffcd2d'}},'sourceFiles':[{'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (R/'sources').glob('*.png')],'scope':'Grounded south-facing rover pilot. Remaining directions are not yet authored. Review only; no runtime integration.'}
 (R/'manifest.json').write_text(json.dumps(manifest,indent=2));(R/'review/pilot-checks.json').write_text(json.dumps({'clips':6,'bodyFrames':480,'sourceDimensions':source.size,'nativeWidth':246,'worldWidth':83.64,'noClipping':True,'travelAlphaInvariant':True,'miningEndpointsMatchIdle':True,'status':'pass'},indent=2))
 frames=[];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
 for n in range(0,180,3):
  board=Image.new('RGB',(1152,460),'#17272e');d=ImageDraw.Draw(board)
  for i,key in enumerate(['drive','steer-left','mine']):
   clip=next(c for c in clips if c['state']==key);j=n%clip['frameCount'];im=Image.open(R/clip['frameFiles'][j]).convert('RGBA');im.alpha_composite(Image.open(R/clip['effectFiles'][j]));ld=ImageDraw.Draw(im);alpha=round(90+165*(.5+.5*math.cos(n/30/.85*math.tau)));ld.ellipse((lamp[0]-2,lamp[1]-2,lamp[0]+2,lamp[1]+2),fill=(48,155,255,alpha));board.paste(im,(i*384,25),im);small=im.resize((131,131),Image.Resampling.LANCZOS);board.paste(small,(i*384+245,310),small);d.text((i*384+10,5),key+' / '+clip['phases'][j],font=font,fill='#cbdde4')
  frames.append(board)
 frames[0].save(R/'review/pilot.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=False);frames[0].save(R/'review/pilot.png');frames[30].save(R/'review/mining-active.png');print('6 south clips, 480 frames; geometry, grounded travel alpha and mining joins pass.')
if __name__=='__main__':main()
