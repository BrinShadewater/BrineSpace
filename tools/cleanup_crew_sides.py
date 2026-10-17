from pathlib import Path
import json,shutil,re
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import map_coordinates
S=Path('character/crew-polish-v1');P=Path('character/crew-side-cleanup-v1');P.mkdir(exist_ok=True);report={};y,x=np.indices((184,184),dtype=float);tracks=[];sheet=Image.new('RGB',(1104,880),'#303b40');dr=ImageDraw.Draw(sheet)
for col,who in enumerate(['bill','veld','branforth']):
 m=json.loads((S/who/'manifest.json').read_text());runtime=Path('character/crew-runtime-matte-v1')/who;rm=json.loads((runtime/'manifest.json').read_text())
 for s in m['states']:
  d=s['id'].split('-')[-1];files=[];source=s['frameFiles'];root=S/who
  if who=='branforth' and s['id'] in ['walk-east','walk-west']:
   rs=next(z for z in rm['states'] if z['id']==s['id']);source=rs['frameFiles'];root=runtime;assert s['frameDurationsMs']==rs['frameDurationsMs']
  for n,f in enumerate(source):
   rel=f"frames/{s['id']}/{n:03}.png";dest=P/who/rel;dest.parent.mkdir(parents=True,exist_ok=True)
   if who=='bill' and s['id'] in ['walk-east','walk-west']:
    a=np.array(Image.open(root/f).convert('RGBA'));top=np.where(a[:,:,3]>127)[0].min();dy=y-top;cx=np.median(x[(a[:,:,3]>127)&(dy<8)])
    # Compress lower face/beard vertically by at most two pixels, taper into neck.
    shift=np.interp(dy,[0,12,19,23,27,184],[0,0,2,2,0,0]);region=(dy>12)&(dy<27)&(abs(x-cx)<14)
    v=a.astype(float)/255;v[:,:,:3]*=v[:,:,3:4];z=np.stack([map_coordinates(v[:,:,k],[y+shift,x],order=3,mode='constant') for k in range(4)],2);al=z[:,:,3:4];z[:,:,:3]=np.divide(z[:,:,:3],al,out=np.zeros_like(z[:,:,:3]),where=al>0);b=np.clip(np.rint(z*255),0,255).astype('uint8');b[~region]=a[~region];assert np.array_equal(b[~region],a[~region]);Image.fromarray(b).save(dest)
   else:shutil.copyfile(root/f,dest)
   files.append(rel)
  s['frameFiles']=files
  if who=='bill' and s['id'] in ['walk-east','walk-west']:s['provenance']={'source':str(root),'method':'Fixed lower-face/beard compression, max2px; crown and all pixels outside local region exact.'}
  if who=='branforth' and s['id'] in ['walk-east','walk-west']:s['provenance']={'source':str(root),'method':'Exact accepted runtime source copies; removes recent scale and torso processing.'}
  report[who+'-'+s['id']]={'frames':len(files),'timingUnchanged':True,'source':str(root)}
 (P/who/'manifest.json').write_text(json.dumps(m,indent=2))
 for row,d in enumerate(['south','east','north','west']):
  idle=next(s for s in m['states'] if s['id']=='idle-'+d);w=next(s for s in m['states'] if s['id']=='walk-'+d)
  tracks.append(dict(label=who.title()+' '+d,row=row,col=col,idle=who+'/'+idle['frameFiles'][0],idleFiles=[who+'/'+f for f in idle['frameFiles']],idleDurations=idle['frameDurationsMs'],files=[who+'/'+f for f in w['frameFiles']],durations=w['frameDurationsMs']))
  for k,s in enumerate([idle,w]):
   im=Image.open(P/who/s['frameFiles'][0]);sheet.paste(im,(col*368+k*184,row*220+25),im)
  dr.text((col*368+5,row*220+3),who+' '+d+' idle / walk',fill='white')
sheet.save(P/'contact.png');(P/'validation.json').write_text(json.dumps(report,indent=2));h=(S/'index.html').read_text();h=re.sub(r'const tracks=.*?;let ready=',lambda _:'const tracks='+json.dumps(tracks)+';let ready=',h);h=h.replace('Crew polish review','Crew side cleanup');h=re.sub(r'<p>.*?</p>','<p>James side walks restored from accepted frames without extra resizing. Bill lower beard/face shortened locally; crown and body unchanged. Preview only.</p>',h,count=1);(P/'index.html').write_text(h);print('Packaged 608 frames; 104 James source copies and 136 local Bill beard corrections; timings retained.')
