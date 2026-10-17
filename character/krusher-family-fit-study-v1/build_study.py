"""Static cross-family fitting study; existing heads, no invented anatomy."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;R=P.parent.parent
(P/'frames').mkdir(parents=True,exist_ok=True)
catalog=json.loads((R/'character/crew-base-reference-v1/catalog.json').read_text())
directions=['south','east','north','west'];families=['bill','veld','branforth','marsh']
names={'bill':'Bill / demonstrated','veld':'Veld / slim build study','branforth':'James / utility build study','marsh':'Marsh / android body study'}
font=lambda n:ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),n)
sheet=Image.new('RGBA',(1600,1740),'#272b2e');draw=ImageDraw.Draw(sheet)
draw.text((28,16),'KRUSHER DOM / BODY FAMILY FITTING STUDY',font=font(36),fill='white')
draw.text((28,65),'Same native head density. Alternate suits keep their original colours and equipment.',font=font(25),fill='#bdcdd0')
records=[];checks=0;errors=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for row,family in enumerate(families):
 y=115+row*380
 draw.text((28,y),names[family],font=font(29),fill='white')
 for col,direction in enumerate(directions):
  rec=next(t for t in catalog['records'] if t['family']==family and t['direction']==direction)
  source=R/rec['source'];original=Image.open(source).convert('RGBA');a=np.array(original)
  headpath=R/f'character/krusher-bill-base-test-v2/sources/{direction}-head-native.png'
  head=Image.open(headpath).convert('RGBA')
  if family=='bill':
   candidate_path=R/f'character/krusher-runtime-candidate-v1/frames/bare/idle-{direction}/000.png'
   candidate=Image.open(candidate_path).convert('RGBA');anchor=None
  else:
   # Preliminary per-family collar boundary; keep all lower body pixels exact.
   # Refine family-specific neck masks after comparison, before any animation reuse.
   upper=(a[:,:,3]>180)&(np.indices(a.shape[:2])[0]<44)
   _,xs=np.where(upper);axis=round((int(xs.min())+int(xs.max()))/2)
   h=np.array(head);hy,hx=np.where((h[:,:,3]>150)&(np.indices(h.shape[:2])[0]>=head.height-5))
   local=round((int(hx.min())+int(hx.max()))/2) if direction in ['east','west'] else head.width//2
   cutoff={'veld':51,'branforth':50,'marsh':51}[family]
   anchor=[axis-local,cutoff-head.height]
   a[:cutoff]=0;candidate=Image.fromarray(a);candidate.paste(head,tuple(anchor))
   checks+=2
   if not np.array_equal(np.array(candidate)[cutoff:],np.array(original)[cutoff:]):errors.append(f'body:{family}:{direction}')
   if not np.array_equal(np.array(candidate)[anchor[1]:anchor[1]+head.height,anchor[0]:anchor[0]+head.width],np.array(head)):errors.append(f'head:{family}:{direction}')
  file=f'frames/{family}-{direction}.png';candidate.save(P/file)
  tile=candidate.resize((368,368),Image.Resampling.NEAREST)
  sheet.alpha_composite(tile,(24+col*390,y+28))
  draw.text((45+col*390,y+344),direction.upper(),font=font(23),fill='white')
  records.append({'family':family,'direction':direction,'source':rec['source'],'sourceHash':sha(source),'headSource':headpath.relative_to(R).as_posix(),'headHash':sha(headpath),'output':file,'outputHash':sha(P/file),'headPaste':anchor,'bodyPreservedFromRow':cutoff if family!='bill' else None})
draw.text((28,1650),'Static fit candidates only. No alternate-family animation, helmet fit or colour mask established.',font=font(24),fill='#bdcdd0')
draw.text((28,1688),'Bill row uses the existing cyan candidate; remaining rows expose fit differences before refinement.',font=font(24),fill='#bdcdd0')
sheet.convert('RGB').save(P/'family-fit-comparison.png')
report={'scope':'Static head/body fitting comparison; alternate source suit colours retained; unselected','checks':checks,'errors':errors,'records':records,'limitations':['Preliminary per-family collar boundaries; require refined neck masks before animation','No alternate-family animation or helmet compatibility claim','No normal selection changes']}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'checks':checks,'errors':errors,'candidates':len(records)}))
assert not errors
