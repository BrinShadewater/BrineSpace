from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1];E=P.parent/'bill-death-ground-helmet-east-coherent-v1'
cfg={'sourceNecks':[[712,238],[1206,322],[165,812],[632,876],[1146,878]],'tilts':[-20,-30,-35,-90,-90],'nativeNeckAnchor':[16,29]}
s=(E/'build.py').read_text(encoding='utf-8').replace('east','west').replace('East','West');s='\n'.join('cfg='+repr(cfg) if line.startswith('cfg=') else line for line in s.splitlines())+'\n';(P/'build.py').write_text(s,encoding='utf-8')
for name in ['verify.py','index.html']:(P/name).write_text((E/name).read_text(encoding='utf-8').replace('east','west').replace('East','West'),encoding='utf-8')
s=(ROOT/'tests/test_bill_death_ground_helmet_east_candidates.gd').read_text(encoding='utf-8').replace('east','west').replace('BILL DEATH GROUND HELMET EAST','BILL DEATH GROUND HELMET WEST')
(ROOT/'tests/test_bill_death_ground_helmet_west_candidates.gd').write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_death_ground_helmet_west_candidates.gd.uid').write_text('uid://q8b8w3m6p2r9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_death_ground_helmet_east_candidate_validation.py').read_text(encoding='utf-8').replace('east','west').replace('BILL DEATH GROUND HELMET EAST','BILL DEATH GROUND HELMET WEST')
(ROOT/'tools/run_bill_death_ground_helmet_west_candidate_validation.py').write_text(s,encoding='utf-8')
