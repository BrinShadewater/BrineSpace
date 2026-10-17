from pathlib import Path
import sys
p=Path(__file__).resolve().parent;phase=int(sys.argv[1]);version=int(sys.argv[2])
s=(p/'prepare_local_material_phase4_v90.py').read_text().replace('phase4',f'phase{phase}').replace(f'local-material-phase{phase}-v90',f'local-material-phase{phase}-v{version}').replace('bare-004.png',f'bare-{phase:03d}.png')
s=s.replace('Change ONLY Image1\'s overly white bright seam and hardware highlights to the master sample\'s subdued matte finish.','Change ONLY Image1\'s overly white bright seam and hardware highlights to the master sample\'s subdued matte finish. Keep the metal hardware dull warm silver instead of bright white, and retain the fine muted stitch detail. Make the shoulder patch muted ochre yellow, not saturated lemon yellow.')
exec(compile(s,str(__file__),'exec'))
