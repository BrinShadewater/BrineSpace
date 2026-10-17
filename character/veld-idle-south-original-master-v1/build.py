from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
rawpath=P/'raw-idle-v1.png';raw=Image.open(rawpath).convert('RGBA');a=np.array(raw);lab,n=label(a[:,:,3]>200);sizes=np.bincount(lab.ravel());sizes[0]=0;boxes=[]
for component in np.argsort(sizes)[-4:]:
 assert sizes[component]>10000
 y,x=np.where(lab==component);boxes.append((int(x.min()),int(x.max())))
boxes.sort();bounds=[0]+[(boxes[i][1]+boxes[i+1][0])//2 for i in range(3)]+[raw.width];cells=[a[:,bounds[i]:bounds[i+1]].copy() for i in range(4)]
y,x=np.where(cells[0][:,:,3]>200);scale=148/(y.max()-y.min()+1)
master=R/'character/veld-south-material-master-v2';shellpath=R/'character/veld-shared-helmet-south-v1/fitted-helmet.png';shell=Image.open(shellpath).convert('RGBA');sa=np.array(shell);_,gx=np.where(sa[-5:,:,3]>160);gasket=(gx.min()+gx.max())/2
board=Image.new('RGB',(1024,650),'#202a30');draw=ImageDraw.Draw(board);rows=[];checks=0;refs={g:[] for g in ['bare','helmet']};bindings={}
(P/'diagnostic-ungraded').mkdir(exist_ok=True)
for i,cell in enumerate(cells):
 assert not np.any(cell[:,[0,-1],3]>20);checks+=1
 labels,n=label(cell[:,:,3]>200);areas=np.bincount(labels.ravel());areas[0]=0;mask=labels==int(areas.argmax());y,x=np.where(mask);floor=int(y.max());top=int(y.min());_,hx=np.where(mask[top:top+round(16/scale)]);axis=(hx.min()+hx.max())/2
 clean=cell.copy();clean[~binary_dilation(mask,iterations=2)]=0;scaled=Image.fromarray(clean).resize((round(cell.shape[1]*scale),round(cell.shape[0]*scale)),Image.Resampling.LANCZOS);scaled_a=np.array(scaled);sy,sx=np.where(scaled_a[:,:,3]>200);st=int(sy.min());_,shx=np.where(scaled_a[st:st+16,:,3]>128);offset=(round(128-(shx.min()+shx.max())/2),224-int(sy.max()));body=Image.new('RGBA',(256,256));body.alpha_composite(scaled,offset);body.save(P/f'diagnostic-ungraded/{i:03}.png')
 ar=np.array(body);y,x=np.where(ar[:,:,3]>200);htop=int(y.min());rgb=ar[:,:,:3].astype(float);warm=(ar[:,:,3]>128)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[htop+16:]=False;wy,wx=np.where(warm)
 if i==0:
  body=Image.open(P/'original-idle-master.png').convert('RGBA');equipped=body.copy();equipped.paste((0,0,0,0),(111,77,143,102));equipped.alpha_composite(shell,(110,69));fit='Exact opaque-ruler original authored idle alias; original35x39shell at11069'
 else:
  _,skullx=np.where(ar[htop:htop+16,:,3]>128);pos=(110,69);clear=(int(skullx.min())-3,htop,int(skullx.max())+4,htop+24)
  equipped=body.copy();equipped.paste((0,0,0,0),clear);equipped.alpha_composite(shell,pos);ea=np.array(equipped);protected=np.ones(ar.shape[:2],bool);protected[min(clear[1],pos[1]):max(clear[3],pos[1]+shell.height),min(clear[0],pos[0]):max(clear[2],pos[0]+shell.width)]=False;assert np.array_equal(ea[protected],ar[protected]);checks+=1;fit={'position':pos,'clearBox':clear,'shellScale':1,'shellGradeChanged':False}
 rows.append({'phase':i,'wholeSourceOffset':offset,'generatedHeight':int(y.max()-y.min()+1),'generatedWidth':int(x.max()-x.min()+1),'headTop':htop,'warmTop16Width':int(wx.max()-wx.min()+1),'helmetFit':fit})
 for row,(gear,im) in enumerate([('bare',body),('helmet',equipped)]):
  path=P/f'frames/{gear}/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path);ref='res://'+path.relative_to(R).as_posix();refs[gear].append(ref);bindings[ref]=hashlib.sha256(path.read_bytes()).hexdigest();ar=np.array(im);assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1;board.paste(im,(i*256,row*300+30),im);draw.text((i*256+3,row*300+4),gear+' '+str(i),fill='white')
for gear in refs:
 data=json.loads((master/f'cargo-{gear}-manifest.json').read_text(encoding='utf-8'));states=[s for s in data['states'] if s['id']!='idle-south']
 for family in ['start','gait']:
  for state in json.loads((master/f'{family}-{gear}-manifest.json').read_text(encoding='utf-8'))['states']:
   if state['id'] not in [s['id'] for s in states]:states.append(state)
 for state in states:
  if state['id']=='unload-south':state['frameFiles'][-1]=refs[gear][0]
  elif state['id']=='pickup-south':state['frameFiles'][0]=refs[gear][0]
 states.append({'id':'idle-south','frameFiles':refs[gear],'frameCount':4,'frameDurationsMs':[375]*4,'loop':True,'facings':['south']*4,'waterKinds':['idle']*4,'waterPoses':[False]*4,'depthOffsets':[0.0]*4})
 data.update(name='Veld South original-master breathing idle '+gear,status='staged_idle_not_installed',states=states)
 (P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 previews=[]
 for ref in refs[gear]:
  bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(Image.open(R/ref[6:]).convert('RGBA'));previews.append(bg)
 path=P/f'{gear}-idle-south.apng';previews[0].save(path,format='PNG',save_all=True,append_images=previews[1:],duration=[375]*4,loop=0,disposal=0,blend=0)
 with Image.open(path) as im:
  assert im.n_frames==4
  for j,frame in enumerate(previews):im.seek(j);assert im.convert('RGBA').tobytes()==frame.tobytes();assert im.info['duration']==375;checks+=2
board.save(P/'paired-original-idle.png')
record={'checks':checks,'failures':0,'sourceSHA256':hashlib.sha256(rawpath.read_bytes()).hexdigest(),'oneStandingRuler':148,'scale':scale,'gutters':bounds,'rows':rows,'bindings':bindings,'gradeChanged':False,'shellSource':shellpath.relative_to(R).as_posix(),'shellSHA256':hashlib.sha256(shellpath.read_bytes()).hexdigest(),'durationMs':1500,'scope':'Whole authored source idle, exact original bare/helmet master-palette phase0 joins. No normal controller/route/save/prop lifecycle/full set acceptance.'}
(P/'registration.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':checks,'scale':scale,'rows':rows}))
