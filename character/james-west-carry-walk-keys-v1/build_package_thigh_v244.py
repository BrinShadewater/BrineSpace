from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'package_knee_v240.py').read_text(encoding='utf-8').replace('knee-material-phase30-v240','thigh-construction-phase0-v244').replace('knee-detail-review.png','thigh-detail-review.png').replace('Original restored knee','Original thigh construction').replace('[29,30,31,32]','[48,0,1,2]').replace('if phase==30','if phase==0')
(p/'package_thigh_v244.py').write_text(s,encoding='utf-8')
