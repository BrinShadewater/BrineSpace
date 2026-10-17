from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
from scipy.ndimage import binary_dilation
P=Path(__file__).resolve().parent;R=P.parent.parent;C=R/'character/krusher-james-canonical-v4';P.joinpath('frames').mkdir(exist_ok=True);records=[];outputs={};yy,xx=np.indices((184,184))
fit=json.load(open(R/'character/krusher-james-motion-fit-v2/verification.json'));helmet=json.load(open(R/'character/krusher-james-helmet-fit-v2/verification.json'))
for gear in ['bare','helmet']:
 m=json.load(open(C/(gear+'-manifest.json')))
 for direction in ['south','east','north','west']:
  key='idle-'+direction;state=next(q for q in m['states'] if q['id']==key);src=C/state['frameFiles'][0];im=Image.open(src).convert('RGBA');a=np.array(im);out=a.copy();mask=np.zeros((184,184),bool);kind='unchanged';details={}
  if gear=='bare' and direction in ['east','west']:
   q=next(q for q in fit['records'] if q['state']==key and q['frame']==0);mask=np.array(Image.open(R/'character/krusher-james-motion-fit-v2'/q['mask']))>0
   h=Image.open(R/'character/krusher-bill-base-test-v2/sources'/(direction+'-head-native.png')).convert('RGBA');x,y=q['headPaste'];x+=-2 if direction=='east' else 2;y+=2
   layer=Image.new('RGBA',(184,184));layer.paste(h,(x,y));new=np.array(layer);out[mask]=new[mask];kind='registered native head moved back2/down2 inside protected original collar';details={'headPaste':[x,y]}
  elif gear=='helmet' and direction!='north':
   q=next(q for q in helmet['records'] if q['state']==key and q['frame']==0);old=np.array(Image.open(R/'character/krusher-james-helmet-fit-v2/masks'/(key+'-000-face.png')))>0
   x0,y0,x1,y1=q['faceBox'];x0-=2 if direction=='south' else 1;x1+=2 if direction=='south' else 1;y0-=3
   mask=binary_dilation(old,iterations=2)&(xx>=x0)&(xx<x1)&(yy>=y0)&(yy<y1)&(a[:,:,3]>0)
   head=Image.open(R/'character/krusher-bill-base-test-v2/sources'/(direction+'-head-native.png')).convert('RGBA').crop(tuple(q['faceSourceCrop']))
   size=(x1-x0,y1-y0);head=head.resize(size,Image.Resampling.LANCZOS);layer=Image.new('RGBA',(184,184));layer.paste(head,(x0,y0));new=np.array(layer);mask&=new[:,:,3]>60
   out[mask,:3]=new[mask,:3];kind='larger full-height visor face using existing identity source';details={'oldFaceSize':q['faceSize'],'newFaceSize':list(size),'faceBox':[x0,y0,x1,y1]}
  assert np.array_equal(a[~mask],out[~mask]);assert np.array_equal(a[54:],out[54:])
  file=P/'frames'/(gear+'-'+direction+'.png');Image.fromarray(out).save(file);outputs[(gear,direction)]=Image.fromarray(out);Image.fromarray(mask.astype('uint8')*255).save(P/'frames'/(gear+'-'+direction+'-mask.png'))
  records.append({'gear':gear,'direction':direction,'source':src.relative_to(R).as_posix(),'sourceSHA256':hashlib.sha256(src.read_bytes()).hexdigest(),'output':file.relative_to(P).as_posix(),'kind':kind,'details':details,'changedPixels':int(np.any(a!=out,axis=2).sum()),'outsideMaskExact':True,'bodyFromRow54Exact':True})
b=Image.new('RGBA',(1600,1030),'#272b2e');d=ImageDraw.Draw(b);font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24)
d.text((28,18),'KRUSHER DOM / SYSTEM ADMINISTRATOR',font=font,fill='white');d.text((28,54),'Head-fit correction study / original James suit pixels / matte muted cyan #527C80',font=font,fill='#b9d0d2')
for row,gear in enumerate(['bare','helmet']):
 for col,direction in enumerate(['south','east','north','west']):
  x=col*400+16;y=row*445+118;b.alpha_composite(outputs[(gear,direction)].resize((368,368),Image.Resampling.NEAREST),(x,y));d.text((x+10,y-30),direction.upper()+' / '+gear.upper(),font=font,fill='white')
d.text((28,990),'Native184x184 / foot92,172 / ruler148 / 2x nearest / correction not yet propagated',font=font,fill='#b9d0d2');b.save(P/'native-fit-sheet.png')
(P/'native-fit-verification.json').write_text(json.dumps({'records':records,'checks':16,'failures':0,'scope':'Eight canonical reference pose candidates. Existing native head registration and visor fit corrected; original body pixels below row54 exact. Generated fit sheet guides fit direction only, generated body pixels are not used. Not animation propagation/native motion acceptance.'},indent=2)+'\n');print('Eight native reference poses assembled; body pixels and density preserved.')
