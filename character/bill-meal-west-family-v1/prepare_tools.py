from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;N=P.parent/'bill-meal-north-family-v1'
s=(N/'build.py').read_text(encoding='utf-8').replace('north','west').replace('Bill north','Bill west')
s=s.replace('Current galley approaches face west or south;','Current galley approaches face north or south; west is an authored directional candidate;')
(P/'build.py').write_text(s,encoding='utf-8')
s=(ROOT/'tests/test_bill_meal_north_family_candidates.gd').read_text(encoding='utf-8').replace('north','west').replace('BILL MEAL NORTH FAMILY','BILL MEAL WEST FAMILY')
s=s.replace('func run():','func run():\n\tprint("BILL MEAL WEST FAMILY profile: "+OS.get_user_data_dir())')
(ROOT/'tests/test_bill_meal_west_family_candidates.gd').write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_meal_west_family_candidates.gd.uid').write_text('uid://k8b8w3m6p2r9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_meal_north_family_candidate_validation.py').read_text(encoding='utf-8').replace('north','west').replace('BILL MEAL NORTH FAMILY','BILL MEAL WEST FAMILY')
(ROOT/'tools/run_bill_meal_west_family_candidate_validation.py').write_text(s,encoding='utf-8')
