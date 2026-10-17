from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1];E=P.parent/'bill-death-ground-helmet-east-coherent-v1';H=P.parent/'bill-death-ground-helmet-south-lateral-v1';H.mkdir(exist_ok=True)
cfg={'sourceNecks':[[765,250],[1310,280],[357,768],[909,839],[1421,839]],'tilts':[0,18,35,90,90],'nativeNeckAnchor':[18,33]}
s=(E/'build.py').read_text(encoding='utf-8').replace('east','south').replace("BARE=P.parent/'bill-death-ground-south-coherent-v1'","BARE=P.parent/'bill-death-ground-south-lateral-v1'")
s='\n'.join('cfg='+repr(cfg) if line.startswith('cfg=') else line for line in s.splitlines())+'\n'
s=s.replace("'Bill south dry ground collapse with canonical helmet candidate'","'Bill south lateral collapse with canonical front helmet candidate'")
s=s.replace('rotated=head.rotate(-angle', 'selected_head=Image.open(P/"sources/canonical-closed-eyes.png").convert("RGBA") if i>=4 else head\n  rotated=selected_head.rotate(-angle')
s=s.replace("'scope':'candidate helmet/collar visual registration;", "'closedEyeComponent':'sources/canonical-closed-eyes.png','closedEyeComponentSha256':sha(P/'sources/canonical-closed-eyes.png'),'scope':'candidate helmet/collar visual registration;")
(H/'build.py').write_text(s,encoding='utf-8')
s=(E/'verify.py').read_text(encoding='utf-8').replace('east','south').replace("B=P.parent/'bill-death-ground-south-coherent-v1'","B=P.parent/'bill-death-ground-south-lateral-v1'")
s=s.replace("result={'passed'",'''closed=json.loads((P/'closed-eye-registration.json').read_text());original=np.array(Image.open(P/'sources/canonical-head.png'));corrected=np.array(Image.open(P/'sources/canonical-closed-eyes.png'));region=np.zeros(original.shape[:2],bool)
for item in closed['regions']:
 x0,y0,x1,y1=item['target'];region[y0:y1,x0:x1]=True
check(np.array_equal(original[~region],corrected[~region]) and np.array_equal(original[:,:,3],corrected[:,:,3]),'Canonical helmet exact outside authored eye windows, all alpha exact')
check(closed['changedPixels']==24 and sha(P/'sources/closed-eyes-v1.png')==closed['sourceSha256'],'Twenty-four authored eye RGB pixels only, bound source')
check(sha(P/'sources/canonical-closed-eyes.png')==r['closedEyeComponentSha256']==closed['resultSha256'],'Bound closed-eye terminal component')
result={'passed' ''')
(H/'verify.py').write_text(s,encoding='utf-8')
s=(R/'tests/test_bill_death_ground_helmet_east_candidates.gd').read_text(encoding='utf-8').replace('east','south').replace('BILL DEATH GROUND HELMET EAST','BILL DEATH GROUND HELMET SOUTH').replace('bill-death-ground-helmet-south-coherent-v1','bill-death-ground-helmet-south-lateral-v1').replace('bill-death-ground-south-coherent-v1','bill-death-ground-south-lateral-v1').replace('bill-death-ground-helmet-south-candidate-native-v1','bill-death-ground-helmet-south-lateral-candidate-native-v1')
(R/'tests/test_bill_death_ground_helmet_south_lateral_candidates.gd').write_text(s,encoding='utf-8');(R/'tests/test_bill_death_ground_helmet_south_lateral_candidates.gd.uid').write_text('uid://h9b8w3m6p2r9v\n')
s=(R/'tools/run_bill_death_ground_helmet_east_candidate_validation.py').read_text(encoding='utf-8').replace('east','south').replace('BILL DEATH GROUND HELMET EAST','BILL DEATH GROUND HELMET SOUTH').replace('test_bill_death_ground_helmet_south_candidates.gd','test_bill_death_ground_helmet_south_lateral_candidates.gd').replace('bill-death-ground-helmet-south-candidate-native-v1','bill-death-ground-helmet-south-lateral-candidate-native-v1')
(R/'tools/run_bill_death_ground_helmet_south_lateral_candidate_validation.py').write_text(s,encoding='utf-8')
s=(R/'tests/test_bill_death_ground_south_lateral_station.gd').read_text(encoding='utf-8').replace('bill-death-ground-south-lateral-station-v1','bill-death-ground-south-lateral-paired-station-v1')
needle='\tplayer.load_manifest("res://character/bill-death-ground-south-lateral-v1/manifest.json",true)';assert needle in s
s=s.replace(needle,needle+'\n\tcheck(player.load_equipment_manifest("diving-helmet","res://character/bill-death-ground-helmet-south-lateral-v1/manifest.json"),"Lateral shared front helmet paired")')
s=s.replace('for gear in [false]:','for gear in [false,true]:').replace('projections.size()==48','projections.size()==96').replace('Six bare authored slots','Six paired authored slots')
(R/'tests/test_bill_death_ground_south_lateral_paired_station.gd').write_text(s,encoding='utf-8');(R/'tests/test_bill_death_ground_south_lateral_paired_station.gd.uid').write_text('uid://i9b8w3m6p2r9v\n')
s=(R/'tools/run_bill_death_ground_south_lateral_station_validation.py').read_text(encoding='utf-8').replace('bill-death-ground-south-lateral-station-v1','bill-death-ground-south-lateral-paired-station-v1').replace('test_bill_death_ground_south_lateral_station.gd','test_bill_death_ground_south_lateral_paired_station.gd')
(R/'tools/run_bill_death_ground_south_lateral_paired_station_validation.py').write_text(s,encoding='utf-8')
print('Prepared canonical front helmet and paired south station tools')
