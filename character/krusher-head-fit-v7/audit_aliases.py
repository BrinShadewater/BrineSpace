"""Check that previously identical registered poses remain identical."""
from pathlib import Path
from PIL import Image
import hashlib,json,sys
H=Path(__file__).resolve().parent;R=H.parents[1];OLD=R/'character/krusher-animation-package-v4';NEW=R/'character/krusher-coherent-bank-v3'
before='--before' in sys.argv
if before:NEW=R/'character/krusher-coherent-bank-v2'
read=lambda p:json.loads(p.read_text());old=read(OLD/'package.json');index=read(NEW/'candidate-bank-index.json');states={};cache={};groups={};slots=0
def digest(p):
 p=p.resolve()
 if p not in cache:
  im=Image.open(p).convert('RGBA');cache[p]=hashlib.sha256(str(im.size).encode()+im.tobytes()).hexdigest()
 return cache[p]
for g,paths in index['candidatePacks'].items():
 for path in paths:
  mp=R/path[6:];m=read(mp)
  for s in m['states']:states[g+':'+s['id']]=(mp,m,s)
for full,(mp,m,s) in states.items():
 q=old['states'][full];op=OLD/q['manifest'];om=read(op);os=next(t for t in om['states'] if t['id']==s['id'])
 for i,(a,b) in enumerate(zip(os['frameFiles'],s['frameFiles'])):
  key=(full.split(':')[0],digest(op.parent/a),tuple(m['pivot']));src=R/b[6:] if b.startswith('res://') else mp.parent/b;new=digest(src);groups.setdefault(key,{}).setdefault(new,[]).append({'state':full,'frame':i,'file':src.relative_to(R).as_posix()});slots+=1
conflicts=[{'oldPixels':k[1],'gear':k[0],'variants':list(v.values())} for k,v in groups.items() if len(v)>1]
report={'slots':slots,'originalPoseGroups':len(groups),'inconsistentGroups':len(conflicts),'conflicts':conflicts}
(H/('alias-audit.json' if before else 'alias-final-audit.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'slots':slots,'originalPoseGroups':len(groups),'inconsistentGroups':len(conflicts),'examples':[[[q['state'] for q in variant[:2]] for variant in c['variants']] for c in conflicts[:5]]}))
if not before:assert not conflicts,'Shared-pose continuity differs'
