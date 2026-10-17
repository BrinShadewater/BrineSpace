from pathlib import Path
import shutil
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OLD=ROOT/'output/bill-death-ground-station-candidate-v1';archive=OLD/'before-lowered-v1'
if not archive.exists():
 archive.mkdir()
 for f in OLD.iterdir():
  if f.is_file() and f.suffix in ['.png','.json','.log']:shutil.copy2(f,archive/f.name)
 review=P/'revisions/station-join-v1';review.mkdir(parents=True,exist_ok=True)
 for name in ['station-review.json','station-review.html','station-counter-review.png','station-aisle-review.png','station-evidence.json']:shutil.copy2(P/name,review/name)
s=(ROOT/'tests/test_bill_death_ground_station_candidates.gd').read_text(encoding='utf-8')
s=s.replace('for phase in ["before-kneel","entry","terminal"]:', 'var prior_crown:float=grid._get_human_frame_source("kneel",d).get_meta("crew_alpha_extent").position.y\n\t\t\t\tfor phase in ["before-kneel","entry","terminal"]:')
s=s.replace('if phase!="before-kneel":check', 'if phase=="entry":\n\t\t\t\t\t\tcheck(texture.get_meta("crew_alpha_extent").position.y>=prior_crown-.5,"Lowered death entry does not lift kneeling caller")\n\t\t\t\t\t\tcheck(actor.death_entry_seconds>0,"Lowered phase retained")\n\t\t\t\t\tif phase!="before-kneel":check')
s=s.replace('check(texture.get_meta("crew_alpha_extent").position.y>=prior_crown-.5,"Lowered death entry does not lift kneeling caller")','check(is_equal_approx(actor.death_entry_seconds,.55) if d in ["north","south"] else texture.get_meta("crew_alpha_extent").position.y>=prior_crown-.5,"Authored axial kneel or side entry without lift")')
(ROOT/'tests/test_bill_death_ground_station_lowered_candidates.gd').write_text(s,encoding='utf-8');(ROOT/'tests/test_bill_death_ground_station_lowered_candidates.gd.uid').write_text('uid://x8b8w3m6p2r9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_death_ground_station_candidate_validation.py').read_text(encoding='utf-8').replace('test_bill_death_ground_station_candidates.gd','test_bill_death_ground_station_lowered_candidates.gd');(ROOT/'tools/run_bill_death_ground_station_lowered_candidate_validation.py').write_text(s,encoding='utf-8')
s=(ROOT/'tests/test_bill_death_ground_mortality_candidates.gd').read_text(encoding='utf-8').replace('for before in ["idle","walk"]:', 'for before in ["kneel","repair"]:').replace('BILL GROUND MORTALITY CANDIDATE','BILL LOWERED MORTALITY CANDIDATE').replace('bill-death-ground-mortality-candidate-native-v1','bill-death-ground-lowered-mortality-candidate-native-v1')
s=s.replace('Flood.step_crew(game,actor,"bill",.02)', 'game.visual_time_seconds+=1.0\n\t\t\t\t\t\t\tvar prior_crown:float=grid._get_human_frame_source(before,direction).get_meta("crew_alpha_extent").position.y\n\t\t\t\t\t\t\tFlood.step_crew(game,actor,"bill",.02)')
s=s.replace('==row[0],"Actual renderer death entry"', '==player.frame_at_elapsed(key,actor.death_entry_seconds,equipment),"Actual renderer lowered death entry"')
s=s.replace('game.visual_time_seconds=102+offset','game.visual_time_seconds=103+offset')
s=s.replace('check(actor.path.is_empty()', 'check(grid._get_human_frame_source(actor.animation_state(),direction).get_meta("crew_alpha_extent").position.y>=prior_crown-.5,"No lowered caller crown lift")\n\t\t\t\t\t\t\tcheck(actor.path.is_empty()')
s=s.replace('check(grid._get_human_frame_source(actor.animation_state(),direction).get_meta("crew_alpha_extent").position.y>=prior_crown-.5,"No lowered caller crown lift")','check(is_equal_approx(actor.death_entry_seconds,.55) if direction in ["north","south"] else grid._get_human_frame_source(actor.animation_state(),direction).get_meta("crew_alpha_extent").position.y>=prior_crown-.5,"Authored axial kneel entry or side fall without crown lift: "+direction+str(gear)+before)')
s=s.replace('var expected: PackedByteArray=', 'var saved_entry:float=game.bill_npc.death_entry_seconds\n\t\t\t\tvar expected: PackedByteArray=')
s=s.replace('check(game.bill_npc.dead and', 'check(is_equal_approx(game.bill_npc.death_entry_seconds,saved_entry),"Lowered entry phase persists through disk restore")\n\t\t\t\t\tcheck(game.bill_npc.dead and')
(ROOT/'tests/test_bill_death_ground_lowered_mortality_candidates.gd').write_text(s,encoding='utf-8');(ROOT/'tests/test_bill_death_ground_lowered_mortality_candidates.gd.uid').write_text('uid://y8b8w3m6p2r9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_death_ground_mortality_candidate_validation.py').read_text(encoding='utf-8').replace('bill-death-ground-mortality-candidate-native-v1','bill-death-ground-lowered-mortality-candidate-native-v1').replace('test_bill_death_ground_mortality_candidates.gd','test_bill_death_ground_lowered_mortality_candidates.gd').replace('BILL GROUND MORTALITY CANDIDATE','BILL LOWERED MORTALITY CANDIDATE');(ROOT/'tools/run_bill_death_ground_lowered_mortality_candidate_validation.py').write_text(s,encoding='utf-8')
