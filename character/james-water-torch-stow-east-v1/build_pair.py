from pathlib import Path
import sys,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'james-water-family-v1'))
from extract_sources import extract
w=P.parent/'james-water-east-v1'
hr=json.loads((w/'helmet-registration.json').read_text())
patch=extract(w/'source-helmet.png',6,6)[4][0]
a=np.array(patch);r,g,b=a[:,:,:3].astype(float).transpose(2,0,1)
mask=(a[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17)
a[mask,:3]=np.rint(a[mask,:3].astype(float)*.9).clip(0,255).astype('uint8')
patch=Image.fromarray(a).resize((round(patch.width*hr['fixedHeadScale']),round(patch.height*hr['fixedHeadScale'])),Image.Resampling.LANCZOS)
point=np.array([142,118]);target=point+hr['centerOffset'];pos=np.rint(target-[patch.width/2,patch.height/2]).astype(int).tolist()
rows=[];equal=[]
for i in range(6):
 bare=Image.open(P/'frames/bare'/f'{i:03d}.png').convert('RGBA')
 if i in (0,5):
  donor=P.parent/('james-water-cargo-east-v1/frames/helmet/salvage/003.png' if i==0 else 'james-water-east-v1/frames/helmet/swim/000.png')
  helm=Image.open(donor).convert('RGBA')
 else:
  v=np.array(bare);yy,xx=np.indices(v.shape[:2]);erase=((xx-point[0])/14)**2+((yy-(point[1]-1))/14)**2<=1;v[erase]=0
  helm=Image.fromarray(v);helm.alpha_composite(patch,pos)
  changed=np.zeros(erase.shape,bool);changed[pos[1]:pos[1]+patch.height,pos[0]:pos[0]+patch.width]=True;changed|=erase
  equal.append({'index':i,'sharedBodyExactOutsideHelmet':bool(np.array_equal(np.array(helm)[~changed],np.array(bare)[~changed]))})
 helm.save(P/'frames'/f'{i:03d}.png');rows.append(helm)
m=json.loads((P/'helmet-manifest.json').read_text());m['states'][0]['provenance']={'bodySource':'source-bare.png','headSource':'../james-water-east-v1/source-helmet.png','derivation':'Shared whole authored bare body with accepted native prone helmet shell, exact selected helmet endpoints. Fixed body and helmet scales; no limb splice, mirror or body warp.'};(P/'helmet-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
reg=json.loads((P/'registration.json').read_text());reg.update({'activeBodySource':'source-bare.png','bodySourceSha256':hashlib.sha256((P/'source-bare.png').read_bytes()).hexdigest(),'bareRegistration':'registration-bare.json','helmetShellRegistration':'../james-water-east-v1/helmet-registration.json','helmetShellPosition':pos,'sharedBodyChecks':equal,'selectedHashes':{'frames/'+f'{i:03d}.png':hashlib.sha256((P/'frames'/f'{i:03d}.png').read_bytes()).hexdigest() for i in range(6)}});(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n')
board=Image.new('RGB',(1536,552),'#303b40');d=ImageDraw.Draw(board)
for i,h in enumerate(rows):
 b=Image.open(P/'frames/bare'/f'{i:03d}.png');board.paste(b,(i*256,0),b);board.paste(h,(i*256,276),h);d.text((i*256+8,8),'bare '+str(i),fill='white');d.text((i*256+8,282),'helmet '+str(i),fill='white')
board.save(P/'contact-pair.png')
review=[]
for i,h in enumerate(rows):
 b=Image.new('RGB',(960,330),'#303b40');d=ImageDraw.Draw(b);d.text((8,8),'James East stow / shared body / master148px + native82/54/27',fill='white');b.paste(h,(30,30),h)
 for height,x in [(82,370),(54,600),(27,780)]:
  s=height/148;small=h.resize((round(h.width*s),round(h.height*s)),Image.Resampling.BILINEAR);b.paste(small,(x,170-round(128*s)),small)
 review.append(b)
review[0].save(P/'review.gif',save_all=True,append_images=review[1:],duration=[400,60,80,80,70,600],loop=0,disposal=2,optimize=False)
(P/'pair-evidence.json').write_text(json.dumps({'checks':4,'failures':sum(not x['sharedBodyExactOutsideHelmet'] for x in equal),'records':equal,'scope':'Shared interior body pixels outside accepted helmet shell region; endpoints retained independently.'},indent=2)+'\n')
print(json.dumps({'pairedInteriors':4,'sharedBodyExact':all(x['sharedBodyExactOutsideHelmet'] for x in equal),'shellPosition':pos}))
