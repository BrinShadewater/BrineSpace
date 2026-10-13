from pathlib import Path
import json,numpy as np
from PIL import Image,ImageDraw
Y=np.indices((184,184))[0];L=np.array([.2126,.7152,.0722]);reports={}
def sample(a):
 r=a[:,:,:3].astype(float);v=r.mean(2);return (a[:,:,3]>240)&(Y>=62)&(Y<153)&(np.ptp(r,axis=2)<30)&(v>25)&(v<90)
for who,ef in [('branforth','branforth-idle-led-east-neutral-v3')]:
 S=Path('character')/(who+'-idle-led-west-loop-v2');E=Path('character')/ef;P=Path('character')/(who+'-idle-led-west-matched-v2');P.mkdir(exist_ok=True);m=json.loads((S/'manifest.json').read_text());s=m['states'][0];em=json.loads((E/'manifest.json').read_text());arr=[np.array(Image.open(S/f).convert('RGBA')) for f in s['frameFiles']];ea=[np.array(Image.open(E/f).convert('RGBA')) for f in em['states'][0]['frameFiles']];base=np.median(np.concatenate([a[:,:,:3][sample(a)] for a in arr]),axis=0);target=np.median(np.concatenate([a[:,:,:3][sample(a)] for a in ea]),axis=0);gain=target/base;preview=[];sheet=Image.new('RGB',(552,220),'#303b40');draw=ImageDraw.Draw(sheet)
 for i,(a,f) in enumerate(zip(arr,s['frameFiles'])):
  r=a[:,:,:3].astype(float);v=r.mean(2);w=np.clip((40-np.ptp(r,axis=2))/12,0,1)*np.clip((110-v)/20,0,1)*np.clip((v-12)/13,0,1)*np.clip((Y-53)/9,0,1)*(a[:,:,3]>16);result=r*(1+w[:,:,None]*(gain-1));allowed=w>0
  if who=='branforth':
   top=np.where(a[:,:,3]>127)[0].min();dy=Y-top;yellow=(r[:,:,1]>r[:,:,2]*1.5)&(r[:,:,0]>r[:,:,1]*1.05);mag=np.minimum(result[:,:,0]-result[:,:,1],result[:,:,2]-result[:,:,1]);wm=np.clip((mag-1)/5,0,1)*(a[:,:,3]>0)*(~yellow);lum=result@L;result+=wm[:,:,None]*(lum[:,:,None]-result);allowed|=wm>0
   skin=(dy<34)&(a[:,:,3]>0)&(~yellow)&(r[:,:,0]>95)&(r[:,:,0]>r[:,:,1]*1.15)&(r[:,:,1]>r[:,:,2]*1.06);shift=np.minimum(np.maximum(r[:,:,2]-(r[:,:,1]-.32*(r[:,:,0]-r[:,:,1])),0),12)*skin;result[:,:,2]-=shift;result[:,:,1]+=shift*(L[2]/L[1]);allowed|=shift>0
  b=a.copy();b[:,:,:3]=np.clip(np.rint(result),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[~allowed],b[~allowed]);dest=P/f;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest);bg=Image.new('RGB',(552,220),'#303b40')
  for height,x in [(148,0),(82,210),(54,350),(27,450)]:
   side=round(184*height/148);im=Image.fromarray(b).resize((side,side),Image.Resampling.BILINEAR);bg.paste(im,(x,20),im)
  preview.append(bg)
  if i==0:
   for j,(c,label) in enumerate([(ea[0],'Accepted east'),(a,'West before'),(b,'West matched')]):
    im=Image.fromarray(c);sheet.paste(im,(j*184,25),im);draw.text((j*184+5,5),label,fill='white')
 s['provenance']['colourMatch']={'reference':str(E),'fixedGain':gain.tolist(),'method':'Fixed neutral fabric gain, James magenta cleanup follows accepted east method; no geometry/timing edits.'};(P/'manifest.json').write_text(json.dumps(m,indent=2));sheet.save(P/'comparison.png');preview[0].save(P/'review.gif',save_all=True,append_images=preview[1:],duration=[10*(round((i+1)*100/24)-round(i*100/24)) for i in range(len(arr))],loop=0);reports[who]={'frames':len(arr),'fixedGain':gain.tolist(),'targetMedian':target.tolist(),'alphaExact':True,'outsideMaskExact':True,'timingUnchanged':True};(P/'validation.json').write_text(json.dumps(reports[who],indent=2))
p=Path('character/crew-idle-led-west-review-v3');p.mkdir(exist_ok=True);h='<meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#303b40;color:white;font:18px system-ui;max-width:1100px;margin:24px auto}img{max-width:100%}</style><h1>West loops and east colour matching</h1><p>Original source speed. No geometry changes or invented frames. Candidate only.</p>'
for who in ['branforth']:h+='<h2>'+who.title()+'</h2><img src="../'+who+'-idle-led-west-matched-v2/review.gif"><img src="../'+who+'-idle-led-west-matched-v2/comparison.png">'
(p/'index.html').write_text(h);print(reports)
