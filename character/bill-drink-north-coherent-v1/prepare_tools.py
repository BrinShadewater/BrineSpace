from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OLD=P.parent/'bill-drink-east-coherent-v1'
for name in ['build.py','verify.py','index.html']:
 s=(OLD/name).read_text(encoding='utf-8').replace('east','north').replace('bill-seated-north-coherent-v1/grade.py','bill-seated-north-coherent-v1/build.py')
 if name=='index.html':s=s.replace('Cup pickup and return and runtime installation remain pending.','Cup pickup/return and normal service phase installation remain pending. Cup remains naturally occluded in front from this rear camera.')
 (P/name).write_text(s,encoding='utf-8')
s=(ROOT/'tests/test_bill_drink_east_candidates.gd').read_text().replace('east','north').replace('BILL DRINK EAST','BILL DRINK NORTH')
(ROOT/'tests/test_bill_drink_north_candidates.gd').write_text(s)
(ROOT/'tests/test_bill_drink_north_candidates.gd.uid').write_text('uid://w7b8w3m6p2r9v\n')
s=(ROOT/'tools/run_bill_drink_east_candidate_validation.py').read_text().replace('east','north').replace('BILL DRINK EAST','BILL DRINK NORTH')
(ROOT/'tools/run_bill_drink_north_candidate_validation.py').write_text(s)
