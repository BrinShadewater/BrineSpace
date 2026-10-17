from pathlib import Path
import json,re,numpy as np
from PIL import Image,ImageDraw
S=Path('character/crew-side-gameplay-review-v7');P=Path('character/james-idle-degreen-v1');P.mkdir(exist_ok=True);h=(S/'index.html').read_text(encoding='utf-8');raw=re.search(r'const tracks=(.*?);const c=',h).group(1);tracks=json.loads(raw);sheet=Image.new('RGB',(552,440),'#303b40');dr=ImageDraw.Draw(sheet);report={}
for row,t in enumerate(tracks[2:]):
 a=np.array(Image.open(S/t['idle']).convert('RGBA'));r=a[:,:,:3].astype(float);yellow=(r[:,:,0]>r[:,:,2]*1.5)&(r[:,:,1]>r[:,:,2]*1.4)&(r[:,:,0]>=r[:,:,1]);spread=np.ptp(r,axis=2);w=np.clip((50-spread)/20,0,1)*(~yellow)*(a[:,:,3]>240)
 # Restrained idle-only reduction; opaque pixels only so cleaned antialiased edges remain exact.
 b=a.copy();g=np.minimum(r[:,:,1]*.055,4)*w;b[:,:,1]=np.clip(np.rint(r[:,:,1]-g),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[w==0],b[w==0]);name='east' if row==0 else 'west';f=name+'.png';Image.fromarray(b).save(P/f);t['idle']='../james-idle-degreen-v1/'+f;report[name]={'opaqueGreenReduction':'.055 capped4 levels, feathered chroma mask','yellowProtected':True,'alphaAndOutsideMaskExact':True,'walksUnchanged':True}
 walk=np.array(Image.open(S/t['files'][0]).convert('RGBA'))
 for k,(c,label) in enumerate([(a,'Previous idle'),(b,'Adjusted idle'),(walk,'Current walk')]):
  im=Image.fromarray(c);sheet.paste(im,(k*184,row*220+25),im);dr.text((k*184+4,row*220+5),name+' '+label,fill='white')
sheet.save(P/'comparison.png');(P/'validation.json').write_text(json.dumps(report,indent=2));Q=Path('character/crew-side-gameplay-review-v8');Q.mkdir(exist_ok=True);h=h.replace(raw,json.dumps(tracks));h=h.replace('Green edge spill suppressed on all four pairs. James walking fabric brightness matched toward idle. Alpha, geometry and timing unchanged. Preview only.','James idle-only green reduction. Current walks, cleaned translucent edges, yellow patches and timing unchanged. Preview only.');(Q/'index.html').write_text(h,encoding='utf-8');print('Two idles corrected; all walking references unchanged.')
