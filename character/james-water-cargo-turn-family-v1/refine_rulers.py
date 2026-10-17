from pathlib import Path
import json
P=Path(__file__).resolve().parent
c=json.loads((P/'anatomy-config.json').read_text())
c['south-west'].update(scale=25/70,ruler='70px source side/oblique cranium compared with25px selected side skull; fixed sheet scale, not silhouette fitting')
c['north-east'].update(scale=25/65,ruler='65px source side/oblique cranium compared with25px selected side skull; fixed sheet scale, not rear first-pose height fitting')
(P/'anatomy-config.json').write_text(json.dumps(c,indent=2)+'\n')
print('Recalibrated two sheets from matching cranial views rather than oversized rear width estimates')
