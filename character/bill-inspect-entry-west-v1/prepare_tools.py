from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;E=P.parent/'bill-inspect-entry-east-v1'
for name in ['build.py','verify.py','build_review.py']:
    text=(E/name).read_text().replace('east','west')
    if name=='build.py':text=text.replace('(x>np.median(x))','(x<np.median(x))').replace('(bx>np.median(bx))','(bx<np.median(bx))').replace('(hx-19,hy-4)','(hx-20,hy-4)')
    if not (P/name).exists():(P/name).write_text(text)
test=(ROOT/'tests/test_bill_inspect_entry_east_candidates.gd').read_text().replace('east','west').replace('EAST','WEST')
(ROOT/'tests/test_bill_inspect_entry_west_candidates.gd').write_text(test)
(ROOT/'tests/test_bill_inspect_entry_west_candidates.gd.uid').write_text('uid://h7b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_inspect_entry_east_candidate_validation.py').read_text().replace('east','west').replace('EAST','WEST')
(ROOT/'tools/run_bill_inspect_entry_west_candidate_validation.py').write_text(runner)
print('Prepared independent west draw/stow builder and source-player join fixture')
