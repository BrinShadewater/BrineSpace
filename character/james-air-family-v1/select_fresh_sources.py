from pathlib import Path
import json,shutil,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent
for d,r in json.loads((P/'fresh-source-record.json').read_text()).items():
 p=P.parent/('james-air-'+d+'-v1');origin=r['hint'].split(' as ')[1].split(' by default')[0]
 if d=='west':
  for name in ['source.png','source-audit.json','source-prompt.txt','source-origin.json']:
   dest=p/name.replace('source','source-v3',1)
   if not dest.exists():shutil.copy2(p/name,dest)
  if not (p/'source-crops-v3').exists():shutil.copytree(p/'source-crops',p/'source-crops-v3')
  shutil.copy2(origin,p/'source-v4-master-only.png');shutil.copy2(origin,p/'source.png');(p/'source-prompt.txt').write_text(r['prompt']);(p/'source-origin.json').write_text(json.dumps(dict(originalPath=origin,sha256=hashlib.sha256((p/'source.png').read_bytes()).hexdigest(),revision='v4-master-only'),indent=2)+'\n')
 else:
  file=p/'recover-source-v4.png';shutil.copy2(origin,file);(p/'recover-source-v4-prompt.txt').write_text(r['prompt']);(p/'recover-source-v4-origin.json').write_text(json.dumps(dict(originalPath=origin,sha256=hashlib.sha256(file.read_bytes()).hexdigest(),revision='v4-master-only-recovery'),indent=2)+'\n')
  a=np.array(Image.open(file).convert('RGBA'));labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;ids=sorted(np.argsort(counts)[-6:],key=lambda k:np.where(labs==k)[1].mean());records=[];heads=[];board=Image.new('RGB',(1536,300),'#303b40');draw=ImageDraw.Draw(board)
  for j,k in enumerate(ids):
   yy,xx=np.where(labs==k);box=[max(0,int(xx.min())-3),max(0,int(yy.min())-3),min(a.shape[1],int(xx.max())+4),min(a.shape[0],int(yy.max())+4)];x0,y0,x1,y1=box;cell=a[y0:y1,x0:x1].copy();cell[~binary_dilation(labs[y0:y1,x0:x1]==k,iterations=2)]=0;im=Image.fromarray(cell);dest=p/'recovery-crops-v4'/f'{j+6:03d}.png';dest.parent.mkdir(exist_ok=True);im.save(dest)
   rr,gg,bb=cell[:,:,:3].astype(float).transpose(2,0,1);warm=(cell[:,:,3]>180)&(rr-gg>10)&(gg-bb>7)&(rr-bb>24)&((rr-gg)/np.maximum(1,rr-bb)>.42);ls,ns=label(warm);cs=np.bincount(ls.ravel());cs[0]=0;hy,hx=np.where(ls==cs.argmax());point=np.array([hx.mean()-10,hy.mean()-16]);heads.append(point.tolist());records.append(dict(index=j+6,sourceBox=box,width=im.width,height=im.height))
   zoom=im.crop((*np.rint(point-[75,75]).astype(int),*np.rint(point+[75,75]).astype(int))).resize((210,210),Image.Resampling.NEAREST);at=(j*256+8,50);board.paste(zoom,at,zoom);draw.line((at[0]+105,at[1],at[0]+105,at[1]+210),fill='cyan');draw.line((at[0],at[1]+105,at[0]+210,at[1]+105),fill='cyan');draw.text((at[0],10),str(j+6)+' '+str(np.rint(point).astype(int).tolist()),fill='white')
  (p/'recovery-v4-audit.json').write_text(json.dumps(dict(sourceSha256=hashlib.sha256(file.read_bytes()).hexdigest(),poses=records,heads=heads),indent=2)+'\n');board.save(p/'recovery-v4-head-audition.png');print('East recovery',[(q['width'],q['height']) for q in records],np.rint(heads).astype(int).tolist())
