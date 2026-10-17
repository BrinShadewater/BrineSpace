from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent;registrations={}
for kind,gen in [('crouch','exec-e54443bb-3bfa-40d8-ad93-33c1e37570bd'),('push','exec-de353a1d-a1f6-4b13-b0e9-da41351515a6')]:
 raw=Image.open(P/f'sources/{kind}-canvas-v1.png').convert('RGBA');assert raw.width==raw.height;a=np.array(raw);labs,_=label(a[:,:,3]>250);counts=np.bincount(labs.ravel());component=int(np.argmax(counts[1:])+1);mask=binary_dilation(labs==component,iterations=3)&(a[:,:,3]>0);a[~mask]=0
 im=Image.fromarray(a).resize((320,320),Image.Resampling.LANCZOS);shift=0;sole=None;b=np.array(im);yy,xx=np.indices(b.shape[:2])
 if kind=='crouch':
  boot=(b[:,:,3]>180)&(xx>=130)&(xx<205)&(yy>=190)&(yy<260);assert boot.any();sole=int(yy[boot].max())+1;shift=224-sole
 out=Image.new('RGBA',(320,320));out.paste(im,(0,shift));assert np.count_nonzero(np.array(out)[:,:,3])==np.count_nonzero(b[:,:,3]);out.save(P/f'sources/{kind}-native-v1.png');out.resize((1280,1280),Image.Resampling.NEAREST).save(P/f'sources/reference-{kind}-4x.png')
 registrations[kind]={'rawCanvas':raw.size,'wholeCanvasScale':320/raw.width,'translation':[0,shift],'semanticBootROI':[130,190,205,260] if kind=='crouch' else None,'soleBefore':sole,'allPaintedSupportPreserved':True,'generation':gen,'prompt':f'sources/{kind}-prompt-v1.txt','nativeAlphaBBox':out.getchannel('A').getbbox()}
frames=[Image.open(P/'sources'/f).convert('RGBA') for f in ['reference-idle-native.png','arm-ready-native-v3.png','crouch-native-v1.png','push-native-v1.png','reference-swim-native.png']]
board=Image.new('RGB',(1920,360),'#182932');d=ImageDraw.Draw(board);master=Image.open(R/'crew-side-masters-v1/bill-side-master-01.png').convert('RGB');scale=148/956;sm=master.crop((850,0,1280,1024)).resize((round(430*scale),round(1024*scale)),Image.Resampling.LANCZOS);board.paste(sm,(125,25+224-round(977*scale)));d.text((4,3),'West original master /148 ruler',fill='white')
for i,(name,im) in enumerate(zip(['exact idle','arm-ready trial','new crouch trial','new push-off trial','swim reference (missing lift poses)'],frames),1):
 x=i*320;board.paste(im,(x,25),im);d.text((x+4,3),name,fill='white');d.line((x,101,x+319,101),fill='#61707c')
 if i<4:d.line((x,249,x+319,249),fill='#6aa39e')
board.save(P/'west-pose-review.png')
e={'scope':'Five source poses including exact idle/swim references. Crouch/push authored West; missing lift/prone intermediates, no complete transition or normal admission. No borrowed East mirrors, per-pose scale fit or grade reapplication.','canvas':[320,320],'pivot':[160,224],'standingHeight':148,'registrations':registrations,'headAndMaterialAcceptance':'pending complete source/native motion review','sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [P/'sources/crouch-native-v1.png',P/'sources/push-native-v1.png']}}
(P/'pose-review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8');(P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill West water poses</title><style>body{background:#182932;color:#eee;font:16px sans-serif}img{max-width:100%}</style><h1>Bill West — water transition pose development</h1><p>'+e['scope']+'</p><img src="west-pose-review.png"><h2>Earlier arm-ready comparison</h2><img src="arm-ready-master-review.png">',encoding='utf-8')
print(json.dumps({'newSources':2,'registrations':registrations,'completeTransition':False}))
