from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_full_gait_v173.py').read_text(encoding='utf-8').replace('full-gait-review-v173','full-gait-review-v233')
(p/'prepare_full_gait_v233.py').write_text(s,encoding='utf-8')
s=(p/'build_playback_v173.py').read_text(encoding='utf-8').replace('full-gait-review-v173','full-gait-review-v233')
(p/'build_playback_v233.py').write_text(s,encoding='utf-8')
