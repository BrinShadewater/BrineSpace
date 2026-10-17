from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;E=P.parent/'bill-inspect-entry-east-v1'
for name in ['build.py','verify.py','build_review.py']:
    text=(E/name).read_text().replace('east','north')
    if name=='build.py':text=text.replace("B/'grade.py'","B/'build.py'").replace('(hx-19,hy-4)','(hx-17,hy-6)')
    if name=='build_review.py':text=text.replace('Draw the reader, inspect, stow.','Draw the reader in front of the body, inspect, stow. Rear view naturally occludes the reader and gloves during the held pose.')
    if not (P/name).exists():(P/name).write_text(text)
test=(ROOT/'tests/test_bill_inspect_entry_east_candidates.gd').read_text().replace('east','north').replace('EAST','NORTH')
(ROOT/'tests/test_bill_inspect_entry_north_candidates.gd').write_text(test)
(ROOT/'tests/test_bill_inspect_entry_north_candidates.gd.uid').write_text('uid://i7b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_inspect_entry_east_candidate_validation.py').read_text().replace('east','north').replace('EAST','NORTH')
(ROOT/'tools/run_bill_inspect_entry_north_candidate_validation.py').write_text(runner)
print('Prepared rear grade/native helmet and finite draw/stow source-player fixture')
