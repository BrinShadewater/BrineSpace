from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[2]
s=(R/'tests/test_veld_east_neutral_source_v1.gd').read_text(encoding='utf-8')
for a,b in [('continuous-video-v3-white','single-transition-source-v1'),('veld-east-neutral-source-v1','veld-east-single-transition-v1'),('veld-east-neutral-scratch','veld-east-transition-scratch'),('source-carry-east','carry-transition-key-east'),('141','1'),('5.875','.320'),('Full walking source','Whole transition key'),('full neutral-background source','independent whole source key'),('VELD EAST NEUTRAL SOURCE','VELD EAST SINGLE TRANSITION')]:s=s.replace(a,b)
s=s.replace('frame_at_elapsed("carry-transition-key-east",6','frame_at_elapsed("carry-transition-key-east",1')
s=s.replace('Complete source-clock native appearance/master comparison only. No selected gait loop, world movement/contact, start/stop or normal integration.','One whole-source KEY appearance comparison only; no full start/stop/physical root contact or normal integration.')
t=R/'tests/test_veld_east_single_transition_v1.gd';assert not t.exists();t.write_text(s,encoding='utf-8');t.with_suffix('.gd.uid').write_text('uid://cveldeastsingletransition1\n',encoding='utf-8')
q=(R/'tools/run_veld_east_neutral_source_v1.py').read_text(encoding='utf-8')
for a,b in [('continuous-video-v3-white','single-transition-source-v1'),('veld-east-neutral-source-v1','veld-east-single-transition-v1'),('test_veld_east_neutral_source_v1','test_veld_east_single_transition_v1'),('veld-east-neutral-scratch','veld-east-transition-scratch'),('full-source-record.json','key-record.json'),('build_source_clip.py','package_key.py')]:q=q.replace(a,b)
q=q.replace('Complete paired source-clock native three-scale master comparison only; no accepted gait/world contacts/controller/save integration.','One paired whole-source transition key appearance at47/93/148 only; no full start/stop/physical contact or normal integration.')
t=R/'tools/run_veld_east_single_transition_v1.py';assert not t.exists();t.write_text(q,encoding='utf-8')
print('Native one-key paired review prepared; prior shell quoting failure launched no game.')
