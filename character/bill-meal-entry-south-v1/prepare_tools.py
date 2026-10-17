from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OLD=P.parent/'bill-meal-entry-north-v1'
for name in ['build.py','verify.py','build_preview.py']:
 s=(OLD/name).read_text(encoding='utf-8').replace('north','south').replace('bill-seated-south-coherent-v1/build.py','bill-seated-loops-south-v1/build.py').replace("s['heads'],s['count'],s['density']","s['heads'],s['density']")
 if name=='build.py':s=s.replace('\ndonors=',"\nfrom grade_shoulders import apply\napply(prepared,cfg,module.IDLE)\n\ndonors=")
 if name=='build_preview.py':s=s.replace(".replace('DATA',json.dumps(states)))",".replace('DATA',json.dumps(states)),encoding='utf-8')")
 (P/name).write_text(s,encoding='utf-8')
s=(ROOT/'tests/test_bill_meal_entry_north_candidates.gd').read_text().replace('north','south').replace('BILL MEAL ENTRY NORTH','BILL MEAL ENTRY SOUTH')
(ROOT/'tests/test_bill_meal_entry_south_candidates.gd').write_text(s)
(ROOT/'tests/test_bill_meal_entry_south_candidates.gd.uid').write_text('uid://c8b8w3m6p2r9v\n')
s=(ROOT/'tools/run_bill_meal_entry_north_candidate_validation.py').read_text().replace('north','south').replace('BILL MEAL ENTRY NORTH','BILL MEAL ENTRY SOUTH')
(ROOT/'tools/run_bill_meal_entry_south_candidate_validation.py').write_text(s)
