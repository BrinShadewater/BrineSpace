from pathlib import Path
import subprocess,sys,os
root=Path(__file__).resolve().parents[1]
log=root/'output'/sys.argv[1]
with log.open('w',encoding='utf-8') as out:
    result=subprocess.run([os.environ['BRINE_GODOT'],'--path',str(root),*sys.argv[2:]],stdout=out,stderr=subprocess.STDOUT,timeout=240)
print('exit',result.returncode,'log',log.name)
lines=log.read_text(encoding='utf-8',errors='replace').splitlines()
for line in [line for line in lines if any(word in line for word in ['ERROR','Error','SCRIPT','PASS','FAIL','failures='])][:20]:print(line)
sys.exit(result.returncode)
