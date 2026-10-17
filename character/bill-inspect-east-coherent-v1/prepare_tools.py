from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
test=(ROOT/'tests/test_bill_seated_loops_east_candidates.gd').read_text().replace('bill-seated-loops-east-v1','bill-inspect-east-coherent-v1').replace('bill-seated-loops-east-candidate-native-v1','bill-inspect-east-candidate-native-v1')
test=test.replace('actor.stage="observation_read" if state.id=="read-seated-east" else "life_seated"','actor.stage="life_inspect"')
test=test.replace('row[i].get_meta("crew_depth_offset")==40.0','row[i].get_meta("crew_depth_offset")==0.0')
test=test.replace('check(not actor.valid_snapshot(actor.snapshot()) if state.id=="read-seated-east" else actor.valid_snapshot(actor.snapshot()),"Current east reading snapshot restriction;seated snapshot valid")','check(actor.valid_snapshot(actor.snapshot()),"Inspection stage snapshot valid")')
test=test.replace('BILL SEATED LOOPS','BILL INSPECT EAST')
test=test.replace('check(actor.valid_snapshot(actor.snapshot()),"Inspection stage snapshot valid")','check(row[0].get_image().get_data()==row[-1].get_image().get_data(),"Exact inspection loop closure")\n\t\t\tcheck(actor.valid_snapshot(actor.snapshot()),"Inspection stage snapshot valid")')
(ROOT/'tests/test_bill_inspect_east_candidates.gd').write_text(test)
(ROOT/'tests/test_bill_inspect_east_candidates.gd.uid').write_text('uid://c7b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_seated_loops_east_candidate_validation.py').read_text().replace('bill-seated-loops-east-candidate-native-v1','bill-inspect-east-candidate-native-v1').replace('test_bill_seated_loops_east_candidates','test_bill_inspect_east_candidates').replace('BILL SEATED','BILL INSPECT EAST')
(ROOT/'tools/run_bill_inspect_east_candidate_validation.py').write_text(runner)
print('Prepared east inspection source/player fixture;no runtime changes')
