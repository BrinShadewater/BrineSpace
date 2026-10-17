from pathlib import Path
import json,hashlib,subprocess,sys
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent; R=P.parents[1]; checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reg=json.loads((P/'registration.json').read_text()); box=reg['insertRegion']; mask=np.zeros((256,256),bool);mask[box[1]:box[3],box[0]:box[2]]=True
check(sha(P/reg['source'])==reg['sourceSha256'],'generated source binding')
check(sha(R/reg['gradeAuthority'])==reg['gradeAuthoritySha256'],'frozen material curves binding')
files=[];refs=0
for gear in ('bare','helmet'):
 m=json.loads((P/f'{gear}-manifest.json').read_text());full,entry,exit,hold=m['states'];base_path=R/reg['bodyAuthority'][gear]['path'];base=np.array(Image.open(base_path).convert('RGBA'))
 check(sha(base_path)==reg['bodyAuthority'][gear]['sha256'],'body authority unchanged')
 check(m['status']=='staged_candidate' and m['pivot']==[128,224] and m['standingHeight']==148,'standing calibration')
 check(sum(full['frameDurationsMs'])==12000 and not full['loop'],'finite full12s reading choreography')
 check(sum(entry['frameDurationsMs'])==480 and sum(exit['frameDurationsMs'])==480 and sum(hold['frameDurationsMs'])==11040,'draw/hold/stow clocks')
 check(not entry['loop'] and not exit['loop'] and hold['loop'],'finite bridges and held loop')
 check(exit['frameFiles']==entry['frameFiles'][::-1] and exit['frameDurationsMs']==entry['frameDurationsMs'][::-1],'exact stow reverse')
 check(full['frameFiles']==entry['frameFiles']+hold['frameFiles']+exit['frameFiles'],'full state uses explicit bridges and hold')
 check(full['frameFiles'][0]==full['frameFiles'][-1]==entry['frameFiles'][0],'neutral reading joins')
 for state in m['states']:
  count=len(state['frameFiles']);refs+=count
  check(all(len(state[key])==count for key in ('frameDurationsMs','facings','waterPoses','waterKinds','depthOffsets')),'per-slot metadata lengths')
  check(state['seatContactDepth'] and state['facings']==['south']*count and state['waterPoses']==[False]*count,'dry South registered seat')
 for file in sorted(set(full['frameFiles'])):
  p=P/file;image=Image.open(p);a=np.array(image);files.append(p)
  check(image.mode=='RGBA' and image.size==(256,256),'RGBA canvas')
  check(np.array_equal(a[~mask],base[~mask]),'exact body/head/face/hair/helmet/boots outside insertion')
  check(np.array_equal(a[185:],base[185:]) and np.array_equal(a[:148],base[:148]),'upper body and lower limbs exact')
  if file.endswith('/000.png'):check(np.array_equal(a,base),'exact neutral seated pixels')
 files.append(P/f'{gear}-manifest.json')
files += [P/'registration.json',P/'paired-contact.png']
before={p.relative_to(P).as_posix():sha(p) for p in files};subprocess.run([sys.executable,str(P/'fit.py')],check=True,capture_output=True)
check(before=={p.relative_to(P).as_posix():sha(p) for p in files},'deterministic insertion/rebuild')
(P/'verification.json').write_text(json.dumps({'checks':checks,'failures':0,'uniqueExports':12,'states':8,'frameReferences':refs,'normalSelection':False,'bindings':before,'scope':'bounded source/body/grade/clocks/reverse/neutral joins/rebuild; native furniture/interruptions/Continue/acceptance separate'},indent=2)+'\n')
print(json.dumps({'checks':checks,'failures':0,'deterministicFiles':len(before),'states':8,'references':refs}))
