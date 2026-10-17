"""Reproducible staged water clips; explicit cranial anchors, one scale per sheet."""
from pathlib import Path
import copy,json,hashlib,os
import numpy as np
from PIL import Image,ImageDraw
from extract_sources import extract
P=Path(__file__).resolve().parent;R=P.parents[1]
HEADS={
'east':[(141,92),(421,100),(691,100),(951,100),(1213,99),(1477,92),(220,473),(486,473),(749,474),(1008,474),(1267,474),(1498,475),(141,662),(420,696),(700,718),(975,747),(1260,752),(1518,774)],
'south':[(149,80),(410,95),(674,104),(940,105),(1200,105),(1454,80),(139,544),(410,545),(674,549),(942,544),(1200,546),(1469,543),(149,705),(410,704),(667,762),(941,804),(1199,840),(1473,840)],
'west':[(112,128),(356,132),(638,128),(900,128),(1165,133),(1450,126),(109,496),(377,490),(646,491),(872,487),(1120,490),(1410,496),(112,705),(334,726),(606,738),(865,768),(1125,760),(1410,768)],
'north':[(124,86),(383,87),(650,87),(916,85),(1161,87),(1407,87),(124,462),(386,466),(641,466),(870,471),(1155,478),(1406,465),(124,712),(386,715),(649,735),(920,748),(1170,729),(1410,729)]}
TREAD={'east':[138,110],'south':[128,110],'west':[118,110],'north':[128,110]}
SWIM={'east':[142,118],'south':[128,143],'west':[114,118],'north':[128,110]}
def gold(a,protect):
 r,g,b=a[:,:,:3].astype(float).transpose(2,0,1)
 return (a[:,:,3]>0)&(r-b>35)&(g-b>20)&~protect
def protection(size,head,d):
 yy,xx=np.indices((size[1],size[0]));rx=12 if d=='north' else 14;ry=13 if d=='north' else 16
 return ((xx-head[0])/rx)**2+((yy-head[1])/ry)**2<=1
def grade(im,protect,gain):
 a=np.array(im);rgb=a[:,:,:3].astype(float);gm=gold(a,protect);body=(a[:,:,3]>0)&~protect&~gm;lum=rgb.mean(2)
 mapped=np.interp(lum,[0,50,70,90,120,160,200,255],[0,50,68,80,99,126,149,170]);factor=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0)
 rgb[body]*=factor[body,None];rgb[gm]*=gain;a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');return Image.fromarray(a)
def build(d):
 p=P.parent/('james-water-'+d+'-v1');cells=extract(p/'source.png');heads=list(HEADS[d]);sources=['source.png']*18;scales=[json.loads((p/'anatomy-audition.json').read_text())['fixedScale']]*18
 if d=='north':
  # Separate source density, calibrated from the first rear cranial cap, not pose height.
  donor=extract(p/'source-start-interiors-v4.png',4,4);cells+=donor;heads +=[(318,150),(867,168),(1390,206),(1910,211)];sources+=['source-start-interiors-v4.png']*4;scales +=[22/106]*4
 rows=[];tracking=[];mroot=R/'character/crew-runtime-matte-v1/branforth';masterpack=json.loads((mroot/'manifest.json').read_text());ms=next(s for s in masterpack['states'] if s['id']=='idle-'+d);master=Image.open(mroot/ms['frameFiles'][0]).convert('RGBA');ma=np.array(master);yy,xx=np.where(ma[:,:,3]>180);mtop=int(yy.min());my,mx=np.where((ma[:,:,3]>180)&(np.indices(ma.shape[:2])[0]<mtop+5));mh=[float(mx.mean()),mtop+13];masterprotect=protection(master.size,mh,d)
 for i,(cell,box) in enumerate(cells):
  sc=scales[i];local=np.array(heads[i],float)-box[:2]
  if i<6 or i==12:target=np.array(TREAD[d],float)
  elif i<12 or i==17:target=np.array(SWIM[d],float)
  else:
   t=(i-12)/5 if i<18 else (i-17)/5;target=(1-t)*np.array(TREAD[d])+t*np.array(SWIM[d])
  at=np.rint(target-local*sc).astype(int);small=cell.resize((round(cell.width*sc),round(cell.height*sc)),Image.Resampling.LANCZOS);im=Image.new('RGBA',(256,276));im.alpha_composite(small,tuple(at));actual=local*sc+at
  tracking.append(dict(source=sources[i],sourceBox=box,fixedScale=sc,sourceHeadAnchor=list(heads[i]),headAnchor=actual.tolist(),translation=at.tolist(),registration='Cranial anchor interpolation; shoulder/collar continuity visually reviewed separately'))
  rows.append(im);dest=p/'registered-ungraded'/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True);im.save(dest)
 a=np.array(rows[0]);gain=np.median(ma[:,:,:3][gold(ma,masterprotect)],axis=0)/np.median(a[:,:,:3][gold(a,protection(rows[0].size,tracking[0]['headAnchor'],d))],axis=0)
 for i,im in enumerate(rows):rows[i]=grade(im,protection(im.size,tracking[i]['headAnchor'],d),gain)
 start=[0,13,14,15,16,6] if d!='north' else [0,18,19,20,21,6]
 poses={'tread':[0,1,2,3,4,0],'swim':[6,7,8,9,10,6],'swim-start':start,'swim-stop':start[::-1]}
 contracts=json.loads((p/'retained-contracts.json').read_text());old={c['state']['id']:c['state'] for c in contracts};oldroot=R/'character/chief-engineer-branforth-v2';catalog=json.loads((oldroot/'catalog.json').read_text())
 for rel in catalog['body']:
  for s in json.loads((oldroot/rel).read_text())['states']:
   if s['id']=='swim-stop-'+d:old[s['id']]=s
 pack=dict(name='James '+d+' water staged',frameWidth=256,frameHeight=276,pivot=[128,128],standingHeight=148,precomposed=True,textureFilter='linear',status='staged_water_registration_review',states=[]);hashes={}
 for action,ids in poses.items():
  state=copy.deepcopy(old[action+'-'+d]);files=[]
  for j,i in enumerate(ids):
   f=p/'frames'/action/f'{j:03d}.png';f.parent.mkdir(parents=True,exist_ok=True);rows[i].save(f);rel=f.relative_to(p).as_posix();files.append(rel);hashes[rel]=hashlib.sha256(f.read_bytes()).hexdigest()
  state.update(frameFiles=files,frameCount=6,provenance=dict(sourcePoses=ids,derivation='Independent facing source, fixed anatomical scale, common canvas/pivot, exact shared loop and transition endpoints; stop reverses start',northInteriorsReviewPending=d=='north'))
  pack['states'].append(state)
 (p/'bare-manifest.json').write_text(json.dumps(pack,indent=2)+'\n');(p/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n');(p/'registration.json').write_text(json.dumps(dict(goldGain=gain.tolist(),tracking=tracking,sourceHashes={s:hashlib.sha256((p/s).read_bytes()).hexdigest() for s in set(sources)},status='staged_not_runtime_verified'),indent=2)+'\n')
 board=Image.new('RGB',(1792,1280),'#303b40');draw=ImageDraw.Draw(board)
 for row,(action,ids) in enumerate(poses.items()):
  for j,i in enumerate(ids):
   at=(j*256,38+row*312);board.paste(rows[i],at,rows[i]);draw.text((at[0]+8,at[1]-27),action+' '+d+' '+str(j),fill='white')
 full=Image.new('RGBA',(256,276));full.alpha_composite(master,(36,66));board.paste(full,(1536,38),full);draw.text((1544,10),'standing master / anatomy ruler',fill='white');board.save(p/'registered-contact.png')
 # All actions share world registration; no review-time bottom alignment.
 return pack,p,rows,poses
if __name__=='__main__':
 combined=None;allrows=[]
 for d in ['east','south','west','north']:
  pack,p,rows,poses=build(d);allrows.append((d,rows,poses))
  if combined is None:combined={k:copy.deepcopy(v) for k,v in pack.items() if k!='states'};combined.update(name='James directional water staged',states=[])
  for st in pack['states']:
   st=copy.deepcopy(st);st['frameFiles']=[Path(os.path.relpath(p/f,P)).as_posix() for f in st['frameFiles']];combined['states'].append(st)
  print(d,'24 staged refs; fixed scales',sorted(set(t['fixedScale'] for t in json.loads((p/'registration.json').read_text())['tracking'])))
 (P/'bare-manifest.json').write_text(json.dumps(combined,indent=2)+'\n')
 seq=[('tread',i,160) for i in range(6)]+[('swim-start',i,t) for i,t in enumerate([70,90,100,100,90,70])]+[('swim',i,160) for _ in range(2) for i in range(6)]+[('swim-stop',i,t) for i,t in enumerate([70,90,100,100,90,70])]
 gif=[];dur=[]
 for action,j,t in seq:
  im=Image.new('RGB',(1024,328),'#303b40');dr=ImageDraw.Draw(im)
  for k,(d,rows,poses) in enumerate(allrows):
   sprite=rows[poses[action][j]];im.paste(sprite,(k*256,40),sprite);dr.text((k*256+8,8),d+' / '+action+' / '+str(j),fill='white')
  gif.append(im);dur.append(t)
 gif[0].save(P/'bare-review.gif',save_all=True,append_images=gif[1:],duration=dur,loop=0,disposal=2,optimize=False)
