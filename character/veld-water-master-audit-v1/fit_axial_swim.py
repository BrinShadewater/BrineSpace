"""Fit generated master construction at axial swim pitch; preserve body/arms."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];coverage=json.loads((ROOT/'character/veld-consistency-audit-v2/coverage.json').read_text());records=[];checks=0
sheet=Image.new('RGBA',(6*208,2*246),'#202a30');draw=ImageDraw.Draw(sheet)
for row,direction in enumerate(['north','south']):
 raw=Image.open(HERE/('axial-helmet-source-v1.png' if direction=='north' else 'south-helmet-source-v2.png')).convert('RGBA')
 if direction=='north':raw=raw.crop((0,0,raw.width//2,raw.height))
 a=np.array(raw);labels,n=label(a[:,:,3]>160);largest=1+np.argmax(np.bincount(labels.ravel())[1:]);keep=binary_dilation(labels==largest,iterations=2);a[~keep]=0;y,x=np.where(a[:,:,3]>200);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];raw=Image.fromarray(a).crop(box)
 scale=(33 if direction=='north' else 35)/raw.width;head=raw.resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS)
 a=np.array(head);rgb=a[:,:,:3].astype(float);skin=(rgb[:,:,0]>rgb[:,:,1]*1.17)&(rgb[:,:,1]>rgb[:,:,2]*1.12)&(rgb[:,:,0]>110);rgb[skin]*=[.83,.83,.85];neutral=(rgb.max(2)-rgb.min(2)<38)&(rgb.mean(2)>145);lamp=(rgb.mean(2)>205)&(rgb[:,:,2]>=rgb[:,:,0]);rgb[neutral&~lamp]*=.86;a[:,:,:3]=rgb.clip(0,255).astype('uint8');a[a[:,:,3]<4]=0;head=Image.fromarray(a);head.save(HERE/f'fitted-swim-{direction}-head.png')
 selected=coverage['selected']['bare']['swim-'+direction];source=json.loads((ROOT/selected['manifest']).read_text());state=next(s for s in source['states'] if s['id']=='swim-'+direction).copy();files=[]
 for i,path in enumerate(selected['files']):
  body=Image.open(ROOT/path).convert('RGBA');before=np.array(body);out=body.copy()
  if direction=='north':
   crown=[28,24,21,20,25,25][i];pos=(76,crown-5);clear=(77,crown-1,109,crown+26);foreground=[(68,0,116,26)] if i in [0,5] else ([(56,16,76,50),(108,16,128,50)] if i==4 else [])
  else:pos=(86,180-head.height);clear=(80,140,120,181);foreground=[]
  out.paste((0,0,0,0),clear);out.alpha_composite(head,pos)
  for rect in foreground:out.paste(body.crop(rect),rect[:2])
  # South fingers cross below visor in the catch phase; preserve only neutral glove pixels.
  if direction=='south' and i==3:
   b=before[:,:,:3].astype(int);yy,xx=np.indices(before.shape[:2]);fg=(yy>=178)&(yy<199)&(xx>=83)&(xx<122)&(before[:,:,3]>200)&(b[:,:,0]<b[:,:,1]+12)
   after=np.array(out);after[fg]=before[fg];out=Image.fromarray(after)
  after=np.array(out);protected=np.ones(before.shape[:2],bool);protected[clear[1]:clear[3],clear[0]:clear[2]]=False;protected[pos[1]:pos[1]+head.height,pos[0]:pos[0]+head.width]=False
  assert np.array_equal(before[protected],after[protected]);checks+=1
  assert not np.any(np.concatenate([after[0,:,3],after[-1,:,3],after[:,0,3],after[:,-1,3]])>20);checks+=1
  assert head.width==(33 if direction=='north' else 35);checks+=1
  file=f'frames/helmet/swim-{direction}/{i:03}.png';(HERE/file).parent.mkdir(parents=True,exist_ok=True);out.save(HERE/file);files.append(file)
  records.append({'direction':direction,'slot':i,'source':path,'sourceSha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),'headSource':'axial-helmet-source-v1.png' if direction=='north' else 'south-helmet-source-v2.png','sourceCrop':box,'anatomicalScale':scale,'position':pos,'clear':clear,'foreground':foreground,'neutralGloveMask':direction=='south' and i==3})
  sheet.alpha_composite(out,(i*208,row*246+22));draw.text((i*208+4,row*246+4),direction+' / '+str(i),fill='white')
 state['frameFiles']=files;manifest={**source,'name':'Veld master axial swim '+direction,'equipment':'diving-helmet','status':'staged_master_fit_pending_visual_review','states':[state]};(HERE/f'swim-{direction}-helmet-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(HERE/'axial-swim-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'records':records,'installed':False},indent=2)+'\n',encoding='utf-8');sheet.save(HERE/'axial-swim-master-fits-v1.png');print(f'{checks} axial body/scale/clipping checks pass.')
