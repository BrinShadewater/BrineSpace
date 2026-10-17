from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
s=(ROOT/'tests/test_bill_pickup_live_boundary.gd').read_text(encoding='utf-8')
s=s.replace('east','DIRECTION_SWAP').replace('west','east').replace('DIRECTION_SWAP','west').replace('actor.foot-Vector2(384,0)','actor.foot+Vector2(384,0)').replace('bill-pickup-live-boundary-v1','bill-pickup-west-live-boundary-v1')
(ROOT/'tests/test_bill_pickup_west_live_boundary.gd').write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_pickup_west_live_boundary.gd.uid').write_text('uid://k4m8r3s2b6w9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_pickup_live_boundary_validation.py').read_text(encoding='utf-8').replace("'bill-pickup-live-boundary-v1'","'bill-pickup-west-live-boundary-v1'").replace("'test_bill_pickup_live_boundary.gd'","'test_bill_pickup_west_live_boundary.gd'")
(ROOT/'tools/run_bill_pickup_west_live_boundary_validation.py').write_text(s,encoding='utf-8')
s=(P.parent/'bill-swim-pickup-east-coherent-v1/build_live_review.py').read_text(encoding='utf-8').replace('east','west').replace('East','West').replace('bill-pickup-live-boundary-v1','bill-pickup-west-live-boundary-v1').replace('test_bill_pickup_live_boundary.gd','test_bill_pickup_west_live_boundary.gd')
(P/'build_live_review.py').write_text(s,encoding='utf-8')
