"""Fit one independently authored prone death row at a fixed anatomical ruler."""
from pathlib import Path
import copy,hashlib,importlib.util,json,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1];KEY='death-water-tread-east'
REF=R/'character/veld-water-east-coherent-v1/frames/bare/tread-east/000.png'
HELM=R/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png'
SOURCE=P/'sources/death-v1.png'
spec=importlib.util.spec_from_file_location('east_materials',R/'character/veld-swim-distress-east-coherent-v1/build.py')
grade=importlib.util.module_from_spec(spec);spec.loader.exec_module(grade)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
VIAL_ROIS=[(194,265,241,283),(686,273,734,295),(1225,259,1275,300),(252,720,295,769),(763,726,798,775),(1277,763,1307,813)]
def vial_anchor(a,roi):
 v=a[:,:,:3].astype(float);Y,X=np.indices(a.shape[:2])
 mask=(a[:,:,3]>200)&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.15)&(v[:,:,2]>70)&(X>=roi[0])&(X<roi[2])&(Y>=roi[1])&(Y<roi[3])
 lab,n=label(mask);sizes=np.bincount(lab.ravel());assert n,'Vial cap region missing'
 parts=[]
 for k in range(1,n+1):
  y,x=np.where(lab==k)
  if sizes[k]>=2:parts.append((int(sizes[k]),float(x.mean()),float(y.mean())))
 parts=sorted(parts,reverse=True)[:3];assert parts
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
  a=np.array(Image.fromarray(cut).crop(b));gr=VIAL_ROIS[i];vr=[gr[0]-b[0],gr[1]-b[1],gr[2]-b[0],gr[3]-b[1]];anchor,parts=vial_anchor(a,vr)
  crops.append(a);records.append({'sourcePose':i,'vialROI':vr,'crop':b,'face':grade.box(grade.face(a)),'vialAnchor':anchor.tolist(),'vialParts':parts})
  f=P/f'sources/crops/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(a).save(f)
 ref=np.array(Image.open(REF).convert('RGBA'));rm=grade.materials(ref);start_anchor,_=vial_anchor(ref,[103,163,118,171]);finish_anchor=np.array([106.0,141.0])
 face_height=grade.box(grade.face(ref))[3]-grade.box(grade.face(ref))[1]
 scale=face_height/float(np.median([r['face'][3]-r['face'][1] for r in records]))
 assert .28<scale<.35,'Fixed source ruler'
 curves={};q=[0,15,35,55,75,90,100]
 for key,mask in rm.items():
  pool=np.concatenate([a[:,:,:3][grade.materials(a)[key]] for a in crops]).astype(float)
  assert len(pool)>30 and np.count_nonzero(mask)>5
  curves[key]={'knots':np.percentile(pool.mean(1),q),'targets':np.percentile(ref[:,:,:3][mask],q,axis=0)}
 images={g:[Image.open(R/f'character/veld-water-east-coherent-v1/frames/{g}/tread-east/000.png').convert('RGBA')] for g in ['bare','helmet']}
 checks=0;fits=[];angles=[0,-4,-10,-18,-24,-27]
 native=Image.open(HELM).convert('RGBA').crop((82,17,116,55))
 for a,record in zip(crops[1:5],records[1:5]):
  v=a[:,:,:3].astype(float);graded=a.copy()
  for key,mask in grade.materials(a).items():
   for c in range(3):graded[mask,c]=np.interp(v[mask].mean(1),curves[key]['knots'],curves[key]['targets'][:,c]).clip(0,255).astype('uint8')
  im=Image.fromarray(graded).resize((round(a.shape[1]*scale),round(a.shape[0]*scale)),Image.Resampling.LANCZOS)
  target=start_anchor+(finish_anchor-start_anchor)*record['sourcePose']/5
  pos=tuple(np.rint(target-np.array(record['vialAnchor'])*scale).astype(int))
  bare=Image.new('RGBA',(256,256));bare.alpha_composite(im,pos)
  ar=np.array(bare);patch=grade.materials(ar)['patch'];ar[patch,:3]=np.clip(ar[patch,:3].astype(int)+np.array([0,3,10]),0,255).astype('uint8');bare=Image.fromarray(ar)
  facebox=grade.box(grade.face(np.array(bare)));end=facebox[2:4]
  angle=angles[record['sourcePose']]
  head=native.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
  ha=np.array(head);hf=grade.box(grade.face(ha));hp=(end[0]-hf[2],end[1]-hf[3])
  # Retain the source's closing eyes/face within the selected helmet's skin window.
  # Hardware and glass/rim pixels outside that window stay native and unchanged.
  source_face=bare.crop(facebox).resize((hf[2]-hf[0],hf[3]-hf[1]),Image.Resampling.LANCZOS)
  fa=np.array(source_face);skin=grade.face(ha)[hf[1]:hf[3],hf[0]:hf[2]]
  region=ha[hf[1]:hf[3],hf[0]:hf[2]];region[skin,:3]=fa[skin,:3]
  head=Image.fromarray(ha)
  clear=(end[0]-37,end[1]-38,end[0]+2,end[1]+1)
  helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(head,hp)
  protected=np.ones((256,256),bool);protected[clear[1]:clear[3],clear[0]:clear[2]]=False;protected[hp[1]:hp[1]+head.height,hp[0]:hp[0]+head.width]=False
  assert np.array_equal(np.array(bare)[protected],np.array(helmet)[protected]);checks+=1
  for g,image in [('bare',bare),('helmet',helmet)]:
   ar=np.array(image);assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1
   images[g].append(image)
  fits.append({**record,'slot':record['sourcePose'],'scale':scale,'position':[int(z) for z in pos],'headAngle':angle,'headPosition':hp,'clear':clear,'faceWindow':hf,'targetVialAnchor':target.tolist()})
 for g in images:images[g].append(Image.open(R/f'character/veld-death-water-east-coherent-v1/frames/{g}/death-water-east/005.png').convert('RGBA'))
 durations=[180,180,220,220,260,500]
 for g,row in images.items():
  paths=[]
  for i,im in enumerate(row):
   f=P/f'frames/{g}/{KEY}/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);paths.append(f.relative_to(P).as_posix())
  parent=R/f'character/dr-veld-v2/packs/{g}-256x256-p128.0-128.0/manifest.json';m=json.loads(parent.read_text(encoding='utf-8'))
  old=next(s for s in json.loads((R/f'character/dr-veld-v2/packs/{g}-184x184-p122.0-88.0/manifest.json').read_text(encoding='utf-8'))['states'] if s['id']=='death-water-east')
  state=copy.deepcopy(old);state.update(id=KEY,frameFiles=paths,frameDurationsMs=durations,waterPoses=[True]*6,waterKinds=['tread','transition','transition','transition','transition','swim'],facings=['east']*6)
  out={**m,'name':'Veld authored east prone water death '+g,'states':[state],'status':'staged_tread_entrance_candidate_controller_world_restore_normal_selection_pending'}
  (P/f'{g}-manifest.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
  bg=[]
  for im in row:
   canvas=Image.new('RGBA',(256,256),'#202a30');canvas.alpha_composite(im);bg.append(canvas.convert('RGB'))
  bg[0].save(P/f'{g}-death.gif',save_all=True,append_images=bg[1:],duration=durations,loop=0,disposal=2)
 board=Image.new('RGBA',(7*256,2*256),'#202a30');d=ImageDraw.Draw(board)
 for ri,g in enumerate(images):
  for col,im in enumerate([images[g][0]]+images[g]):
   board.alpha_composite(im,(col*256,ri*256));d.text((col*256+4,ri*256+4),g+(' selected tread' if col==0 else ' death '+str(col-1)),fill='white')
 board.save(P/'paired-contact.png')
 small=board.resize((994,284),Image.Resampling.LANCZOS);small.save(P/'station-scale-contact.png')
 evidence={'fitChecks':checks,'fixedScale':scale,'interiorPatchResidualRGB':[0,3,10],'startVialAnchor':start_anchor.tolist(),'finishVialAnchor':finish_anchor.tolist(),'sourceSha256':sha(SOURCE),'sourceProvider':'exec-6a755b62-4eb5-4799-ab44-631f9a039c8c','sourcePoses':records,'selectedPoses':[1,2,3,4],'exactProneTerminal':True,'exactMasterEntry':True,'fits':fits,'materialCurves':{k:{'knots':v['knots'].tolist(),'targets':v['targets'].tolist()} for k,v in curves.items()},'scope':'independent tread-to-prone source; exact tread0/prone terminal, four authored interiors; controller selection and arbitrary live entry still pending'}
 (P/'build-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
 (P/'index.html').write_text('<meta charset="utf-8"><title>Veld east prone water death candidate</title><style>body{background:#202a30;color:#eee;font:16px sans-serif;margin:24px}img{max-width:100%}</style><h1>Veld east prone water death — candidate</h1><p>Exact selected swim entry, five independently authored relaxed poses, fixed vial/hip anchor and anatomical ruler, pooled master material grade. Native helmet hardware with authored closing face. Original1560ms finite timing/terminal hold retained. Prone-source candidate only; upright tread entry, actual room clearance/restore and normal selection remain separate.</p><img src="station-scale-contact.png"><p><img src="bare-death.gif"><img src="helmet-death.gif"></p><a href="paired-contact.png">Full-size master comparison</a>',encoding='utf-8')
 if (P/'make_review.py').exists():subprocess.run([sys.executable,str(P/'make_review.py')],check=True,capture_output=True,text=True)
 print(f'{checks} fit/body-protection/clipping checks PASS; fixed scale{scale:.8f};2states/12refs,finite1560ms')
if __name__=='__main__':main()
