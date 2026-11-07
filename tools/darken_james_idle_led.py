from pathlib import Path
import json,numpy as np
from PIL import Image,ImageDraw
S=Path('character/branforth-idle-led-east-loop-v1');P=Path('character/branforth-idle-led-east-darker-v1');P.mkdir(exist_ok=True);m=json.loads((S/'manifest.json').read_text());s=m['states'][0];y=np.indices((184,184))[0];preview=[];sheet=Image.new('RGB',(368,220),'#303b40');dr=ImageDraw.Draw(sheet)
for i,f in enumerate(s['frameFiles']):
 a=np.array(Image.open(S/f).convert('RGBA'));rgb=a[:,:,:3].astype(float);v=rgb.mean(2);w=np.clip((28-np.ptp(rgb,axis=2))/12,0,1)*np.clip((105-v)/25,0,1)*np.clip((v-15)/12,0,1)*np.clip((y-53)/9,0,1)*(a[:,:,3]>16);b=a.copy();b[:,:,:3]=np.clip(np.rint(rgb*(1-.07*w[:,:,None])),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[w==0],b[w==0]);dest=P/f;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest)
 bg=Image.new('RGB',(552,220),'#303b40')
 for h,x in [(148,0),(82,210),(54,350),(27,450)]:
  side=round(184*h/148);im=Image.fromarray(b).resize((side,side),Image.Resampling.BILINEAR);bg.paste(im,(x,20),im)
 preview.append(bg)
 if i==0:
  for j,(c,label) in enumerate([(a,'Previous'),(b,'Suit slightly darker')]):
   im=Image.fromarray(c);sheet.paste(im,(j*184,25),im);dr.text((j*184+5,5),label,fill='white')
s['provenance']['colourPass']={'source':str(S),'neutralFabricGain':.93,'method':'Fixed feathered neutral fabric mask; head and saturated yellow excluded, bright silver protected.'};(P/'manifest.json').write_text(json.dumps(m,indent=2));(P/'validation.json').write_text(json.dumps({'frames':len(preview),'alphaExact':True,'outsideMaskExact':True,'timingUnchanged':True,'fabricGain':.93},indent=2));preview[0].save(P/'review.gif',save_all=True,append_images=preview[1:],duration=[10*(round((i+1)*100/24)-round(i*100/24)) for i in range(len(preview))],loop=0);sheet.save(P/'comparison.png')
p=Path('character/crew-idle-led-review-v6');p.mkdir(exist_ok=True);h=Path('character/crew-idle-led-review-v5/index.html').read_text().replace('../branforth-idle-led-east-loop-v1/review.gif','../branforth-idle-led-east-darker-v1/review.gif').replace('Reduced arm swing retry.39 frames /1.625seconds, source frames27-65. Raw full clip below.','James suit fabric darkened7%; head, yellow accents and motion retained. Raw video below is the uncorrected source.');h += '<img src="../branforth-idle-led-east-darker-v1/comparison.png">';(p/'index.html').write_text(h);print('39 frames; alpha, outside-mask pixels and timing verified unchanged.')
