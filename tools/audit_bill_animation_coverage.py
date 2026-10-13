"""Inventory Bill's current loader sources and staged replacements, not visual approval."""
from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'character/bill-animation-coverage-2026-09-30'

def main():
 source=(ROOT/'scripts/grid_canvas.gd').read_text(encoding='utf-8')
 block=source.split('func _load_major_bill_animations() -> void:',1)[1].split('\nfunc ',1)[0]
 base=ROOT/'character/major-bill-v3';catalog=json.loads((base/'catalog.json').read_text())
 selected={k:{} for k in ['bare','helmet']};orders={k:[] for k in selected}
 def add(kind,path):
  data=json.loads(path.read_text(encoding='utf-8'));relative=path.relative_to(ROOT).as_posix();orders[kind].append(relative)
  for state in data['states']:
   selected[kind][state['id']]={'manifest':relative,'frames':len(state['frameFiles']),'revision':'current_master_replacement' if 'major-bill-v3/' not in relative else 'retained_older_library'}
 for kind,field in [('bare','body'),('helmet','equipment')]:
  for relative in catalog[field]:add(kind,base/relative)
 for match in re.finditer(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet",\s*)?"res://([^\"]+)"',block):
  add('bare' if match[1]=='load_manifest' else 'helmet',ROOT/match[2])
 installed={p for paths in orders.values() for p in paths};staged={};referenced_roots=set()
 for relative in installed:
  path=ROOT/relative;data=json.loads(path.read_text())
  for state in data['states']:
   for file in state['frameFiles']:referenced_roots.add((path.parent/file).resolve().parents[2])
 for pattern in ['bill-cargo-*-v1','bill-carry-turn-*-v1','bill-swim-*-v1','bill-tread-*-v1']:
  for folder in sorted((ROOT/'character').glob(pattern)):
   path=folder/'manifest.json'
   if not path.exists():continue
   data=json.loads(path.read_text());relative=path.relative_to(ROOT).as_posix()
   if relative not in installed and folder.resolve() not in referenced_roots:staged[relative]={'status':data.get('status',''),'equipment':data.get('equipment','bare'),'states':[s['id'] for s in data['states']]}
 for kind in ['bare','helmet']:
  path=ROOT/f'character/bill-carry-turn-matrix-v1/{kind}-manifest.json'
  if path.exists() and path.relative_to(ROOT).as_posix() not in installed:
   data=json.loads(path.read_text());staged[path.relative_to(ROOT).as_posix()]={'status':data.get('status',''),'equipment':data.get('equipment','bare'),'states':[s['id'] for s in data['states']],'aggregateReferences':True}
 unique_staged={kind:sorted({state for pack in staged.values() if ('helmet' if pack['equipment']=='diving-helmet' else 'bare')==kind for state in pack['states']}) for kind in ['bare','helmet']}
 report={'scope':'Bill only;actual _load_major_bill_animations manifest sequence plus base catalog;staged scan scoped to cargo/carry-turn/swim/tread v1 families;runtime-derived joins not simulated','loaderSha256':hashlib.sha256(block.encode()).hexdigest(),'loadOrder':orders,'selectedStateSources':selected,'stagedPacks':staged,'uniqueStagedStateKeys':unique_staged,'visualAcceptanceProven':False,'runtimeJoinsToReview':['whole-station carry travel/settle/turn/resume visual motion','new swim/tread/start/stop and equipment endpoint continuity'],'completion':False}
 OUT.mkdir(exist_ok=True);(OUT/'coverage.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 lines=['# Bill full-set coverage audit','', 'Loader source inventory only. State presence does not prove visual consistency, native playback or full-set completion.','']
 for kind,states in selected.items():
  older=[key for key,v in states.items() if v['revision']=='retained_older_library']
  lines += [f'## {kind}: {len(states)} selected keys, {len(older)} still from older library','', '| State | Selected manifest |','|---|---|']
  lines += [f"| {key} | {value['manifest']} |" for key,value in sorted(states.items())]
 lines += ['',f'## {len(staged)} staged cargo/turn/swim/tread manifests','', 'Staged discovery is scoped to cargo/carry-turn/swim/tread v1 families. Aggregate matrix manifests reuse quarter clips; manifest counts are not unique authored coverage.', '',f"Unique staged keys:bare {len(unique_staged['bare'])},helmet {len(unique_staged['helmet'])}.", '']+[f"- {path}: {v['status']} ({len(v['states'])} states)" for path,v in staged.items()]
 lines += ['', '## Remaining requirements','', '- Full owner visual acceptance remains pending, separate from installed cargo selection and native clock tests.', '- Review whole-station walking settle/resume and half-turn movement.', '- Four-direction basic swimming, cargo, turns, distress, salvage and pickup installed; retained recovery/death and full outward/airlock journeys remain.', '- Replace or explicitly audit every older selected state against the current masters, including water, everyday life and death.', '- Cross-reference all new packs for anatomy, perspective, material and timing.', '- Isolated native playback and runtime join verification; owner acceptance remains distinct.']
 (OUT/'coverage.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print({kind:{'selected':len(states),'retainedOlder':sum(v['revision']=='retained_older_library' for v in states.values())} for kind,states in selected.items()});print(f'{len(staged)} staged manifests;unique bare/helmet keys '+str({k:len(v) for k,v in unique_staged.items()})+';full goal remains incomplete')
if __name__=='__main__':main()
