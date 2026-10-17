"""Rear helmet follows sagittal pitch without an incorrect sideways image roll."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
DONOR=ROOT/'character/veld-shared-helmet-v1/frames/idle-north/000.png'
COMPONENT=ROOT/'character/veld-shared-helmet-v1/fitted-north.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((P/'manifest.json').read_text());r=json.loads((P/'registration.json').read_text())
 idle=Image.open(DONOR).convert('RGBA');head=Image.open(COMPONENT).convert('RGBA');head.save(P/'sources/canonical-north-helmet.png')
 records=[];files=[];yy,xx=np.indices((256,256));rows={f['sourcePose']:f for f in r['frames']}
 for i,file in enumerate(m['states'][0]['frameFiles']):
  bare=np.array(Image.open(P/file).convert('RGBA'))
  if i in [0,5]:out=Image.new('RGBA',(256,256));out.paste(idle,(36,52))
  else:
   row=rows[i];hx,hy=row['headCrown'];projection=row['headProjection']
   # Shell foreshortens with the authored skull; collar retains its native thickness.
   height=round(8+(head.height-8)*projection)
   tilted=head.resize((head.width,height),Image.Resampling.LANCZOS)
   position=(round(hx-head.width/2),round(hy-7*projection))
   rgb=bare[:,:,:3].astype(float);warm=(rgb[:,:,0]>1.1*rgb[:,:,1])&(rgb[:,:,1]>1.1*rgb[:,:,2])
   erase=(abs(xx-hx)<18)&(yy>=hy-2)&(yy<hy+27)&warm
   a=bare.copy();a[erase]=0;out=Image.fromarray(a);out.alpha_composite(tilted,position)
   protected=position[1]+height;a=np.array(out);a[protected:]=bare[protected:];out=Image.fromarray(a)
   records.append({'frame':i,'headCrown':[hx,hy],'sagittalPitchDegrees':row['headTiltDegrees'],'imageRollDegrees':0,'headProjection':projection,'helmetHeight':height,'helmetWidth':head.width,'position':position,'protectedBodyFromY':protected,'nativeScale':1})
  dest=P/f'frames/helmet/recover-air-north/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest);files.append(dest.relative_to(P).as_posix())
 m.update(name='Veld north native helmet dry recovery',equipment='diving-helmet');m['states'][0]['frameFiles']=files
 (P/'helmet-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 (P/'helmet-registration.json').write_text(json.dumps({'donor':DONOR.relative_to(ROOT).as_posix(),'donorSha256':sha(DONOR),'componentAuthority':COMPONENT.relative_to(ROOT).as_posix(),'componentSha256':sha(COMPONENT),'nativeScale':1,'projection':'native width, sagittal height follows authored skull plus fixed8px collar;no sideways roll','frames':records},indent=2)+'\n')
 print('Rear helmet fitted without image roll; exact selected equipped idle endpoints')
if __name__=='__main__':main()
