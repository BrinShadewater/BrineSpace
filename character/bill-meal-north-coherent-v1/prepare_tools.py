from pathlib import Path
p=Path(__file__).parent
east=p.parent/'bill-meal-east-coherent-v1'
text=(east/'build.py').read_text().replace("'east_grade'","'north_grade'").replace("bill-seated-east-coherent-v1/grade.py","bill-seated-north-coherent-v1/build.py").replace('eat-east','eat-north').replace("['east']","['north']").replace('Bill east','Bill north').replace('Built east','Built north')
(p/'build.py').write_text(text)
(p/'verify.py').write_text((east/'verify.py').read_text())
(p/'index.html').write_text((east/'index.html').read_text().replace('east','north').replace('Meal entry, drink, return and runtime installation remain pending.','Bowl pickup/return, drinking and normal service phase installation remain pending. Rear props remain naturally occluded.'))
root=p.parent.parent
s=(root/'tests/test_bill_meal_east_candidates.gd').read_text().replace('bill-meal-east','bill-meal-north').replace('eat-east','eat-north').replace('"east"','"north"').replace('bill-seated-east','bill-seated-north').replace('sit-down-east','sit-down-north').replace('BILL MEAL EAST','BILL MEAL NORTH')
(root/'tests/test_bill_meal_north_candidates.gd').write_text(s)
(root/'tests/test_bill_meal_north_candidates.gd.uid').write_text('uid://v7b8w3m6p2r9v\n')
s=(root/'tools/run_bill_meal_east_candidate_validation.py').read_text().replace('bill-meal-east','bill-meal-north').replace('test_bill_meal_east','test_bill_meal_north').replace('BILL MEAL EAST','BILL MEAL NORTH')
(root/'tools/run_bill_meal_north_candidate_validation.py').write_text(s)
