from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parents[1];f=json.loads((P/'frozen-bindings.json').read_text());reg=json.loads((P/'registration.json').read_text());checks=[]
def check(ok,name):
 assert ok,name
 checks.append(name)
bodycal=reg['bodyCalibration'];raw=np.array(Image.open(P/bodycal['source']))[:,:384];labs,_=label(raw[:,:,3]>180);n=np.bincount(labs.ravel());n[0]=0;y,x=np.where(labs==n.argmax());sourceheight=int(y.max()-y.min()+1)
check(bodycal['opaqueSourceHeight']==sourceheight and bodycal['cell']==0,'Body ruler uses actual complete first source figure')
check(reg['scale']==148/sourceheight and bodycal['scale']==reg['scale'],'One complete-source ruler')
cal=reg['helmetCalibration']
heights=[Image.open(R/file).height for file in cal['masterPaths']]
check(heights==cal['masterHeights'] and cal['targetNativeHeight']==float(np.median(heights)),'Helmet calibration matches complete current canonical components')
check(cal['scale']==cal['targetNativeHeight']/cal['opaqueSourceHeight'] and cal['cell']==0,'One complete first-head ruler for independent component sheet')
current=json.loads((P/'material-grade.json').read_text())['fixedGains'];baseline=json.loads((P/'sources/material-grade-v7.json').read_text())['fixedGains'];recipe=json.loads((P/'sources/material-grade-skin-v9.json').read_text())['fixedGains']
check(current==recipe,'One recorded shared skin correction recipe')
check(all(current[k]==baseline[k] for k in baseline if k!='skin'),'Every non-skin material gain remains unchanged')
Y,X=np.indices((256,256));protected=(Y>=110)|(X<=100)|(X>=160)
for gear in ['bare','helmet']:
 for i in [1,2,3,4]:
  filename=f'frames/{gear}/carry-turn-east-south/{i:03}.png'
  a=np.array(Image.open(P/filename));old=np.array(Image.open(P/'review-before-skin-v9'/filename))
  fit=reg['frames'][i-1].get('caseFit');case_region=np.zeros((256,256),dtype=bool)
  if fit:
   x0,y0,x1,y1=fit['nativeFitBox'];case_region=(X>=x0)&(X<x1)&(Y>=y0)&(Y<y1)
  check(np.array_equal(a[protected&~case_region],old[protected&~case_region]) and np.array_equal(a[:,:,3][~case_region],old[:,:,3][~case_region]),'Skin/case pass preserves pixels and alpha outside bounded intended edits')
  if fit:check(np.array_equal(a[y0:y1,x0:x1],np.array(Image.open(P/fit['component']))),'Recorded bounded case/glove component exact in both gears')
for r in reg['frames']:
 check(r['scale']==reg['scale'],'All body poses share whole-source ruler')
 check(r['helmetScale']==cal['scale'],'All helmets share single independent-source ruler')
 check(r['helmetSourceBox'][0]>3 and r['helmetSourceBox'][2]<380,'Complete unclipped helmet source width')
 check(abs(r['opaqueSourceHeight']*reg['scale']-148)<2,'Native stature varies less than2px')
 check(r['sourceBox'][1]>10 and r['sourceBox'][3]<1010,'Complete source soles/crown')
 i=r['frame'];bare=np.array(Image.open(P/f'frames/bare/carry-turn-east-south/{i:03}.png'));gear=np.array(Image.open(P/f'frames/helmet/carry-turn-east-south/{i:03}.png'));head=Image.open(P/f'sources/component-helmet-{i:03}.png');plane=Image.new('RGBA',(256,256));plane.alpha_composite(head,tuple(r['helmetPosition']));ha=np.array(plane);mask=np.array(Image.open(P/f'sources/erase-{i:03}.png'))>0;region=mask|(ha[:,:,3]>0)
 check(np.array_equal(bare[~region],gear[~region]),'Paired suit/case/feet exact outside helmet fit')
 base=bare.copy();base[mask]=0;expected=Image.fromarray(base);expected.alpha_composite(head,tuple(r['helmetPosition']));check(np.array_equal(gear,np.array(expected)),'Recorded helmet component exact')
 y,x=np.where(bare[:,:,3]>180);check(y.max()==224,'Native soles registered to fixed foot')
 labs,_=label(gear[:,:,3]>160);counts=np.bincount(labs.ravel());counts[0]=0;h=ha[:,:,3]>200;check((labs[h]==counts.argmax()).mean()>.98,'Helmet connected to body')
for g,name in [('bare','bare-manifest.json'),('helmet','helmet-manifest.json')]:
 m=json.loads((P/name).read_text());old=json.loads((R/f['turn'][g]['manifest']).read_text());check(m['status']=='staged_visual_review','Candidate explicitly unselected');check(m['pivot']==[128,224] and m['standingHeight']==148,'Native density metadata')
 for s in m['states']:
  original=next(o for o in old['states'] if o['id']==s['id']);check(s['frameDurationsMs']==original['frameDurationsMs'] and s['facings']==original['facings'],'Existing source clocks and facing metadata')
  check(all((R/file[6:]).is_file() for file in s['frameFiles']),'All literal frame paths available')
 check(m['states'][0]['frameFiles']==m['states'][1]['frameFiles'][::-1],'Exact reverse without mirror')
 for index,direction in [(0,'east'),(5,'south')]:check((P/f'frames/{g}/carry-turn-east-south/{index:03}.png').read_bytes()==(R/f['endpoints'][g][direction][6:]).read_bytes(),'Exact current held cardinal endpoint')
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':len(checks),'scope':'Staged source density/complete soles/paired-body protection/endpoints/clock checks;no native selection or motion acceptance'},indent=2)+'\n');print(str(len(checks))+' staged package checks pass')
