from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;index=json.load(open(P/'package.json'));cache={};checks=0;errors=[];slots=0

def check(ok,label):
 global checks
 checks+=1
 if not ok:errors.append(label)
def read(p):
 if p not in cache:cache[p]=json.load(open(p))
 return cache[p]
for full,q in index['states'].items():
 gear,key=full.split(':',1);original=read(R/q['sourceManifest']);pack=read(P/q['manifest']);a=next(x for x in original['states'] if x['id']==key);b=next(x for x in pack['states'] if x['id']==key)
 check({k:v for k,v in original.items() if k!='states'}=={k:v for k,v in pack.items() if k!='states'},full+' entire root metadata')
 check({k:v for k,v in a.items() if k!='frameFiles'}=={k:v for k,v in b.items() if k!='frameFiles'},full+' entire state metadata')
 check(len(q['sourceFrames'])==len(b['frameFiles']),full+' pose count')
 x=320-pack['pivot'][0]*2;y=560-pack['pivot'][1]*2
 check(x>=0 and y>=0 and x+pack['frameWidth']*2<=640 and y+pack['frameHeight']*2<=960,full+' entire viewer canvas enclosed')
 for source,dest in zip(q['sourceFrames'],b['frameFiles']):
  out=((P/q['manifest']).parent/dest).resolve();check(out.is_relative_to(P.resolve()),full+' portable frame path')
  check((R/source).read_bytes()==out.read_bytes(),full+' exact packaged PNG');slots+=1
check(sum(k.startswith('bare:') for k in index['states'])==338,'bare state count');check(sum(k.startswith('helmet:') for k in index['states'])==248,'helmet state count')
report={'checks':checks,'errors':errors,'slots':slots,'uniquePNG':len(index['files']),'scope':'Entire root/state metadata compared with selected current sources; all8058PNG bytes exact and frame paths inside package; all profiles fit corrected viewer canvas. Native/source/world and owner visual acceptance are separate.'}
(P/'package-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'checks':checks,'errors':len(errors),'slots':slots,'firstErrors':errors[:5]}));assert not errors
