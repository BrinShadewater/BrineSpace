from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
s=(ROOT/'tools/run_bill_meal_west_candidate_validation.py').read_text(encoding='utf-8').replace('bill-meal-west','bill-death-ground-west').replace('test_bill_meal_west','test_bill_death_ground_west').replace('BILL MEAL WEST','BILL DEATH GROUND WEST')
(ROOT/'tools/run_bill_death_ground_west_candidate_validation.py').write_text(s,encoding='utf-8')
