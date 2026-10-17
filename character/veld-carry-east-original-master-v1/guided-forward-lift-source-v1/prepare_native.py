from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2];old=P.parent/'small-clearance-source-v1'
s=(old/'package_key.py').read_text(encoding='utf-8')
for a,b in [('raw-small-clearance-v1.png','raw-guided-lift-v1.png'),('a92ca06b-d33b-48db-81af-c3af120fbed6','5c6d42d3-112c-4216-b914-d4c0ef62b780'),('carry-trailing-recovery-key-east','carry-guided-forward-lift-key-east')]:s=s.replace(a,b)
s=s.replace('Rear/trailing boot airborne behind forward support boot. Requested tiny FAR forward lift failed; retain as alternative trailing recovery source, not forward first-lift or toe-contact proof. Near/far anatomical identity and support/root calibration pending.','Guide-identified far smaller screen-right boot lifts forward/right; larger near foreground boot stays down. Clearance and advance exceed tiny requested first-lift magnitude. One forward airborne key only, not heel-peel/toe-contact or full gait proof.')
s=s.replace('Whole source height148/head26/upperbody42 matches held148/26/42; cloth68,67,66vs66,64,63 slightly lighter. Forward support foot has moved relative to head, physical root/contact calibration and final fidelity pending.','Whole source height148/head27/upperbody43 vs original148/26/42; cloth65,64,63 vs66,64,63 close. Source registered by whole head/floor only; independent planted-foot/world-root/contact and final fidelity pending.')
(P/'package_key.py').write_text(s,encoding='utf-8')
for source,dest in [(R/'tests/test_veld_east_trailing_key_v1.gd',R/'tests/test_veld_east_guided_lift_v1.gd'),(R/'tools/run_veld_east_trailing_key_v1.py',R/'tools/run_veld_east_guided_lift_v1.py')]:
 assert not dest.exists()
 s=source.read_text(encoding='utf-8')
 for a,b in [('small-clearance-source-v1','guided-forward-lift-source-v1'),('veld-east-trailing-key-v1','veld-east-guided-lift-v1'),('test_veld_east_trailing_key_v1','test_veld_east_guided_lift_v1'),('veld-east-trailing-scratch','veld-east-guided-lift-scratch'),('carry-trailing-recovery-key-east','carry-guided-forward-lift-key-east'),('VELD EAST TRAILING KEY','VELD EAST GUIDED LIFT'),('Trailing recovery key','Guided forward lift key')]:s=s.replace(a,b)
 dest.write_text(s,encoding='utf-8')
 if dest.suffix=='.gd':dest.with_suffix('.gd.uid').write_text('uid://cveldeastguidedlift1\n',encoding='utf-8')
print('Whole forward key paired native fixture prepared.')
