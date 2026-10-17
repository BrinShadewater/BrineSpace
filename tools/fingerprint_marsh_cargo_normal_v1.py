from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1];paths={ROOT/'project.godot',ROOT/'scenes/main.tscn'}
for folder in ['scripts','rooms']:
 paths.update((ROOT/folder).rglob('*.gd'));paths.update((ROOT/folder).rglob('*.gd.uid'))
for name in ['install_marsh_cargo_matched_v1.py','review_marsh_cargo_normal_player_v1.gd','review_marsh_cargo_normal_player_v1.gd.uid','review_marsh_cargo_normal_world_v1.gd','review_marsh_cargo_normal_world_v1.gd.uid','fingerprint_marsh_cargo_normal_v1.py']:paths.add(ROOT/'tools'/name)
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
for rel in ['admission.json','selection.json']:paths.add(ROOT/'character/marsh-v2/supplemental/cargo-matched-v1'/rel)
receipt=json.loads((ROOT/'character/marsh-v2/supplemental/cargo-matched-v1/admission.json').read_text())
for m in receipt['manifests']:paths.add(ROOT/m['sourceManifest'])
for f in receipt['wholeFrameCopies']:paths.add(ROOT/f['source'])
records={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
Path(sys.argv[1]).write_text(json.dumps(records,indent=2)+'\n');print(len(records),'bounded normal cargo source/runtime/art inputs')
