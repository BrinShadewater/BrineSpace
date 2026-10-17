from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;N=P.parent/'bill-death-ground-north-coherent-v1'
cfg={'generation':'exec-0e84ecc9-8ad4-433f-8d84-b81b6efa0b19','fixedRuler':[.265,.338],'heads':[[272,100],[766,153],[1243,176],[266,642],[768,652],[1261,655]],'sourceContacts':[[272,498],[766,498],[1261,498],[272,947],[768,964],[1261,964]],'targetContacts':[[128,223]]*6,'sequence':[1,2,3,4,5],'durations':[250,300,350,400,400,300]}
s=(N/'build.py').read_text(encoding='utf-8').replace('north','south').replace('North','South').replace('sources/death-limp-v2.png','sources/death-head-v2.png')
s='\n'.join('cfg='+repr(cfg) if l.startswith('cfg=') else l for l in s.splitlines())+'\n'
(P/'build.py').write_text(s,encoding='utf-8')
s=(N/'verify.py').read_text(encoding='utf-8').replace('north','south').replace('sources/death-limp-v2.png','sources/death-head-v2.png').replace('[.31,.363]','[.265,.338]').replace('centered rear floor axis','centered front floor axis').replace('rear prone projection','front supine projection')
(P/'verify.py').write_text(s,encoding='utf-8')
(P/'index.html').write_text((N/'index.html').read_text(encoding='utf-8').replace('north','south'),encoding='utf-8')
s=(ROOT/'tests/test_bill_death_ground_north_candidates.gd').read_text(encoding='utf-8').replace('north','south').replace('BILL DEATH GROUND NORTH','BILL DEATH GROUND SOUTH')
(ROOT/'tests/test_bill_death_ground_south_candidates.gd').write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_death_ground_south_candidates.gd.uid').write_text('uid://o8b8w3m6p2r9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_death_ground_north_candidate_validation.py').read_text(encoding='utf-8').replace('north','south').replace('BILL DEATH GROUND NORTH','BILL DEATH GROUND SOUTH').replace('eating candidate','ground-collapse candidate')
(ROOT/'tools/run_bill_death_ground_south_candidate_validation.py').write_text(s,encoding='utf-8')
