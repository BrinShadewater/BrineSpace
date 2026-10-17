from pathlib import Path
import re
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OLD=P.parent/'bill-drink-north-coherent-v1'
for name in ['build.py','verify.py','index.html']:
 s=(OLD/name).read_text(encoding='utf-8').replace('bill-drink-north','bill-meal-south').replace('north','south').replace('bill-seated-south-coherent-v1/build.py','bill-seated-loops-south-v1/build.py').replace("cfg['heads'],6,cfg['density']","cfg['heads'],cfg['density']").replace('drinking','eating').replace('Drinking','Eating').replace('drink-v1','eat-v1')
 s=re.sub(r'\bdrink\b','eat',s)
 s=s.replace('Cup pickup/return','Bowl pickup/return').replace('Cup remains naturally occluded in front from this rear camera.','Front bowl support and spoon grip remain visible throughout.').replace('drink candidate','meal candidate')
 (P/name).write_text(s,encoding='utf-8')
s=(ROOT/'tests/test_bill_drink_north_candidates.gd').read_text().replace('bill-drink','bill-meal').replace('north','south').replace('life_drink','life_eat').replace('drinking','eating').replace('BILL DRINK NORTH','BILL MEAL SOUTH')
s=re.sub(r'\bdrink\b','eat',s)
(ROOT/'tests/test_bill_meal_south_candidates.gd').write_text(s)
(ROOT/'tests/test_bill_meal_south_candidates.gd.uid').write_text('uid://a8b8w3m6p2r9v\n')
s=(ROOT/'tools/run_bill_drink_north_candidate_validation.py').read_text().replace('bill-drink','bill-meal').replace('test_bill_drink','test_bill_meal').replace('north','south').replace('BILL DRINK NORTH','BILL MEAL SOUTH')
(ROOT/'tools/run_bill_meal_south_candidate_validation.py').write_text(s)
