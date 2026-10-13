"""Bounded actor + full staged body/effect family input freeze."""
from pathlib import Path
import hashlib,json,runpy,sys
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'tools/fingerprint_marsh_south_collapse_actor.py'))
out=Path(sys.argv[1]);records=json.loads(out.read_text())
base=ROOT/'character/marsh-south-injury-material-v1'
paths=[ROOT/p for p in ['tools/prepare_marsh_south_injury_fluid.py','tools/build_marsh_south_injury_material.py','tools/review_marsh_south_injury_actor.gd','tools/review_marsh_south_injury_actor.gd.uid','tools/fingerprint_marsh_south_injury_actor.py']]
paths+=list((base/'sources').glob('*'))+list((base/'candidate-01').glob('*'))
for action in ['injury-ground-south','injury-rise-south']:paths+=list((base/'candidate-01'/action).glob('*'))
for p in paths:
    if p.is_file():records[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
out.write_text(json.dumps(records,indent=2)+'\n');print(len(records),'bounded injury actor/source inputs saved')
