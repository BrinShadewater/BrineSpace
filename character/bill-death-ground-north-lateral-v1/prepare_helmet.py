from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];E=P.parent/'bill-death-ground-helmet-east-coherent-v1';H=P.parent/'bill-death-ground-helmet-north-lateral-v1';H.mkdir(exist_ok=True)
cfg={'sourceNecks':[[765,213],[1280,288],[370,780],[904,815],[1423,815]],'tilts':[0,20,50,90,90],'nativeNeckAnchor':[17,29]}
s=(E/'build.py').read_text().replace('east','north').replace("BARE=P.parent/'bill-death-ground-north-coherent-v1'","BARE=P.parent/'bill-death-ground-north-lateral-v1'")
s='\n'.join('cfg='+repr(cfg) if line.startswith('cfg=') else line for line in s.splitlines())+'\n'
s=s.replace("'Bill north dry ground collapse with canonical helmet candidate'","'Bill north lateral collapse with canonical rear helmet candidate'")
s=s.replace('(xx-center[0])/17','(xx-center[0])/13').replace('(yy-center[1])/19','(yy-center[1])/13').replace("'radii':[17,19]","'radii':[13,13]")
(H/'build.py').write_text(s,encoding='utf-8')
s=(E/'verify.py').read_text().replace('east','north').replace("B=P.parent/'bill-death-ground-north-coherent-v1'","B=P.parent/'bill-death-ground-north-lateral-v1'")
(H/'verify.py').write_text(s,encoding='utf-8')
s=(R/'tests/test_bill_death_ground_helmet_east_candidates.gd').read_text().replace('east','north').replace('BILL DEATH GROUND HELMET EAST','BILL DEATH GROUND HELMET NORTH').replace('bill-death-ground-helmet-north-coherent-v1','bill-death-ground-helmet-north-lateral-v1').replace('bill-death-ground-north-coherent-v1','bill-death-ground-north-lateral-v1').replace('bill-death-ground-helmet-north-candidate-native-v1','bill-death-ground-helmet-north-lateral-candidate-native-v1')
(R/'tests/test_bill_death_ground_helmet_north_lateral_candidates.gd').write_text(s,encoding='utf-8')
(R/'tests/test_bill_death_ground_helmet_north_lateral_candidates.gd.uid').write_text('uid://d9b8w3m6p2r9v\n')
s=(R/'tools/run_bill_death_ground_helmet_east_candidate_validation.py').read_text().replace('east','north').replace('BILL DEATH GROUND HELMET EAST','BILL DEATH GROUND HELMET NORTH').replace('test_bill_death_ground_helmet_north_candidates.gd','test_bill_death_ground_helmet_north_lateral_candidates.gd').replace('bill-death-ground-helmet-north-candidate-native-v1','bill-death-ground-helmet-north-lateral-candidate-native-v1')
(R/'tools/run_bill_death_ground_helmet_north_lateral_candidate_validation.py').write_text(s,encoding='utf-8')
print('Prepared canonical rear helmet lateral candidate tools')
