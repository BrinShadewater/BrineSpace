"""Fit one independently authored prone death row at a fixed anatomical ruler."""
from pathlib import Path
import copy,hashlib,importlib.util,json,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1];KEY='death-water-west'
REF=R/'character/veld-water-west-coherent-v1/frames/bare/swim-west/000.png'
HELM=R/'character/veld-shared-helmet-v1/fitted-west.png'
SOURCE=P/'sources/death-v1.png'
spec=importlib.util.spec_from_file_location('west_materials',R/'character/veld-swim-distress-west-coherent-v1/build.py')
grade=importlib.util.module_from_spec(spec);spec.loader.exec_module(grade)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def scanner_anchor(a):
 v=a[:,:,:3].astype(float);fb=grade.box(grade.face(a));fh=fb[3]-fb[1];Y,X=np.indices(a.shape[:2])
 mask=(a[:,:,3]>180)&(v[:,:,2]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,0]*1.3)&(abs(v[:,:,2]-v[:,:,1])<45)&(v[:,:,1]>65)&(Y>fb[3]+fh*.3)&(X>fb[2]+fh*.65)
 lab,n=label(mask);sizes=np.bincount(lab.ravel());parts=[]
 for k in range(1,n+1):
  y,x=np.where(lab==k)
  if sizes[k]>=2:parts.append((int(sizes[k]),float(x.mean()),float(y.mean())))
 parts=sorted(parts,reverse=True)[:2]
 assert parts,'Expected nearhip scanner display landmarks'
 return np.average(np.array([t[1:] for t in parts]),axis=0,weights=[t[0] for t in parts]),parts
def main():
 raw=np.array(Image.open(SOURCE).convert('RGBA'));lab,n=label(raw[:,:,3]>160);sizes=np.bincount(lab.ravel())
 ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:6]
 assert len(ids)==6 and all(sizes[k]>30000 for k in ids)
 ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(raw.shape[0]/2)),np.where(lab==k)[1].mean()))
 crops=[];records=[]
 for i,k in enumerate(ids):
  b=grade.box(lab==k);b=[b[0]-2,b[1]-2,b[2]+2,b[3]+2];assert min(b)>=0 and b[2]<=raw.shape[1] and b[3]<=raw.shape[0]
  cut=raw.copy();cut[~binary_dilation(lab==k,iterations=2)]=0
  a=np.array(Image.fromarray(cut).crop(b));anchor,parts=scanner_anchor(a)
  crops.append(a);records.append({'sourcePose':i,'crop':b,'face':grade.box(grade.face(a)),'scannerAnchor':anchor.tolist(),'scannerParts':parts})
  f=P/f'sources/crops/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(a).save(f)
 ref=np.array(Image.open(REF).convert('RGBA'));rm=grade.materials(ref);target,_=scanner_anchor(ref)
 face_height=grade.box(grade.face(ref))[3]-grade.box(grade.face(ref))[1]
 scale=face_height/float(np.median([r['face'][3]-r['face'][1] for r in records]))
 assert .28<scale<.35,'Fixed source ruler'
 curves={};q=[0,15,35,55,75,90,100]
 for key,mask in rm.items():
  pool=np.concatenate([a[:,:,:3][grade.materials(a)[key]] for a in crops]).astype(float)
  assert len(pool)>30 and np.count_nonzero(mask)>5
  curves[key]={'knots':np.percentile(pool.mean(1),q),'targets':np.percentile(ref[:,:,:3][mask],q,axis=0)}
 images={g:[Image.open(R/f'character/veld-water-west-coherent-v1/frames/{g}/swim-west/000.png').convert('RGBA')] for g in ['bare','helmet']}
 checks=0;fits=[];angles=[0,0,3,6,9,11]
 native=Image.open(HELM).convert('RGBA')
 for a,record in zip(crops[1:],records[1:]):
  v=a[:,:,:3].astype(float);graded=a.copy()
  for key,mask in grade.materials(a).items():
   for c in range(3):graded[mask,c]=np.interp(v[mask].mean(1),curves[key]['knots'],curves[key]['targets'][:,c]).clip(0,255).astype('uint8')
  im=Image.fromarray(graded).resize((round(a.shape[1]*scale),round(a.shape[0]*scale)),Image.Resampling.LANCZOS)
  pos=tuple(np.rint(target-np.array(record['scannerAnchor'])*scale).astype(int))
  bare=Image.new('RGBA',(256,256));bare.alpha_composite(im,pos)
  facebox=grade.box(grade.face(np.array(bare)));end=[facebox[0],facebox[3]]
  angle=16+angles[record['sourcePose']]
  head=native.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
  ha=np.array(head);hf=grade.box(grade.face(ha));hp=(end[0]-hf[0],end[1]-hf[3])
  # Retain the source's closing eyes/face within the selected helmet's skin window.
  # Hardware and glass/rim pixels outside that window stay native and unchanged.
  source_face=bare.crop(facebox).resize((hf[2]-hf[0],hf[3]-hf[1]),Image.Resampling.LANCZOS)
  fa=np.array(source_face);skin=grade.face(ha)[hf[1]:hf[3],hf[0]:hf[2]]
  region=ha[hf[1]:hf[3],hf[0]:hf[2]];region[skin,:3]=fa[skin,:3]
  head=Image.fromarray(ha)
  clear=(end[0]-2,end[1]-38,end[0]+37,end[1]+1)
  helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(head,hp)
  protected=np.ones((256,256),bool);protected[clear[1]:clear[3],clear[0]:clear[2]]=False;protected[hp[1]:hp[1]+head.height,hp[0]:hp[0]+head.width]=False
  assert np.array_equal(np.array(bare)[protected],np.array(helmet)[protected]);checks+=1
  for g,image in [('bare',bare),('helmet',helmet)]:
   ar=np.array(image);assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1
   images[g].append(image)
  fits.append({**record,'slot':record['sourcePose'],'scale':scale,'position':[int(z) for z in pos],'headAngle':angle,'headPosition':hp,'clear':clear,'faceWindow':hf})
 durations=[180,180,220,220,260,500]
 for g,row in images.items():
  paths=[]
  for i,im in enumerate(row):
   f=P/f'frames/{g}/{KEY}/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);paths.append(f.relative_to(P).as_posix())
  parent=R/f'character/dr-veld-v2/packs/{g}-256x256-p128.0-128.0/manifest.json';m=json.loads(parent.read_text(encoding='utf-8'))
  old=next(s for s in m['states'] if s['id']==KEY)
  state=copy.deepcopy(old);state.update(frameFiles=paths,frameDurationsMs=durations,waterPoses=[True]*6,waterKinds=['swim']*6,facings=['west']*6)
  out={**m,'name':'Veld authored west prone water death '+g,'states':[state],'status':'staged_prone_candidate_tread_entry_world_restore_normal_selection_pending'}
  (P/f'{g}-manifest.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
  bg=[]
  for im in row:
   canvas=Image.new('RGBA',(256,256),'#202a30');canvas.alpha_composite(im);bg.append(canvas.convert('RGB'))
  bg[0].save(P/f'{g}-death.gif',save_all=True,append_images=bg[1:],duration=durations,loop=0,disposal=2)
 board=Image.new('RGBA',(7*256,2*256),'#202a30');d=ImageDraw.Draw(board)
 for ri,g in enumerate(images):
  for col,im in enumerate([images[g][0]]+images[g]):
   board.alpha_composite(im,(col*256,ri*256));d.text((col*256+4,ri*256+4),g+(' selected swim' if col==0 else ' death '+str(col-1)),fill='white')
 board.save(P/'paired-contact.png')
 small=board.resize((994,284),Image.Resampling.LANCZOS);small.save(P/'station-scale-contact.png')
 evidence={'fitChecks':checks,'fixedScale':scale,'targetScannerAnchor':target.tolist(),'sourceSha256':sha(SOURCE),'sourceProvider':'exec-7f453d26-1730-4b92-8223-5d28e95c1444','sourcePoses':records,'selectedPoses':[1,2,3,4,5],'exactMasterEntry':True,'fits':fits,'materialCurves':{k:{'knots':v['knots'].tolist(),'targets':v['targets'].tolist()} for k,v in curves.items()},'scope':'independent prone body row, fixed belt anchor/ruler, source face fitted into native skin window; candidate only'}
 (P/'build-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
 (P/'index.html').write_text('<meta charset="utf-8"><title>Veld west prone water death candidate</title><style>body{background:#202a30;color:#eee;font:16px sans-serif;margin:24px}img{max-width:100%}</style><h1>Veld west prone water death — candidate</h1><p>Exact selected swim entry, five independently authored relaxed poses, fixed scanner/hip anchor and anatomical ruler, pooled master material grade. Native helmet hardware with authored closing face. Original1560ms finite timing/terminal hold retained. Prone-source candidate only; upright tread entry, actual room clearance/restore and normal selection remain separate.</p><img src="station-scale-contact.png"><p><img src="bare-death.gif"><img src="helmet-death.gif"></p><a href="paired-contact.png">Full-size master comparison</a>',encoding='utf-8')
 if (P/'make_review.py').exists():subprocess.run([sys.executable,str(P/'make_review.py')],check=True,capture_output=True,text=True)
 print(f'{checks} fit/body-protection/clipping checks PASS; fixed scale{scale:.8f};2states/12refs,finite1560ms')
if __name__=='__main__':main()
