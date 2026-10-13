from pathlib import Path
import json,re,numpy as np
from PIL import Image,ImageDraw
P=Path('character/crew-side-idle-colour-v1');P.mkdir(exist_ok=True);review=Path('character/crew-side-gameplay-review-v1');choices=json.loads((review/'selection.json').read_text());reports={};sheet=Image.new('RGB',(736,440),'#303b40');dr=ImageDraw.Draw(sheet);y=np.indices((184,184))[0]
def masks(a):
 r=a[:,:,:3].astype(float);v=r.mean(2);top=np.where(a[:,:,3]>127)[0].min();skin=(a[:,:,3]>240)&(y>=top+7)&(y<top+26)&(r[:,:,0]>95)&(r[:,:,0]>r[:,:,1]*1.15)&(r[:,:,1]>r[:,:,2]*1.08);fabric=(a[:,:,3]>240)&(y>=62)&(y<153)&(np.ptp(r,axis=2)<26)&(v>25)&(v<95);return fabric,skin
newIdle={}
for j,(label,who,d,folder) in enumerate(choices):
 R=Path('character')/folder;m=json.loads((R/'manifest.json').read_text());walk=[np.array(Image.open(R/f).convert('RGBA')) for f in m['states'][0]['frameFiles']];ir=Path('character/crew-idle-match-v1')/who;im=json.loads((ir/'manifest.json').read_text());st=next(s for s in im['states'] if s['id']=='idle-'+d);a=np.array(Image.open(ir/st['frameFiles'][0]).convert('RGBA'));r=a[:,:,:3].astype(float);baseMasks=masks(a);gains=[]
 for k in range(2):
  source=r[baseMasks[k]];samples=[w[:,:,:3][masks(w)[k]] for w in walk];target=np.median(np.concatenate(samples),axis=0);base=np.median(source,axis=0);gains.append(np.clip(target/base,.85,1.15))
 v=r.mean(2);w=np.clip((34-np.ptp(r,axis=2))/10,0,1)*np.clip((110-v)/20,0,1)*np.clip((v-15)/12,0,1)*np.clip((y-53)/9,0,1)*(a[:,:,3]>16);result=r*(1+w[:,:,None]*(gains[0]-1));result[baseMasks[1]]=r[baseMasks[1]]*gains[1];b=a.copy();b[:,:,:3]=np.clip(np.rint(result),0,255).astype('uint8');allowed=(w>0)|baseMasks[1];assert np.array_equal(a[~allowed],b[~allowed]);assert np.array_equal(a[:,:,3],b[:,:,3]);rel=who+'-'+d+'.png';Image.fromarray(b).save(P/rel);newIdle[label]='../crew-side-idle-colour-v1/'+rel;reports[label]={'fabricGain':gains[0].tolist(),'skinGain':gains[1].tolist(),'alphaExact':True,'outsideMaskExact':True}
 for k,c in enumerate([b,walk[0]]):
  ii=Image.fromarray(c);sheet.paste(ii,((j%2)*368+k*184,(j//2)*220+25),ii)
 dr.text(((j%2)*368+5,(j//2)*220+3),label+' matched idle / walk',fill='white')
sheet.save(P/'comparison.png');(P/'validation.json').write_text(json.dumps(reports,indent=2));Q=Path('character/crew-side-gameplay-review-v2');Q.mkdir(exist_ok=True);h=(review/'index.html').read_text(encoding='utf-8');raw=re.search(r'const tracks=(.*?);const c=',h).group(1);tracks=json.loads(raw)
for t in tracks:t['idle']=newIdle[t['label']]
h=h.replace(raw,json.dumps(tracks)).replace('<option value="walk">','<option value="walk">').replace('<option value="transition">','<option value="transition" selected>').replace('Exact selected PNGs and manifest timing, linear sampling. No generation or runtime installation.','Idle fabric and skin adjusted toward selected walks. Walk pixels and timing unchanged. No runtime installation.');(Q/'index.html').write_text(h,encoding='utf-8');print(reports)
