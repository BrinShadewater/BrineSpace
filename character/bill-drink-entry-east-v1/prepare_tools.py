from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OLD=P.parent/'bill-meal-entry-east-v1'
for name in ['build.py','verify.py','build_preview.py']:
    s=(OLD/name).read_text().replace('bill-meal-east-coherent-v1','bill-drink-east-coherent-v1').replace('eat-east','drink-east').replace('eat-enter','drink-enter').replace('eat-exit','drink-exit').replace('bowl','cup').replace('Bowl','Cup').replace('eating','drinking').replace('meal','drink')
    s=s.replace('pickup, eat and return','pickup, drink and return').replace('cup transitions and normal drink service integration remain pending','normal meal service integration remains pending')
    (P/name).write_text(s)
s=(ROOT/'tests/test_bill_meal_entry_east_candidates.gd').read_text().replace('bill-meal-entry-east-v1','bill-drink-entry-east-v1').replace('bill-meal-entry-east-candidate-native-v1','bill-drink-entry-east-candidate-native-v1').replace('bill-meal-east-coherent-v1','bill-drink-east-coherent-v1').replace('eat-east','drink-east').replace('eat-enter','drink-enter').replace('eat-exit','drink-exit').replace('BILL MEAL ENTRY EAST','BILL DRINK ENTRY EAST').replace('bowl','cup').replace('eating','drinking')
(ROOT/'tests/test_bill_drink_entry_east_candidates.gd').write_text(s)
s=(ROOT/'tools/run_bill_meal_entry_east_candidate_validation.py').read_text().replace('bill-meal-entry-east-candidate-native-v1','bill-drink-entry-east-candidate-native-v1').replace('test_bill_meal_entry_east_candidates.gd','test_bill_drink_entry_east_candidates.gd').replace('BILL MEAL ENTRY EAST','BILL DRINK ENTRY EAST').replace('bowl','cup')
(ROOT/'tools/run_bill_drink_entry_east_candidate_validation.py').write_text(s)
print('Prepared cup finite source/native candidate tools')
