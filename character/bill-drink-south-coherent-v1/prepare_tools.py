from pathlib import Path
import re
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OLD=P.parent/'bill-meal-south-coherent-v1'
for name in ['build.py','verify.py','index.html','compare_master.py']:
 s=(OLD/name).read_text(encoding='utf-8').replace('bill-meal-south','bill-drink-south').replace('eating','drinking').replace('Eating','Drinking').replace('meal candidate','drink candidate').replace('eat-v1','drink-badge-v2')
 s=re.sub(r'\beat\b','drink',s).replace('Bowl pickup/return','Cup pickup/return').replace('Front bowl support and spoon grip remain visible throughout.','One right cup hand and relaxed left arm; corrected steel chest badge throughout.')
 (P/name).write_text(s,encoding='utf-8')
s=(ROOT/'tests/test_bill_meal_south_candidates.gd').read_text().replace('bill-meal','bill-drink').replace('life_eat','life_drink').replace('eating','drinking').replace('BILL MEAL SOUTH','BILL DRINK SOUTH')
s=re.sub(r'\beat\b','drink',s)
(ROOT/'tests/test_bill_drink_south_candidates.gd').write_text(s)
(ROOT/'tests/test_bill_drink_south_candidates.gd.uid').write_text('uid://b8b8w3m6p2r9v\n')
s=(ROOT/'tools/run_bill_meal_south_candidate_validation.py').read_text().replace('bill-meal','bill-drink').replace('test_bill_meal','test_bill_drink').replace('BILL MEAL SOUTH','BILL DRINK SOUTH')
(ROOT/'tools/run_bill_drink_south_candidate_validation.py').write_text(s)
