from pathlib import Path
import sys
p=Path(__file__).resolve().parent;phase=int(sys.argv[1]);version=int(sys.argv[2])
s=(p/'package_local_material_phase4_v90.py').read_text().replace('local-material-phase4-v90',f'local-material-phase{phase}-v{version}').replace('bare-004.png',f'bare-{phase:03d}.png').replace('helmet-004.png',f'helmet-{phase:03d}.png').replace('{mode}-004.png',f'{{mode}}-{phase:03d}.png').replace('actual original4',f'actual original{phase}')
s=s.replace('previous phase3','phase3 prior provisional reference')
exec(compile(s,str(__file__),'exec'))
