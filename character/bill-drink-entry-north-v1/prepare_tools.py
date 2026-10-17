from pathlib import Path
import re
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OLD=P.parent/'bill-meal-entry-north-v1'
for name in ['build.py','verify.py','build_preview.py']:
 s=re.sub(r'\beat\b','drink',(OLD/name).read_text().replace('bill-meal-north','bill-drink-north').replace('eating','drinking').replace('bowl','cup').replace('Bowl','Cup'))
 (P/name).write_text(s)
s=re.sub(r'\beat\b','drink',(ROOT/'tests/test_bill_meal_entry_north_candidates.gd').read_text().replace('bill-meal','bill-drink').replace('test_bill_meal','test_bill_drink').replace('eating','drinking').replace('BILL MEAL ENTRY NORTH','BILL DRINK ENTRY NORTH'))
(ROOT/'tests/test_bill_drink_entry_north_candidates.gd').write_text(s)
(ROOT/'tests/test_bill_drink_entry_north_candidates.gd.uid').write_text('uid://y7b8w3m6p2r9v\n')
s=(ROOT/'tools/run_bill_meal_entry_north_candidate_validation.py').read_text().replace('bill-meal','bill-drink').replace('test_bill_meal','test_bill_drink').replace('BILL MEAL ENTRY NORTH','BILL DRINK ENTRY NORTH')
(ROOT/'tools/run_bill_drink_entry_north_candidate_validation.py').write_text(s)
