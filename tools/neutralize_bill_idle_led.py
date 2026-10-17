from pathlib import Path
import json,numpy as np
from PIL import Image,ImageDraw
S=Path('character/bill-idle-led-east-loop-v2');P=Path('character/bill-idle-led-east-neutral-v1');P.mkdir(exist_ok=True);m=json.loads((S/'manifest.json').read_text());s=m['states'][0];arr=[np.array(Image.open(S/f).convert('RGBA')) for f in s['frameFiles']];ir=Path('character/crew-idle-match-v1/bill');im=json.loads((ir/'manifest.json').read_text());idle=np.array(Image.open(ir/next(t for t in im['states'] if t['id']=='idle-east')['frameFiles'][0]).convert('RGBA'));y=np.indices((184,184))[0];lum=np.array([.2126,.7152,.0722])
def mask(a):
 r=a[:,:,:3].astype(float);v=r.mean(2);return (a[:,:,3]>240)&(y>60)&(y<153)&(np.ptp(r,axis=2)<25)&(v>25)&(v<100)
base=np.median(np.concatenate([a[:,:,:3][mask(a)] for a in arr]),axis=0);target=np.median(idle[:,:,:3][mask(idle)],axis=0);delta=(target-target@lum)-(base-base@lum);delta*=.8
preview=[];sheet=Image.new('RGB',(552,220),'#303b40');dr=ImageDraw.Draw(sheet)
for i,(a,f) in enumerate(zip(arr,s['frameFiles'])):
 r=a[:,:,:3].astype(float);v=r.mean(2);w=np.clip((30-np.ptp(r,axis=2))/12,0,1)*np.clip((y-53)/9,0,1)*(a[:,:,3]>16);b=a.copy();b[:,:,:3]=np.clip(np.rint(r+w[:,:,None]*delta),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[w==0],b[w==0]);dest=P/f;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest);bg=Image.new('RGB',(552,220),'#303b40')
 for h,x in [(148,0),(82,210),(54,350),(27,450)]:
  side=round(184*h/148);im=Image.fromarray(b).resize((side,side),Image.Resampling.BILINEAR);bg.paste(im,(x,20),im)
 preview.append(bg)
 if i==0:
  for j,(c,label) in enumerate([(idle,'Idle'),(a,'Previous'),(b,'Neutral suit')]):
   im=Image.fromarray(c);sheet.paste(im,(j*184,25),im);dr.text((j*184+8,5),label,fill='white')
s['provenance']['colourPass']={'source':str(S),'fixedChromaOffset':delta.tolist(),'method':'80% neutral-material chroma correction toward idle; luminance preserved before rounding; head and saturated patches excluded.'};(P/'manifest.json').write_text(json.dumps(m,indent=2));(P/'validation.json').write_text(json.dumps({'frames':len(arr),'beforeMedian':base.tolist(),'idleMedian':target.tolist(),'fixedOffset':delta.tolist(),'alphaExact':True,'outsideMaskExact':True,'timingUnchanged':True},indent=2));preview[0].save(P/'review.gif',save_all=True,append_images=preview[1:],duration=[10*(round((i+1)*100/24)-round(i*100/24)) for i in range(len(arr))],loop=0);sheet.save(P/'comparison.png');print('Fixed colour offset',delta.tolist())
p=Path('character/crew-idle-led-review-v5');p.mkdir(exist_ok=True);h=Path('character/crew-idle-led-review-v4/index.html').read_text().replace('../bill-idle-led-east-loop-v2/review.gif','../bill-idle-led-east-neutral-v1/review.gif').replace('48 frames / 2 seconds, source frames31-78. Raw full clip below.','Approved loop with a restrained neutral-suit colour correction. Head, geometry and timing unchanged. Raw video below is the uncorrected source.');h=h.replace('<h2>James</h2>','<img src="../bill-idle-led-east-neutral-v1/comparison.png"><h2>James</h2>');(p/'index.html').write_text(h)
