from pathlib import Path
import subprocess,sys,shutil
H=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(H/'audit_aliases.py'),'--before'],check=True)
subprocess.run([sys.executable,str(H/'consolidate_aliases.py')],check=True)
shutil.copyfile(H.parent/'krusher-coherent-bank-v3/candidate-bank-index.json',H/'candidate-bank-index.json')
subprocess.run([sys.executable,str(H/'run_pipeline.py'),'build_package','validate_package','audit_aliases','refresh_bunk_scope','run_native_verify'],check=True)
