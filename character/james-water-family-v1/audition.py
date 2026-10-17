"""Fixed cranial-ruler scale review; not a registered runtime animation pack."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from extract_sources import extract
P=Path(__file__).resolve().parent;R=P.parents[1]
master_root=R/'character/crew-runtime-matte-v1/branforth';master_pack=json.loads((master_root/'manifest.json').read_text());reports={}
for d in ['east','south','west','north']:
 p=P.parent/('james-water-'+d+'-v1');cells=extract(p/'source.png');state=next(s for s in master_pack['states'] if s['id']=='idle-'+d);master=Image.open(master_root/state['frameFiles'][0]).convert('RGBA');ma=np.array(master);mask=ma[:,:,3]>180;yy,xx=np.indices(mask.shape);mtop=int(np.where(mask)[0].min());my,mx=np.where(mask&(yy<mtop+20));mw=int(mx.max()-mx.min()+1)
 first=np.array(cells[0][0]);mask=first[:,:,3]>180;yy,xx=np.indices(mask.shape);top=int(np.where(mask)[0].min());y,x=np.where(mask&(yy<top+36));sw=int(x.max()-x.min()+1);scale=mw/sw
 # The crown cap excludes shoulders/collar. Bent tread knees never set scale.
 gain=None;rows=[];records=[]
 for i,(cell,box) in enumerate(cells):
  a=np.array(cell);h,w=a.shape[:2];mask=a[:,:,3]>180;cy,cx=np.where(mask);at=(round(128-(cx.min()+cx.max())/2*scale),round(238-(cy.max())*scale));im=Image.new('RGBA',(256,276));small=cell.resize((round(w*scale),round(h*scale)),Image.Resampling.LANCZOS);im.alpha_composite(small,at)
  path=p/'audition'/f'{i:03d}.png';path.parent.mkdir(exist_ok=True);im.save(path);rows.append(im);records.append(dict(index=i,sourceBox=box,scale=scale,translation=list(at),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 board=Image.new('RGB',(1792,936),'#303b40');draw=ImageDraw.Draw(board)
 for i,im in enumerate(rows):at=(i%6*256,36+i//6*312);board.paste(im,at,im);draw.text((at[0]+8,at[1]-28),d+' fixed-scale raw '+str(i),fill='white')
 full=Image.new('RGBA',(256,276));full.alpha_composite(master,(36,66));board.paste(full,(1536,36),full);draw.text((1544,8),'selected standing master',fill='white');board.save(p/'anatomy-audition.png')
 report=dict(status='source_anatomy_audition_pending',sourceSha256=hashlib.sha256((p/'source.png').read_bytes()).hexdigest(),scaleLandmark='First tread pose opaque cranial cap width, top36 raw pixels compared with selected master top20 native pixels; reviewed independently of bent knees',nativeCranialCapWidth=mw,sourceCranialCapWidth=sw,fixedScale=scale,poses=records,limitations=['Bottom alignment is an audit layout, not world shoulder registration','Raw source colours, not a selected matte grade','North start interiors retain twist and need replacement','Water endpoints/helmets/clearance/native selection remain pending'])
 (p/'anatomy-audition.json').write_text(json.dumps(report,indent=2)+'\n');reports[d]={k:v for k,v in report.items() if k!='poses'};print(d,'fixed scale',round(scale,5),'cranial ruler',mw,sw)
(P/'anatomy-auditions.json').write_text(json.dumps(reports,indent=2)+'\n')
