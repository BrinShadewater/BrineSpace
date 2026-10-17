from pathlib import Path
import sys
p=Path(__file__).resolve().parent
phase=int(sys.argv[1]);version=int(sys.argv[2]);baseversion={1:66,3:70}[phase]
s=(p/'prepare_detail_phase2_v75.py').read_text()
s=s.replace('detail-phase2-v75',f'detail-phase{phase}-v{version}').replace('master-material-phase2-v69',f'master-material-phase{phase}-v{baseversion}').replace('bare-002.png',f'bare-{phase:03d}.png').replace('phase2',f'phase{phase}')
exec(compile(s,str(__file__),'exec'))
