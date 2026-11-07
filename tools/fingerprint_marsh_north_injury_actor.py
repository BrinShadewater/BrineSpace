"""Bounded North injury body/effect and actual actor interval."""
from pathlib import Path
import hashlib,json,runpy,sys
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'tools/fingerprint_marsh_north_collapse.py'))
out=Path(sys.argv[1]);records=json.loads(out.read_text())
base=ROOT/'character/marsh-north-injury-material-v1'
paths=[ROOT/p for p in ['tools/prepare_marsh_north_injury_material.py','tools/build_marsh_north_injury_material.py','tools/prepare_marsh_north_injury_fixture.py','tools/review_marsh_north_injury_actor.gd','tools/review_marsh_north_injury_actor.gd.uid','tools/fingerprint_marsh_north_injury_actor.py']]
paths+=list((base/'sources').glob('*'))+list((base/'candidate-01').glob('*'))
for action in ['injury-ground-north','injury-rise-north']:paths+=list((base/'candidate-01'/action).glob('*'))
request=json.loads((base/'sources/reuse-request.json').read_text())
paths+=[ROOT/r['path'] for r in request['bodyGuideFrames']+request['reusedAuthoredEffects']]
for p in paths:
    if p.is_file():records[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
out.write_text(json.dumps(records,indent=2)+'\n');print(len(records),'bounded North injury inputs saved')
