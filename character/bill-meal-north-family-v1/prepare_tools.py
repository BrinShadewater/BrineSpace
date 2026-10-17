from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;E=P.parent/'bill-meal-east-family-v1'
s=(E/'build.py').read_text(encoding='utf-8').replace('east','north').replace("'status':'selected_runtime'","'status':'staged_candidate'")
s=s.replace('North art normally selected. Current galley approaches face north or south; activity transitions, counter contact and restore checks remain pending.','Staged north family. Actual service phases, counter contact and restore checks remain pending.')
# Source text has lowercase direction at the start of this preview caption.
s=s.replace('North art normally selected.','Staged north family.').replace('East art normally selected.','Staged north family.')
s=s.replace(".replace('DATA',json.dumps(preview)))",".replace('DATA',json.dumps(preview)),encoding='utf-8')")
(P/'build.py').write_text(s,encoding='utf-8')
s=(ROOT/'tests/test_bill_meal_east_family_candidates.gd').read_text().replace('east','north').replace('BILL MEAL EAST FAMILY','BILL MEAL NORTH FAMILY')
(ROOT/'tests/test_bill_meal_north_family_candidates.gd').write_text(s)
(ROOT/'tests/test_bill_meal_north_family_candidates.gd.uid').write_text('uid://z7b8w3m6p2r9v\n')
s=(ROOT/'tools/run_bill_meal_east_family_candidate_validation.py').read_text().replace('east','north').replace('BILL MEAL EAST FAMILY','BILL MEAL NORTH FAMILY')
(ROOT/'tools/run_bill_meal_north_family_candidate_validation.py').write_text(s)
