"""Freeze normal ordered selection and complete checkpoint/Continue consumers."""
from pathlib import Path
import hashlib,json,runpy,sys
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'tools/fingerprint_marsh_south_run05_actor.py'))
out=Path(sys.argv[1]);data=json.loads(out.read_text())
for name in ['tests/test_marsh_south_run_production.gd','tests/test_marsh_south_run_production.gd.uid','tools/install_marsh_south_run05.py','tools/prepare_marsh_south_run_normal.py','tools/fingerprint_marsh_south_run_normal.py','scripts/run_save.gd','scripts/title_screen.gd','scenes/title_screen.tscn']:
    data[name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
out.write_text(json.dumps(data,indent=2)+'\n');print(len(data),'bounded normal running inputs')
