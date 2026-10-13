from pathlib import Path
import json,hashlib,argparse
parser=argparse.ArgumentParser()
parser.add_argument('--output',default='character/marsh-selected-normal-audit-2026-10-03-post-gesture')
args=parser.parse_args()
root=Path.cwd();cp=root/'character/marsh-v2/catalog.json';cat=json.loads(cp.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();states={};manifests=[]
for rel in cat['body']:
 mp=(cp.parent/rel).resolve();m=json.loads(mp.read_text());manifests.append({'path':mp.relative_to(root).as_posix(),'sha256':sha(mp)})
 for s in m['states']:
  files=[root/p.removeprefix('res://') if p.startswith('res://') else (mp.parent/p).resolve() for p in s['frameFiles']]
  states[s['id']]={'manifest':mp.relative_to(root).as_posix(),'state':s,'canvas':m.get('canvas'),'pivot':m.get('pivot'),'standingHeight':m.get('standingHeight'),'frames':[{'path':p.relative_to(root).as_posix(),'sha256':sha(p)} for p in files]}
o=root/args.output;o.mkdir(exist_ok=True)
r={'catalog':{'path':cp.relative_to(root).as_posix(),'sha256':sha(cp)},'orderedBodyManifests':manifests,'states':states,'stateCount':len(states),'slotCount':sum(len(s['frames']) for s in states.values()),'scope':'Current normal body selection at inventory creation; equipment manifests separately retained in catalog. Source inventory only, not visual/native full-state acceptance.'}
(o/'inventory.json').write_text(json.dumps(r,indent=2)+'\n');print(f"Current normal inventory: {r['stateCount']}states/{r['slotCount']}slots/{len(manifests)}ordered body manifests")
