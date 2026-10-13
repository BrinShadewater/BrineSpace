"""Independent normal eight full-checkpoint East03 regression from passed South."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tests/test_marsh_south_run_production.gd').read_text().replace('south','east').replace('South','East').replace('SOUTH','EAST').replace('candidate-05','candidate-03').replace('exact05','exact03')
stage=(ROOT/'tools/review_marsh_east_run03_actor.gd').read_text();route=stage[stage.index('\tvar route_start :='):stage.index('\tactor.foot=route_start')]
start=source.index('\tvar route_start:=');end=source.index('\tactor=reset_actor',start);source=source[:start]+route+source[end:]
source=source.replace('route_start+Vector2(0,168)','route_start+Vector2(168,0)').replace('actor.foot.y>before.y','actor.foot.x>before.x').replace('normal paid/failure loop','normal economy/failure flags').replace('actual furnished room clears whole damage silhouette','actual furnished room clears actor envelope')
source=source.replace('normal costs/failures. Provisional','normal global cost/failure flags, free authored fixture room. Provisional')
old='\t\tvar expected=Image.load_from_file("res://character/marsh-east-run-material-v1/candidate-03/%03d.png"%slot)'
paths=','.join('"res://character/marsh-east-run-material-v1/candidate-03/%03d.png"'%i for i in range(6));source=source.replace(old,'\t\tvar expected=Image.load_from_file(['+paths+'][slot])');assert old not in source
target=ROOT/'tests/test_marsh_east_run_production.gd';assert not target.exists();target.write_text(source);target.with_suffix('.gd.uid').write_text('uid://ct1ehrunm4v87\n')
install=(ROOT/'tools/install_marsh_south_run05.py').read_text().replace('south','east').replace('South','East').replace('run05','run03').replace('run-south05','run-east03').replace('candidate-05','candidate-03').replace('actor-review-v2','actor-review-v3');(ROOT/'tools/install_marsh_east_run03.py').write_text(install)
fingerprint=(ROOT/'tools/fingerprint_marsh_south_run_normal.py').read_text().replace('south','east').replace('south_run05','east_run03');fingerprint=fingerprint.replace('east_run05','east_run03').replace('install_marsh_east_run05','install_marsh_east_run03');(ROOT/'tools/fingerprint_marsh_east_run_normal.py').write_text(fingerprint)
publisher=(ROOT/'tools/publish_marsh_south_run_normal.py').read_text().replace('south','east').replace('South','East').replace('run05','run03').replace('candidate-05','candidate-03');(ROOT/'tools/publish_marsh_east_run_normal.py').write_text(publisher)
register=(ROOT/'tools/register_marsh_south_run_test.py').read_text().replace('south','east').replace('South','East');(ROOT/'tools/register_marsh_east_run_test.py').write_text(register)
print('Prepared normal East03 factory/full-save/visibleContinue fixture, exact paths, validated horizontal route, installer and publishers.')
