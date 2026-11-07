from pathlib import Path
import hashlib,json,runpy,sys
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'tools/fingerprint_marsh_south_step_inputs.py'))
out=Path(sys.argv[1]);records=json.loads(out.read_text())
for path in ['tests/test_marsh_south_step_production.gd','tests/test_marsh_south_step_production.gd.uid','tools/fingerprint_marsh_south_step_normal.py','tests/index.json','tests/test_marsh_north_step_controller.gd','tests/test_marsh_south_start_controller.gd','tests/test_marsh_south_stop_controller.gd','tests/test_marsh_south_snapshots.gd']:
    records[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
out.write_text(json.dumps(records,indent=2)+'\n');print(len(records),'normal South step inputs saved')
