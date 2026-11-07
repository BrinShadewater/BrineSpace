"""Freeze actor/playback inputs in addition to staged collapse source provenance."""
from pathlib import Path
import hashlib,json,runpy,sys
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'tools/fingerprint_marsh_south_collapse.py'))
out=Path(sys.argv[1]);records=json.loads(out.read_text())
for path in ['tools/review_marsh_south_collapse_actor.gd','tools/review_marsh_south_collapse_actor.gd.uid','tools/fingerprint_marsh_south_collapse_actor.py','scripts/main.gd','scripts/marsh_npc.gd','scripts/marsh_south_snapshot.gd','scripts/marsh_ground_motion.gd','scripts/marsh_west_motion.gd','scripts/bill_npc.gd','scripts/loading_transition.gd','scripts/title_settings.gd','scripts/room_layout_store.gd','scenes/main.tscn','rooms/whole-room/nursery_whole_view.gd']:
    records[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
out.write_text(json.dumps(records,indent=2)+'\n');print(len(records),'bounded collapse actor/source inputs saved')
