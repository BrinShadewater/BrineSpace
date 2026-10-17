from pathlib import Path
import json,copy,hashlib,math,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;R=P.parent.parent
SOURCE=R/'character/krusher-marsh-motion-fit-v1'
for folder in ['frames','masks','review','native']:(P/folder).mkdir(parents=True,exist_ok=True)
m=json.loads((SOURCE/'manifest.json').read_text());fit=json.loads((SOURCE/'verification.json').read_text());fits={(t['state'],t['frame']):t for t in fit['records']}
yy,xx=np.indices((184,184));target=np.array([82.,124.,128.]);luma=np.array([.2126,.7152,.0722]);records=[];frames={};originals={};checks=0;errors=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for state in m['states']:
 key=state['id'];(P/'frames'/key).mkdir(exist_ok=True);frames[key]=[];originals[key]=[];files=[]
 for i,relative in enumerate(state['frameFiles']):
  source=SOURCE/relative;im=Image.open(source).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(float)
  registration=fits[(key,i)];dy=registration['headShift'][1]
  fit_allowed=np.array(Image.open(SOURCE/registration['mask']))>0
  # Only preserved upper suit pixels. Head RGB and lower tool/utility colours excluded.
  blue=(rgb[:,:,1]>rgb[:,:,2]*1.25)&(rgb[:,:,0]<rgb[:,:,1]*1.12)&(rgb[:,:,1]>35)
  mask=blue&(a[:,:,3]>0)&(~fit_allowed)&(yy>=44+dy)&(yy<72+dy)
  gain=np.minimum(1.15,(rgb@luma)/(target@luma));colour=np.rint(gain[:,:,None]*target).astype('uint8')
  out=a.copy();out[mask,:3]=colour[mask]
  checks+=3
  if not np.array_equal(a[~mask],out[~mask]):errors.append('outside:'+key+str(i))
  if not np.array_equal(a[:,:,3],out[:,:,3]):errors.append('alpha:'+key+str(i))
  if not np.array_equal(a[yy>=85+dy],out[yy>=85+dy]):errors.append('tools:'+key+str(i))
  file=f'frames/{key}/{i:03}.png';image=Image.fromarray(out);image.save(P/file);files.append(file)
  maskfile=f'masks/{key}-{i:03}.png';Image.fromarray(mask.astype('uint8')*255).save(P/maskfile)
  records.append({'state':key,'frame':i,'source':source.relative_to(R).as_posix(),'sourceHash':sha(source),'output':file,'outputHash':sha(P/file),'markingMask':maskfile,'toolProtectionFromRow':85+dy,'changedPixels':int(np.any(a!=out,axis=2).sum())})
  frames[key].append(image);originals[key].append(im)
 state['frameFiles']=files
 images=frames[key];images[0].save(P/f'review/{key}.png',save_all=True,append_images=images[1:],duration=state['frameDurationsMs'],loop=0,disposal=1,blend=0)
m['name']='Krusher Dom / Marsh body / matte muted cyan trial';m['status']='unselected four-direction idle/walk candidate'
(P/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
report={'checks':checks,'errors':errors,'sourceManifest':'character/krusher-marsh-motion-fit-v1/manifest.json','sourceManifestHash':sha(SOURCE/'manifest.json'),'fitVerificationHash':sha(SOURCE/'verification.json'),'targetRGB':[82,124,128],'maxShadeGain':1.15,'records':records,'scope':'Upper suit olive-to-muted-cyan mask; source head, tools, alpha and clocks preserved'}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
font=lambda n:ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),n)
def board(key,index):
 im=Image.new('RGB',(800,600),'#272b2e');d=ImageDraw.Draw(im)
 d.text((20,12),'KRUSHER / MARSH BODY / MUTED CYAN TEST',font=font(29),fill='white')
 for col,(title,image) in enumerate([('Before / original olive',originals[key][index]),('After / muted cyan',frames[key][index])]):
  d.text((25+col*390,52),title,font=font(23),fill='white')
  tile=image.resize((368,368),Image.Resampling.NEAREST);im.paste(tile,(10+col*390,83),tile)
  small=image.resize((92,92),Image.Resampling.LANCZOS);im.paste(small,(150+col*390,453),small)
 d.text((20,557),key+' / tools and source clock preserved / unselected',font=font(22),fill='#bdcdd0')
 return im
for state in m['states']:board(state['id'],0).save(P/f"review/{state['id']}-comparison.png")
comparison=Image.new('RGB',(800,600),'#272b2e');d=ImageDraw.Draw(comparison)
d.text((20,12),'KRUSHER DOM / TWO CYAN BODY OPTIONS',font=font(29),fill='white')
for col,(label,image) in enumerate([('Bill / current candidate',Image.open(R/'character/krusher-runtime-candidate-v1/frames/bare/idle-south/000.png').convert('RGBA')),('Marsh / pale body test',frames['idle-south'][0])]):
 d.text((25+col*390,52),label,font=font(23),fill='white');tile=image.resize((368,368),Image.Resampling.NEAREST);comparison.paste(tile,(10+col*390,83),tile)
 small=image.resize((92,92),Image.Resampling.LANCZOS);comparison.paste(small,(150+col*390,453),small)
d.text((20,557),'Same native head density and physical ruler / separate source body silhouettes',font=font(21),fill='#bdcdd0');comparison.save(P/'review/bill-marsh-comparison.png')
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','800x600','-framerate','60','-i','-','-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p',str(P/'review/motion-preview.mp4')],stdin=subprocess.PIPE)
for state in m['states']:
 ends=np.cumsum(state['frameDurationsMs'])
 for j in range(math.ceil(ends[-1]*60/1000)):
  index=min(int(np.searchsorted(ends,j*1000/60,side='right')),len(ends)-1);proc.stdin.write(board(state['id'],index).tobytes())
proc.stdin.close();assert proc.wait()==0
print(json.dumps({'frames':len(records),'checks':checks,'errors':errors,'changedPixelsRange':[min(t['changedPixels'] for t in records),max(t['changedPixels'] for t in records)]}));assert not errors
