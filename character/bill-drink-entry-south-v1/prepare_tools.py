from pathlib import Path
import re
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OLD=P.parent/'bill-meal-entry-south-v1'
for name in ['build.py','verify.py','build_preview.py','grade_shoulders.py']:
 s=(OLD/name).read_text(encoding='utf-8').replace('bill-meal-south','bill-drink-south').replace('eating','drinking').replace('bowl','cup').replace('Bowl','Cup')
 s=re.sub(r'\beat\b','drink',s)
 (P/name).write_text(s,encoding='utf-8')
s=(ROOT/'tests/test_bill_meal_entry_south_candidates.gd').read_text().replace('bill-meal','bill-drink').replace('eating','drinking').replace('BILL MEAL ENTRY SOUTH','BILL DRINK ENTRY SOUTH')
s=re.sub(r'\beat\b','drink',s)
(ROOT/'tests/test_bill_drink_entry_south_candidates.gd').write_text(s)
(ROOT/'tests/test_bill_drink_entry_south_candidates.gd.uid').write_text('uid://d8b8w3m6p2r9v\n')
s=(ROOT/'tools/run_bill_meal_entry_south_candidate_validation.py').read_text().replace('bill-meal','bill-drink').replace('test_bill_meal','test_bill_drink').replace('BILL MEAL ENTRY SOUTH','BILL DRINK ENTRY SOUTH')
(ROOT/'tools/run_bill_drink_entry_south_candidate_validation.py').write_text(s)
