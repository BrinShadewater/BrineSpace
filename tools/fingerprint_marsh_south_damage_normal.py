"""Freeze normal damage full-save/Continue code and selected family inputs."""
from pathlib import Path
import hashlib,json,runpy,sys
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'tools/fingerprint_marsh_south_injury_actor.py'))
out=Path(sys.argv[1]);records=json.loads(out.read_text())
for path in ['tests/test_marsh_south_damage_production.gd','tests/test_marsh_south_damage_production.gd.uid','tools/install_marsh_south_damage_material.py','tools/fingerprint_marsh_south_damage_normal.py','tools/prepare_marsh_south_damage_normal_fixture.py','scripts/run_save.gd','scripts/title_screen.gd','scenes/title_screen.tscn']:
    records[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
out.write_text(json.dumps(records,indent=2)+'\n');print(len(records),'bounded normal damage inputs saved')
