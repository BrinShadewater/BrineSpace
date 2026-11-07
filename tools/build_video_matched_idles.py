from pathlib import Path
import json,re,numpy as np
from PIL import Image,ImageDraw
P=Path('character/crew-video-idles-v1');P.mkdir(exist_ok=True);base=Path('character/crew-side-gameplay-review-v2');h=(base/'index.html').read_text(encoding='utf-8');raw=re.search(r'const tracks=(.*?);const c=',h).group(1);tracks=json.loads(raw);Y=np.indices((184,184))[0];L=np.array([.2126,.7152,.0722]);sheet=Image.new('RGB',(736,440),'#303b40');draw=ImageDraw.Draw(sheet);report={}
for j,t in enumerate(tracks):
 who='bill' if t['label'].startswith('Bill') else 'branforth';direction='east' if 'east' in t['label'] else 'west';version=2 if who=='bill' and direction=='east' else 4 if who=='branforth' and direction=='east' else 1;source=Path('character')/f'{who}-idle-led-{direction}-v{version}'/'frames/000.png';a=np.array(Image.open(source).convert('RGBA'));r=a[:,:,:3].astype(float);v=r.mean(2);top=np.where(a[:,:,3]>127)[0].min();dy=Y-top
 if who=='bill' and direction=='east':
  w=np.clip((30-np.ptp(r,axis=2))/12,0,1)*np.clip((Y-53)/9,0,1)*(a[:,:,3]>16);result=r+w[:,:,None]*np.array([-3.3752,1.4248,-4.1752])
 else:
  gain=([.9423076923,1.023255814,.87037037] if who=='bill' else [.7538461538,.88,.734375] if direction=='east' else [.8813559322,1,.8620689655]);w=np.clip((40-np.ptp(r,axis=2))/12,0,1)*np.clip((110-v)/20,0,1)*np.clip((v-12)/13,0,1)*np.clip((Y-53)/9,0,1)*(a[:,:,3]>16);result=r*(1+w[:,:,None]*(np.array(gain)-1))
 if who=='branforth':
  yellow=(r[:,:,1]>r[:,:,2]*1.5)&(r[:,:,0]>r[:,:,1]*1.05);mag=np.minimum(result[:,:,0]-result[:,:,1],result[:,:,2]-result[:,:,1]);w=np.clip((mag-1)/5,0,1)*(a[:,:,3]>0)*(~yellow);l=result@L;result+=w[:,:,None]*(l[:,:,None]-result);skin=(dy<34)&(a[:,:,3]>0)&(~yellow)&(r[:,:,0]>95)&(r[:,:,0]>r[:,:,1]*1.15)&(r[:,:,1]>r[:,:,2]*1.06);shift=np.minimum(np.maximum(r[:,:,2]-(r[:,:,1]-.32*(r[:,:,0]-r[:,:,1])),0),12)*skin;result[:,:,2]-=shift;result[:,:,1]+=shift*(L[2]/L[1])
 b=a.copy();b[:,:,:3]=np.clip(np.rint(result),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);f=f'{who}-{direction}.png';Image.fromarray(b).save(P/f);t['idle']='../crew-video-idles-v1/'+f;report[f]={'source':str(source),'geometryAlphaExact':True,'method':'Standing first source frame; fixed selected walk material treatment, no geometry warps.'}
 walk=np.array(Image.open(base/t['files'][0]).convert('RGBA'))
 for k,c in enumerate([b,walk]):
  im=Image.fromarray(c);sheet.paste(im,((j%2)*368+k*184,(j//2)*220+25),im)
 draw.text(((j%2)*368+5,(j//2)*220+3),who+' '+direction+' source idle / walk',fill='white')
sheet.save(P/'comparison.png');(P/'provenance.json').write_text(json.dumps(report,indent=2));Q=Path('character/crew-side-gameplay-review-v3');Q.mkdir(exist_ok=True);h=h.replace(raw,json.dumps(tracks)).replace('Idle fabric and skin adjusted toward selected walks. Walk pixels and timing unchanged. No runtime installation.','Standing frames from the same video sources, with matching material treatment. Walks unchanged. Experimental idles; no runtime installation.');(Q/'index.html').write_text(h,encoding='utf-8');print('4 source-derived standing candidates; alpha and geometry preserved.')
