from pathlib import Path
import json,re,ast,numpy as np
from PIL import Image,ImageDraw
T=ast.parse(Path('tools/polish_bill_selected_hair.py').read_text(encoding='utf-8-sig'));fn=next(n for n in T.body if isinstance(n,ast.FunctionDef) and n.name=='hair');exec(compile(ast.Module(body=[fn],type_ignores=[]),'hair','exec'))
S=Path('character/crew-installed-motion-check-v2');P=Path('character/crew-targeted-tones-v1');P.mkdir(exist_ok=True);h=(S/'index.html').read_text(encoding='utf-8');raw=re.search(r'const tracks=(.*?);let ready=',h).group(1);tracks=json.loads(raw);Y=np.indices((184,184))[0];report={};sheet=Image.new('RGB',(736,8*210),'#303b40');draw=ImageDraw.Draw(sheet);row=0
for t in tracks:
 who,d=t['label'].lower().split()
 for kind,st in t['states'].items():
  adjust=('hair' if who=='bill' and ((kind=='idle' and d in ['east','west']) or (kind=='walk' and d=='south')) else 'dimskin' if who=='branforth' and kind=='walk' and d in ['south','east','west'] else 'liftskin' if who=='veld' and kind=='idle' and d in ['east','west'] else None)
  if not adjust:continue
  files=[];counts=[]
  for i,f in enumerate(st['files']):
   a=np.array(Image.open(S/f).convert('RGBA'));r=a[:,:,:3].astype(float);top=np.where(a[:,:,3]>127)[0].min()
   if adjust=='hair':
    sel=hair(a,d)
    if kind=='idle' and d in ['east','west']:sel=(a[:,:,3]>16)&(Y<top+7)&(r.max(2)<140)
    weight=sel.astype(float);gain=1.10
   else:
    dy=Y-top;sel=(a[:,:,3]>240)&(dy>=6)&(dy<27)&(r[:,:,0]>95)&(r[:,:,1]>50)&(r[:,:,2]>30)&(r[:,:,0]>r[:,:,1]*1.12)&(r[:,:,1]>r[:,:,2]*1.06);weight=sel.astype(float);gain=1.08 if adjust=='liftskin' else .93
    if adjust=='dimskin':weight*=np.clip((r.mean(2)-65)/40,0,1)
   b=a.copy();b[:,:,:3]=np.clip(np.rint(r*(1+weight[:,:,None]*(gain-1))),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[weight==0],b[weight==0]);rel=f'{who}/{kind}-{d}/{i:03}.png';dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest);files.append('../crew-targeted-tones-v1/'+rel);counts.append(int((weight>0).sum()))
   if i==0:
    for col,(c,label) in enumerate([(a,'Before'),(b,'Adjusted')]):
     im=Image.fromarray(c);sheet.paste(im,(col*368+92,row*210+20),im);draw.text((col*368+5,row*210+3),t['label']+' '+kind+' '+label,fill='white')
  st['files']=files;report[who+'-'+kind+'-'+d]={'adjustment':adjust,'gain':gain,'frames':len(files),'changedMaskPixelsRange':[min(counts),max(counts)],'alphaOutsideMaskExact':True,'timingUnchanged':True};row+=1
sheet.save(P/'comparison.png');(P/'validation.json').write_text(json.dumps(report,indent=2));(P/'tracks.json').write_text(json.dumps(tracks,indent=2));Q=Path('character/crew-installed-motion-check-v3');Q.mkdir(exist_ok=True);h=h.replace(raw,json.dumps(tracks)).replace('Candidate Bill idle hair/beard and minor fabric matching; all walks and other crew remain installed versions.','Targeted trial: Bill selected hair lighter; James south/side walking skin highlights softer; Veld side-idle skin lighter. Suits and motion unchanged.');(Q/'index.html').write_text(h,encoding='utf-8');print(report)
