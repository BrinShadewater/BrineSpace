from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OLD=P.parent/'bill-drink-entry-east-v1'
for name in ['build.py','verify.py','build_preview.py']:
 s=(OLD/name).read_text().replace('east','north').replace('bill-seated-north-coherent-v1/grade.py','bill-seated-north-coherent-v1/build.py').replace('bill-drink-north-coherent-v1','bill-meal-north-coherent-v1').replace('drink','eat').replace('cup','bowl').replace('Cup','Bowl').replace('drinking','eating')
 (P/name).write_text(s)
s=(ROOT/'tests/test_bill_drink_entry_east_candidates.gd').read_text().replace('east','north').replace('bill-drink-north-coherent-v1','bill-meal-north-coherent-v1').replace('bill-drink-entry-north-v1','bill-meal-entry-north-v1').replace('bill-drink-entry-north-candidate','bill-meal-entry-north-candidate').replace('drink','eat').replace('BILL DRINK ENTRY EAST','BILL MEAL ENTRY NORTH')
(ROOT/'tests/test_bill_meal_entry_north_candidates.gd').write_text(s)
(ROOT/'tests/test_bill_meal_entry_north_candidates.gd.uid').write_text('uid://x7b8w3m6p2r9v\n')
s=(ROOT/'tools/run_bill_drink_entry_east_candidate_validation.py').read_text().replace('east','north').replace('drink','meal').replace('BILL DRINK ENTRY EAST','BILL MEAL ENTRY NORTH')
(ROOT/'tools/run_bill_meal_entry_north_candidate_validation.py').write_text(s)
