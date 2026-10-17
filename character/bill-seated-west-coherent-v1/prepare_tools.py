from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
east=P.parent/'bill-seated-east-coherent-v1'
grade=(east/'grade.py').read_text().replace('idle-east','idle-west')
grade=grade.replace('(xx>hx)&(xx<hx+45*density)','(xx<hx)&(xx>hx-45*density)').replace('(xx>hx-90*density)&(xx<hx-5*density)','(xx>hx+5*density)&(xx<hx+90*density)').replace('(rx>92)','(rx<92)')
(P/'grade.py').write_text(grade)
H=P.parent/'bill-seated-helmet-west-coherent-v1';H.mkdir(exist_ok=True)
helmet=(P.parent/'bill-recover-air-helmet-west-coherent-v1/build.py').read_text().replace('bill-recover-air-west-coherent-v1','bill-seated-west-coherent-v1').replace("record['sourcePose']","record['frame']").replace('if i in [0,5]:','if i==0:').replace('Bill west helmet air recovery candidate','Bill west helmet sitting candidate').replace('exact equipped idle endpoints','exact equipped standing endpoint;original body preserved')
(H/'build.py').write_text(helmet)
fixture=(ROOT/'tests/test_bill_seated_east_candidates.gd').read_text().replace('east','west')
(ROOT/'tests/test_bill_seated_west_candidates.gd').write_text(fixture)
(ROOT/'tests/test_bill_seated_west_candidates.gd.uid').write_text('uid://x6b8w3m6p2r9v\n')
runner=(ROOT/'tools/run_bill_seated_east_candidate_validation.py').read_text().replace('east','west')
(ROOT/'tools/run_bill_seated_west_candidate_validation.py').write_text(runner)
preview=(P.parent/'bill-seated-south-coherent-v1/build_review.py').read_text().replace('south','west').replace('native rear helmet','native selected west helmet').replace('real sofa contact','real furniture contact').replace('South sofa base: upright seated endpoint after the forward lowering poses.','West seated base: independent lowering poses into an upright seated endpoint.').replace('paired west recovery review','paired west sitting review')
(P/'build_review.py').write_text(preview)
print('Prepared west material masks, native helmet and isolated candidate fixture')
