from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'tests/test_bill_meal_east_family_candidates.gd'
s=p.read_text().replace(';player.load_manifest(PACK,true)','').replace('m.status=="staged_candidate"','m.status=="selected_runtime"').replace('BILL MEAL EAST FAMILY','BILL MEAL EAST SELECTED').replace('bill-meal-east-family-candidate-native-v1','bill-meal-east-family-selected-native-v1')
assert 'load_manifest(PACK' not in s
(ROOT/'tests/test_bill_meal_east_family_selected.gd').write_text(s)
p=ROOT/'tools/run_bill_meal_east_family_candidate_validation.py'
s=p.read_text().replace('bill-meal-east-family-candidate-native-v1','bill-meal-east-family-selected-native-v1').replace('test_bill_meal_east_family_candidates.gd','test_bill_meal_east_family_selected.gd').replace('BILL MEAL EAST FAMILY','BILL MEAL EAST SELECTED')
(ROOT/'tools/run_bill_meal_east_family_selected_validation.py').write_text(s)
print('Prepared normal loader fixture; no candidate injection')
