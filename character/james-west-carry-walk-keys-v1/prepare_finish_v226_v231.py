from pathlib import Path
p=Path(__file__).resolve().parent
prep=p/'prepare_lower_material_stride.py'
s=prep.read_text(encoding='utf-8').replace('42:156}[phase]','42:156,43:157,44:158,45:160,46:161,47:163,48:164}[phase]')
prep.write_text(s,encoding='utf-8')
import subprocess,sys
for phase,version in [(43,226),(44,227),(45,228),(46,229),(47,230),(48,231)]:
 subprocess.run([sys.executable,str(prep),str(phase),str(version)],check=True)
s=(p/'prepare_finish_v215_v216.py').read_text(encoding='utf-8')
s=s.replace('[(35,215),(36,216)]','[(43,226),(44,227),(45,228),(46,229),(47,230),(48,231)]')
s=s.replace('The feet are separating: the boot on the left points left, while the boot on the right retains its diagonal down-left toe and raised up-right heel.', 'This is the exact ending portion of the walking stride. Preserve the original independent sole angle, toe height, heel height and spacing of each boot in Image1. Do not force the boots to a shared pitch or floor height.')
exec(compile(s,str(p/'prepare_finish_v226_v231.py'),'exec'))
