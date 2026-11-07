"""Independent normal North factory/full-save/visible Continue validation."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tests/test_marsh_south_run_production.gd').read_text().replace('south','north').replace('South','North').replace('SOUTH','NORTH').replace('candidate-05','candidate-03').replace('exact05','exact03')
stage=(ROOT/'tools/review_marsh_north_run03_actor.gd').read_text()
route=stage[stage.index('\tvar route_start :='):stage.index('\tactor.foot=route_start')]
start=source.index('\tvar route_start:=');end=source.index('\tactor=reset_actor',start)
source=source[:start]+route+source[end:]
source=source.replace('route_start+Vector2(0,168)','route_start+Vector2(0,-168)').replace('actor.foot.y>before.y','actor.foot.y<before.y')
old='Image.load_from_file("res://character/marsh-north-run-material-v1/candidate-03/%03d.png"%slot)'
paths='["res://character/marsh-north-run-material-v1/candidate-03/000.png","res://character/marsh-north-run-material-v1/candidate-03/001.png","res://character/marsh-north-run-material-v1/candidate-03/002.png","res://character/marsh-north-run-material-v1/candidate-03/003.png","res://character/marsh-north-run-material-v1/candidate-03/004.png","res://character/marsh-north-run-material-v1/candidate-03/005.png"][slot]'
assert old in source;source=source.replace(old,'Image.load_from_file('+paths+')')
p=ROOT/'tests/test_marsh_north_run_production.gd';assert not p.exists();p.write_text(source);p.with_suffix('.gd.uid').write_text('uid://cy6nhrunm9v92\n')
install=(ROOT/'tools/install_marsh_west_run02.py').read_text().replace('west','north').replace('West','North').replace('run02','run03').replace('candidate-02','candidate-03').replace('actor-review-v1','actor-review-v2')
(ROOT/'tools/install_marsh_north_run03.py').write_text(install)
fingerprint=(ROOT/'tools/fingerprint_marsh_west_run_normal.py').read_text().replace('west','north').replace('run02','run03')
(ROOT/'tools/fingerprint_marsh_north_run_normal.py').write_text(fingerprint)
publisher=(ROOT/'tools/publish_marsh_west_run_normal.py').read_text().replace('marsh-west-run-material-v1','marsh-north-run-material-v1').replace('west-run-normal-native-v1','north-run-normal-native-v1').replace('run-west','run-north').replace('candidate-02','candidate-03').replace('West','North').replace('run02','run03').replace('shared planted sole plane','shared whole-frame anchor')
(ROOT/'tools/publish_marsh_north_run_normal.py').write_text(publisher)
register=(ROOT/'tools/register_marsh_west_run_test.py').read_text().replace('west','north').replace('West','North')
(ROOT/'tools/register_marsh_north_run_test.py').write_text(register)
print('Prepared independent North03 normal eight full saves/visible Continues; six whole quoted source paths and paired UID.')
