from pathlib import Path
import json,re,numpy as np
from PIL import Image,ImageDraw
S=Path('character/crew-side-gameplay-review-v8');P=Path('character/james-walk-muted-v1');P.mkdir(exist_ok=True);h=(S/'index.html').read_text(encoding='utf-8');raw=re.search(r'const tracks=(.*?);const c=',h).group(1);tracks=json.loads(raw);L=np.array([.2126,.7152,.0722]);report={};sheet=Image.new('RGB',(736,440),'#303b40');draw=ImageDraw.Draw(sheet)
for row,t in enumerate(tracks[2:]):
 d='east' if row==0 else 'west';files=[]
 for i,f in enumerate(t['files']):
  a=np.array(Image.open(S/f).convert('RGBA'));rgb=a[:,:,:3].astype(float);lum=rgb@L;b=a.copy();b[:,:,:3]=np.clip(np.rint(lum[:,:,None]+.88*(rgb-lum[:,:,None])),0,255).astype('uint8');b[a[:,:,3]==0]=a[a[:,:,3]==0];assert np.array_equal(a[:,:,3],b[:,:,3]);rel=f'{d}/{i:03}.png';dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest);files.append('../james-walk-muted-v1/'+rel)
  if i==0:
   for col,(c,label) in enumerate([(a,'Previous'),(b,'Slightly muted')]):
    im=Image.fromarray(c);sheet.paste(im,(col*368+92,row*220+25),im);draw.text((col*368+5,row*220+4),d+' '+label,fill='white')
 report[d]={'frames':len(files),'chromaFactor':.88,'luminancePreservedBeforeRounding':True,'alphaExact':True,'timingUnchanged':True};t['files']=files
sheet.save(P/'comparison.png');(P/'validation.json').write_text(json.dumps(report,indent=2));(P/'tracks.json').write_text(json.dumps(tracks,indent=2));Q=Path('character/crew-side-gameplay-review-v9');Q.mkdir(exist_ok=True);h=h.replace(raw,json.dumps(tracks)).replace('James idle-only green reduction. Current walks, cleaned translucent edges, yellow patches and timing unchanged. Preview only.','James walking colours muted12% in both directions, retaining luminance and timing. Idles and Bill unchanged. Preview only.');(Q/'index.html').write_text(h,encoding='utf-8');print(report)
