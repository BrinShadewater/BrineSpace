"""Rebuild the final animation asset package from saved sources, without generation."""
from pathlib import Path
import subprocess,sys,shutil
H=Path(__file__).resolve().parent
def run(name,*args):
 with (H/(name+'-rebuild.log')).open('w',encoding='utf8') as log:
  r=subprocess.run([sys.executable,str(H/(name+'.py')),*args],stdout=log,stderr=subprocess.STDOUT)
 if r.returncode:raise RuntimeError(f'{name} failed; see {name}-rebuild.log')
 print(name+' passed',flush=True)
for kind in ['action','quarter','rest','rear']:run('extract_'+kind+'_sources')
stages=['build_inspection','build_actions','validate_actions','build_cargo','validate_cargo','build_meals','validate_meals','build_equipment','validate_equipment','build_rest','validate_rest','build_recovery','build_death','validate_recovery_death','build_water','validate_water']
for name in stages:run(name)
run('finish_palette');run('audit_aliases','--before');run('consolidate_aliases')
shutil.copyfile(H.parent/'krusher-coherent-bank-v3/candidate-bank-index.json',H/'candidate-bank-index.json')
for name in ['build_package','validate_package','audit_aliases']:run(name)
if '--native' in sys.argv:run('run_native_verify')
print('Final package: character/krusher-animation-package-v8')

