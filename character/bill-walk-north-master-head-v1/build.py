"""Bounded native master-head fit over unchanged selected north walking bodies."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_fill_holes,binary_dilation,label
P=Path(__file__).resolve().parent;R=P.parents[1];P.mkdir(exist_ok=True)
inventory=R/'character/bill-selected-source-audit-2026-10-01-locomotion-v4/source-inventory.json';audit=json.loads(inventory.read_text());s=audit['selectedStateSources']['bare']['walk-north'];m=json.loads((R/s['manifest']).read_text());state=copy.deepcopy(next(s for s in m['states'] if s['id']=='walk-north'))
reg=json.loads((P.parent/'bill-run-head-locked-v1/head-registration.json').read_text());d=next(d for d in reg['directions'] if d['direction']=='north');head=Image.open(P.parent/'bill-run-head-locked-v1'/d['componentFile']).convert('RGBA');h=np.array(head);box=d['sourceBox'];nativehead=P/'sources/north-master-head.png';nativehead.parent.mkdir(exist_ok=True);head.save(nativehead);headbottom=int(np.where(h[:,:,3]>160)[0].max());rows=[];files=[];yy,xx=np.indices((256,256))
master=Image.open(R/d['master']).convert('RGBA');choices=[('Master',master)]
for i,f in enumerate(s['sourceFiles']):
 original=Image.open(R/f[6:]).convert('RGBA');plane=Image.new('RGBA',(256,256));offset=[round(128-s['pivot'][0]),round(224-s['pivot'][1])];plane.alpha_composite(original,offset);a=np.array(plane);rgb=a[:,:,:3].astype(int);roi=(a[:,:,3]>180)&(xx>=100)&(xx<166)&(yy>=55)&(yy<105);y,x=np.where(roi);top=int(y.min());crown=roi&(yy<top+14);y,x=np.where(crown);left=int(x.min())-2;right=int(x.max())+3;axis=(int(x.min())+int(x.max()))/2
 tinted=(a[:,:,3]>0)&(rgb[:,:,0]>1.08*rgb[:,:,2])&(rgb[:,:,1]>1.04*rgb[:,:,2])&(np.ptp(rgb,axis=2)>5)&(xx>=left)&(xx<right)&(yy>=top)&(yy<top+25);erase=np.zeros((256,256),bool)
 for row in range(top,top+25):
  x=np.where(tinted[row])[0]
  if len(x):erase[row,int(x.min()):int(x.max())+1]=True
 erase=(binary_dilation(binary_fill_holes(erase),iterations=1)|((yy>=top-2)&(yy<top+16)))&(a[:,:,3]>0)&(xx>=left)&(xx<right)&(yy>=top-2)&(yy<top+25)
 pos=[round(axis-(128-box[0])),top+24-headbottom];a[erase]=0;out=Image.fromarray(a);out.alpha_composite(head,pos);dest=P/f'frames/walk-north/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest);files.append('res://'+dest.relative_to(R).as_posix());mask=P/f'sources/erase-{i:03}.png';Image.fromarray(erase.astype('uint8')*255).save(mask);sizes=np.bincount(label(np.array(out)[:,:,3]>160)[0].ravel());components=[int(n) for n in sizes[1:] if n>30]
 rows.append({'frame':i,'originalFile':f,'originalSha256':hashlib.sha256((R/f[6:]).read_bytes()).hexdigest(),'originalPivot':s['pivot'],'nativePlaneOffset':offset,'headPosition':pos,'eraseMask':mask.relative_to(P).as_posix(),'substantialComponents':components})
 choices.append((str(i),out))
state['frameFiles']=files
man={'name':'Bill north walk native master-head fit','status':'selected_runtime','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'strideDistanceCells':{'walk-north':m['strideDistanceCells']['walk-north']},'states':[state]}
(P/'manifest.json').write_text(json.dumps(man,indent=2)+'\n');(P/'head-registration.json').write_text(json.dumps({'master':d['master'],'sourceBox':box,'componentFile':'sources/north-master-head.png','nativeScale':1,'sourceManifest':s['manifest'],'inventorySha256':hashlib.sha256(inventory.read_bytes()).hexdigest(),'frames':rows},indent=2)+'\n')
board=Image.new('RGB',(1344,1344),(34,52,62));draw=ImageDraw.Draw(board)
for i,(name,im) in enumerate(choices):
 x=i%6*224;y=i//6*224;small=im.resize((142,142),Image.Resampling.LANCZOS);board.paste(small,(x+41,y+16),small);crop=im.crop((100,65,166,115)).resize((158,120),Image.Resampling.NEAREST);board.paste(crop,(x+33,y+96),crop);draw.text((x+7,y+4),name,fill='white')
board.save(P/'master-head-review.png');print(json.dumps({'frames':len(files),'candidateOnly':True,'detachedFrames':[r['frame'] for r in rows if len(r['substantialComponents'])!=1]}))
