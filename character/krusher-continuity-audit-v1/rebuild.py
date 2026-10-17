from pathlib import Path
import subprocess,sys
H=Path(__file__).resolve().parent
for name in ['build_repairs','build_package','audit_registered','propagate_registered','build_package','audit_registered','validate_package','validate_continuity']:
 subprocess.run([sys.executable,str(H/(name+'.py'))],check=True)
