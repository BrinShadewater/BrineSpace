"""Fit the actual selected east helmet component at one native ruler."""
from pathlib import Path
import json,math,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
DONOR=ROOT/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((P/'manifest.json').read_text());r=json.loads((P/'registration.json').read_text())
 idle=Image.open(DONOR).convert('RGBA');head=idle.crop((82,17,116,55));head.save(P/'sources/canonical-east-helmet.png')
 records=[];files=[];yy,xx=np.indices((256,256))
 rows={f['sourcePose']:f for f in r['frames']}
 for i,file in enumerate(m['states'][0]['frameFiles']):
  bare=np.array(Image.open(P/file).convert('RGBA'))
  if i in [0,5]:out=Image.new('RGBA',(256,256));out.paste(idle,(36,52))
  else:
   row=rows[i];hx,hy=row['headCrown'];angle=row['headTiltDegrees'];tilted=head.rotate(-angle,resample=Image.Resampling.BICUBIC,expand=True)
   rad=math.radians(angle);dx=19-head.width/2;dy=-head.height/2
   ax=tilted.width/2+math.cos(rad)*dx-math.sin(rad)*dy;ay=tilted.height/2+math.sin(rad)*dx+math.cos(rad)*dy
   position=(round(hx-ax),round(hy-7-ay))
   rgb=bare[:,:,:3].astype(float);warm=(rgb[:,:,0]>1.1*rgb[:,:,1])&(rgb[:,:,1]>1.1*rgb[:,:,2])
   erase=(xx>=hx-20)&(xx<=hx+21)&(yy>=hy-2)&(yy<hy+27)&warm
   a=bare.copy();a[erase]=0;out=Image.fromarray(a);out.alpha_composite(tilted,position)
   protected=hy+34;a=np.array(out);a[protected:]=bare[protected:];out=Image.fromarray(a)
   records.append({'frame':i,'headCrown':[hx,hy],'tiltDegrees':angle,'position':position,'protectedBodyFromY':protected,'nativeScale':1})
  dest=P/f'frames/helmet/recover-air-east/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest);files.append(dest.relative_to(P).as_posix())
 m.update(name='Veld east native helmet dry recovery',equipment='diving-helmet');m['states'][0]['frameFiles']=files
 (P/'helmet-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 (P/'helmet-registration.json').write_text(json.dumps({'donor':DONOR.relative_to(ROOT).as_posix(),'donorSha256':sha(DONOR),'sourceBox':[82,17,116,55],'nativeScale':1,'frames':records},indent=2)+'\n')
 print('Native master helmet fitted; exact selected equipped idle endpoints')
if __name__=='__main__':main()
