from pathlib import Path
import hashlib,json,runpy,sys
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'tools/fingerprint_marsh_south_step_priorities.py'))
out=Path(sys.argv[1]);records=json.loads(out.read_text())
for path in ['tools/review_marsh_south_step_traffic.gd','tools/review_marsh_south_step_traffic.gd.uid','tools/fingerprint_marsh_south_step_traffic.py']:
    records[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
out.write_text(json.dumps(records,indent=2)+'\n');print(len(records),'live coordinator study inputs saved')
