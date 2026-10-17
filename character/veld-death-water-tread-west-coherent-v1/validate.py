"""Contract, exact selected entry, fixed ruler and material continuity evidence."""
from pathlib import Path
import hashlib,importlib.util,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def check(ok,why):
 global checks
 assert ok,why
 checks+=1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('fit',P/'build.py');fit=importlib.util.module_from_spec(spec);spec.loader.exec_module(fit)
e=json.loads((P/'build-evidence.json').read_text(encoding='utf-8'))
check(sha(P/'sources/death-v1.png')==e['sourceSha256'],'retained source')
check(len({v['scale'] for v in e['fits']})==1,'one anatomical ruler')
ref=np.array(Image.open(fit.REF).convert('RGBA'))
medians={k:np.median(ref[:,:,:3][v],axis=0) for k,v in fit.grade.materials(ref).items()}
rows=[]
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text(encoding='utf-8'));s=m['states'][0]
 check(m['pivot']==[128,128] and m['standingHeight']==148 and m['precomposed'],'prone equipment contract')
 check(s['id']=='death-water-tread-west' and len(s['frameFiles'])==6 and not s['loop'],'finite death coverage')
 check(s['frameDurationsMs']==[180,180,220,220,260,500],'original1560ms death duration')
 check(s['waterPoses']==[True]*6 and s['waterKinds']==['tread','transition','transition','transition','transition','swim'] and s['facings']==['west']*6,'water camera metadata')
 donor=np.array(Image.open(R/f'character/veld-water-west-coherent-v1/frames/{gear}/tread-west/000.png').convert('RGBA'))
 for i,file in enumerate(s['frameFiles']):
  im=Image.open(P/file);a=np.array(im);y,x=np.where(a[:,:,3]>20)
  check(im.mode=='RGBA' and im.size==(256,256),'RGBA source canvas')
  check(x.min()>0 and y.min()>0 and x.max()<255 and y.max()<255,'no alpha clipping')
  row={'gear':gear,'slot':i,'sha256':sha(P/file),'alphaExtent':[((z-128)*65.28/148) for z in [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]]}
  if i==0:check(np.array_equal(a,donor),'exact selected swim entry pixels')
  if i==5:
   terminal=np.array(Image.open(R/f'character/veld-death-water-west-coherent-v1/frames/{gear}/death-water-west/005.png').convert('RGBA'))
   check(np.array_equal(a,terminal),'exact prone corpse terminal pixels')
  if gear=='bare':
   fb=fit.grade.box(fit.grade.face(a));mf=fit.grade.box(fit.grade.face(ref))
   check(abs((fb[3]-fb[1])-(mf[3]-mf[1]))<=3,'face-height ruler within three pixels of selected master')
   check(abs((fb[2]-fb[0])-(mf[2]-mf[0]))<=3,'face width within three pixels of selected master')
   row['faceBox']=fb
   if i in [1,2,3,4]:
    target=np.array(next(f for f in e['fits'] if f['slot']==i)['targetScannerAnchor']);anchor,_=fit.scanner_anchor(a,[target[0]-8,target[1]-7,target[0]+8,target[1]+7])
    check(float(np.max(np.abs(anchor-target)))<=1,'rendered interpolated scanner anchor within one pixel')
    row['renderedScannerAnchor']=anchor.tolist();row['targetScannerAnchor']=target.tolist()
   row['materials']={}
   for k,mask in fit.grade.materials(a).items():
    value=np.median(a[:,:,:3][mask],axis=0);delta=float(np.max(np.abs(value-medians[k])))
    check(delta<=12,'material median vs selected master: '+k)
    row['materials'][k]={'medianRGB':value.tolist(),'masterMedianRGB':medians[k].tolist(),'maxChannelDelta':delta}
  rows.append(row)
report={'passed':True,'checks':checks,'runtimeSelected':False,'profileChanged':False,'rows':rows,'sourceSha256':e['sourceSha256'],'referenceHashes':{str(f.relative_to(R).as_posix()):sha(f) for f in [fit.REF,fit.HELM,R/'character/veld-swim-distress-west-coherent-v1/build.py']},'scope':'contract/master entry/median palette/alpha evidence; perceived motion,world clearance and normal selection separate'}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'{checks} contract/source/palette/registration checks PASS;2states/12refs,candidate only')
