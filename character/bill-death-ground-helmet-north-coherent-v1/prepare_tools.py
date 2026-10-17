from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1];E=P.parent/'bill-death-ground-helmet-east-coherent-v1'
s=(E/'verify.py').read_text(encoding='utf-8').replace('east','north')
s=s.replace("check(sha(P/r['component'])==r['componentSha256']==sha(ROOT/r['donor']),'Exact accepted native dry component')", "check(sha(P/r['source'])==r['sourceSha256'] and sha(ROOT/r['authority'])==r['authoritySha256'],'Bound generated perspective and canonical material authority')\ncheck(all(a<=b for a,b in zip(r['curveOutput'],r['curveOutput'][1:])), 'Monotonic shared matte palette curve')")
s=s.replace("row['nativeScale']==1", "row['fixedHelmetRuler']==[.35,.36]").replace('Frozen equipment scale','Frozen authored equipment ruler')
(P/'verify.py').write_text(s,encoding='utf-8')
(P/'index.html').write_text((E/'index.html').read_text(encoding='utf-8').replace('east','north').replace('Canonical helmet candidate','Authored rear helmet perspective candidate'),encoding='utf-8')
s=(ROOT/'tests/test_bill_death_ground_helmet_east_candidates.gd').read_text(encoding='utf-8').replace('east','north').replace('BILL DEATH GROUND HELMET EAST','BILL DEATH GROUND HELMET NORTH')
(ROOT/'tests/test_bill_death_ground_helmet_north_candidates.gd').write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_death_ground_helmet_north_candidates.gd.uid').write_text('uid://r8b8w3m6p2r9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_death_ground_helmet_east_candidate_validation.py').read_text(encoding='utf-8').replace('east','north').replace('BILL DEATH GROUND HELMET EAST','BILL DEATH GROUND HELMET NORTH')
(ROOT/'tools/run_bill_death_ground_helmet_north_candidate_validation.py').write_text(s,encoding='utf-8')
