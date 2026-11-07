"""Extend the bounded South input inventory for the priority study."""
from pathlib import Path
import hashlib,json,runpy,sys
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'tools/fingerprint_marsh_south_step_inputs.py'))
out=Path(sys.argv[1]);records=json.loads(out.read_text())
for path in ['tools/review_marsh_south_step_priorities.gd','tools/review_marsh_south_step_priorities.gd.uid','tools/fingerprint_marsh_south_step_priorities.py','scripts/room_flooding.gd','scripts/fire_safety.gd','scripts/flood_safety.gd']:
    records[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
out.write_text(json.dumps(records,indent=2)+'\n');print(len(records),'priority study inputs saved')
