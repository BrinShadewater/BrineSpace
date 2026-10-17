from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2]
s=(P.parent/'continuous-video-v3-white/build_source_clip.py').read_text(encoding='utf-8').replace('141','142').replace('5.875','5.917').replace('108,140','108,141').replace('neutral-background full source study','native-input full source study')
(P/'build_source_clip.py').write_text(s,encoding='utf-8')
for source,dest in [(R/'tests/test_veld_east_neutral_source_v1.gd',R/'tests/test_veld_east_native_input_source_v1.gd'),(R/'tools/run_veld_east_neutral_source_v1.py',R/'tools/run_veld_east_native_input_source_v1.py')]:
 assert not dest.exists()
 s=source.read_text(encoding='utf-8')
 for a,b in [('continuous-video-v3-white','standing-step-video-v2-native'),('veld-east-neutral-source-v1','veld-east-native-input-source-v1'),('test_veld_east_neutral_source_v1','test_veld_east_native_input_source_v1'),('veld-east-neutral-scratch','veld-east-native-input-scratch'),('141','142'),('5.875','5.917'),('VELD EAST NEUTRAL SOURCE','VELD EAST NATIVE INPUT SOURCE'),('neutral-background source','native-input source')]:s=s.replace(a,b)
 dest.write_text(s,encoding='utf-8')
 if dest.suffix=='.gd':dest.with_suffix('.gd.uid').write_text('uid://cveldeastnativeinput1\n',encoding='utf-8')
print('Complete paired142-pose source review fixture prepared.')
