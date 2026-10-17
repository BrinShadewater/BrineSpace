from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1];paths={ROOT/'project.godot',ROOT/'scenes/main.tscn'}
paths.update(ROOT/p for p in ['tools/install_marsh_south_step_contact_v1.py','character/marsh-v2/supplemental/south-step-contact-v1/admission.json','character/marsh-south-step-detail-v1/candidate-02-registered-frame.png'])
for folder in ['scripts','rooms']:
 paths.update((ROOT/folder).rglob('*.gd'));paths.update((ROOT/folder).rglob('*.gd.uid'))
for name in ['review_marsh_south_step_normal_world_v1.gd','review_marsh_south_step_normal_world_v1.gd.uid','fingerprint_marsh_south_step_normal_world_v1.py','install_marsh_south_step_detail_v1.py','review_marsh_south_step_detail_v1.gd','review_marsh_south_step_detail_v1.gd.uid','fingerprint_marsh_south_step_detail_v1.py','install_marsh_cargo_matched_v1.py','review_marsh_cargo_normal_player_v1.gd','review_marsh_cargo_normal_player_v1.gd.uid','review_marsh_cargo_normal_world_v1.gd','review_marsh_cargo_normal_world_v1.gd.uid','fingerprint_marsh_cargo_normal_v1.py']:paths.add(ROOT/'tools'/name)
# Freeze quoted runtime artwork/data; no folder-prefix expansion or output traversal.
for p in list(paths):
 if p.suffix=='.gd':
  for ref in re.findall(r'"(res://[^"\n]+\.(?:png|json|tscn|ttf))"',p.read_text()):
   q=ROOT/ref.removeprefix('res://')
   if q.is_file():paths.add(q)
catalog=ROOT/'character/marsh-v2/catalog.json';paths.add(catalog);data=json.loads(catalog.read_text())
for rel in data['body']+data['equipment']:
 mp=(catalog.parent/rel).resolve();paths.add(mp)
 for state in json.loads(mp.read_text())['states']:
  for f in state['frameFiles']:paths.add(ROOT/f.removeprefix('res://') if f.startswith('res://') else (mp.parent/f).resolve())
for rel in ['admission.json','selection.json']:paths.add(ROOT/'character/marsh-v2/supplemental/south-step-detail-v1'/rel)
receipt=json.loads((ROOT/'character/marsh-v2/supplemental/south-step-detail-v1/admission.json').read_text())
paths.add(ROOT/receipt['oldManifest']);paths.add(ROOT/receipt['wholeSource'])
for f in receipt['originalSources']:paths.add(ROOT/f['path'])
paths.update(p for p in (ROOT/'character/marsh-east-walk-family-detail-v1').glob('*') if p.is_file())
paths.update(ROOT/'tools'/n for n in ['prepare_marsh_east_walk_family_detail_v1.py','review_marsh_east_walk_family_detail_v1.py','prepare_marsh_east_walk_family_native_v1.py','review_marsh_east_walk_family_detail_v1.gd','review_marsh_east_walk_family_detail_v1.gd.uid','fingerprint_marsh_east_walk_family_detail_v1.py'])
paths.update(p for p in (ROOT/'character/marsh-east-walk-family-contact-v1').glob('*') if p.is_file())
paths.add(ROOT/'tools/register_marsh_east_walk_family_contact_v1.py')
paths.update(ROOT/'tools'/n for n in ['prepare_marsh_east_walk_world_v1.py','review_marsh_east_walk_world_v1.gd','review_marsh_east_walk_world_v1.gd.uid','fingerprint_marsh_east_walk_world_v1.py'])
paths.update(p for folder in ['character/marsh-east-walk-bob-polish-v1','character/marsh-east-walk-bob-contact-v1'] for p in (ROOT/folder).glob('*') if p.is_file())
paths.update(ROOT/'tools'/n for n in ['prepare_marsh_east_walk_bob_polish_v1.py','review_marsh_east_walk_bob_polish_v1.py','prepare_marsh_east_walk_bob_contact_v1.py','review_marsh_east_walk_bob_world_v1.gd','review_marsh_east_walk_bob_world_v1.gd.uid','fingerprint_marsh_east_walk_bob_world_v1.py'])
paths.update(p for folder in ['character/marsh-east-walk-halfcycle-polish-v1','character/marsh-v2/supplemental/east-walk-polish-v1'] for p in (ROOT/folder).glob('*') if p.is_file())
paths.update(ROOT/'tools'/n for n in ['prepare_marsh_east_walk_halfcycle_v1.py','review_marsh_east_walk_halfcycle_v1.py','install_marsh_east_walk_halfcycle_v1.py','prepare_marsh_east_walk_selected_v1.py','review_marsh_east_walk_selected_v1.gd','review_marsh_east_walk_selected_v1.gd.uid','fingerprint_marsh_east_walk_selected_v1.py'])
paths.update(p for folder in ['character/marsh-west-walk-family-detail-v1','character/marsh-west-walk-family-contact-v1'] for p in (ROOT/folder).glob('*') if p.is_file())
paths.update(ROOT/'tools'/n for n in ['prepare_marsh_west_walk_family_v1.py','review_marsh_west_walk_family_v1.py','prepare_marsh_west_walk_world_v1.py','review_marsh_west_walk_world_v1.gd','review_marsh_west_walk_world_v1.gd.uid','fingerprint_marsh_west_walk_world_v1.py'])
paths.update(p for folder in ['character/marsh-west-walk-family-detail-v1','character/marsh-v2/supplemental/west-walk-polish-v1'] for p in (ROOT/folder).glob('*') if p.is_file())
paths.update(ROOT/'tools'/n for n in ['prepare_marsh_west_walk_family_v1.py','review_marsh_west_walk_family_v1.py','install_marsh_west_walk_family_v1.py','prepare_marsh_west_walk_selected_v1.py','review_marsh_west_walk_selected_v1.gd','review_marsh_west_walk_selected_v1.gd.uid','fingerprint_marsh_west_walk_selected_v1.py'])
paths.update(p for p in (ROOT/'character/marsh-north-walk-family-detail-v1').glob('*') if p.is_file())
paths.update(ROOT/'tools'/n for n in ['prepare_marsh_north_walk_family_v1.py','review_marsh_north_walk_family_v1.py','review_marsh_north_walk_world_v1.gd','review_marsh_north_walk_world_v1.gd.uid','fingerprint_marsh_north_walk_world_v1.py'])
paths.update(p for p in (ROOT/'character/marsh-south-walk-family-detail-v1').glob('*') if p.is_file())
paths.update(ROOT/'tools'/n for n in ['review_marsh_south_walk_world_v1.gd','review_marsh_south_walk_world_v1.gd.uid','fingerprint_marsh_south_walk_world_v1.py'])
paths.update(p for p in (ROOT/'character/marsh-v2/supplemental/south-walk-polish-v1').glob('*') if p.is_file())
paths.update(ROOT/'tools'/n for n in ['review_marsh_south_walk_selected_v1.gd','review_marsh_south_walk_selected_v1.gd.uid','fingerprint_marsh_south_walk_selected_v1.py','install_marsh_south_walk_family_v1.py'])
paths.update(ROOT/'tools'/n for n in ['review_marsh_final_save_v1.gd','review_marsh_final_save_v1.gd.uid','fingerprint_marsh_final_save_v1.py'])
paths.add(ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-south-walk/inventory.json')
paths.update(ROOT/'tools'/n for n in ['review_marsh_cardinal_continue_v1.gd','review_marsh_cardinal_continue_v1.gd.uid','fingerprint_marsh_cardinal_continue_v1.py'])
paths.update(p for p in (ROOT/'character/marsh-south-work-polish-v1').glob('*') if p.is_file())
paths.update(ROOT/'tools'/n for n in ['review_marsh_south_work_polish_v1.gd','review_marsh_south_work_polish_v1.gd.uid','fingerprint_marsh_south_work_polish_v1.py','review_marsh_south_work_polish_v1.py'])
paths.update(p for p in (ROOT/'character/marsh-v2/supplemental/south-work-polish-v1').glob('*') if p.is_file())
paths.update(ROOT/'tools'/n for n in ['review_marsh_south_work_polish_normal_v1.gd','review_marsh_south_work_polish_normal_v1.gd.uid','fingerprint_marsh_south_work_polish_normal_v1.py','install_marsh_south_work_polish_v1.py'])
paths.add(ROOT/'character/marsh-selected-normal-audit-2026-10-04-post-south-work/inventory.json')
paths.update(ROOT/'tools'/n for n in ['review_marsh_south_work_dispatch_v1.gd','review_marsh_south_work_dispatch_v1.gd.uid','fingerprint_marsh_south_work_dispatch_v1.py'])
paths.update(ROOT/'tools'/n for n in ['review_marsh_south_repair_joins_v1.gd','review_marsh_south_repair_joins_v1.gd.uid','fingerprint_marsh_south_repair_joins_v1.py'])
paths.update(p for p in (ROOT/'character/marsh-south-repair-joins-v1').glob('*') if p.is_file())
paths.add(ROOT/'tools/install_marsh_south_repair_joins_v1.py')
paths.update(p for p in (ROOT/'character/marsh-v2/supplemental/south-repair-joins-v1').glob('*') if p.is_file())
paths.update(ROOT/'tools'/n for n in ['review_marsh_south_repair_continue_v1.gd','review_marsh_south_repair_continue_v1.gd.uid','fingerprint_marsh_south_repair_continue_v1.py'])
paths.update(ROOT/'tools'/n for n in ['review_marsh_south_salvage_job_v1.gd','review_marsh_south_salvage_job_v1.gd.uid','fingerprint_marsh_south_salvage_job_v1.py'])
records={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
Path(sys.argv[1]).write_text(json.dumps(records,indent=2)+'\n');print(len(records),'bounded normal cargo source/runtime/art inputs')
