from pathlib import Path
import copy,json,hashlib,math,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;R=P.parent.parent
for name in ['frames','masks','review','native']:(P/name).mkdir(parents=True,exist_ok=True)
active=json.loads((R/'character/ACTIVE_ASSETS.json').read_text())
base=R/active['locomotionOverrides']['branforth'];manifest=json.loads(base.read_text())
headpath=R/'character/krusher-bill-base-test-v2/sources/south-head-native.png';head=Image.open(headpath).convert('RGBA')
yy,xx=np.indices((184,184));records=[];outputs={};originals={};checks=0;errors=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def registration(a):
 top=int(np.where((a[:,:,3]>180)&(yy<44)&(xx>60)&(xx<125))[0].min())
 ys,xs=np.where((a[:,:,3]>180)&(yy>=top)&(yy<top+19)&(xx>60)&(xx<125))
 return top,round((int(xs.min())+int(xs.max()))/2)
selected=[copy.deepcopy(s) for s in manifest['states'] if s['id'] in ['idle-south','walk-south']]
idle=next(s for s in selected if s['id']=='idle-south')
reference=np.array(Image.open(base.parent/idle['frameFiles'][0]).convert('RGBA'));base_top,base_axis=registration(reference)
for state in selected:
 key=state['id'];(P/'frames'/key).mkdir(exist_ok=True);outputs[key]=[];originals[key]=[];newfiles=[]
 for i,relative in enumerate(state['frameFiles']):
  source=(base.parent/relative).resolve();original=Image.open(source).convert('RGBA');a=np.array(original)
  top,axis=registration(a);dy=top-base_top;dx=axis-base_axis
  collar=((yy>=49+dy)&(yy<54+dy))|((yy>=45+dy)&(yy<54+dy)&((xx<axis-8)|(xx>axis+8)))
  collar&=a[:,:,3]>0;allowed=(yy<54+dy)&(~collar)
  layer=a.copy();layer[yy<54+dy]=0;candidate=Image.fromarray(layer)
  anchor=[axis-head.width//2,48+dy-head.height];candidate.paste(head,tuple(anchor))
  out=np.array(candidate);out[collar]=a[collar];candidate=Image.fromarray(out)
  checks+=2
  if not np.array_equal(a[~allowed],out[~allowed]):errors.append('body:'+key+str(i))
  if not np.array_equal(a[collar],out[collar]):errors.append('collar:'+key+str(i))
  file=f'frames/{key}/{i:03}.png';candidate.save(P/file);newfiles.append(file)
  mask=f'masks/{key}-{i:03}.png';Image.fromarray(allowed.astype('uint8')*255).save(P/mask)
  records.append({'state':key,'frame':i,'source':source.relative_to(R).as_posix(),'sourceHash':sha(source),'output':file,'outputHash':sha(P/file),'mask':mask,'headPaste':anchor,'headShift':[dx,dy]})
  outputs[key].append(candidate);originals[key].append(original)
 state['frameFiles']=newfiles
 frames=outputs[key];frames[0].save(P/f'review/{key}.png',save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0,disposal=1,blend=0)
out_manifest=copy.deepcopy(manifest);out_manifest['states']=selected;out_manifest['name']='Krusher Dom / James body moving neck-fit study';out_manifest['status']='unselected; original suit colours retained'
(P/'manifest.json').write_text(json.dumps(out_manifest,indent=2)+'\n')
report={'checks':checks,'errors':errors,'baseManifest':base.relative_to(R).as_posix(),'baseManifestHash':sha(base),'headSource':headpath.relative_to(R).as_posix(),'headHash':sha(headpath),'records':records,'scope':'South idle/walk head fit with original James suit colours and clocks; protected collar/body pixels; no helmet or station integration'}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
font=lambda n:ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),n)
def board(key,index):
 im=Image.new('RGB',(800,600),'#272b2e');d=ImageDraw.Draw(im)
 d.text((20,12),'KRUSHER / JAMES BODY / MOVING NECK FIT',font=font(29),fill='white')
 for col,(title,frame) in enumerate([('Original James',originals[key][index]),('Krusher head study',outputs[key][index])]):
  d.text((25+col*390,52),title,font=font(23),fill='white')
  tile=frame.resize((368,368),Image.Resampling.NEAREST);im.paste(tile,(10+col*390,83),tile)
  small=frame.resize((92,92),Image.Resampling.LANCZOS);im.paste(small,(150+col*390,453),small)
 d.text((20,557),key+' / source colours and timing retained / unselected',font=font(22),fill='#bdcdd0')
 return im
for state in selected:
 key=state['id'];board(key,0).save(P/f'review/{key}-comparison.png')
 samples=Image.new('RGB',(1200,960),'#272b2e')
 for j,i in enumerate(np.linspace(0,len(outputs[key])-1,12,dtype=int)):
  tile=outputs[key][i].crop((65,15,120,65)).resize((220,200),Image.Resampling.NEAREST)
  samples.paste(tile,(j%5*240,j//5*240),tile)
  ImageDraw.Draw(samples).text((j%5*240+8,j//5*240+204),f'frame {i}',font=font(24),fill='white')
 samples.save(P/f'review/{key}-neck-samples.png')
video=P/'review/motion-preview.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','800x600','-framerate','60','-i','-','-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p',str(video)],stdin=subprocess.PIPE)
chapters=[];clock=0
for state in selected:
 ends=np.cumsum(state['frameDurationsMs']);total=int(ends[-1]);chapters.append({'state':state['id'],'sourceStartMs':clock,'sourceDurationMs':total})
 for j in range(math.ceil(total*60/1000)):
  i=min(int(np.searchsorted(ends,j*1000/60,side='right')),len(ends)-1);proc.stdin.write(board(state['id'],i).tobytes())
 clock+=total
proc.stdin.close();assert proc.wait()==0
(P/'review/preview.json').write_text(json.dumps({'chapters':chapters,'sourceDurationMs':clock,'videoHash':sha(video),'scope':'Source-derived 60fps preview, not native continuous-motion capture'},indent=2)+'\n')
print(json.dumps({'frames':len(records),'checks':checks,'errors':errors,'headShifts':sorted(set(tuple(r['headShift']) for r in records)),'videoBytes':video.stat().st_size}));assert not errors
