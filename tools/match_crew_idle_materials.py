from pathlib import Path
import json,ast,re
import numpy as np
from PIL import Image,ImageDraw
P=Path('character/crew-idle-match-v1');P.mkdir(exist_ok=True);reports={};sheet=Image.new('RGB',(1104,880),'#303b40');draw=ImageDraw.Draw(sheet)
# Reuse established crown and facial-hair region definitions without running their builders.
for script,name in [('tools/polish_bill_selected_hair.py','hair'),('tools/match_bill_facial_hair.py','mask')]:
 tree=ast.parse(Path(script).read_text(encoding='utf-8-sig'));fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name);exec(compile(ast.Module(body=[fn],type_ignores=[]),script,'exec'))
def fabric(a):
 r=a[:,:,:3].astype(float);y=np.indices(a.shape[:2])[0];v=r.mean(2);return (a[:,:,3]>240)&(y>=60)&(y<153)&(np.ptp(r,axis=2)<18)&(v>25)&(v<90)
for col,who in enumerate(['bill','veld','branforth']):
 root=Path('character/crew-runtime-matte-v1')/who;m=json.loads((root/'manifest.json').read_text())
 for row,d in enumerate(['south','east','north','west']):
  idle=next(s for s in m['states'] if s['id']=='idle-'+d);walk=next(s for s in m['states'] if s['id']=='walk-'+d);arr=[np.array(Image.open(root/f).convert('RGBA')) for f in idle['frameFiles']];wa=[np.array(Image.open(root/f).convert('RGBA')) for f in walk['frameFiles']];target=np.median(np.concatenate([a[:,:,:3][fabric(a)] for a in wa]),axis=0);base=np.median(np.concatenate([a[:,:,:3][fabric(a)] for a in arr]),axis=0);gain=target/base
  hg=np.ones(3)
  if who=='bill':
   samples=np.concatenate([a[:,:,:3][hair(a,d)|mask(a,d)] for a in arr]);hg=np.array([47,33,26])/np.median(samples,axis=0)
  files=[]
  for i,a in enumerate(arr):
   rgb=a[:,:,:3].astype(float);y=np.indices(a.shape[:2])[0];v=rgb.mean(2);w=np.clip((22-np.ptp(rgb,axis=2))/10,0,1)*np.clip((105-v)/25,0,1)*np.clip((v-18)/12,0,1)*np.clip((y-53)/9,0,1)*(a[:,:,3]>16);result=rgb*(1+w[:,:,None]*(gain-1));h=np.zeros(a.shape[:2],bool)
   if who=='bill':
    h=hair(a,d)|mask(a,d);c=rgb[h]*hg;l=c@np.array([.2126,.7152,.0722]);brown=np.array([43,34,28]);result[h]=.25*c+.75*l[:,None]*brown/(brown@np.array([.2126,.7152,.0722]))
   b=a.copy();b[:,:,:3]=np.clip(np.rint(result),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[(w==0)&~h],b[(w==0)&~h]);rel=f'frames/idle-{d}/{i:03}.png';out=P/who/rel;out.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(out);files.append(rel)
   if i==0:
    x=col*368;yy=row*220;im=Image.fromarray(b);wi=Image.fromarray(wa[0]);sheet.paste(im,(x,yy+25),im);sheet.paste(wi,(x+184,yy+25),wi);draw.text((x+5,yy+3),who+' '+d+' matched idle / walk',fill='white')
  idle['frameFiles']=files;reports[who+'-'+d]=dict(idleFrames=len(arr),fixedFabricGain=gain.tolist(),targetFabric=target.tolist(),fixedHairGain=hg.tolist(),alphaAndOutsideMasksExact=True)
 for s in m['states']:
  if not s['id'].startswith('idle-'):s['frameFiles']=['../../crew-runtime-matte-v1/'+who+'/'+f for f in s['frameFiles']]
 (P/who/'manifest.json').write_text(json.dumps(m,indent=2))
sheet.save(P/'contact.png');(P/'validation.json').write_text(json.dumps(reports,indent=2))
html=Path('character/crew-idle-walk-check-v1/index.html').read_text();raw=re.search(r'const tracks=(.*?);let ready=',html).group(1);tracks=json.loads(raw)
for s in tracks:
 who,d=s['label'].lower().split();s['idle']=who+f'/frames/idle-{d}/000.png'
html=html.replace(raw,json.dumps(tracks)).replace('Idle to walk: installed crew','Matched idle preview').replace('Each pair shows idle on the left and moving walk on the right.','Each pair shows colour-matched idle on the left and installed walk on the right. Candidate only; no runtime changes.');(P/'index.html').write_text(html);print('Matched 32 idle frames; geometry, alpha and timing unchanged.')
