"""Independent north prone distress; source-density rulers and native rear helmet."""
from pathlib import Path
import copy,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1];KEY='swim-distress-north'
REF=R/'character/veld-water-north-coherent-v1/frames/bare/swim-north/000.png'
HELM=R/'character/veld-water-master-audit-v1/fitted-swim-north-head.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bbox(mask):
 y,x=np.where(mask);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
def head_mask(a,roi=None):
 v=a[:,:,:3].astype(float)
 warm=(a[:,:,3]>200)&(v[:,:,0]>35)&(v[:,:,0]>v[:,:,1]*1.15)&(v[:,:,1]>v[:,:,2]*1.12)
 if roi:
  support=np.zeros(warm.shape,bool);support[roi[1]:roi[3],roi[0]:roi[2]]=True;warm&=support
 # Dark hair strand gaps split color components; group nearby warm support
 # before choosing the head, then return only the original warm pixels.
 lab,n=label(binary_dilation(warm,iterations=3));sizes=np.bincount(lab.ravel());assert n,'Rear brown head landmark missing'
 return warm&(lab==(1+np.argmax(sizes[1:])))
def landmark(a,roi=None):
 head=head_mask(a,roi);b=bbox(head);height=b[3]-b[1]
 # Use a named widest scalp row above ears/bun, not full pose or head height.
 rows=[]
 for y in range(b[1]+round(height*.15),b[1]+round(height*.55)+1):
  x=np.where(head[y])[0]
  if len(x)>1:rows.append((int(x[-1]-x[0]+1),y,int(x[0]),int(x[-1]+1)))
 width,y,left,right=max(rows)
 return {'headBox':b,'scalpWidth':width,'scalpRow':y,'centerX':(left+right)/2,'crownY':b[1]}
def materials(a,roi=None):
 v=a[:,:,:3].astype(float);h=head_mask(a,roi);b=bbox(h);Y,X=np.indices(a.shape[:2])
 headregion=(Y>=b[1]-2)&(Y<=b[3]+2)&(X>=b[0]-3)&(X<=b[2]+3)
 opaque=a[:,:,3]>200
 skin=h&(v[:,:,0]>115)&(v[:,:,0]>v[:,:,1]*1.25)
 return {'hair':h&~skin,'skin':skin,'cloth':~headregion&opaque&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),
   'patch':~headregion&opaque&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35)}
def extract(file,rows=3):
 a=np.array(Image.open(file).convert('RGBA'));lab,n=label(a[:,:,3]>160);sizes=np.bincount(lab.ravel())
 ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:6];assert len(ids)==6 and min(sizes[k] for k in ids)>5000
 ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(a.shape[0]/rows)),np.where(lab==k)[1].mean()));result=[]
 for i,k in enumerate(ids):
  b=bbox(lab==k);b=[b[0]-2,b[1]-2,b[2]+2,b[3]+2]
  assert b[0]>=0 and b[1]>=0 and b[2]<=a.shape[1] and b[3]<=a.shape[0]
  cut=a.copy();cut[~binary_dilation(lab==k,iterations=2)]=0
  raw=np.array(Image.fromarray(cut).crop(b))
  roi=[72,52,175,134] if file.name=='distress-arm-edit-v2.png' and i==5 else None
  result.append((raw,{'slot':i,'source':file.relative_to(P).as_posix(),'sourceSha256':sha(file),'sourceGridRows':rows,'sourceGridColumns':6//rows,'crop':b,'headROI':roi,**landmark(raw,roi)}))
 return result
def main():
 original=extract(P/'sources/distress-v1.png');edited=extract(P/'sources/distress-arm-edit-v2.png',2)
 # Provider edit changed atlas layout to3columns/2rows. Only its corrected
 # bottom-right cell is selected; five original cells remain authoritative.
 poses=original.copy();poses[3]=edited[5]
 poses[3][1]['sourceCellSlot']=5;poses[3][1]['slot']=3
 # Separate source ruler for the generated edit, keeping the primary atlas frozen.
 scales={'sources/distress-v1.png':21/float(np.median([r['scalpWidth'] for _,r in original])),
         'sources/distress-arm-edit-v2.png':21/float(edited[5][1]['scalpWidth'])}
 ref=np.array(Image.open(REF).convert('RGBA'));rv=ref[:,:,:3].astype(float);rm=materials(ref,[115,101,142,126]);q=[0,15,35,55,75,90,100];curves={}
 for key,mask in rm.items():
  pooled=np.concatenate([a[:,:,:3][materials(a,r.get('headROI'))[key]] for a,r in poses]).astype(float)
  if np.count_nonzero(mask)<2 or len(pooled)<4:continue
  curves[key]={'knots':np.percentile(pooled.mean(1),q),'targets':np.percentile(rv[mask],q,axis=0)}
 assert all(k in curves for k in ['hair','cloth','patch'])
 head=Image.open(HELM).convert('RGBA');headpos=(112,99);clear=(114,103,142,126)
 images={'bare':[],'helmet':[]};records=[];checks=0
 for raw,record in poses:
  a=raw.copy();v=raw[:,:,:3].astype(float);masks=materials(raw,record.get('headROI'))
  for key,curve in curves.items():
   mask=masks[key]
   for c in range(3):a[mask,c]=np.interp(v[mask].mean(1),curve['knots'],curve['targets'][:,c]).clip(0,255).astype('uint8')
  support=np.logical_or.reduce([masks[k] for k in curves]);assert np.array_equal(a[~support],raw[~support]) and np.array_equal(a[:,:,3],raw[:,:,3]);checks+=1
  scale=scales[record['source']];im=Image.fromarray(a);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
  pos=(round(128-record['centerX']*scale),round(104-record['crownY']*scale))
  bare=Image.new('RGBA',(256,256));bare.alpha_composite(im,pos)
  helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(head,headpos)
  before=np.array(bare);after=np.array(helmet);Y,X=np.indices((256,256));rgb=before[:,:,:3].astype(float)
  # Forward support glove may cross the crown; restore original gray glove only.
  fg=(before[:,:,3]>200)&(np.ptp(rgb,axis=2)<28)&(Y>=99)&(Y<109)&(X>=112)&(X<145)
  after[fg]=before[fg];helmet=Image.fromarray(after)
  protected=np.ones((256,256),bool);protected[clear[1]:clear[3],clear[0]:clear[2]]=False
  protected[headpos[1]:headpos[1]+head.height,headpos[0]:headpos[0]+head.width]=False
  assert np.array_equal(before[protected],after[protected]);checks+=1
  record.update(anatomicalScale=scale,bodyPosition=list(pos),targetHeadCenterX=128,targetCrownY=104,headPosition=list(headpos),clear=list(clear),foregroundPixels=int(fg.sum()))
  records.append(record)
  crop=P/f'sources/selected-crops/{record["slot"]:03}.png';crop.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(raw).save(crop)
  for gear,image in [('bare',bare),('helmet',helmet)]:
   ar=np.array(image);assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1
   file=P/f'frames/{gear}/{KEY}/{record["slot"]:03}.png';file.parent.mkdir(parents=True,exist_ok=True);image.save(file);images[gear].append(image)
 for gear in images:
  old=json.loads((R/f'character/dr-veld-v2/packs/{gear}-256x256-p128.0-128.0/manifest.json').read_text());state=copy.deepcopy(next(s for s in old['states'] if s['id']==KEY))
  state['frameFiles']=[f'frames/{gear}/{KEY}/{i:03}.png' for i in range(6)]
  manifest={**old,'name':'Veld independently authored north prone distress '+gear,'states':[state],'status':'staged_candidate_pending_family_clearance_lifecycle_motion_review'}
  (P/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
  preview=[]
  for im in images[gear]:
   bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(im);preview.append(bg.convert('RGB'))
  preview[0].save(P/f'{gear}-distress.gif',save_all=True,append_images=preview[1:],duration=[160]*6,loop=0,disposal=2)
 for name,size,pitch in [('paired-contact.png',256,280),('station-scale-contact.png',142,165)]:
  board=Image.new('RGBA',(7*size,2*pitch),'#202a30');d=ImageDraw.Draw(board)
  for row,gear in enumerate(images):
   refim=Image.open(R/f'character/veld-water-north-coherent-v1/frames/{gear}/swim-north/000.png').convert('RGBA')
   for i,im in enumerate([refim]+images[gear]):
    board.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),(i*size,row*pitch+20));d.text((i*size+3,row*pitch+2),gear+(' master' if i==0 else ' '+str(i-1)),fill='white')
  board.save(P/name)
 detail=Image.new('RGBA',(6*240,480),'#202a30')
 for row,gear in enumerate(images):
  for i,im in enumerate(images[gear]):detail.alpha_composite(im.crop((88,80,168,160)).resize((240,240),Image.Resampling.NEAREST),(i*240,row*240))
 detail.save(P/'head-arm-detail.png')
 e={'checks':checks,'failures':0,'selected':False,'sourceSha256':sha(P/'sources/distress-v1.png'),'references':{f.relative_to(R).as_posix():sha(f) for f in [REF,HELM]},
    'physicalRulers':scales,'records':records,'curves':{k:{kk:vv.tolist() for kk,vv in c.items()} for k,c in curves.items()},
    'frameHashes':{f.relative_to(P).as_posix():sha(f) for f in sorted((P/'frames').rglob('*.png'))},
    'scope':'five original cells plus edited slot3 only; frozen anatomical source rulers,pooled grade,alpha/material ownership,native rear helmet; not lifecycle/world/motion acceptance'}
 (P/'build-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
 (P/'index.html').write_text('<meta charset="utf-8"><title>Veld north swimming distress candidate</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:24px}img{max-width:100%}</style><h1>Veld north prone swimming distress — candidate</h1><p>Rear/overhead swim master, original equipment sides, one primary anatomical ruler plus independently calibrated edited cell3. Same working arm remains at front throat collar, naturally hidden from rear. Staged; real furnished clearance,lifecycle/restore and full motion/handoffs remain.</p><h2>Station scale beside selected swim</h2><img src="station-scale-contact.png"><h2>Motion</h2><img src="bare-distress.gif"><img src="helmet-distress.gif"><p><a href="paired-contact.png">Full contact</a> · <a href="head-arm-detail.png">Head and arms</a></p>')
 print(f'{checks} north source/material/body/border checks PASS;12candidate frames; frozen rulers {scales}')
if __name__=='__main__':main()
