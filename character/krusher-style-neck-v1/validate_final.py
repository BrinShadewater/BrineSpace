from pathlib import Path
import subprocess,sys
H=Path(__file__).resolve().parent
for name in ['validate_bank','build_package','validate_package','admit_floor_cues','refresh_bunk_scope','run_native_verify','run_repair','run_bunk','run_water','run_west','review_final']:
 print('RUN '+name,flush=True);r=subprocess.run([sys.executable,str(H/(name+'.py'))]);assert r.returncode==0,name
