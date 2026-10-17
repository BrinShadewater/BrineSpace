from pathlib import Path
import hashlib,json,subprocess,sys
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def check(ok,why):
 global checks
 assert ok,why
 checks+=1
binding=json.loads((P/'source-bindings.json').read_text(encoding='utf-8'))
for path,h in binding['bindings'].items():check(hashlib.sha256((R/path).read_bytes()).hexdigest()==h,'immutable authority')
for gear in ('bare','helmet'):
 m=json.loads((P/f'{gear}-manifest.json').read_text(encoding='utf-8'))
 check(m['pivot']==[128,224] and m['standingHeight']==148,'master ruler')
 check(len(m['states'])==3 and sum(len(s['frameFiles']) for s in m['states'])==18,'complete North sit/down-held-rise profile')
 expected={}
 for family in ('veld-seated-north-coherent-v1','veld-seated-north-breathing-source-v1'):
  source=R/f'character/{family}/{gear}-manifest.json'
  for state in json.loads(source.read_text(encoding='utf-8'))['states']:
   state['frameFiles']=['res://'+(source.parent/f).relative_to(R).as_posix() for f in state['frameFiles']];expected[state['id']]=state
 for state in m['states']:
  check(state==expected[state['id']],'entire tested source state unchanged')
  for name in state['frameFiles']:
   path=R/name.removeprefix('res://');im=Image.open(path)
   check(name.startswith('res://') and im.mode=='RGBA' and im.size==(256,256),'whole paths/native source')
 states={s['id']:s for s in m['states']}
 def raw(state,index):return (R/states[state]['frameFiles'][index].removeprefix('res://')).read_bytes()
 check(raw('sit-down-north',-1)==raw('sit-idle-north',0)==raw('sit-idle-north',-1)==raw('sit-rise-north',0),'byte-exact neutral joins')
files=[P/'bare-manifest.json',P/'helmet-manifest.json',P/'source-bindings.json']
def hashes():return {f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
before=hashes();subprocess.run([sys.executable,str(P/'build.py')],check=True,capture_output=True)
check(before==hashes(),'deterministic composition')
(P/'verification.json').write_text(json.dumps({'checks':checks,'failures':0,'hashes':before,'sourceBindings':len(binding['bindings']),'scope':'immutable source composition and exact neutral joins; normal selection/native acceptance separate'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'sourceBindings':len(binding['bindings'])}))
