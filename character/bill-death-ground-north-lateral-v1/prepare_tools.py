from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];N=P.parent/'bill-death-ground-north-coherent-v1'
cfg={'generation':'exec-2ce04e0f-480d-4f18-84fe-df00c2811e58','fixedRuler':[.328,.355],'heads':[[270,127],[765,181],[1295,250],[397,753],[942,804],[1459,804]],'sourceContacts':[[270,508],[765,511],[1210,511],[160,915],[597,870],[1106,870]],'targetContacts':[[128,223],[128,223],[128,223],[84,223],[84,223],[84,223]],'sequence':[1,2,3,4,5],'durations':[250,300,350,400,400,300]}
s=(N/'build.py').read_text().replace('sources/death-limp-v2.png','sources/lateral-v1.png')
s='\n'.join('cfg='+repr(cfg) if line.startswith('cfg=') else line for line in s.splitlines())+'\n'
s=s.replace("'Bill north dry ground collapse candidate'","'Bill north lateral dry collapse candidate'")
s=s.replace("'status':'staged_candidate','states'","'status':'staged_candidate','deathEntryMode':'lowered-start-v1','states'")
(P/'build.py').write_text(s,encoding='utf-8')
s=(N/'verify.py').read_text().replace('sources/death-limp-v2.png','sources/lateral-v1.png')
s=s.replace("r['fixedRuler']==[.31,.363] and all(row['target']==[128,223] for row in r['frames'])","r['fixedRuler']==[.328,.355] and [row['target'] for row in r['frames']]==[[128,223],[128,223],[84,223],[84,223],[84,223]]")
s=s.replace('Fixed atlas ruler and centered rear floor axis; foreshortening allowed','Fixed anatomical ruler and authored lateral floor contacts')
s=s.replace("check(crowns[5]>=crowns[4],'Terminal settles; rear prone projection does not use side-fall crown invariants')","check(abs(crowns[5]-crowns[4])<=3,'Small authored terminal settlement')")
(P/'verify.py').write_text(s,encoding='utf-8')
if not (P/'index.html').exists():
 (P/'index.html').write_text((N/'index.html').read_text(encoding='utf-8').replace('Bill north','Bill north lateral'),encoding='utf-8')
s=(R/'tests/test_bill_death_ground_north_candidates.gd').read_text().replace('bill-death-ground-north-coherent-v1','bill-death-ground-north-lateral-v1').replace('bill-death-ground-north-candidate-native-v1','bill-death-ground-north-lateral-candidate-native-v1')
(R/'tests/test_bill_death_ground_north_lateral_candidates.gd').write_text(s,encoding='utf-8')
(R/'tests/test_bill_death_ground_north_lateral_candidates.gd.uid').write_text('uid://b9b8w3m6p2r9v\n')
s=(R/'tools/run_bill_death_ground_north_candidate_validation.py').read_text().replace('bill-death-ground-north-candidate-native-v1','bill-death-ground-north-lateral-candidate-native-v1').replace('test_bill_death_ground_north_candidates.gd','test_bill_death_ground_north_lateral_candidates.gd')
(R/'tools/run_bill_death_ground_north_lateral_candidate_validation.py').write_text(s,encoding='utf-8')
print('Prepared lateral candidate tools; exact idle, one ruler, authored lateral registration')
