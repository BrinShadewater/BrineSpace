"""Rebuild independent north water body family and shared helmet fits from saved sources."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
H=Path(__file__).resolve().parent;R=H.parents[1];OLD=R/'character/veld-water-material-v2'
cov=json.loads((R/'character/veld-consistency-audit-v2/coverage.json').read_text())
Q=[0,15,35,55,75,90,100];SIZE=(256,256);PIVOT=[128,128];checks=0;records=[]
def components(path,count,grid=False):
 a=np.array(Image.open(path).convert('RGBA'));lab,n=label(a[:,:,3]>160);sizes=np.bincount(lab.ravel());ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:count]
 ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(a.shape[0]/2)) if grid else 0,np.where(lab==k)[1].mean()));result=[]
 for k in ids:
  y,x=np.where(lab==k);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];cut=a.copy();cut[~binary_dilation(lab==k,iterations=2)]=0;result.append((Image.fromarray(cut).crop(box),box))
 return result
ref=np.array(Image.open(R/cov['selected']['bare']['idle-north']['files'][0]).convert('RGBA'));rr=ref[:,:,:3].astype(float)
refMasks={'cloth':(ref[:,:,3]>200)&(np.ptp(rr,axis=2)<22)&(rr.mean(2)>20)&(rr.mean(2)<130),'patch':(ref[:,:,3]>200)&(rr[:,:,2]>rr[:,:,0]*1.2)&(rr[:,:,2]>rr[:,:,1]*1.3)&(rr[:,:,2]>35)}
refMasks['cloth'][:59]=False
# Combine body sources for one shared cloth/patch curve, not separate exposures.
sources=[H/'tread-source-v1.png',H/'swim-source-v1.png',OLD/'north-transition-source-v2.png'];sourceValues={key:[] for key in refMasks}
def masks(a):
 v=a[:,:,:3].astype(float)
 return {'cloth':(a[:,:,3]>200)&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),'patch':(a[:,:,3]>200)&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35)}
for source in sources:
 a=np.array(Image.open(source).convert('RGBA'));v=a[:,:,:3].astype(float)
 for key,mask in masks(a).items():sourceValues[key].extend(v[mask])
curves={key:{'knots':np.percentile(np.mean(values,axis=1),Q),'targets':np.percentile(rr[refMasks[key]],Q,axis=0)} for key,values in sourceValues.items()}
def grade(raw):
 a=np.array(raw);v=a[:,:,:3].astype(float)
 for key,mask in masks(a).items():
  curve=curves[key]
  for c in range(3):a[mask,c]=np.interp(v[mask].mean(1),curve['knots'],curve['targets'][:,c]).clip(0,255).astype('uint8')
 return Image.fromarray(a)
def equip(bare,head,crown,pitch):
 global checks
 before=np.array(bare);pos=(112,crown-(7 if pitch=='upright' else 5));clear=(114,crown-1,142,crown+22);out=bare.copy();out.paste((0,0,0,0),clear);out.alpha_composite(head,pos)
 a=np.array(out);Y,X=np.indices(before.shape[:2]);v=before[:,:,:3].astype(int)
 # Forward gloves may cross outside the brown bare-head support; retain their pixels.
 fg=(before[:,:,3]>200)&(np.ptp(v,axis=2)<28)&(Y<crown+5)&(Y>=pos[1])&(X>=112)&(X<145)
 if pitch!='upright':a[fg]=before[fg]
 protected=np.ones(before.shape[:2],bool);protected[clear[1]:clear[3],clear[0]:clear[2]]=False;protected[pos[1]:pos[1]+head.height,pos[0]:pos[0]+head.width]=False
 assert np.array_equal(before[protected],a[protected]);checks+=1
 return Image.fromarray(a),{'headPosition':list(pos),'clear':list(clear),'foregroundPixels':int(fg.sum()) if pitch!='upright' else 0}
def contain(im):
 global checks
 a=np.array(im);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1
upright=Image.open(R/'character/veld-shared-helmet-v1/fitted-north.png').convert('RGBA');prone=Image.open(R/'character/veld-water-master-audit-v1/fitted-swim-north-head.png').convert('RGBA')
allRows={v:{} for v in ['bare','helmet']}
landmarks={'tread':[(203,53,139),(627,50,138),(1049,53,140),(204,653,739),(628,658,745),(1050,657,744)],'swim':[(235,106,191),(627,107,192),(1008,102,192),(235,699,784),(627,718,803),(1018,716,801)]}
scales={'tread':21/93,'swim':21/97}
for kind in ['tread','swim']:
 source=H/f'{kind}-source-v1.png';poses=components(source,6,True);bareRows=[];helmetRows=[]
 for i,(raw,box) in enumerate(poses):
  scale=scales[kind];hx,hy,bottom=landmarks[kind][i];crown=107 if kind=='tread' else 104
  raw=grade(raw);pose=raw.resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS);pos=(round(128-(hx-box[0])*scale),round(crown-(hy-box[1])*scale));bare=Image.new('RGBA',SIZE);bare.alpha_composite(pose,pos);helmet,fit=equip(bare,upright if kind=='tread' else prone,crown,'upright' if kind=='tread' else 'prone');contain(bare);contain(helmet);bareRows.append(bare);helmetRows.append(helmet)
  records.append({'state':kind+'-north','slot':i,'source':source.name,'sourceBox':box,'anatomicalScale':scale,'sourceHeadLandmark':list(landmarks[kind][i]),'bodyPosition':list(pos),'bareCrown':crown,**fit})
 allRows['bare'][kind+'-north']=bareRows;allRows['helmet'][kind+'-north']=helmetRows
# Four separately authored source interiors retain their fixed physical-ruler calibration.
launch={v:[allRows[v]['tread-north'][0]] for v in allRows}
for i,(raw,box) in enumerate(components(sources[2],4)):
 scale=21/95;hx,hy,bottom=[(295,81,175),(834,147,231),(1368,176,254),(1884,168,246)][i];crown=[106,105,104,104][i];raw=grade(raw);pose=raw.resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS);pos=(round(128-(hx-box[0])*scale),round(crown-(hy-box[1])*scale));bare=Image.new('RGBA',SIZE);bare.alpha_composite(pose,pos);head=Image.open(OLD/f'north-pitch-head-{i+1:02}.png').convert('RGBA');helmet,fit=equip(bare,head,crown,'pitch');contain(bare);contain(helmet)
 for variant,im in [('bare',bare),('helmet',helmet)]:launch[variant].append(im)
 records.append({'state':'swim-start-north','slot':i+1,'source':sources[2].relative_to(R).as_posix(),'sourceBox':box,'anatomicalScale':scale,'bodyPosition':list(pos),'bareCrown':crown,**fit})
for variant in allRows:
 launch[variant].append(allRows[variant]['swim-north'][0]);allRows[variant]['swim-start-north']=launch[variant];allRows[variant]['swim-stop-north']=list(reversed(launch[variant]))
 states=[]
 for key,rows in allRows[variant].items():
  selected=cov['selected'][variant][key];src=json.loads((R/selected['manifest']).read_text());state=next(s for s in src['states'] if s['id']==key).copy();files=[]
  for i,im in enumerate(rows):
   path=f'frames/{variant}/{key}/{i:03}.png';(H/path).parent.mkdir(parents=True,exist_ok=True);im.save(H/path);files.append(path)
  state['frameFiles']=files;states.append(state)
 manifest={**src,'name':'Veld coherent north water '+variant,'frameWidth':256,'frameHeight':256,'pivot':PIVOT,'states':states,'status':'staged_coherent_body_pending_visual_acceptance'}
 (H/f'{variant}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
contact=Image.new('RGBA',(1536,1120),'#202a30');draw=ImageDraw.Draw(contact)
for row,(variant,key) in enumerate([('bare','tread-north'),('helmet','tread-north'),('bare','swim-north'),('helmet','swim-north')]):
 for i,im in enumerate(allRows[variant][key]):contact.alpha_composite(im,(i*256,row*280+24));draw.text((i*256+4,row*280+4),variant+' '+key+' / '+str(i),fill='white')
contact.save(H/'loops-master-v1.png')
contact=Image.new('RGBA',(1536,560),'#202a30');draw=ImageDraw.Draw(contact)
for row,variant in enumerate(['bare','helmet']):
 for i,im in enumerate(launch[variant]):contact.alpha_composite(im,(i*256,row*280+24));draw.text((i*256+4,row*280+4),variant+' launch / '+str(i),fill='white')
contact.save(H/'launch-master-v1.png')
(H/'fit-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'installed':False,'physicalRulers':{'targetBareHairWidth':21,'treadSourceHairWidth':93,'treadSourceHairRow':106,'swimSourceHairWidth':97,'swimSourceHairRow':161,'transitionSourceHairWidth':95},'curves':{k:{kk:vv.tolist() for kk,vv in v.items()} for k,v in curves.items()},'sources':[{'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sources],'records':records},indent=2)+'\n',encoding='utf-8')
print(f'{checks} source fitting/protected-body/clipping checks pass;8 staged states/48 frames.')
