from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OLD=P.parent/'bill-meal-east-coherent-v1'
for name in ['build.py','verify.py','index.html']:
    s=(OLD/name).read_text(encoding='utf-8').replace('eat-east','drink-east').replace('eating','drinking').replace('Eating','Drinking').replace('meal candidate','drink candidate').replace('eat-v1.png','drink-v1.png').replace('meal and','drink and').replace('Meal entry, drink, return','Cup pickup and return').replace('meal draw/stow','cup pickup/return')
    s=s.replace("'waterKinds':['eat']","'waterKinds':['drink']")
    (P/name).write_text(s,encoding='utf-8')
source=ROOT/'tests/test_bill_meal_east_candidates.gd'
s=source.read_text().replace('bill-meal-east-coherent-v1','bill-drink-east-coherent-v1').replace('bill-meal-east-candidate-native-v1','bill-drink-east-candidate-native-v1').replace('eat-east','drink-east').replace('life_eat','life_drink').replace('actor.timer=4','actor.timer=2').replace('=="eat"','=="drink"').replace('frame("eat"','frame("drink"').replace('BILL MEAL EAST','BILL DRINK EAST').replace('meal','drink').replace('eating','drinking')
(ROOT/'tests/test_bill_drink_east_candidates.gd').write_text(s)
s=(ROOT/'tools/run_bill_meal_east_candidate_validation.py').read_text().replace('bill-meal-east-candidate-native-v1','bill-drink-east-candidate-native-v1').replace('test_bill_meal_east_candidates.gd','test_bill_drink_east_candidates.gd').replace('BILL MEAL EAST','BILL DRINK EAST').replace('eating candidate','drinking candidate')
(ROOT/'tools/run_bill_drink_east_candidate_validation.py').write_text(s)
print('Prepared independent drink candidate tools/fixture')
