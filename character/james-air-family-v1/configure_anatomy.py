from pathlib import Path
import json
P=Path(__file__).resolve().parent
if (P/'anatomy-config.json').exists():raise SystemExit('Reviewed anatomy config preserved; edit directly for deliberate revisions')
widths={'east':[65,70],'south':[78,72],'west':[60,70],'north':[66,66]};config={}
for d,rows in widths.items():
 p=P.parent/('james-air-'+d+'-v1');heads=json.loads((p/'head-candidates.json').read_text())['heads'];target=22 if d=='north' else 25
 config[d]={'heads':heads}
 for action,width in zip(['swim-distress','recover-air'],rows):config[d][action]=dict(scale=target/width,ruler=str(width)+'px visually reviewed full cranium against '+str(target)+'px master skull; fixed action-row source scale, not per-pose height normalization')
# Rear warm components incorrectly choose boot leather; source crown centers manually reviewed.
config['north']['heads'][:6]=[[92,69],[108,68],[88,65],[100,37],[95,61],[94,62]]
config['north']['heads'][6]=[118,18];config['north']['heads'][7]=[119,20]
(P/'anatomy-config.json').write_text(json.dumps(config,indent=2)+'\n')
