from pathlib import Path
import sys
p=Path(__file__).resolve().parent
phase=int(sys.argv[1]);version=int(sys.argv[2]);assert phase in range(49)
s=(p/'prepare_material_v49.py').read_text()
s=s.replace("out=p/'master-material-v49'",f"out=p/'master-material-phase{phase}-v{version}'").replace('bare-000.png',f'bare-{phase:03d}.png')
s=s.replace("r/'character/james-west-master-carry-v1/local-v3-carry-pose.png'","p/'master-material-v49/bare-head-protected.png'")
s=s.replace('carrying-case design/finish only','repaired material finish only').replace('walking-entry pose',f'distinct walking stride{phase} pose').replace('No body reproportioning','Do not copy Image3 walking-entry legs. No body reproportioning')
s=s.replace("print(json.dumps(dict(references=[str(f) for f in refs],prompt=prompt)))","print('Prepared stride reference and frozen inputs.')")
exec(compile(s,str(__file__),'exec'))
