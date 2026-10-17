from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
test=(ROOT/'tests/test_bill_seated_loops_south_candidates.gd').read_text().replace('south','east')
test=test.replace('check(actor.valid_snapshot(actor.snapshot()),"Actual actor snapshot validity")','check(not actor.valid_snapshot(actor.snapshot()) if state.id=="read-seated-east" else actor.valid_snapshot(actor.snapshot()),"Current east reading snapshot restriction;seated snapshot valid")')
(ROOT/'tests/test_bill_seated_loops_east_candidates.gd').write_text(test)
(ROOT/'tests/test_bill_seated_loops_east_candidates.gd.uid').write_text('uid://u6b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_seated_loops_south_candidate_validation.py').read_text().replace('south','east')
(ROOT/'tools/run_bill_seated_loops_east_candidate_validation.py').write_text(runner)
verifier=(P.parent/'bill-seated-loops-south-v1/verify.py').read_text().replace('south','east').replace('abs(int(y.max())-222)<=1','int(y.max())==223')
(P/'verify.py').write_text(verifier)
print('Prepared candidate loop fixture;east read snapshot restriction remains explicit')
