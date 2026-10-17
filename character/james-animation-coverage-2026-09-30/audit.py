from pathlib import Path
import json,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
folder=ROOT/'character/chief-engineer-branforth-v2';catalog=json.loads((folder/'catalog.json').read_text());body={};equipment={}
for group,target in [('body',body),('equipment',equipment)]:
 for rel in catalog[group]:
  p=folder/rel;m=json.loads(p.read_text());target.update({s['id']:dict(path=p.relative_to(ROOT).as_posix(),frames=len(s['frameFiles']),selection='retained') for s in m['states']})
source=(ROOT/'scripts/grid_canvas.gd').read_text();start=source.index('elif actor == "branforth":');end=source.index('\nfunc ',start);block=source[start:end]
for kind,path in re.findall(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet",\s*)?"res://([^"]+)"',block):
 p=ROOT/path;m=json.loads(p.read_text());sel=p.parent/'selection.json';status=json.loads(sel.read_text()).get('status','') if sel.exists() else m.get('status','')
 target=body if kind=='load_manifest' else equipment;target.update({st['id']:dict(path=path,frames=len(st['frameFiles']),selection=status) for st in m['states']})
report=dict(method='Retained catalog followed by whole-path James overrides in source loader order; no native coverage claim',body=body,equipment=equipment)
(HERE/'runtime-coverage.json').write_text(json.dumps(report,indent=2)+'\n')
families={}
for key,row in body.items():
 family=re.sub(r'-(east|west|north|south)(-(east|west|north|south))?$','',key)
 entry=families.setdefault(family,dict(total=0,retained=0,states=[]));entry['total']+=1;entry['retained']+=row['selection']=='retained';entry['states'].append(key)
lines=['# James full-set coverage ledger','', 'Source selection inventory; refreshed by audit.py. Native evidence remains scoped to individual packs.', '', '| Family | Body states | Retained to review/replace |','|---|---:|---:|']
for key,row in sorted(families.items()):lines.append(f"| {key} | {row['total']} | {row['retained']} |")
lines+=['','The retained count describes selection provenance, not a technical failure or proof of visual quality. Full-set completion needs master/style/perspective/size/proportion/material and motion review for every family, bare and equipped, followed by cross-family consistency and polish.','', 'Current work: all listed families now have selected revised sources; zero retained James clips. Continue full pose, motion and handoff review; prior representative comparisons cover only their recorded source revisions. Read docs/JAMES_CONSISTENCY_HANDOFF_2026-09-30.md and the latest James entry in CURRENT_STATUS for current checks and remaining scope. Preserve authored crouch/swim/fallen dimensions; do not force them to standing bounds.', '', 'Runtime selection is not full-set visual, owner or release acceptance.']
(HERE/'README.md').write_text('\n'.join(lines)+'\n')
print('James body',len(body),'states /',sum(r['frames'] for r in body.values()),'slots;',sum(r['selection']=='retained' for r in body.values()),'retained states. Helmet',len(equipment),'states /',sum(r['frames'] for r in equipment.values()),'slots.')
