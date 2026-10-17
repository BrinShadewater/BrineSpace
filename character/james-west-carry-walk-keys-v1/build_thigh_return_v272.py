from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'prepare_thigh_run_v268.py').read_text(encoding='utf-8').replace('thigh-run-v268','thigh-return-v272').replace('[16,17,18,19,20,15]','[21,22,23,24,25,20]').replace("p/'thigh-boundaries-v264/phase15'","p/'thigh-run-v270/phase20'").replace('phase==15','phase==20').replace('phase!=15','phase!=20')
s=s.replace('top row16,17,18; bottom row19,20,15','top row21,22,23; bottom row24,25,20').replace('Bottom-right15','Bottom-right20').replace('cells16..20','cells21..25').replace('adjacent pose15','adjacent pose20').replace('cell15','cell20').replace('x255..437,y170..315','x215..375,y170..290')
(p/'prepare_thigh_return_v272.py').write_text(s,encoding='utf-8')
s=(p/'package_thigh_run_v268.py').read_text(encoding='utf-8').replace('thigh-run-v268','thigh-return-v272');(p/'package_thigh_return_v272.py').write_text(s,encoding='utf-8')
s=(p/'prepare_thigh_window_v271.py').read_text(encoding='utf-8').replace('thigh-window-v271','thigh-window-v273').replace('[14,15,16,17,18,19,20,21]','[20,21,22,23,24,25,26,27]').replace('phase14..21','phase20..27')
start=s.index('    studies=');end=s.index('\nbaseline=',start)
s=s[:start]+"    studies={20:'thigh-run-v270/phase20',21:'thigh-return-v272/phase21',22:'thigh-return-v272/phase22',23:'thigh-return-v272/phase23',24:'thigh-return-v272/phase24',25:'thigh-return-v272/phase25'}\n    return p/studies[i]/(mode+'-head-protected.png') if i in studies else r/ledger['states'][i]['candidateSources'][mode]['file']"+s[end:]
(p/'prepare_thigh_window_v273.py').write_text(s,encoding='utf-8')
