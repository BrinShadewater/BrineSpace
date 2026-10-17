from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2];old=P.parent/'single-transition-source-v1'
s=(old/'package_key.py').read_text(encoding='utf-8').replace('raw-transition-v1.png','raw-small-clearance-v1.png').replace('75bc5398-31b6-427d-a1b5-3c7c2067de8c','a92ca06b-d33b-48db-81af-c3af120fbed6').replace('carry-transition-key-east','carry-trailing-recovery-key-east')
s=s.replace('Far/smaller-pad boot lifts toward screen right; near/larger-pad boot stays down. Prompt requested near boot lift; semantic distinction retained, not relabeled as that requested foot.','Rear/trailing boot airborne behind forward support boot. Requested tiny FAR forward lift failed; retain as alternative trailing recovery source, not forward first-lift or toe-contact proof. Near/far anatomical identity and support/root calibration pending.')
s=s.replace('Whole source head axis123.5/floor223/height148, head27 vs held26 and original empty27. Planted sole band is108..130 vs held113..133, needs physical root/contact calibration, not head-axis zero-travel acceptance.','Whole source height148/head26/upperbody42 matches held148/26/42; cloth68,67,66vs66,64,63 slightly lighter. Forward support foot has moved relative to head, physical root/contact calibration and final fidelity pending.')
(P/'package_key.py').write_text(s,encoding='utf-8')
for source,dest in [(R/'tests/test_veld_east_single_transition_v1.gd',R/'tests/test_veld_east_trailing_key_v1.gd'),(R/'tools/run_veld_east_single_transition_v1.py',R/'tools/run_veld_east_trailing_key_v1.py')]:
 assert not dest.exists();s=source.read_text(encoding='utf-8')
 for a,b in [('single-transition-source-v1','small-clearance-source-v1'),('veld-east-single-transition-v1','veld-east-trailing-key-v1'),('test_veld_east_single_transition_v1','test_veld_east_trailing_key_v1'),('veld-east-transition-scratch','veld-east-trailing-scratch'),('carry-transition-key-east','carry-trailing-recovery-key-east'),('VELD EAST SINGLE TRANSITION','VELD EAST TRAILING KEY'),('Whole transition key','Trailing recovery key')]:s=s.replace(a,b)
 dest.write_text(s,encoding='utf-8')
 if dest.suffix=='.gd':dest.with_suffix('.gd.uid').write_text('uid://cveldeasttrailingkey1\n',encoding='utf-8')
print('Actual trailing-recovery one-key native review prepared; requested forward lift remains missing.')
