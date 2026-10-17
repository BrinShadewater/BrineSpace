from pathlib import Path
import json
P=Path(__file__).resolve().parent
c=json.loads((P/'anatomy-config.json').read_text())
for pair in ['east-south','west-north']:
 p=P.parent/('james-water-cargo-turn-'+pair+'-v1')
 c[pair]['heads']=json.loads((p/'head-candidates.json').read_text())['heads']
c['west-north']['heads'][2]=[102,42]
c['west-north']['heads'][3]=[87,49]
c['west-north']['heads'][5]=[80,83]
c['east-south']['ruler']='76px source cranium at v2 body density, 25px selected side skull; one fixed sheet scale'
c['west-north']['ruler']='63px source cranium at v2 body density, 25px selected side skull; manually reviewed rear-crown centers'
(P/'anatomy-config.json').write_text(json.dumps(c,indent=2)+'\n')
