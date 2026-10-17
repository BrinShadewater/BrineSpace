from pathlib import Path
import json,numpy as np
from PIL import Image,ImageDraw
S=Path('character/branforth-idle-led-east-loop-v1');B=Path('character/bill-idle-led-east-neutral-v1');P=Path('character/branforth-idle-led-east-bill-match-v1');P.mkdir(exist_ok=True);m=json.loads((S/'manifest.json').read_text());s=m['states'][0];bm=json.loads((B/'manifest.json').read_text());y=np.indices((184,184))[0]
def sample(a):
 r=a[:,:,:3].astype(float);v=r.mean(2);return (a[:,:,3]>240)&(y>=62)&(y<153)&(np.ptp(r,axis=2)<30)&(v>25)&(v<90)
aframes=[np.array(Image.open(S/f).convert('RGBA')) for f in s['frameFiles']];bframes=[np.array(Image.open(B/f).convert('RGBA')) for f in bm['states'][0]['frameFiles']];base=np.median(np.concatenate([a[:,:,:3][sample(a)] for a in aframes]),axis=0);target=np.median(np.concatenate([a[:,:,:3][sample(a)] for a in bframes]),axis=0);gain=target/base;preview=[];after=[];sheet=Image.new('RGB',(552,220),'#303b40');draw=ImageDraw.Draw(sheet)
for i,(a,f) in enumerate(zip(aframes,s['frameFiles'])):
 r=a[:,:,:3].astype(float);v=r.mean(2);w=np.clip((40-np.ptp(r,axis=2))/12,0,1)*np.clip((110-v)/20,0,1)*np.clip((v-12)/13,0,1)*np.clip((y-53)/9,0,1)*(a[:,:,3]>16);b=a.copy();b[:,:,:3]=np.clip(np.rint(r*(1+w[:,:,None]*(gain-1))),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[w==0],b[w==0]);after.append(b[:,:,:3][sample(a)]);dest=P/f;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest)
 bg=Image.new('RGB',(552,220),'#303b40')
 for h,x in [(148,0),(82,210),(54,350),(27,450)]:
  side=round(184*h/148);im=Image.fromarray(b).resize((side,side),Image.Resampling.BILINEAR);bg.paste(im,(x,20),im)
 preview.append(bg)
 if i==0:
  for j,(c,label) in enumerate([(bframes[0],'Bill reference'),(a,'James before'),(b,'James matched')]):
   im=Image.fromarray(c);sheet.paste(im,(j*184,25),im);draw.text((j*184+5,5),label,fill='white')
report={'frames':len(aframes),'beforeFabricMedian':base.tolist(),'billTargetMedian':target.tolist(),'afterFabricMedian':np.median(np.concatenate(after),axis=0).tolist(),'fixedGain':gain.tolist(),'alphaExact':True,'outsideMaskExact':True,'timingUnchanged':True};s['provenance']['colourPass']={'source':str(S),'reference':str(B),'fixedGain':gain.tolist(),'method':'One fixed neutral fabric channel gain for entire clip, excluding head and saturated patches; feathered silver protection.'};(P/'manifest.json').write_text(json.dumps(m,indent=2));(P/'validation.json').write_text(json.dumps(report,indent=2));sheet.save(P/'comparison.png');preview[0].save(P/'review.gif',save_all=True,append_images=preview[1:],duration=[10*(round((i+1)*100/24)-round(i*100/24)) for i in range(len(preview))],loop=0)
p=Path('character/crew-idle-led-review-v7');p.mkdir(exist_ok=True);h=Path('character/crew-idle-led-review-v6/index.html').read_text().replace('../branforth-idle-led-east-darker-v1/','../branforth-idle-led-east-bill-match-v1/').replace('James suit fabric darkened7%; head, yellow accents and motion retained. Raw video below is the uncorrected source.','James neutral suit fabric matched to Bill using fixed clip-wide colour gains. Head and yellow patches preserved; motion unchanged. Raw video below is uncorrected.');(p/'index.html').write_text(h);print(report)
