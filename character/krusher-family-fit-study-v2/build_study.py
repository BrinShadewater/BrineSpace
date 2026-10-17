"""Static cross-family fitting study; existing heads, no invented anatomy."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parent.parent
(P/'frames').mkdir(parents=True,exist_ok=True)
(P/'masks').mkdir(exist_ok=True)
catalog=json.loads((R/'character/crew-base-reference-v1/catalog.json').read_text())
directions=['south','east','north','west'];families=['bill','veld','branforth','marsh']
names={'bill':'Bill / demonstrated','veld':'Veld / slim build study','branforth':'James / utility build study','marsh':'Marsh / android body study'}
font=lambda n:ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),n)
sheet=Image.new('RGBA',(1600,1740),'#272b2e');draw=ImageDraw.Draw(sheet)
draw.text((28,16),'KRUSHER DOM / COLLAR-PRESERVING FIT STUDY',font=font(36),fill='white')
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
   yy,xx=np.indices(a.shape[:2]);rgb=a[:,:,:3].astype(float)
   upper=(a[:,:,3]>180)&(yy<44)
   _,xs=np.where(upper);axis=round((int(xs.min())+int(xs.max()))/2)
   h=np.array(head);hy,hx=np.where((h[:,:,3]>150)&(np.indices(h.shape[:2])[0]>=head.height-5))
   local=round((int(hx.min())+int(hx.max()))/2) if direction in ['east','west'] else head.width//2
   cutoff=54
   neck_bottom={'veld':{'south':49,'east':49,'north':45,'west':49},'branforth':{'south':48,'east':47,'north':45,'west':47},'marsh':{'south':50,'east':50,'north':47,'west':50}}[family][direction]
   anchor=[axis-local,neck_bottom-head.height]
   # Explicit source-reviewed collar boundaries, not colour classification.
   # Dark hair and warm suit trim cannot reliably be separated by RGB alone.
   central={'veld':{'south':50,'east':49,'north':45,'west':49},'branforth':{'south':49,'east':46,'north':45,'west':46},'marsh':{'south':51,'east':50,'north':46,'west':50}}[family][direction]
   collar=(yy>=central)&(yy<54)&(a[:,:,3]>0)
   if direction=='south':
    collar|=(yy>=45)&(yy<54)&((xx<axis-8)|(xx>axis+8))&(a[:,:,3]>0)
   elif direction in ['east','west']:
    rear=(xx<axis-3) if direction=='east' else (xx>axis+3)
    collar|=(yy>=45)&(yy<54)&rear&(a[:,:,3]>0)
   original_a=a.copy();a[:cutoff]=0
   candidate=Image.fromarray(a);candidate.paste(head,tuple(anchor))
   ca=np.array(candidate);ca[collar]=original_a[collar];candidate=Image.fromarray(ca)
   allowed=(yy<cutoff)&(~collar)
   Image.fromarray(collar.astype('uint8')*255).save(P/f'masks/{family}-{direction}-collar.png')
   Image.fromarray(allowed.astype('uint8')*255).save(P/f'masks/{family}-{direction}-allowed.png')
   checks+=3
   if not np.array_equal(ca[~allowed],original_a[~allowed]):errors.append(f'protected:{family}:{direction}')
   if not np.array_equal(ca[collar],original_a[collar]):errors.append(f'collar:{family}:{direction}')
   expected=np.array(head);actual=ca[anchor[1]:anchor[1]+head.height,anchor[0]:anchor[0]+head.width]
   visible=~collar[anchor[1]:anchor[1]+head.height,anchor[0]:anchor[0]+head.width]
   if not np.array_equal(actual[visible],expected[visible]):errors.append(f'head:{family}:{direction}')
  file=f'frames/{family}-{direction}.png';candidate.save(P/file)
  tile=candidate.resize((368,368),Image.Resampling.NEAREST)
  sheet.alpha_composite(tile,(24+col*390,y+28))
  draw.text((45+col*390,y+344),direction.upper(),font=font(23),fill='white')
  records.append({'family':family,'direction':direction,'source':rec['source'],'sourceHash':sha(source),'headSource':headpath.relative_to(R).as_posix(),'headHash':sha(headpath),'output':file,'outputHash':sha(P/file),'headPaste':anchor,'bodyPreservedFromRow':cutoff if family!='bill' else None})
draw.text((28,1650),'Static fit candidates only. No alternate-family animation, helmet fit or colour mask established.',font=font(24),fill='#bdcdd0')
draw.text((28,1688),'Bill row uses the existing cyan candidate; alternate rows preserve complete source collar pixels over the new head.',font=font(24),fill='#bdcdd0')
sheet.convert('RGB').save(P/'family-fit-comparison.png')
report={'scope':'Static head/body fitting comparison; alternate source suit colours retained; unselected','checks':checks,'errors':errors,'records':records,'limitations':['Source-reviewed collar boundaries require moving-frame validation and additional neckline polish','No alternate-family animation or helmet compatibility claim','No normal selection changes']}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'checks':checks,'errors':errors,'candidates':len(records)}))
assert not errors
