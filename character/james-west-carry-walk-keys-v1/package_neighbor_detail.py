from pathlib import Path
import sys
p=Path(__file__).resolve().parent
phase=int(sys.argv[1]);version=int(sys.argv[2]);baseversion={1:66,3:70}[phase]
s=(p/'package_detail_phase2_v75.py').read_text()
s=s.replace('detail-phase2-v75',f'detail-phase{phase}-v{version}').replace('master-material-phase2-v69',f'master-material-phase{phase}-v{baseversion}').replace('bare-002.png',f'bare-{phase:03d}.png').replace('{mode}-002.png',f'{{mode}}-{phase:03d}.png')
s=s.replace('before V69',f'before V{baseversion}').replace('detail candidate V75',f'detail candidate V{version}').replace('stride2',f'stride{phase}')
exec(compile(s,str(__file__),'exec'))
