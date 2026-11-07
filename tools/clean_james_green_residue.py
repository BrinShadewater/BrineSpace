from pathlib import Path
import json,re,numpy as np
from PIL import Image,ImageDraw
S=Path('character/crew-side-gameplay-review-v5');P=Path('character/james-green-cleanup-v1');P.mkdir(exist_ok=True);h=(S/'index.html').read_text(encoding='utf-8');raw=re.search(r'const tracks=(.*?);const c=',h).group(1);tracks=json.loads(raw);L=np.array([.2126,.7152,.0722]);report={};sheet=Image.new('RGB',(736,660),'#303b40');draw=ImageDraw.Draw(sheet);row=0

def correct(a):
 r=a[:,:,:3].astype(float);spread=np.ptp(r,axis=2);yellow=(r[:,:,0]>r[:,:,2]*1.45)&(r[:,:,1]>r[:,:,2]*1.4)&(r[:,:,0]>=r[:,:,1]);skin=(r[:,:,0]>r[:,:,1]*1.18)&(r[:,:,1]>r[:,:,2]*1.12);neutral=np.clip((48-spread)/16,0,1);green=np.maximum(r[:,:,1]-(r[:,:,0]+r[:,:,2])*.5,0);olive=np.maximum(np.minimum(r[:,:,0],r[:,:,1])-r[:,:,2]-2,0);w=np.clip((green+olive*.5)/3,0,1)*neutral*(~yellow)*(~skin)*(a[:,:,3]>0);v=r@L;target=np.repeat(v[:,:,None],3,axis=2);out=r+w[:,:,None]*(target-r);b=a.copy();b[:,:,:3]=np.clip(np.rint(out),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[w==0],b[w==0]);return b,int((w>0).sum())
for t in tracks:
 if not t['label'].startswith('James'):continue
 d='east' if 'east' in t['label'] else 'west';a=np.array(Image.open(S/t['idle']).convert('RGBA'));b,n=correct(a);rel='idle-'+d+'.png';Image.fromarray(b).save(P/rel);t['idle']='../james-green-cleanup-v1/'+rel;report[rel]={'changedMaskPixels':n,'alphaOutsideMaskExact':True}
 for k,c in enumerate([a,b]):
  im=Image.fromarray(c);sheet.paste(im,(k*368+92,row*220+25),im);draw.text((k*368+5,row*220+5),'James '+d+' idle '+('before' if k==0 else 'corrected'),fill='white')
 row+=1
 if d=='west':
  R=Path('character/branforth-idle-led-west-timing-v1');m=json.loads((R/'manifest.json').read_text());st=m['states'][0];new=[]
  for i,f in enumerate(st['frameFiles']):
   a=np.array(Image.open(R/f).convert('RGBA'));b,n=correct(a);rel='frames/walk-west/'+f'{i:03}.png';dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest);new.append(rel)
   if i==0:
    for k,c in enumerate([a,b]):
     im=Image.fromarray(c);sheet.paste(im,(k*368+92,465),im);draw.text((k*368+5,445),'James west walk '+('before' if k==0 else 'corrected'),fill='white')
  st['frameFiles']=new;st['provenance']['greenCleanup']={'source':str(R),'method':'Fixed green/olive neutral-region suppression toward equal-luminance grey; yellow and warm skin excluded.'};(P/'manifest.json').write_text(json.dumps(m,indent=2));t['files']=['../james-green-cleanup-v1/'+f for f in new];report['walk-west']={'frames':len(new),'timingUnchanged':True,'alphaOutsideMaskExact':True}
sheet.save(P/'comparison.png');(P/'validation.json').write_text(json.dumps(report,indent=2));Q=Path('character/crew-side-gameplay-review-v6');Q.mkdir(exist_ok=True);h=h.replace(raw,json.dumps(tracks)).replace('All four idles: neutral shadows, midtones and highlights matched to their walking colour ramps. Brightness and geometry retained. Walks unchanged.','James idles and west walk: green/olive residue removed from neutral materials. Brightness, poses and timing retained. Bill and James east walk unchanged.');(Q/'index.html').write_text(h,encoding='utf-8');print(report)
