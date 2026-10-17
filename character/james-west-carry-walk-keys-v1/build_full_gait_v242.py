from pathlib import Path
p=Path(__file__).resolve().parent
for old,new in [('prepare_full_gait_v233.py','prepare_full_gait_v242.py'),('build_playback_v233.py','build_playback_v242.py'),('build_master_audit_v233.py','build_master_audit_v242.py')]:
 s=(p/old).read_text(encoding='utf-8').replace('full-gait-review-v233','full-gait-review-v242')
 (p/new).write_text(s,encoding='utf-8')
