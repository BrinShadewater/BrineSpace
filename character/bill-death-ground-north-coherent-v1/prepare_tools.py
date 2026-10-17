from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;E=P.parent/'bill-death-ground-east-coherent-v1'
cfg={'generation':'exec-f4dc6c41-2a38-41b4-8c60-11149244468b','fixedRuler':[.31,.363],'heads':[[285,115],[765,149],[1255,210],[285,670],[767,682],[1268,697]],'sourceContacts':[[285,497],[765,497],[1255,497],[285,958],[767,968],[1268,968]],'targetContacts':[[128,223]]*6,'sequence':[1,2,3,4,5],'durations':[250,300,350,400,400,300]}
s=(E/'build.py').read_text(encoding='utf-8').replace('east','north').replace('East','North').replace('sources/death-v1.png','sources/death-limp-v2.png')
s='\n'.join('cfg='+repr(cfg) if l.startswith('cfg=') else l for l in s.splitlines())+'\n'
s=s.replace('(ry<85)','(ry<87)').replace('(rx>115)','(rx>110)&(rx<146)')
s=s.replace("(ry>100)&(rr[:,:,0]>1.4", "(ry>100)&(ry<125)&(rr[:,:,0]>80)&(rr[:,:,0]>1.4")
s=s.replace("'burgundy':~head&(raw[:,:,3]>200)", "'burgundy':~head&(rgb[:,:,0]>70)&(raw[:,:,3]>200)")
s=s.replace("mask=masks[name];gain=", "mask=masks[name];\n if not mask.any() or not authority.any():continue\n gain=")
(P/'build.py').write_text(s,encoding='utf-8')
s=(E/'verify.py').read_text(encoding='utf-8').replace('east','north').replace('sources/death-v1.png','sources/death-limp-v2.png')
s=s.replace("check(all(a<b for a,b in zip(crowns[:5],crowns[1:5])),'Body lowers progressively; no standing-height normalization')", "check(r['fixedRuler']==[.31,.363] and all(row['target']==[128,223] for row in r['frames']),'Fixed atlas ruler and centered rear floor axis; foreshortening allowed')")
s=s.replace("check(abs(crowns[5]-crowns[4])<=3,'Terminal corpse retains settled height')","check(crowns[5]>=crowns[4],'Terminal settles; rear prone projection does not use side-fall crown invariants')")
(P/'verify.py').write_text(s,encoding='utf-8')
(P/'index.html').write_text((E/'index.html').read_text(encoding='utf-8').replace('east','north'),encoding='utf-8')
s=(ROOT/'tests/test_bill_death_ground_east_candidates.gd').read_text(encoding='utf-8').replace('east','north').replace('BILL DEATH GROUND EAST','BILL DEATH GROUND NORTH')
(ROOT/'tests/test_bill_death_ground_north_candidates.gd').write_text(s,encoding='utf-8')
(ROOT/'tests/test_bill_death_ground_north_candidates.gd.uid').write_text('uid://n8b8w3m6p2r9v\n',encoding='utf-8')
s=(ROOT/'tools/run_bill_death_ground_east_candidate_validation.py').read_text(encoding='utf-8').replace('east','north').replace('BILL DEATH GROUND EAST','BILL DEATH GROUND NORTH')
(ROOT/'tools/run_bill_death_ground_north_candidate_validation.py').write_text(s,encoding='utf-8')
