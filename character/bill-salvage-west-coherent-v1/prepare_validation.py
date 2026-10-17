from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent.parent
for src,dst in [('tests/test_bill_salvage_east_candidates.gd','tests/test_bill_salvage_west_candidates.gd'),('tools/run_bill_salvage_east_candidate_validation.py','tools/run_bill_salvage_west_candidate_validation.py')]:
 s=(ROOT/src).read_text(encoding='utf-8').replace('east','west')
 (ROOT/dst).write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_salvage_west_candidates.gd.uid').write_text('uid://h6m3r9s2b8w4v\n',encoding='utf-8')
