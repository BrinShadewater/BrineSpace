from pathlib import Path
import sys
p=Path(__file__).resolve().parent
phase=int(sys.argv[1]);version=int(sys.argv[2]);assert phase in range(49)
s=(p/'package_material_v49.py').read_text().replace("out=p/'master-material-v49'",f"out=p/'master-material-phase{phase}-v{version}'")
s=s.replace('bare-000.png',f'bare-{phase:03d}.png').replace('helmet-000.png',f'helmet-{phase:03d}.png').replace('before walking entry',f'before stride{phase}')
s=s.replace("mode+'-000.png'",f"mode+'-{phase:03d}.png'")
exec(compile(s,str(__file__),'exec'))
