from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2];old=P.parent/'single-transition-source-v1'
s=(old/'package_key.py').read_text(encoding='utf-8').replace('raw-transition-v1.png','raw-prelift-v2.png').replace('75bc5398-31b6-427d-a1b5-3c7c2067de8c','4cedbbc8-4090-4fc5-bad3-9ce05271f0ae')
s=s.replace('Far/smaller-pad boot lifts toward screen right; near/larger-pad boot stays down. Prompt requested near boot lift; semantic distinction retained, not relabeled as that requested foot.','Near-standing initial far-foot clearance: distal far boot219 vs original220, near floor223. Legs remain close. Prompt requested heel peel with toe touching; output appears tiny whole-foot clearance, not confirmed toe-contact heel peel.')
s=s.replace('Whole source head axis123.5/floor223/height148, head27 vs held26 and original empty27. Planted sole band is108..130 vs held113..133, needs physical root/contact calibration, not head-axis zero-travel acceptance.','Whole source head axis123.5/floor223/height148/head26/upperbody42 matches original held26/42. Near-floor opaque band122..130 vs held120..131, centroid126vs125.5. Cloth71,69,68 vs66,64,63 still lighter; final fidelity/contact calibration pending.')
(P/'package_key.py').write_text(s,encoding='utf-8')
for source,dest in [(R/'tests/test_veld_east_single_transition_v1.gd',R/'tests/test_veld_east_initial_step_v2.gd'),(R/'tools/run_veld_east_single_transition_v1.py',R/'tools/run_veld_east_initial_step_v2.py')]:
 assert not dest.exists();s=source.read_text(encoding='utf-8')
 for a,b in [('single-transition-source-v1','prelift-source-v2'),('veld-east-single-transition-v1','veld-east-initial-step-v2'),('test_veld_east_single_transition_v1','test_veld_east_initial_step_v2'),('veld-east-transition-scratch','veld-east-initial-step-scratch'),('VELD EAST SINGLE TRANSITION','VELD EAST INITIAL STEP')]:s=s.replace(a,b)
 dest.write_text(s,encoding='utf-8')
 if dest.suffix=='.gd':dest.with_suffix('.gd.uid').write_text('uid://cveldeastinitialstep2\n',encoding='utf-8')
print('Near-standing initial foot-clearance native review prepared.')
