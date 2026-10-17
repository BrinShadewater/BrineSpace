from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2];old=P.parent/'single-transition-source-v1'
s=(old/'package_key.py').read_text(encoding='utf-8').replace('raw-transition-v1.png','raw-touchdown-v2.png').replace('75bc5398-31b6-427d-a1b5-3c7c2067de8c','19601e31-7374-4d66-9319-672beace3802')
s=s.replace('Far/smaller-pad boot lifts toward screen right; near/larger-pad boot stays down. Prompt requested near boot lift; semantic distinction retained, not relabeled as that requested foot.','Far/smaller-pad leg extends forward, heel low and toe raised. Distal far boot floor220 equals projected original far floor220; near floor223. Provisional contact source, not calibrated support proof.')
s=s.replace('Whole source head axis123.5/floor223/height148, head27 vs held26 and original empty27. Planted sole band is108..130 vs held113..133, needs physical root/contact calibration, not head-axis zero-travel acceptance.','Whole source head axis123.5/near floor223/height148/head27. Upper body47 vs original42, cloth71,70,69 vs66,64,63: final master fidelity pending. Perspective-aware contact verification and moving root still required.')
(P/'package_key.py').write_text(s,encoding='utf-8')
for source,dest in [(R/'tests/test_veld_east_single_transition_v1.gd',R/'tests/test_veld_east_touchdown_key_v2.gd'),(R/'tools/run_veld_east_single_transition_v1.py',R/'tools/run_veld_east_touchdown_key_v2.py')]:
 assert not dest.exists()
 s=source.read_text(encoding='utf-8')
 for a,b in [('single-transition-source-v1','touchdown-source-v2'),('veld-east-single-transition-v1','veld-east-touchdown-key-v2'),('test_veld_east_single_transition_v1','test_veld_east_touchdown_key_v2'),('veld-east-transition-scratch','veld-east-touchdown-scratch'),('VELD EAST SINGLE TRANSITION','VELD EAST TOUCHDOWN KEY')]:s=s.replace(a,b)
 dest.write_text(s,encoding='utf-8')
 if dest.suffix=='.gd':dest.with_suffix('.gd.uid').write_text('uid://cveldeasttouchdownkey2\n',encoding='utf-8')
print('Independent touchdown key native review prepared.')
