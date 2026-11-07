"""Retain the validated physical North route for the one-pose revision."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'tools/review_marsh_north_run03_actor.gd';assert not p.exists()
p.write_text((ROOT/'tools/review_marsh_north_run02_actor.gd').read_text().replace('north-run-actor-02','north-run-actor-03').replace('candidate-02','candidate-03'))
p.with_suffix('.gd.uid').write_text('uid://cx5nhrunm8v91\n')
(ROOT/'tools/publish_marsh_north_run03_actor.py').write_text((ROOT/'tools/publish_marsh_north_run02_actor.py').read_text().replace('north-run-actor-02','north-run-actor-03').replace('candidate-02','candidate-03').replace('actor-review-v1','actor-review-v2'))
source=(ROOT/'tools/fingerprint_marsh_north_run02_actor.py').read_text().replace('review_marsh_north_run02_actor','review_marsh_north_run03_actor').replace('prepare_marsh_north_run02_native','prepare_marsh_north_run03_native').replace('fingerprint_marsh_north_run02_actor','fingerprint_marsh_north_run03_actor').replace('publish_marsh_north_run02_actor','publish_marsh_north_run03_actor')
source=source.replace("'rebuild_bill_art.py']","'rebuild_bill_art.py','prepare_marsh_north_passing04.py','build_marsh_north_passing04.py','build_marsh_north_passing03.py','assemble_marsh_north_run03.py','review_marsh_north_run02_actor.gd','prepare_marsh_north_run02_native.py']")
source=source.replace("'passing-03-unselected']","'passing-03-unselected','passing-04-unselected','candidate-03']")
(ROOT/'tools/fingerprint_marsh_north_run03_actor.py').write_text(source)
print('Prepared North03 actual actor fixture, paired UID, publisher and bounded source/dependency freeze.')
