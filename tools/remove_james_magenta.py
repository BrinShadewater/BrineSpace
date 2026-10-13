from pathlib import Path
import json,numpy as np
from PIL import Image,ImageDraw
S=Path('character/branforth-idle-led-east-bill-match-v1');P=Path('character/branforth-idle-led-east-neutral-v2');P.mkdir(exist_ok=True);m=json.loads((S/'manifest.json').read_text());s=m['states'][0];y=np.indices((184,184))[0];lum=np.array([.2126,.7152,.0722]);preview=[];counts=[];sheet=Image.new('RGB',(368,220),'#303b40');draw=ImageDraw.Draw(sheet)
for i,f in enumerate(s['frameFiles']):
 a=np.array(Image.open(S/f).convert('RGBA'));r=a[:,:,:3].astype(float);top=np.where(a[:,:,3]>127)[0].min();mag=np.minimum(r[:,:,0]-r[:,:,1],r[:,:,2]-r[:,:,1]);w=np.clip((mag-1)/5,0,1)*np.clip((y-top-27)/5,0,1)*(a[:,:,3]>0);l=r@lum;neutral=np.repeat(l[:,:,None],3,axis=2);b=a.copy();b[:,:,:3]=np.clip(np.rint(r+w[:,:,None]*(neutral-r)),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[w==0],b[w==0]);counts.append(int((w>0).sum()));dest=P/f;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest);bg=Image.new('RGB',(552,220),'#303b40')
 for h,x in [(148,0),(82,210),(54,350),(27,450)]:
  side=round(184*h/148);im=Image.fromarray(b).resize((side,side),Image.Resampling.BILINEAR);bg.paste(im,(x,20),im)
 preview.append(bg)
 if i==0:
  for j,(c,label) in enumerate([(a,'Previous'),(b,'Magenta removed')]):
   im=Image.fromarray(c);sheet.paste(im,(j*184,25),im);draw.text((j*184+5,5),label,fill='white')
s['provenance']['magentaCleanup']={'source':str(S),'method':'Fixed body-only magenta chroma suppression toward equal-luminance grey, including silver and alpha edges; head and yellow excluded.'};(P/'manifest.json').write_text(json.dumps(m,indent=2));(P/'validation.json').write_text(json.dumps({'frames':len(preview),'changedRegionPixelsRange':[min(counts),max(counts)],'alphaExact':True,'outsideMaskExact':True,'timingUnchanged':True,'luminancePreservedBeforeRounding':True},indent=2));sheet.save(P/'comparison.png');preview[0].save(P/'review.gif',save_all=True,append_images=preview[1:],duration=[10*(round((i+1)*100/24)-round(i*100/24)) for i in range(len(preview))],loop=0)
p=Path('character/crew-idle-led-review-v8');p.mkdir(exist_ok=True);h=Path('character/crew-idle-led-review-v7/index.html').read_text().replace('../branforth-idle-led-east-bill-match-v1/','../branforth-idle-led-east-neutral-v2/').replace('James neutral suit fabric matched to Bill using fixed clip-wide colour gains. Head and yellow patches preserved; motion unchanged. Raw video below is uncorrected.','James residual magenta removed from fabric, silver and edges while retaining brightness, head and yellow patches. Raw video below is uncorrected.');(p/'index.html').write_text(h);print('39 frames; alpha, outside-mask pixels and timing unchanged.')
