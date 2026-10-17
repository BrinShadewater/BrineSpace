from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'package_thigh_boundaries_v264.py').read_text(encoding='utf-8').replace('thigh-boundaries-v264','thigh-run-v266')
s=s.replace('assert raw.width==raw.height and raw.width%2==0;half=raw.width//2','assert raw.width*2==raw.height*3 and raw.width%3==0 and raw.height%2==0;half=raw.width//3')
s=s.replace('(i%2)','(i%3)').replace('(i//2)','(i//3)').replace('(i%2+1)','(i%3+1)').replace('(i//2+1)','(i//3+1)').replace('(1024,560)','(1536,560)').replace('(1024,480)','(1536,480)')
(p/'package_thigh_run_v266.py').write_text(s,encoding='utf-8')
s=(p/'prepare_thigh_window_v257.py').read_text(encoding='utf-8').replace('thigh-window-v257','thigh-window-v267').replace('[10,11,12,13,14]','[4,5,6,7,8,9,10,11]').replace('phase10..14','phase4..11')
s=s.replace("{12:'thigh-construction-phase12-v256'}", "{5:'thigh-run-v266/phase5',6:'thigh-run-v266/phase6',7:'thigh-run-v266/phase7',8:'thigh-run-v266/phase8',9:'thigh-run-v266/phase9',10:'thigh-boundaries-v264/phase10',11:'thigh-coordinated-v262/phase11'}").replace('i in [12]','i in [5,6,7,8,9,10,11]')
(p/'prepare_thigh_window_v267.py').write_text(s,encoding='utf-8')
