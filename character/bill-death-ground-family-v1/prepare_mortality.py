from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
s=(ROOT/'tests/test_bill_death_water_family_selected.gd').read_text(encoding='utf-8').replace('Normal loader, real survival trigger','Explicit candidate injection, real survival trigger').replace('bill-death-water-family-v1/bare-manifest.json','bill-death-ground-family-v1/manifest.json').replace('bill-death-water-family-v1/helmet-manifest.json','bill-death-ground-family-v1/helmet-manifest.json').replace('death-water','death-ground').replace('bill-death-water-family-selected-native-v1','bill-death-ground-mortality-candidate-native-v1').replace('BILL DEATH SELECTED','BILL GROUND MORTALITY CANDIDATE')
s=s.replace('game.occupied[home].water_level=1.0','game.occupied[home].water_level=0.0').replace('for medium in ["flooded","exterior"]:','for medium in ["dry"]:').replace('actor.foot=center if medium=="flooded" else Vector2(192,192)','actor.foot=center').replace('game.resources.oxygen=100','game.resources.oxygen=0 if cause=="air" else 100').replace('"tread" if before=="idle" else "swim"','before').replace('Vector2(128,128)*82/148','Vector2(128,224)*82/148').replace('Normal loader pixels','Candidate renderer source pixels').replace('Selected coverage','Candidate coverage')
injection='''
\tplayer.load_manifest(PACKS.bare,true)
\tcheck(player.load_equipment_manifest("diving-helmet",PACKS.helmet),"Candidate gear compatibility")
\tif failures:quit(2);return
\t# Exercise the existing production dictionary route with explicit candidate rows.
\t# This fixture does not change normal artwork selection.
\tgrid.human_animations["death-ground"]={}
\tfor facing in ["east","west","north","south"]:
\t\tvar candidate_key: String="death-ground-"+facing
\t\tgrid.human_animations["death-ground"][facing]=player.frames[candidate_key]
\t\tgrid.human_animation_timing[candidate_key]=player.timing[candidate_key]
\tgrid.human_equipment_frames=player.equipment_frames
'''
s=s.replace('var home: Vector2i=',injection+'\tvar home: Vector2i=')
s=s.replace('bill-death-ground-family-selected-native-v1','bill-death-ground-mortality-candidate-native-v1')
s=s.replace('func run() -> void:', 'func run() -> void:\n\tprint("BILL GROUND MORTALITY CANDIDATE profile: "+OS.get_user_data_dir())')
(ROOT/'tests/test_bill_death_ground_mortality_candidates.gd').write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_death_ground_mortality_candidates.gd.uid').write_text('uid://u8b8w3m6p2r9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_death_ground_family_candidate_validation.py').read_text(encoding='utf-8').replace('bill-death-ground-family-candidate-native-v1','bill-death-ground-mortality-candidate-native-v1').replace('test_bill_death_ground_family_candidates.gd','test_bill_death_ground_mortality_candidates.gd').replace('BILL DEATH GROUND FAMILY','BILL GROUND MORTALITY CANDIDATE')
(ROOT/'tools/run_bill_death_ground_mortality_candidate_validation.py').write_text(s,encoding='utf-8')
