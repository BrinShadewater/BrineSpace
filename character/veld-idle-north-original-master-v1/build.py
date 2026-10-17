from pathlib import Path
import json,hashlib,copy
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];B=R/'character/veld-cardinal-actions-shared-original-helmet-v1'
rawpath=P/'raw-idle-v3.png';raw=Image.open(rawpath).convert('RGBA');a=np.array(raw);labels,n=label(a[:,:,3]>200);sizes=np.bincount(labels.ravel());sizes[0]=0;components=[int(i) for i in np.where(sizes>10000)[0]];assert len(components)==4
boxes=[]
for component in components:
 y,x=np.where(labels==component);boxes.append((int(x.min()),int(x.max()),component))
boxes.sort();bounds=[0]+[(boxes[i][1]+boxes[i+1][0])//2 for i in range(3)]+[raw.width];cells=[a[:,bounds[i]:bounds[i+1]].copy() for i in range(4)]
y,x=np.where(cells[0][:,:,3]>200);scale=148/(y.max()-y.min()+1)
for adjustment in [0,1,-1,2,-2]:
 resize_height=round(raw.height*scale)+adjustment
 im=Image.fromarray(cells[0]).resize((round(cells[0].shape[1]*resize_height/raw.height),resize_height),Image.Resampling.LANCZOS);sy,sx=np.where(np.array(im)[:,:,3]>200)
 if sy.max()-sy.min()+1==148:break
else:raise AssertionError('One source ruler cannot be registered')
scale=resize_height/raw.height
shellpath=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/000.png';shell=Image.open(shellpath).convert('RGBA')
refs={g:[] for g in ['bare','helmet']};checks=0;rows=[];bindings={};board=Image.new('RGB',(1024,650),'#202a30');draw=ImageDraw.Draw(board)
for i,cell in enumerate(cells):
 assert not np.any(cell[:,[0,-1],3]>20);checks+=1
 lab,nn=label(cell[:,:,3]>200);areas=np.bincount(lab.ravel());areas[0]=0;mask=lab==int(areas.argmax());clean=cell.copy();clean[~binary_dilation(mask,iterations=2)]=0
 im=Image.fromarray(clean).resize((round(cell.shape[1]*scale),resize_height),Image.Resampling.LANCZOS);s=np.array(im);sy,sx=np.where(s[:,:,3]>200);top=int(sy.min());_,hx=np.where(s[top:top+16,:,3]>128);offset=(round(128-(hx.min()+hx.max())/2),224-int(sy.max()));body=Image.new('RGBA',(256,256));body.alpha_composite(im,offset)
 (P/'diagnostic-generated').mkdir(exist_ok=True);body.save(P/f'diagnostic-generated/{i:03}.png')
 if i==0:body=Image.open(P/'clean-idle-master.png').convert('RGBA')
 b=np.array(body);ys,xs=np.where(b[:,:,3]>200);htop=int(ys.min());_,headx=np.where(b[htop:htop+20,:,3]>128);clear=[int(headx.min())-3,htop,int(headx.max())+4,htop+26];pos=(112,68)
 equipped=body.copy();equipped.paste((0,0,0,0),tuple(clear));equipped.alpha_composite(shell,pos)
 protected=np.ones((256,256),bool);protected[min(clear[1],pos[1]):max(clear[3],pos[1]+shell.height),min(clear[0],pos[0]):max(clear[2],pos[0]+shell.width)]=False
 assert np.array_equal(np.array(equipped)[protected],b[protected]);checks+=1
 rows.append({'phase':i,'wholeSourceOffset':list(offset),'sourceScale':scale,'bodyHeight':int(ys.max()-ys.min()+1),'bodyWidth':int(xs.max()-xs.min()+1),'headRegionWidth':int(headx.max()-headx.min()+1),'helmetPosition':list(pos),'clearBox':clear,'restAlias':i==0})
 for row,(gear,f) in enumerate([('bare',body),('helmet',equipped)]):
  path=P/'frames'/gear/f'{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);f.save(path);ref='res://'+path.relative_to(R).as_posix();refs[gear].append(ref);bindings[ref]=hashlib.sha256(path.read_bytes()).hexdigest();aa=np.array(f)
  assert not np.any(np.concatenate([aa[0,:,3],aa[-1,:,3],aa[:,0,3],aa[:,-1,3]])>20);checks+=1;board.paste(f,(i*256,row*300+30),f);draw.text((i*256+3,row*300+4),gear+' '+str(i),fill='white')
for gear in refs:
 data=json.loads((B/f'{gear}-manifest.json').read_text());data['states']=[s for s in data['states'] if s['id'].endswith('-north')]
 baseline=copy.deepcopy(data);old_idle=next(s for s in baseline['states'] if s['id']=='unload-north')['frameFiles'][-1]
 idle={'id':'idle-north','frameFiles':refs[gear],'frameCount':4,'frameDurationsMs':[375]*4,'loop':True,'facings':['north']*4,'waterKinds':['idle']*4,'waterPoses':[False]*4,'depthOffsets':[0.0]*4}
 old_state=copy.deepcopy(idle);old_state.update(frameFiles=[old_idle],frameCount=1,frameDurationsMs=[1500],facings=['north'],waterKinds=['idle'],waterPoses=[False],depthOffsets=[0.0]);baseline['states'].append(old_state)
 (P/f'baseline-{gear}-manifest.json').write_text(json.dumps(baseline,indent=2)+'\n')
 for state in data['states']:
  if state['id']=='unload-north':state['frameFiles'][-1]=refs[gear][0]
  elif state['id']=='pickup-north':state['frameFiles'][0]=refs[gear][0]
 data['states'].append(idle);data.update(name='Veld original-master North breathing idle '+gear,status='staged_not_installed');(P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n')
 states={s['id']:s for s in data['states']}
 for action,slot in [('unload-north',-1),('pickup-north',0)]:assert states[action]['frameFiles'][slot]==refs[gear][0];checks+=1
 images=[]
 for ref in refs[gear]:bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(Image.open(R/ref[6:]).convert('RGBA'));images.append(bg)
 apng=P/f'{gear}-idle-north.apng';images[0].save(apng,format='PNG',save_all=True,append_images=images[1:],duration=[375]*4,loop=0,disposal=0,blend=0)
 with Image.open(apng) as decoded:
  assert decoded.n_frames==4
  for j,frame in enumerate(images):decoded.seek(j);assert decoded.convert('RGBA').tobytes()==frame.tobytes();assert decoded.info['duration']==375;checks+=2
board.save(P/'paired-original-idle.png')
for f in [rawpath,P/'clean-idle-master.png',P/'clean-master-reference.json',shellpath,B/'bare-manifest.json',B/'helmet-manifest.json']:bindings[f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'sourceScale':scale,'oneStandingRuler':148,'rows':rows,'bindings':bindings,'originalRestSource':'clean-idle-master.png','shellSource':shellpath.relative_to(R).as_posix(),'shellScale':1,'postGenerationGradeChanged':False,'durationMs':1500,'scope':'Whole original-guided North idle; phase0 exact prepared-master alias, not pixel-exact legacy source. Exact cargo/idle source joins, older cargo/gait body grade retained. No normal world/controller/case/save acceptance.'},indent=2)+'\n')
print(f'{checks} source/registration/protected-body/alias/APNG checks0; four paired whole idle poses.')
