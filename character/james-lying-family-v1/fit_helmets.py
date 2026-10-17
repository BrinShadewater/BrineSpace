"""Independent authored helmet pitch donors, one master-calibrated head scale per direction."""
from pathlib import Path
import json,copy,os,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
boxes={
 'east':[[108,139,189,211],[413,225,495,299],[661,258,745,332],[938,287,1029,356],[1257,316,1347,386],[1596,365,1677,440]]+[[20+319*j,630,106+319*j,708] for j in range(6)],
 'west':[[87,142,166,216],[355,221,439,291],[785,263,869,330],[1178,294,1260,361],[1520,339,1601,426],[1845,343,1927,429]]+[[246+321*j,650,327+321*j,737] for j in range(6)],
 'south':[[109,62,216,152],[426,161,535,246],[756,149,867,237],[1078,169,1188,254],[1398,197,1505,270],[1722,206,1828,274]]+[[109+322*j,528,218+322*j,601] for j in range(6)],
 'north':[[103,60,202,141],[392,165,491,243],[685,195,784,266],[987,216,1086,280],[1279,238,1380,302],[1567,247,1666,311]]+[[105+292*j,558,203+292*j,622] for j in range(6)]}
combined=None
for d in ['east','south','west','north']:
 p=P.parent/('james-lying-'+d+'-v1');bare=json.loads((p/'bare-manifest.json').read_text());reg=json.loads((p/'registration.json').read_text());source=Image.open(p/'source-helmet.png').convert('RGBA');master=Image.open(p/'selected-helmet-master.png').convert('RGBA');master_full=Image.new('RGBA',(256,256));master_full.alpha_composite(master,(36,52));ma=np.array(master_full);yy,xx=np.indices(ma.shape[:2])
 # Calibrate only the shell: shoulders below the helmet must not inflate its width.
 opaque=ma[:,:,3]>180;top=int(np.where(opaque)[0].min());mask=opaque&(yy<top+28);y,x=np.where(mask);mw=int(x.max()-x.min()+1);scale=mw/(boxes[d][0][2]-boxes[d][0][0]);bare0=np.array(Image.open(p/'frames/lie-down/000.png').convert('RGBA'));opaque0=bare0[:,:,3]>180;bt=int(np.where(opaque0)[0].min());ym,xm=np.where(opaque0&(yy<bt+5));actual_bare_anchor=np.array([xm.mean(),bt+14]);offset=np.array([x.mean(),y.mean()])-actual_bare_anchor
 eq=copy.deepcopy(bare);eq['name']='James '+d+' lying shared helmet candidate';records=[];rows=[]
 for i,box in enumerate(boxes[d]):
  crop=source.crop(box);a=np.array(crop);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);neutral=(a[:,:,3]>0)&(abs(r-g)<13)&(abs(g-b)<17);rgb[neutral]*=.9;a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');crop=Image.fromarray(a);patch=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
  point=np.array(reg['tracking'][i]['headAnchor']);target=point+offset+[0,5 if d=='south' else (3 if d in ['east','west'] else 0)];pos=np.rint(target-[patch.width/2,patch.height/2]).astype(int);hb=reg['tracking'][i]['protectedHeadBox'];x0,y0,x1,y1=hb;y1-=5
  # The lying endpoint belongs to the selected sleep neutral; do not borrow a generated body.
  f=p/'frames/lie-down'/f'{i:03d}.png' if i<6 else p/'frames/sleep'/f'{i-6:03d}.png';body=Image.open(f).convert('RGBA');base=np.array(body);erase=((xx-point[0])/15)**2+((yy-(point[1]-1))/13)**2<=1;base[erase]=0;out=Image.fromarray(base);out.alpha_composite(patch,tuple(pos));region=[min(x0,int(pos[0])),min(y0,int(pos[1])),max(x1,int(pos[0])+patch.width),max(y1,int(pos[1])+patch.height)]
  if i==0:out=master_full.copy()
  rows.append(out);records.append(dict(sourceHeadBox=box,fixedHeadScale=scale,position=pos.tolist(),editRegion=region,neutralShellGain=.9,exactStandingMaster=i==0))
 rows[6]=rows[5].copy();rows[11]=rows[5].copy();records[6]=copy.deepcopy(records[5]);records[11]=copy.deepcopy(records[5])
 if d=='north':
  for i in range(7,11):rows[i]=rows[5].copy();records[i]=copy.deepcopy(records[5])
 hashes={}
 for st in eq['states']:
  files=[]
  for j,i in enumerate(st['provenance']['sourcePoses']):
   path=p/'frames/helmet'/st['id'].rsplit('-',1)[0]/f'{j:03d}.png';path.parent.mkdir(parents=True,exist_ok=True);rows[i].save(path);rel=path.relative_to(p).as_posix();files.append(rel);hashes[rel]=hashlib.sha256(path.read_bytes()).hexdigest()
  st['frameFiles']=files;st['provenance'].update(helmetSource='source-helmet.png',helmetPrompt='helmet-prompt.txt',fixedHeadScale=scale,helmetDerivation='Independent pitch donor heads, one standing-master-calibrated head scale; exact body outside recorded head edit regions')
 (p/'helmet-manifest.json').write_text(json.dumps(eq,indent=2)+'\n');(p/'helmet-registration.json').write_text(json.dumps(dict(sourceSha256=hashlib.sha256((p/'source-helmet.png').read_bytes()).hexdigest(),masterHeadWidth=mw,headScale=scale,centerOffset=offset.tolist(),tracking=records),indent=2)+'\n');(p/'helmet-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
 board=Image.new('RGB',(1536,640),'#303b40');draw=ImageDraw.Draw(board)
 for i,im in enumerate(rows):at=(i%6*256,50+i//6*320);board.paste(im,at,im);draw.text((at[0]+8,at[1]-42),d+' helmet '+str(i),fill='white')
 board.save(p/'helmet-contact.png')
 if combined is None:combined={k:copy.deepcopy(v) for k,v in eq.items() if k!='states'};combined['states']=[];combined['name']='James directional lying shared helmet candidate'
 for st in eq['states']:st=copy.deepcopy(st);st['frameFiles']=[Path(os.path.relpath(p/f,P)).as_posix() for f in st['frameFiles']];combined['states'].append(st)
 print(d,'18 helmet refs, standing calibrated shell width',mw,'head scale',round(scale,4))
(P/'helmet-manifest.json').write_text(json.dumps(combined,indent=2)+'\n')
