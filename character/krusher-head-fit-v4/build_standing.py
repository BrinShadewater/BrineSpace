from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
pkg=R/'character/krusher-animation-package-v3'; index=json.loads((pkg/'package.json').read_text())
fits=json.loads((R/'character/krusher-james-motion-fit-v2/verification.json').read_text())['records']
helms=json.loads((R/'character/krusher-james-helmet-fit-v2/verification.json').read_text())['records']
records=[]; images={}; yy,xx=np.indices((184,184))
for gear in ['bare','helmet']:
 for direction in ['south','east','north','west']:
  key='idle-'+direction; m=pkg/index['states'][gear+':'+key]['manifest']; data=json.loads(m.read_text()); state=next(s for s in data['states'] if s['id']==key); src=(m.parent/state['frameFiles'][0]).resolve()
  a=np.array(Image.open(src).convert('RGBA')); out=a.copy();head=Image.open(P/'sources'/f'clean-bare-{direction}-native.png').convert('RGBA'); h=np.array(head)
  if gear=='bare':
   q=next(q for q in fits if q['state']==key and q['frame']==0)
   old=Image.open(R/'character/krusher-bill-base-test-v2/sources'/f'{direction}-head-native.png')
   oldarr=np.array(old.convert('RGBA'));hy,hx=np.where((oldarr[:,:,3]>150)&(np.indices(oldarr.shape[:2])[0]>=old.height-5))
   oldaxis=round((int(hx.min())+int(hx.max()))/2) if direction in ['east','west'] else old.width//2
   axis=q['headPaste'][0]+oldaxis
   hy,hx=np.where((h[:,:,3]>150)&(np.indices(h.shape[:2])[0]>=head.height-4))
   neckaxis=round((int(hx.min())+int(hx.max()))/2)
   bottom={'south':48,'east':47,'north':45,'west':47}[direction]
   paste=(axis-neckaxis,bottom-head.height)
   collarbottom={'south':49,'east':46,'north':45,'west':46}[direction]
   original=np.array(Image.open(R/q['source']).convert('RGBA'))
   collar=(yy>=collarbottom)&(yy<54)
   if direction=='south':collar|=(yy>=45)&(yy<54)&((xx<axis-8)|(xx>axis+8))
   elif direction in ['east','west']:collar|=(yy>=45)&(yy<54)&((xx<axis-3) if direction=='east' else (xx>axis+3))
   collar&=original[:,:,3]>0
   allowed=(yy<54)&~collar
   out[allowed]=0
   layer=Image.new('RGBA',(184,184));layer.alpha_composite(head,paste);n=np.array(layer);opaque=n[:,:,3]>0
   out[opaque&allowed]=n[opaque&allowed]
   out[collar]=a[collar]
   # Restore only missing original collar pixels. Retain the current suit
   # palette on shoulder panels that share the same vertical band.
   missing=collar&(a[:,:,3]==0)
   out[missing]=original[missing]
  elif direction!='north':
   q=next(q for q in helms if q['state']==key and q['frame']==0)
   face=R/'character/krusher-james-helmet-fit-v2'/q['allowedMask'].replace('-allowed.png','-face.png')
   allowed=np.array(Image.open(face).convert('L'))>0
   # Head remains at the bare physical scale. Place the natural face behind
   # the original opening; the opening clips it rather than squeezing it.
   paste={'south':(82,25),'east':(81,24),'west':(79,24)}[direction]
   layer=Image.new('RGBA',(184,184));layer.alpha_composite(head,paste);n=np.array(layer)
   opaque=n[:,:,3]>0
   out[allowed&opaque,:3]=n[allowed&opaque,:3]
   # Outside the documented face aperture, shell, collar and visor pixels
   # are byte-identical to the preserved cyan package.
  else:allowed=np.zeros((184,184),bool);paste=None
  assert np.array_equal(a[~allowed],out[~allowed]) if gear=='helmet' else np.array_equal(a[54:],out[54:])
  path=P/'standing'/f'{gear}-{direction}.png';path.parent.mkdir(exist_ok=True);Image.fromarray(out).save(path);images[gear,direction]=Image.fromarray(out)
  records.append({'gear':gear,'direction':direction,'source':src.relative_to(R).as_posix(),'output':path.relative_to(P).as_posix(),'headPaste':paste,'changedPixels':int(np.any(a!=out,2).sum()),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'uniformHeadScale':29/480})
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24)
board=Image.new('RGBA',(900,760),'#252b2e');draw=ImageDraw.Draw(board)
draw.text((24,15),'KRUSHER DOM / HEAD FIT STUDY',font=font,fill='white')
for row,g in enumerate(['bare','helmet']):
 for col,d in enumerate(['south','east','north','west']):
  im=images[g,d];crop=im.crop((55,12,129,180)).resize((148,336),Image.Resampling.NEAREST)
  x=col*220+35;y=row*350+65;board.alpha_composite(crop,(x,y));draw.text((x,y-28),d+' / '+g,font=font,fill='#bfd2d4')
board.save(P/'standing-review-mobile.png')
close=Image.new('RGBA',(1000,420),'#252b2e');draw=ImageDraw.Draw(close)
for row,g in enumerate(['bare','helmet']):
 for col,d in enumerate(['south','east','north','west']):
  crop=images[g,d].crop((70,16,112,58)).resize((168,168),Image.Resampling.NEAREST)
  x=col*250+35;y=row*205+30;close.alpha_composite(crop,(x,y));draw.text((x,y-26),d+' / '+g,font=font,fill='white')
close.save(P/'standing-heads-closeup.png')
(P/'standing-verification.json').write_text(json.dumps({'status':'standing prototype, visual review required; full animation replacement pending','records':records},indent=2)+'\n')
print(json.dumps({'outputs':len(records),'bodyAndShellProtectionChecks':'passed'}))
