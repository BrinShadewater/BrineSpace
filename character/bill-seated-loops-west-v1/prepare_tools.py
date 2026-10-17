from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
east=P.parent/'bill-seated-loops-east-v1';sources=P/'sources';sources.mkdir(exist_ok=True)
for name in ['breathing','reading']:
    prompt=(east/f'sources/prompt-{name}.txt').read_text().replace('RIGHT/east','LEFT/west').replace('EAST','WEST').replace('east/right','west/left').replace('east;','west;').replace('east/right-facing','west/left-facing').replace('forward/right','forward/left')
    # Never rewrite the exact prompts bound to an existing generation.
    destination=sources/f'prompt-{name}.txt'
    if not destination.exists():destination.write_text(prompt)
for name in ['verify.py']:
    (P/name).write_text((east/name).read_text().replace('east','west'))
test=(ROOT/'tests/test_bill_seated_loops_east_candidates.gd').read_text().replace('east','west')
(ROOT/'tests/test_bill_seated_loops_west_candidates.gd').write_text(test)
(ROOT/'tests/test_bill_seated_loops_west_candidates.gd.uid').write_text('uid://y6b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_seated_loops_east_candidate_validation.py').read_text().replace('east','west')
(ROOT/'tools/run_bill_seated_loops_west_candidate_validation.py').write_text(runner)
preview=(P.parent/'bill-seated-loops-south-v1/build_review.py').read_text().replace('south','west').replace('native rear helmet','native selected west helmet').replace('real observation sofa contact and tablet entry/exit review pending','real furniture contact, tablet entry/exit and runtime selection pending')
(P/'build_review.py').write_text(preview)
print('Prepared west loop prompts and candidate tools;source rulers pending inspection')
