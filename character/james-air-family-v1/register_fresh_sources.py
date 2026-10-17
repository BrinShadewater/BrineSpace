from pathlib import Path
import json
P=Path(__file__).resolve().parent;c=json.loads((P/'anatomy-config.json').read_text())
c['east']['heads'][6:]=json.loads((P.parent/'james-air-east-v1/recovery-v4-audit.json').read_text())['heads']
c['east']['recover-air'].update(scale=25/135,ruler='135px visually reviewed cranium at new high-density recovery source against25px selected skull; fixed row scale',cropFolder='recovery-crops-v4',sourceFile='recover-source-v4.png')
c['west']['heads']=json.loads((P.parent/'james-air-west-v1/head-candidates.json').read_text())['heads']
c['west']['recover-air'].update(scale=25/76,ruler='76px visually reviewed cranium at master-onlyv4 dry source against25px selected skull; fixed row scale')
(P/'anatomy-config.json').write_text(json.dumps(c,indent=2)+'\n')
