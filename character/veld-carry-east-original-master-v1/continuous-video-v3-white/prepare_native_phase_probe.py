"""Create bounded native uniform-versus-paced test from corrected distance fixture."""
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2]
text=(R/'tests/test_veld_east_original_motion_probe_v2.gd').read_text(encoding='utf-8')
old=text.splitlines()[1:3]
root='res://character/veld-carry-east-original-master-v1/continuous-video-v3-white/'
text=text.replace(old[0],f'const PACKS=["{root}bare-uniform-phase-manifest.json","{root}bare-paced-phase-manifest.json"]')
text=text.replace(old[1],f'const HELMETS=["{root}helmet-uniform-phase-manifest.json","{root}helmet-paced-phase-manifest.json"]\nconst RECORD="{root}phase-timing-study.json"')
text=text.replace('veld-east-original-motion-probe-v2','veld-east-phase-probe-v1').replace('veld-east-motion-probe-scratch','veld-east-phase-probe-scratch')
text=text.replace('for trial in range(3):','for trial in range(2):').replace('var pixels:float=[96.5333333333335,100.13333333333346,103.73333333333342][trial]','var study:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(RECORD))\n  var pixels:float=study.diagnosticStrideNativePixels')
text=text.replace('player.load_manifest(PACK)','player.load_manifest(PACKS[trial])').replace('equipment,HELMET','equipment,HELMETS[trial]').replace('"diving-helmet",HELMET','"diving-helmet",HELMETS[trial]')
text=text.replace('range(66)','range(76)').replace('n<65','n<75').replace('(n-1)%32','(n-1)%37').replace('(n-1)/32','(n-1)/37').replace('n==65','n==75').replace('range(32)','range(37)')
text=text.replace('    if n%4==0 or n in [1,32,33,64,65]:\n     check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Native traveling capture")','    check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Native traveling capture")')
text=text.replace('gear+" / diagnostic stride "','gear+" / "+["uniform","paced"][trial]+" / diagnostic stride "')
text=text.replace('"slot":index,','"slot":index,"rawSlot":index+18,')
text=text.replace('Three diagnostic stride sweeps through actual distance-driven sprite player at47/93/148. No accepted stride/contact/start/stop/controller/station/save integration.','Two full37-pose diagnostic timing comparisons through actual distance-driven sprite player at47/93/148. No accepted stride/full-contact/start/stop/controller/station/save integration.')
text=text.replace('VELD EAST MOTION PROBE','VELD EAST PHASE PROBE')
fixture=R/'tests/test_veld_east_phase_probe_v1.gd';assert not fixture.exists();fixture.write_text(text,encoding='utf-8')
fixture.with_suffix('.gd.uid').write_text('uid://cveldeastphaseprobe1\n',encoding='utf-8')
runner=(R/'tools/run_veld_east_neutral_source_v1.py').read_text(encoding='utf-8')
runner=runner.replace('veld-east-neutral-source-v1','veld-east-phase-probe-v1').replace('test_veld_east_neutral_source_v1','test_veld_east_phase_probe_v1').replace('veld-east-neutral-scratch','veld-east-phase-probe-scratch').replace('800x620','900x620')
runner=runner.replace("P/'build_source_clip.py'}","P/'build_source_clip.py',P/'phase-timing-study.json',P/'build_phase_timing_study.py',P/'prepare_native_phase_probe.py',P/'support-material-diagnostic-v2.json',P/'track_support_materials_v2.py',P/'track_support_materials.py'}")
runner=runner.replace("for manifest in P.glob('*-source-manifest.json'):","for manifest in P.glob('*-phase-manifest.json'):\n paths.add(manifest)")
runner=runner.replace('Complete paired source-clock native three-scale master comparison only; no accepted gait/world contacts/controller/save integration.','Actual distance-driven full37-pose two-cycle uniform/paced comparison, both gears/three scales. No final physical contact/stride/start-stop or normal integration acceptance.')
target=R/'tools/run_veld_east_phase_probe_v1.py';assert not target.exists();target.write_text(runner,encoding='utf-8')
print('Full37-pose uniform/paced native fixture and isolated runner prepared.')
