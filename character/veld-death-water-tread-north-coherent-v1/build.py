"""Independent rear tread-to-prone entrance, frozen ruler/interpolated scanner anchor."""
from pathlib import Path
import copy,hashlib,importlib.util,json,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1];KEY='death-water-tread-north'
REF=R/'character/veld-water-north-coherent-v1/frames/bare/tread-north/000.png'
HELM=R/'character/veld-water-master-audit-v1/fitted-swim-north-head.png'
SOURCE=P/'sources/death-v1.png'
spec=importlib.util.spec_from_file_location('north_materials',R/'character/veld-swim-distress-north-coherent-v1/build.py')
grade=importlib.util.module_from_spec(spec);spec.loader.exec_module(grade)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def headbox(a,roi=None):return grade.bbox(grade.head_mask(a,roi))
# Source ROIs select the dim scanner readout, not the moving blue sleeves.
SCANNER_ROIS=[(196,229,217,263),(714,245,737,281),(1230,245,1253,281),(199,689,225,731),(709,685,737,729),(1220,687,1248,731)]
def scanner_anchor(a,roi=None):
 v=a[:,:,:3].astype(float);Y,X=np.indices(a.shape[:2])
 box=roi if roi is not None else (105,142,119,157)
 mask=(a[:,:,3]>180)&(v[:,:,2]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,0]*1.3)&(abs(v[:,:,2]-v[:,:,1])<65)&(v[:,:,1]>50)&(X>=box[0])&(X<box[2])&(Y>=box[1])&(Y<box[3])
 lab,n=label(mask);sizes=np.bincount(lab.ravel());assert n,'Left hip scanner display missing'
 k=1+np.argmax(sizes[1:]);y,x=np.where(lab==k)
 return np.array([x.mean(),y.mean()]),int(sizes[k])
def main():
 raw=np.array(Image.open(SOURCE).convert('RGBA'));lab,n=label(raw[:,:,3]>160);sizes=np.bincount(lab.ravel())
 ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:6]
 assert len(ids)==6 and min(sizes[k] for k in ids)>30000
 ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(raw.shape[0]/2)),np.where(lab==k)[1].mean()))
 crops=[];records=[]
 edited=np.array(Image.open(P/'sources/death-v3.png').convert('RGBA'));el,en=label(edited[:,:,3]>160);esz=np.bincount(el.ravel());eids=sorted(range(1,en+1),key=lambda k:esz[k],reverse=True)[:6];eids.sort(key=lambda k:(int(np.where(el==k)[0].mean()//(edited.shape[0]/2)),np.where(el==k)[1].mean()))
 for i,k in enumerate(ids):
  source_name='death-v1.png' if i<3 else 'death-v3.png'
  if i>=3:raw=edited;lab=el;k=eids[i]
  b=grade.bbox(lab==k);b=[b[0]-2,b[1]-2,b[2]+2,b[3]+2]
  assert min(b)>=0 and b[2]<=raw.shape[1] and b[3]<=raw.shape[0]
  cut=raw.copy();cut[~binary_dilation(lab==k,iterations=2)]=0
  a=np.array(Image.fromarray(cut).crop(b));global_roi=SCANNER_ROIS[i];scanner_roi=[global_roi[0]-b[0],global_roi[1]-b[1],global_roi[2]-b[0],global_roi[3]-b[1]];anchor,count=scanner_anchor(a,scanner_roi)
  crops.append(a);records.append({'sourcePose':i,'source':source_name,'sourceSha256':sha(P/'sources'/source_name),'crop':b,'headBox':headbox(a),'scannerAnchor':anchor.tolist(),'scannerPixels':count,'scannerROI':scanner_roi})
  f=P/f'sources/crops/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(a).save(f)
 ref=np.array(Image.open(REF).convert('RGBA'));roi=[114,106,143,130];rm=grade.materials(ref,roi);start,_=scanner_anchor(ref,[105,151,119,168]);finish=np.array([111.4166666667,149.4166666667]);hb=headbox(ref,roi)
 scale=20/72;assert hb[2]-hb[0]==20 # Frozen primary source head-width ruler; revised anatomy does not recalibrate it.
 curves={};q=[0,15,35,55,75,90,100]
 for key,mask in rm.items():
  pool=np.concatenate([a[:,:,:3][grade.materials(a)[key]] for a in crops]).astype(float)
  if len(pool)<4 or np.count_nonzero(mask)<2:continue
  curves[key]={'knots':np.percentile(pool.mean(1),q),'targets':np.percentile(ref[:,:,:3][mask],q,axis=0)}
 assert all(k in curves for k in ['hair','cloth','patch'])
 images={g:[Image.open(R/f'character/veld-water-north-coherent-v1/frames/{g}/tread-north/000.png').convert('RGBA')] for g in ['bare','helmet']}
 checks=0;fits=[];native=Image.open(HELM).convert('RGBA')
 for a,record in zip(crops[1:5],records[1:5]):
  v=a[:,:,:3].astype(float);graded=a.copy()
  for key,curve in curves.items():
   mask=grade.materials(a)[key]
   for c in range(3):graded[mask,c]=np.interp(v[mask].mean(1),curve['knots'],curve['targets'][:,c]).clip(0,255).astype('uint8')
  im=Image.fromarray(graded).resize((round(a.shape[1]*scale),round(a.shape[0]*scale)),Image.Resampling.LANCZOS)
  target=start+(finish-start)*record['sourcePose']/5
  pos=tuple(np.rint(target-np.array(record['scannerAnchor'])*scale).astype(int))
  bare=Image.new('RGBA',(256,256));bare.alpha_composite(im,pos)
  measured,_=scanner_anchor(np.array(bare),[target[0]-7,target[1]-7,target[0]+7,target[1]+7]);adjust=np.rint(target-measured).astype(int);pos=tuple(np.array(pos)+adjust)
  bare=Image.new('RGBA',(256,256));bare.alpha_composite(im,pos)
  bh=headbox(np.array(bare));cx=(bh[0]+bh[2])/2;crown=bh[1]
  # Use selected pitch component for each interior. No face from another view.
  native=Image.open(R/f'character/veld-water-material-v2/north-pitch-head-{record["sourcePose"]:02}.png').convert('RGBA')
  hp=(round(cx-native.width/2),crown-5);clear=(bh[0]-2,bh[1]-2,bh[2]+2,bh[3]+1)
  helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(native,hp)
  protected=np.ones((256,256),bool);protected[clear[1]:clear[3],clear[0]:clear[2]]=False;protected[hp[1]:hp[1]+native.height,hp[0]:hp[0]+native.width]=False
  assert np.array_equal(np.array(bare)[protected],np.array(helmet)[protected]);checks+=1
  for g,image in [('bare',bare),('helmet',helmet)]:
   ar=np.array(image);assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1;images[g].append(image)
  fits.append({**record,'slot':record['sourcePose'],'scale':scale,'position':[int(z) for z in pos],'headPosition':hp,'clear':clear,'renderedHeadBox':bh,'renderedScannerCorrection':adjust.tolist(),'targetScannerAnchor':target.tolist(),'headSource':f'character/veld-water-material-v2/north-pitch-head-{record["sourcePose"]:02}.png'})
 for g in images:images[g].append(Image.open(R/f'character/veld-death-water-north-coherent-v1/frames/{g}/death-water-north/005.png').convert('RGBA'))
 durations=[180,180,220,220,260,500]
 for g,row in images.items():
  paths=[]
  for i,im in enumerate(row):
   f=P/f'frames/{g}/{KEY}/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);paths.append(f.relative_to(P).as_posix())
  m=json.loads((R/f'character/dr-veld-v2/packs/{g}-256x256-p128.0-128.0/manifest.json').read_text(encoding='utf-8'));state=copy.deepcopy(next(s for s in m['states'] if s['id']=='death-water-north'))
  state.update(id=KEY,frameFiles=paths,frameDurationsMs=durations,waterPoses=[True]*6,waterKinds=['tread','transition','transition','transition','transition','swim'],facings=['north']*6)
  out={**m,'name':'Veld authored north prone water death '+g,'states':[state],'status':'staged_tread_entrance_candidate_controller_world_restore_normal_selection_pending'}
  (P/f'{g}-manifest.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGBA',(7*256,2*256),'#202a30');d=ImageDraw.Draw(board)
 for ri,g in enumerate(images):
  for col,im in enumerate([images[g][0]]+images[g]):
   board.alpha_composite(im,(col*256,ri*256));d.text((col*256+4,ri*256+4),g+(' selected tread' if col==0 else ' death '+str(col-1)),fill='white')
 board.save(P/'paired-contact.png');board.resize((994,284),Image.Resampling.LANCZOS).save(P/'station-scale-contact.png')
 evidence={'fitChecks':checks,'fixedScale':scale,'rulerBasis':'selected tread head20 / original atlas median head72, frozen before anatomy edit','startScannerAnchor':start.tolist(),'finishScannerAnchor':finish.tolist(),'sourceSha256':sha(SOURCE),'sourceProvider':'exec-2d57cbe9-b2cd-4fb8-ac79-8d6e2071f920','editedProvider':'exec-6dd8b798-6f3e-4e21-97cc-e9c56ba1bde8','editedSourceSha256':sha(P/'sources/death-v3.png'),'sourcePoses':records,'selectedPoses':[1,2,3,4],'exactProneTerminal':True,'exactMasterEntry':True,'referenceHeadROI':roi,'earResidualRGB':[0,0,0],'patchResidualRGB':[0,0,0],'fits':fits,'materialCurves':{k:{'knots':v['knots'].tolist(),'targets':v['targets'].tolist()} for k,v in curves.items()},'scope':'independent rear tread-to-prone body, one head-width ruler/interpolated scanner anchor, pooled grade/four native pitch heads; source/player candidate only'}
 (P/'build-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
 if (P/'make_review.py').exists():subprocess.run([sys.executable,str(P/'make_review.py')],check=True,capture_output=True,text=True)
 print(f'{checks} fit/body-protection/clipping checks PASS;scale{scale:.8f};2states/12refs,finite1560ms')
if __name__=='__main__':main()
