from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;W=P.parent/'bill-death-ground-west-coherent-v1'
cfg={'generation':'exec-e80aa2db-698c-41fd-81ec-09c4a7d2da89','fixedRuler':[.31,.343],'heads':[[272,140],[787,193],[1312,300],[369,815],[898,878],[1412,878]],'sourceContacts':[[285,530],[774,528],[1250,530],[245,914],[615,914],[1120,914]],'targetContacts':[[143,223],[143,223],[132,223],[122,223],[90,223],[90,223]],'sequence':[1,2,3,4,5],'durations':[250,300,350,400,400,300]}
s=(W/'build.py').read_text(encoding='utf-8').replace('west','east').replace('West','East').replace('rx<140','rx>115')
lines=s.splitlines();lines=[('cfg='+repr(cfg)) if line.startswith('cfg=') else line for line in lines]
(P/'build.py').write_text('\n'.join(lines)+'\n',encoding='utf-8')
s=(W/'verify.py').read_text(encoding='utf-8').replace('west','east').replace("check(crowns[5]>=crowns[4],'Authored terminal settles downward without lifting off floor')","check(abs(crowns[5]-crowns[4])<=3,'Terminal corpse retains settled height')")
(P/'verify.py').write_text(s,encoding='utf-8')
(P/'index.html').write_text((W/'index.html').read_text(encoding='utf-8').replace('west','east'),encoding='utf-8')
s=(ROOT/'tests/test_bill_death_ground_west_candidates.gd').read_text(encoding='utf-8').replace('west','east').replace('BILL DEATH GROUND WEST','BILL DEATH GROUND EAST')
(ROOT/'tests/test_bill_death_ground_east_candidates.gd').write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_death_ground_east_candidates.gd.uid').write_text('uid://m8b8w3m6p2r9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_death_ground_west_candidate_validation.py').read_text(encoding='utf-8').replace('west','east').replace('BILL DEATH GROUND WEST','BILL DEATH GROUND EAST')
(ROOT/'tools/run_bill_death_ground_east_candidate_validation.py').write_text(s,encoding='utf-8')
