"""Prepare fresh staged evidence for revised whole passing and sole registration."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/review_marsh_south_run_actor.gd').read_text().replace('south-run-actor-04-v2-2026-10-02','south-run-actor-05-2026-10-02').replace('marsh-south-run-material-v1/candidate-04','marsh-south-run-material-v1/candidate-05').replace('submillimetre world-coordinate precision','0.001world-unit coordinate precision')
needle='\tcheck(is_equal_approx(player.cycle_seconds("run-south"),.6),"six100ms cycle retained")'
source=source.replace(needle,needle+'''\n	for slot in range(6):
		var used:Rect2i=player.frames["run-south"][slot].get_image().get_used_rect()
		check(used.end.y==172 if slot in [0,1,3,4] else used.end.y<172,"planted sole plane or airborne clearance in actual loaded texture")''')
target=ROOT/'tools/review_marsh_south_run05_actor.gd';assert not target.exists();target.write_text(source,encoding='utf-8');target.with_suffix('.gd.uid').write_text('uid://cn4shrnm9v81\n')
fingerprint=(ROOT/'tools/fingerprint_marsh_south_run_actor.py').read_text().replace('tools/review_marsh_south_run_actor.gd','tools/review_marsh_south_run05_actor.gd').replace('tools/fingerprint_marsh_south_run_actor.py','tools/fingerprint_marsh_south_run05_actor.py').replace("'candidate-04','passing-05-unselected','passing-06-unselected'","'candidate-04','candidate-05','passing-05-unselected','passing-06-unselected','passing-07-unselected','passing-08-unselected'")
fingerprint=fingerprint.replace("'tools/assemble_marsh_south_run04.py'","'tools/assemble_marsh_south_run04.py','tools/build_marsh_south_run05.py','tools/build_marsh_south_run_passing08.py'")
(ROOT/'tools/fingerprint_marsh_south_run05_actor.py').write_text(fingerprint,encoding='utf-8')
publisher=(ROOT/'tools/publish_marsh_south_run_actor.py').read_text().replace('south-run-actor-04-v2-2026-10-02','south-run-actor-05-2026-10-02').replace('candidate-04/','candidate-05/').replace("'actor-review-v1'","'actor-review-v2'")
(ROOT/'tools/publish_marsh_south_run05_actor.py').write_text(publisher,encoding='utf-8')
print('Prepared separate05 native fixture/UID, frozen-input helper and publisher.')
