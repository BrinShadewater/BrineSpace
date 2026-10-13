from pathlib import Path
import json,ast,re,numpy as np
from PIL import Image,ImageDraw
for file,name in [('tools/polish_bill_selected_hair.py','hair'),('tools/match_bill_facial_hair.py','mask')]:
 tree=ast.parse(Path(file).read_text(encoding='utf-8-sig'));fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name);exec(compile(ast.Module(body=[fn],type_ignores=[]),file,'exec'))
R=Path('character/crew-runtime-matte-v1/bill');P=Path('character/bill-idle-hair-consistency-v1');P.mkdir(exist_ok=True);m=json.loads((R/'manifest.json').read_text());L=np.array([.2126,.7152,.0722]);Y=np.indices((184,184))[0];report={};sheet=Image.new('RGB',(1104,880),'#303b40');draw=ImageDraw.Draw(sheet)
def fabric(a):
 r=a[:,:,:3].astype(float);v=r.mean(2);return(a[:,:,3]>240)&(Y>60)&(Y<153)&(np.ptp(r,axis=2)<24)&(v>25)&(v<100)
for row,d in enumerate(['south','east','north','west']):
 idle=next(s for s in m['states'] if s['id']=='idle-'+d);walk=next(s for s in m['states'] if s['id']=='walk-'+d);wa=[np.array(Image.open(R/f).convert('RGBA')) for f in walk['frameFiles']];target=np.median(np.concatenate([a[:,:,:3][hair(a,d)|mask(a,d)] for a in wa]),axis=0);target[0]=min(target[0],target[1]*1.55,target[2]*1.95);ramp=target/(target@L);files=[]
 for i,f in enumerate(idle['frameFiles']):
  a=np.array(Image.open(R/f).convert('RGBA'));r=a[:,:,:3].astype(float);sel=hair(a,d)|mask(a,d);base=np.median(r[sel],axis=0);gain=float(np.clip((target@L)/(base@L),.9,1.05));result=r.copy();lum=r[sel]@L;result[sel]=lum[:,None]*gain*ramp
  fg=np.clip(np.median(np.concatenate([b[:,:,:3][fabric(b)] for b in wa]),axis=0)/np.median(r[fabric(a)],axis=0),.95,1.05);v=r.mean(2);w=np.clip((32-np.ptp(r,axis=2))/12,0,1)*np.clip((105-v)/20,0,1)*np.clip((v-15)/12,0,1)*np.clip((Y-53)/9,0,1)*(a[:,:,3]>240);result*=1+w[:,:,None]*(fg-1);b=a.copy();b[:,:,:3]=np.clip(np.rint(result),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[(~sel)&(w==0)],b[(~sel)&(w==0)]);rel=f'frames/idle-{d}/{i:03}.png';dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest);files.append(rel)
  if i==0:
   for col,(c,label) in enumerate([(a,'Current idle'),(b,'Matched idle'),(wa[0],'Walking reference')]):
    im=Image.fromarray(c);sheet.paste(im,(col*368+92,row*220+25),im);draw.text((col*368+5,row*220+5),d+' '+label,fill='white')
 report[d]={'idleHairMedian':base.tolist(),'walkingHairMedian':target.tolist(),'hairLuminanceGain':gain,'fabricGain':fg.tolist(),'alphaAndOutsideMaskExact':True};idle['frameFiles']=files;idle['provenance']={'source':str(R),'method':'Idle hair/beard hue matched to pooled corresponding walk; bounded brightness and minor fabric gains.'}
for s in m['states']:
 if not s['id'].startswith('idle-'):s['frameFiles']=['../crew-runtime-matte-v1/bill/'+f for f in s['frameFiles']]
(P/'manifest.json').write_text(json.dumps(m,indent=2));(P/'validation.json').write_text(json.dumps(report,indent=2));sheet.save(P/'comparison.png');Q=Path('character/crew-installed-motion-check-v2');Q.mkdir(exist_ok=True);h=Path('character/crew-installed-motion-check-v1/index.html').read_text(encoding='utf-8');raw=re.search(r'const tracks=(.*?);let ready=',h).group(1);tracks=json.loads(raw)
for t in tracks:
 if t['label'].startswith('Bill'):
  d=t['label'].split()[-1];s=next(s for s in m['states'] if s['id']=='idle-'+d);t['states']['idle']['files']=['../bill-idle-hair-consistency-v1/'+f for f in s['frameFiles']]
h=h.replace(raw,json.dumps(tracks)).replace('Actual installed PNGs and timing. Browser playback; native snapshots linked below.','Candidate Bill idle hair/beard and minor fabric matching; all walks and other crew remain installed versions.').replace('<option value="transition">','<option value="transition" selected>');(Q/'index.html').write_text(h,encoding='utf-8');print(report)
