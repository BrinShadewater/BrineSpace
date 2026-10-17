from pathlib import Path
import json,hashlib,copy
P=Path(__file__).resolve().parent;ROOT=P.parents[1];checks=[];bindings={}
def check(ok,name):checks.append({'passed':bool(ok),'check':name})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
profiles={}
for gear in ['bare','helmet']:
 states=[]
 for d in ['east','west','north','south']:
  folder=P.parent/f'bill-death-ground-{"helmet-" if gear=="helmet" else ""}{d}-coherent-v1';m=json.loads((folder/'manifest.json').read_text());s=copy.deepcopy(m['states'][0])
  check(m['pivot']==[128,224] and m['standingHeight']==148 and m['precomposed'],'Shared physical plane '+gear+' '+d)
  check(not s['loop'] and s['terminalFrame']==5 and s['frameDurationsMs']==[250,300,350,400,400,300],'Finite collapse timeline '+gear+' '+d)
  check(s['facings']==[d]*6 and s['waterPoses']==[False]*6 and s['depthOffsets']==[0]*6,'Dry directional metadata '+gear+' '+d)
  s['frameFiles']=['res://'+(folder/f).relative_to(ROOT).as_posix() for f in s['frameFiles']]
  for f in s['frameFiles']:
   path=ROOT/f.removeprefix('res://');check(path.is_file(),'Literal frame '+f);bindings[f]=sha(path)
  states.append(s)
 profiles[gear]={'name':'Bill four-direction dry collapse '+gear+' candidate family','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':states}
 profiles[gear]['deathEntryMode']='lowered-start-v1'
 if gear=='helmet':profiles[gear]['equipment']='diving-helmet'
for b,h in zip(profiles['bare']['states'],profiles['helmet']['states']):check(b['id']==h['id'] and b['frameDurationsMs']==h['frameDurationsMs'] and len(b['frameFiles'])==len(h['frameFiles']),'Compatible gear pair '+b['id'])
for gear,m in profiles.items():(P/('manifest.json' if gear=='bare' else 'helmet-manifest.json')).write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks,'sha256':bindings,'scope':'48 literal references/eight staged directional gear states; assembly does not prove normal mortality, floor clearance or Continue'}
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':result['passed'],'checks':len(checks),'states':8,'frameReferences':len(bindings)}));raise SystemExit(0 if result['passed'] else 1)
