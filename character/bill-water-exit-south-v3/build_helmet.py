from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,copy,hashlib
P=Path(__file__).resolve().parent;R=P.parent;F=P/'helmet/frames/swim-land-south';F.mkdir(parents=True,exist_ok=True)
e=json.loads((P/'exit-review.json').read_text(encoding='utf-8'));registrations=e['registrations'];fits=[];frames=[]
heads={0:R/'bill-shared-helmet-south-v1/fitted-helmet.png',35:R/'bill-swim-helmet-south-coherent-v1/components/001.png',65:R/'bill-swim-helmet-south-coherent-v1/components/002.png',85:R/'bill-swim-helmet-south-coherent-v1/sources/canonical-head.png'}
head_images={key:Image.open(path).convert('RGBA') for key,path in heads.items()}
for i in range(8):
 bare=Image.open(P/f'bare/frames/swim-land-south/{i:03}.png').convert('RGBA');b=np.array(bare);yy,xx=np.indices(b.shape[:2])
 if i in [0,7]:
  path=R/('bill-swim-helmet-south-coherent-v1/frames/swim-south/000.png' if i==0 else 'bill-shared-helmet-runtime-v2/frames/idle-south/000.png');source=Image.open(path).convert('RGBA');shift=(56,72) if i==0 else (68,52)
  out=Image.new('RGBA',(320,352));out.paste(source,shift);assert out.crop((shift[0],shift[1],shift[0]+source.width,shift[1]+source.height)).tobytes()==source.tobytes()
 else:
  x,y=registrations[i-1]['crown'];pitch={1:85,2:65,3:35,4:0,5:0,6:0}[i];head=head_images[pitch]
  offset={0:-9,35:-6,65:-5,85:-4}[pitch];position=(x-head.width//2,y+offset)
  end=position[1]+head.height  # Never erase original collar/chest below shell coverage.
  erase=(xx>=x-12)&(xx<=x+12)&(yy>=y-2)&(yy<end)
  # Prone face/beard can extend below the shell; remove only its warm head pixels,
  # never a rectangular collar/chest band.
  rgb=b[:,:,:3].astype(float)
  remnant=(pitch>0)&(abs(xx-x)<=8)&(yy>=end)&(yy<y+40)&(b[:,:,3]>0)&(rgb[:,:,0]>rgb[:,:,1]*1.2)&(rgb[:,:,1]>rgb[:,:,2]*1.2)
  erase|=remnant
  a=b.copy();a[erase]=0;out=Image.fromarray(a);out.alpha_composite(head,position);a=np.array(out)
  foreground=(b[:,:,3]>0)&((xx<x-12)|(xx>x+12))&(yy<end);a[foreground]=b[foreground]
  mask=Image.new('L',(320,352));mask.paste(head.getchannel('A'),position);allowed=erase|(np.array(mask)>0)
  protected=max(end,y+40 if pitch>0 else end)
  assert np.array_equal(a[~allowed],b[~allowed]);assert np.array_equal(a[foreground],b[foreground]);assert np.array_equal(a[yy>=protected],b[yy>=protected])
  out=Image.fromarray(a);fits.append(dict(pose=i,crown=[x,y],pitchDegrees=pitch,source=heads[pitch].relative_to(R).as_posix(),sourceSHA256=hashlib.sha256(heads[pitch].read_bytes()).hexdigest(),shellPosition=position,nativeShellSize=head.size,scale=1,rotation=0,eraseBox=[x-12,y-2,x+13,end],proneHeadRemnantPixels=int(np.count_nonzero(remnant)),foregroundOutsideCentralHeadExact=True,bodyOutsideAllowedMaskExact=True,protectedBodyFromY=protected,protectedBodyExact=True))
 out.save(F/f'{i:03}.png');frames.append(out)
m=copy.deepcopy(json.loads((P/'bare/manifest.json').read_text(encoding='utf-8')));m['name']='Bill South water exit canonical helmet pitch candidate';m['equipment']='diving-helmet';m['states'][0]['provenance']='Exact selected idle/swim endpoints; same canonical upright helmet and existing independently authored35/65/85degree shell components, translation only, no new rotations/rescaling/recolour. Original bare body/foreground protected. Source-only fitting; native/motion/master acceptance pending.'
(P/'helmet/manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
times=m['states'][0]['frameDurationsMs'];frames[0].save(P/'helmet/source-exit.png',save_all=True,append_images=frames[1:],duration=times,loop=1,disposal=0,blend=0)
with Image.open(P/'helmet/source-exit.png') as ap:
 assert ap.n_frames==8 and ap.info['loop']==1
 for i,im in enumerate(frames):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==times[i]
board=Image.new('RGB',(2560,760),'#182932');d=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
 for i in range(8):
  im=Image.open(P/f'{gear}/frames/swim-land-south/{i:03}.png').convert('RGBA');board.paste(im,(i*320,row*380+24),im);d.text((i*320+6,row*380+5),f'{gear} {i}',fill='white')
board.save(P/'paired-exit-contact.png')
board=Image.new('RGB',(1680,660),'#182932');d=ImageDraw.Draw(board)
for i,r in enumerate(fits):
 x,y=r['crown']
 for row,gear in enumerate(['bare','helmet']):
  im=Image.open(P/f'{gear}/frames/swim-land-south/{r["pose"]:03}.png').convert('RGBA');crop=im.crop((x-35,y-12,x+35,y+65)).resize((280,308),Image.Resampling.NEAREST);board.paste(crop,(i*280,row*330+22),crop);d.text((i*280+5,row*330+4),f'{gear} {r["pose"]} pitch{r["pitchDegrees"]}',fill='white')
board.save(P/'helmet-neck-details.png')
report=dict(fittings=fits,pairedFrames=16,decodedAPNGFramesExact=16,timelineMs=sum(times),finiteLoopCount=1,helmetEndpointsExact=True,scope='Equipment packaging with existing canonical authored pitch resources, no new body poses or normal selection. Protected bare body pixels; full neck/perspective/material/motion/native acceptance pending.',visualReview='Pending both complete and seven neck-pair board inspection.')
(P/'helmet-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(pairedFrames=16,protectedFits=len(fits),decodedExact=16,finiteLoop=1,pitchResources=4)))
