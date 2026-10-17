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
check(sha(P/'sources/death-v2.png')==e['editedSourceSha256'],'retained edited source')
check(len({v['scale'] for v in e['fits']})==1,'one anatomical ruler')
ref=np.array(Image.open(fit.REF).convert('RGBA'))
medians={k:np.median(ref[:,:,:3][v],axis=0) for k,v in fit.grade.materials(ref,e['referenceHeadROI']).items()}
rows=[]
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text(encoding='utf-8'));s=m['states'][0]
 check(m['pivot']==[128,128] and m['standingHeight']==148 and m['precomposed'],'prone equipment contract')
 check(s['id']=='death-water-north' and len(s['frameFiles'])==6 and not s['loop'],'finite death coverage')
 check(s['frameDurationsMs']==[180,180,220,220,260,500],'original1560ms death duration')
 check(s['waterPoses']==[True]*6 and s['waterKinds']==['swim']*6 and s['facings']==['north']*6,'water camera metadata')
 donor=np.array(Image.open(R/f'character/veld-water-north-coherent-v1/frames/{gear}/swim-north/000.png').convert('RGBA'))
 for i,file in enumerate(s['frameFiles']):
  im=Image.open(P/file);a=np.array(im);y,x=np.where(a[:,:,3]>20)
  check(im.mode=='RGBA' and im.size==(256,256),'RGBA source canvas')
  check(x.min()>0 and y.min()>0 and x.max()<255 and y.max()<255,'no alpha clipping')
  row={'gear':gear,'slot':i,'sha256':sha(P/file),'alphaExtent':[((z-128)*65.28/148) for z in [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]]}
  if i==0:check(np.array_equal(a,donor),'exact selected swim entry pixels')
  if gear=='bare':
   head=fit.headbox(a,e['referenceHeadROI'] if i==0 else None);master_head=fit.headbox(ref,e['referenceHeadROI']);extent=fit.grade.bbox(a[:,:,3]>160);master_extent=fit.grade.bbox(ref[:,:,3]>160)
   check(abs((head[2]-head[0])-(master_head[2]-master_head[0]))<=2,'rear head width within two pixels of master')
   check(abs((extent[3]-head[1])-(master_extent[3]-master_head[1]))<=10,'crown-to-sole span within ten pixels of master')
   check(abs(extent[3]-master_extent[3])<=5,'relaxed soles within five pixels of registered master')
   row['headBox']=head;row['crownToSoleSpan']=extent[3]-head[1];row['masterCrownToSoleSpan']=master_extent[3]-master_head[1]
   anchor,_=fit.scanner_anchor(a)
   check(float(np.max(np.abs(anchor-np.array(e['targetScannerAnchor']))))<=1,'registered belt anchor within one pixel')
   row['renderedScannerAnchor']=anchor.tolist()
   row['materials']={}
   for k,mask in fit.grade.materials(a,e['referenceHeadROI'] if i==0 else None).items():
    if k not in e['materialCurves']:continue
    value=np.median(a[:,:,:3][mask],axis=0);delta=float(np.max(np.abs(value-medians[k])))
    check(delta<=12,'material median vs selected master: '+k)
    row['materials'][k]={'medianRGB':value.tolist(),'masterMedianRGB':medians[k].tolist(),'maxChannelDelta':delta}
  rows.append(row)
report={'passed':True,'checks':checks,'runtimeSelected':False,'profileChanged':False,'rows':rows,'sourceSha256':e['sourceSha256'],'referenceHashes':{str(f.relative_to(R).as_posix()):sha(f) for f in [fit.REF,fit.HELM,R/'character/veld-swim-distress-north-coherent-v1/build.py']},'scope':'contract/master entry/median palette/alpha evidence; perceived motion,world clearance and normal selection separate'}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'{checks} contract/source/palette/registration checks PASS;2states/12refs,candidate only')
