from pathlib import Path
import json
P=Path(__file__).resolve().parent;c=json.loads((P/'anatomy-config.json').read_text())
for d in ['east','west']:
 heads=json.loads((P.parent/('james-air-'+d+'-v1')/'head-candidates.json').read_text())['heads']
 if d=='east':c[d]['heads'][6:]=heads[6:];c[d]['swim-distress'].update(cropFolder='source-crops-v2',sourceFile='source-v2.png')
 else:c[d]['heads']=heads
(P/'anatomy-config.json').write_text(json.dumps(c,indent=2)+'\n')
