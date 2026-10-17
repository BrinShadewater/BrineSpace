from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
for room in ['crew_lounge','observation_room']:
 r=subprocess.run([sys.executable,str(p/'run_chairs.py'),room])
 if r.returncode:raise SystemExit(r.returncode)
