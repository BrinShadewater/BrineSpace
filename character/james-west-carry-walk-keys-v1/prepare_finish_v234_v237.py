from pathlib import Path
p=Path(__file__).resolve().parent
prep=p/'prepare_lower_material_stride.py'
s=prep.read_text(encoding='utf-8').replace('baseversion={4:90','baseversion={0:167,1:168,2:169,3:170,4:90')
prep.write_text(s,encoding='utf-8')
import subprocess,sys
for phase,version in [(0,234),(1,235),(2,236),(3,237)]:subprocess.run([sys.executable,str(prep),str(phase),str(version)],check=True)
s=(p/'prepare_finish_v215_v216.py').read_text(encoding='utf-8').replace('[(35,215),(36,216)]','[(0,234),(1,235),(2,236),(3,237)]')
s=s.replace('The feet are separating: the boot on the left points left, while the boot on the right retains its diagonal down-left toe and raised up-right heel.', 'This is the beginning of the walking stride at its loop join. Preserve each original toe, heel and sole angle and exact near/far overlap in Image1. Do not spread the feet, flatten the soles or shift an ankle.')
exec(compile(s,str(p/'prepare_finish_v234_v237.py'),'exec'))
