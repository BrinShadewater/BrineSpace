from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent
raw=Image.open(P/'sources/arm-ready-canvas-v3.png').convert('RGBA');assert raw.width==raw.height
arr=np.array(raw);labs,_=label(arr[:,:,3]>250);counts=np.bincount(labs.ravel());assert len(counts)>1
core=int(np.argmax(counts[1:])+1);mask=binary_dilation(labs==core,iterations=3)&(arr[:,:,3]>0);arr[~mask]=0
lean=Image.fromarray(arr).resize((320,320),Image.Resampling.LANCZOS);a=np.array(lean); yy,xx=np.indices(a.shape[:2]); contact=(a[:,:,3]>180)&(xx>=130)&(xx<185)&(yy>=190)&(yy<260); assert contact.any(); sole=int(yy[contact].max())+1; shift=224-sole; registered=Image.new('RGBA',(320,320));registered.paste(lean,(0,shift));lean=registered;lean.save(P/'sources/arm-ready-native-v3.png')
idle=Image.open(P/'sources/reference-idle-native.png').convert('RGBA');swim=Image.open(P/'sources/reference-swim-native.png').convert('RGBA')
master=Image.open(R/'crew-side-masters-v1/bill-side-master-01.png').convert('RGB');scale=148/956
master_crop=master.crop((850,0,1280,1024));master_small=master_crop.resize((round(430*scale),round(1024*scale)),Image.Resampling.LANCZOS)
board=Image.new('RGB',(1280,360),'#182932');d=ImageDraw.Draw(board);board.paste(master_small,(125,25+224-round(977*scale)));d.text((4,3),'West original master /148 ruler',fill='white')
for i,(name,im) in enumerate([('exact West idle',idle),('new West arm-ready trial',lean),('exact West swim reference',swim)],1):
 x=i*320;board.paste(im,(x,25),im);d.text((x+4,3),name,fill='white');d.line((x,249,x+319,249),fill='#6aa39e');d.line((x,101,x+319,101),fill='#61707c')
board.save(P/'arm-ready-master-review.png')
e={'scope':'New standalone West arm-ready pose trial, not complete transition/normal admitted bank. Exact West idle and swim reference endpoints on same fixed320canvas/p160224/H148; no mirrored East anatomy. New crouch/lift/prone intermediates, helmet pair, exact live phases/timing/native/Continue and full-family consistency remain.','authoringCanvas':raw.size,'wholeCanvasScale':320/raw.width,'translation':[0,shift],'semanticBootROI':[130,190,185,260],'soleBefore':sole,'soleAfter':224,'perPoseBBoxHeightFit':False,'grade':'Conditioned on graded West refs/original right master; no unrelated old raw-source curve reapplied. Visual grade acceptance pending.','coreOpaqueBBox':Image.fromarray((labs==core).astype('uint8')*255).getbbox(),'nativeAlphaBBox':lean.getchannel('A').getbbox(),'sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [P/'sources/arm-ready-canvas-v3.png',P/'sources/arm-ready-native-v3.png',P/'sources/reference-idle-native.png',P/'sources/reference-swim-native.png']}}
(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8');(P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill West water lean trial</title><style>body{background:#182932;color:#eee;font:16px sans-serif}img{max-width:100%}</style><h1>Bill West — first water transition pose</h1><p>'+e['scope']+'</p><img src="arm-ready-master-review.png">',encoding='utf-8')
print(json.dumps({'rawCanvas':raw.size,'wholeCanvasScale':320/raw.width,'bbox':e['nativeAlphaBBox'],'scope':'partial source-only pose trial'}))
