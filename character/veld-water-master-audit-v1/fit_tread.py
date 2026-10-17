"""Fit unchanged accepted directional helmet heads onto selected treading bodies."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
coverage=json.loads((ROOT/'character/veld-consistency-audit-v2/coverage.json').read_text())
masters={'north':'character/veld-shared-helmet-v1/fitted-north.png','east':'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png','south':'character/veld-shared-helmet-south-v1/fitted-helmet.png','west':'character/veld-shared-helmet-v1/fitted-west.png'}
# East uses the exact accepted fitted source crop, as in the turn family.
records=[];states=[];checks=0
sheet=Image.new('RGBA',(6*184,4*220),'#202a30');draw=ImageDraw.Draw(sheet)
for row,direction in enumerate(['north','east','south','west']):
 key='tread-'+direction;selected=coverage['selected']['bare'][key]
 original=json.loads((ROOT/selected['manifest']).read_text());state=next(s for s in original['states'] if s['id']==key).copy();files=[]
 head=Image.open(ROOT/masters[direction]).convert('RGBA')
 if direction=='east':
  head=head.crop((82,17,116,55))
 for i,path in enumerate(selected['files']):
  bare=Image.open(ROOT/path).convert('RGBA');a=np.array(bare);ys,xs=np.where(a[20:55,60:125,3]>200)
  crown=int(ys.min())+20;center=(int(xs.min())+int(xs.max()))/2+60
  pos=(round(center-head.width/2),crown-7)
  # Clear the original head above the shoulder/collar, then graft the native component.
  clear=(60,20,125,62);out=bare.copy();out.paste((0,0,0,0),clear);out.alpha_composite(head,pos)
  after=np.array(out);protected=np.ones(a.shape[:2],bool);protected[20:70,60:125]=False
  assert np.array_equal(a[protected],after[protected]);checks+=1
  assert head.size in [(33,35),(34,38),(35,39)];checks+=1
  assert not np.any(np.concatenate([after[0,:,3],after[-1,:,3],after[:,0,3],after[:,-1,3]])>20);checks+=1
  file=f'frames/helmet/{key}/{i:03}.png';(HERE/file).parent.mkdir(parents=True,exist_ok=True);out.save(HERE/file);files.append(file)
  records.append({'state':key,'slot':i,'body':path,'bodySha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),'head':masters[direction],'headSha256':hashlib.sha256((ROOT/masters[direction]).read_bytes()).hexdigest(),'headSize':head.size,'headCrop':[82,17,116,55] if direction=='east' else None,'position':pos,'bareCrown':crown,'clearBox':clear,'protectedOutside':[60,20,125,70]})
  sheet.alpha_composite(out,(i*184,row*220+24));draw.text((i*184+4,row*220+4),key+' / '+str(i),fill='white')
 state['frameFiles']=files;states.append(state)
manifest={**original,'name':'Veld master helmet treading','standingHeight':148,'pivot':[92,70],'equipment':'diving-helmet','status':'staged_master_fit_pending_visual_review','states':states}
(HERE/'tread-helmet-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(HERE/'tread-fit-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'noScalingOrGradeChange':True,'installed':False,'records':records},indent=2)+'\n',encoding='utf-8');sheet.save(HERE/'tread-master-fits.png')
print(f'{checks} exact-body/native-scale/clipping checks passed for 24 fitted treading frames.')
