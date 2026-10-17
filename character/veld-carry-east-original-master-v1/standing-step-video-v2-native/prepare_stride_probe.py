from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2]
s=(R/'tests/test_veld_east_phase_probe_v1.gd').read_text(encoding='utf-8')
for a,b in [('continuous-video-v3-white','standing-step-video-v2-native'),('veld-east-phase-probe-v1','veld-east-native-stride-probe-v1'),('veld-east-phase-probe-scratch','veld-east-native-stride-scratch'),('for trial in range(2):','for trial in range(1):'),('range(76)','range(78)'),('n<75','n<77'),('n==75','n==77'),('%37','%38'),('/37','/38'),('range(37)','range(38)'),('index+18','index+16'),('full37-pose','full38-pose'),('VELD EAST PHASE PROBE','VELD EAST NATIVE STRIDE PROBE')]:s=s.replace(a,b)
s=s.replace(',"res://character/veld-carry-east-original-master-v1/standing-step-video-v2-native/bare-paced-phase-manifest.json"','').replace(',"res://character/veld-carry-east-original-master-v1/standing-step-video-v2-native/helmet-paced-phase-manifest.json"','')
s=s.replace('Two full38-pose diagnostic timing comparisons','One full38-pose diagnostic stride trial')
fixture=R/'tests/test_veld_east_native_stride_probe_v1.gd';assert not fixture.exists();fixture.write_text(s,encoding='utf-8');fixture.with_suffix('.gd.uid').write_text('uid://cveldeastnativestride1\n',encoding='utf-8')
s=(R/'tools/run_veld_east_native_input_source_v1.py').read_text(encoding='utf-8')
for a,b in [('veld-east-native-input-source-v1','veld-east-native-stride-probe-v1'),('test_veld_east_native_input_source_v1','test_veld_east_native_stride_probe_v1'),('veld-east-native-input-scratch','veld-east-native-stride-scratch'),('800x620','900x620')]:s=s.replace(a,b)
s=s.replace("P/'build_source_clip.py'}","P/'build_source_clip.py',P/'phase-timing-study.json',P/'build_stride_study.py',P/'prepare_stride_probe.py',P/'support-window-diagnostic.json',P/'audit_support_windows.py'}")
s=s.replace("for manifest in P.glob('*-source-manifest.json'):","for manifest in P.glob('*-phase-manifest.json'):\n paths.add(manifest)")
s=s.replace('Complete paired source-clock native three-scale master comparison only; no accepted gait/world contacts/controller/save integration.','Actual distance-driven full38-pose two-cycle stride trial, both gears/three scales. No final rigid contact/stride/start-stop or normal integration acceptance.')
runner=R/'tools/run_veld_east_native_stride_probe_v1.py';assert not runner.exists();runner.write_text(s,encoding='utf-8')
print('Complete38-pose distance-driven stride probe prepared; no source art changed.')
