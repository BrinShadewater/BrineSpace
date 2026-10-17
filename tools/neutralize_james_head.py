from pathlib import Path
import json,numpy as np
from PIL import Image,ImageDraw
S=Path('character/branforth-idle-led-east-neutral-v2');P=Path('character/branforth-idle-led-east-neutral-v3');P.mkdir(exist_ok=True);m=json.loads((S/'manifest.json').read_text());s=m['states'][0];y=np.indices((184,184))[0];lum=np.array([.2126,.7152,.0722]);preview=[];sheet=Image.new('RGB',(368,220),'#303b40');draw=ImageDraw.Draw(sheet)
for i,f in enumerate(s['frameFiles']):
 a=np.array(Image.open(S/f).convert('RGBA'));r=a[:,:,:3].astype(float);top=np.where(a[:,:,3]>127)[0].min();dy=y-top
 # Remove excess blue relative to a warm skin ramp, and neutralize cool magenta in hair/collar.
 head=(dy<34)&(a[:,:,3]>0);warm=(r[:,:,0]>r[:,:,1]*1.15)&(r[:,:,1]>r[:,:,2]*1.06);yellow=(r[:,:,1]>r[:,:,2]*1.5)&(r[:,:,0]>r[:,:,1]*1.05)
 mag=np.minimum(r[:,:,0]-r[:,:,1],r[:,:,2]-r[:,:,1]);weight=np.clip((mag-.5)/4,0,1)*head*(~yellow)
 l=r@lum;result=r+weight[:,:,None]*(l[:,:,None]-r)
 skin=head&warm&(~yellow)&(r[:,:,0]>95);excess=np.maximum(r[:,:,2]-(r[:,:,1]-.32*(r[:,:,0]-r[:,:,1])),0);shift=np.minimum(excess,12)*skin
 result[:,:,2]-=shift;result[:,:,1]+=shift*(lum[2]/lum[1])
 b=a.copy();b[:,:,:3]=np.clip(np.rint(result),0,255).astype('uint8');allowed=(weight>0)|(shift>0);assert np.array_equal(a[~allowed],b[~allowed]);assert np.array_equal(a[:,:,3],b[:,:,3]);dest=P/f;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest);bg=Image.new('RGB',(552,220),'#303b40')
 for h,x in [(148,0),(82,210),(54,350),(27,450)]:
  side=round(184*h/148);im=Image.fromarray(b).resize((side,side),Image.Resampling.BILINEAR);bg.paste(im,(x,20),im)
 preview.append(bg)
 if i==0:
  for j,(c,label) in enumerate([(a,'Previous'),(b,'Head and collar corrected')]):
   im=Image.fromarray(c);sheet.paste(im,(j*184,25),im);draw.text((j*184+3,5),label,fill='white')
s['provenance']['headCleanup']={'source':str(S),'method':'Fixed head/collar magenta suppression; warm-skin excess blue reduction capped12, luminance retained; yellow excluded.'};(P/'manifest.json').write_text(json.dumps(m,indent=2));(P/'validation.json').write_text(json.dumps({'frames':len(preview),'alphaExact':True,'outsideMaskExact':True,'timingUnchanged':True},indent=2));sheet.save(P/'comparison.png');preview[0].save(P/'review.gif',save_all=True,append_images=preview[1:],duration=[10*(round((i+1)*100/24)-round(i*100/24)) for i in range(len(preview))],loop=0)
p=Path('character/crew-idle-led-review-v9');p.mkdir(exist_ok=True);h=Path('character/crew-idle-led-review-v8/index.html').read_text().replace('../branforth-idle-led-east-neutral-v2/','../branforth-idle-led-east-neutral-v3/').replace('James residual magenta removed from fabric, silver and edges while retaining brightness, head and yellow patches. Raw video below is uncorrected.','James hair, face and collar colour cleanup added. Warm skin and yellow patches retained. Raw video below is uncorrected.');(p/'index.html').write_text(h);print('39 frames processed; alpha, outside-mask pixels and timing unchanged.')
