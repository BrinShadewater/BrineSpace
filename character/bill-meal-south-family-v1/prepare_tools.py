from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OLD=P.parent/'bill-meal-north-family-v1'
(P/'build.py').write_text((OLD/'build.py').read_text(encoding='utf-8').replace('north','south'),encoding='utf-8')
s=(ROOT/'tests/test_bill_meal_north_family_candidates.gd').read_text().replace('north','south').replace('BILL MEAL NORTH FAMILY','BILL MEAL SOUTH FAMILY')
(ROOT/'tests/test_bill_meal_south_family_candidates.gd').write_text(s)
(ROOT/'tests/test_bill_meal_south_family_candidates.gd.uid').write_text('uid://e8b8w3m6p2r9v\n')
s=(ROOT/'tools/run_bill_meal_north_family_candidate_validation.py').read_text().replace('north','south').replace('BILL MEAL NORTH FAMILY','BILL MEAL SOUTH FAMILY')
(ROOT/'tools/run_bill_meal_south_family_candidate_validation.py').write_text(s)
