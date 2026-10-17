from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent.parent
test=(ROOT/'tests/test_bill_reading_entry_south_candidates.gd').read_text()
test=test.replace('bill-reading-entry-south','bill-reading-north').replace('BILL READING ENTRY','BILL READING NORTH')
test=test.replace('is_equal_approx(elapsed,.48)','is_equal_approx(elapsed,.96)').replace('Finite480ms endpoint hold','Finite source API endpoint hold')
test=test.replace('var reviews:=[]','var reviews:=[]')
(ROOT/'tests/test_bill_reading_north_candidates.gd').write_text(test)
(ROOT/'tests/test_bill_reading_north_candidates.gd.uid').write_text('uid://n6b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_reading_entry_south_candidate_validation.py').read_text()
runner=runner.replace('bill-reading-entry-south','bill-reading-north').replace('bill_reading_entry_south','bill_reading_north').replace('BILL READING ENTRY','BILL READING NORTH')
(ROOT/'tools/run_bill_reading_north_candidate_validation.py').write_text(runner)
print('Prepared isolated north reading native fixture; no runtime selection')
