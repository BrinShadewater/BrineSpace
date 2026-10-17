from pathlib import Path
import json,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[2];P=R/'character/krusher-animation-package-v10';OLD=R/'character/krusher-animation-package-v9';read=lambda p:json.loads(p.read_text());new=read(P/'package.json');old=read(OLD/'package.json');coverage=read(R/'character/krusher-complete-animation-v1/source-coverage.json')['resolved'];required={g+':'+sid for g,states in coverage.items() for sid in states};checks=0;errors=[];refs=0
cache={}
def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
def manifest(root,rel):
 key=str(root/rel)
 if key not in cache:cache[key]=read(root/rel)
 return cache[key]
check(set(new['states'])==required==set(old['states']),'all586frozen states exact')
for key,q in new['states'].items():
 m=manifest(P,q['manifest']);s=next(s for s in m['states'] if key.split(':',1)[1]==s['id']);om=manifest(OLD,old['states'][key]['manifest']);os=next(s for s in om['states'] if key.split(':',1)[1]==s['id']);check({k:v for k,v in m.items() if k not in ['states','status']}=={k:v for k,v in om.items() if k not in ['states','status']},'root profile and metadata '+key);check({k:v for k,v in s.items() if k!='frameFiles'}=={k:v for k,v in os.items() if k!='frameFiles'},'state profile and metadata '+key);check(len(s['frameFiles'])==len(q['sourceFrames'])==len(os['frameFiles']),'slot counts '+key)
 for f,source in zip(s['frameFiles'],q['sourceFrames']):
  dest=(P/q['manifest']).parent/f;src=R/source;content=src.read_bytes();check(dest.read_bytes()==content,'exact corrected source '+key+' '+f);refs+=1
for rel,q in new['files'].items():
 p=P/rel;content=p.read_bytes();check(hashlib.sha256(content).hexdigest()==q['sha256'] and len(content)==q['bytes'],'indexed content hash '+rel);im=Image.open(p);check(im.format=='PNG' and im.mode=='RGBA','native PNG encoding '+rel)
check(refs==8058,'all8058references');report={'checks':checks,'errors':errors,'states':len(new['states']),'references':refs,'uniquePng':len(new['files']),'scope':'Full frozen state set, every corrected source byte, original root/state metadata and slot counts versus V9 package, all indexed content hashes and native PNG encodings. Does not certify station appearance.'};(P/'source-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['checks','states','references','uniquePng']}|{'errors':len(errors),'examples':errors[:12]}))
if errors:raise SystemExit(1)



