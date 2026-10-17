from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_thigh_window_v257.py').read_text(encoding='utf-8').replace('thigh-window-v257','thigh-window-v263').replace('[10,11,12,13,14]','[10,11,12,13,14,15]').replace('phase10..14','phase10..15')
s=s.replace("{12:'thigh-construction-phase12-v256'}", "{11:'thigh-coordinated-v262/phase11',12:'thigh-coordinated-v262/phase12',13:'thigh-coordinated-v262/phase13',14:'thigh-coordinated-v262/phase14'}").replace('i in [12]','i in [11,12,13,14]')
(p/'prepare_thigh_window_v263.py').write_text(s,encoding='utf-8')
