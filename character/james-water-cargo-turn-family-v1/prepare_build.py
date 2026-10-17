from pathlib import Path
import json
P=Path(__file__).resolve().parent
if (P/'anatomy-config.json').exists() or (P/'build.py').exists():
 raise SystemExit('Existing reviewed builder and anatomy config preserved. Edit those files directly for revisions.')
pairs=['east-south','south-west','west-north','north-east'];widths=[76,75,63,75];config={}
source=(P.parent/'james-water-turn-family-v1/build.py').read_text()
a=source.index('CONFIG={');b=source.index('ANCHORS=',a)
source=source[:a]+"CONFIG=json.loads((P/'anatomy-config.json').read_text())\n"+source[b:]
source=source.replace('james-water-turn-','james-water-cargo-turn-').replace("james-water-'+d","james-water-cargo-'+d").replace('swim-turn-','swim-carry-turn-').replace("'swim-'","'swim-carry-'").replace('520ms quarters','800ms quarters').replace('James ordinary water turns','James underwater cargo turns')
source=source.replace("('james-water-cargo-'+d+'-v1')/'helmet-registration.json'","('james-water-'+d+'-v1')/'helmet-registration.json'")
source=source.replace("donor_folder=p/('source-crops-v1' if (p/'source-crops-v1').exists() else 'source-crops')","donor_folder=p/'source-crops'")
source=source.replace("p/('source-audit-v1.json' if (p/'source-audit-v1.json').exists() else 'source-audit.json')","p/'source-audit.json'")
source=source.replace('Exact installed swim endpoints','Exact staged cargo endpoints').replace('staged_water_turns_visual_review_pending','staged_cargo_turns_anatomy_review_pending').replace('staged_visual_review_pending','staged_cargo_turns_anatomy_review_pending')
(P/'build.py').write_text(source)
for pair,width in zip(pairs,widths):
 config[pair]=dict(scale=(22 if pair=='north-east' else 25)/width,heads=json.loads((P.parent/('james-water-cargo-turn-'+pair+'-v1')/'head-candidates.json').read_text())['heads'],ruler=str(width)+'px visually estimated full cranium; fixed anatomical scale audition')
config['west-north']['heads'][2]=[98,33];config['west-north']['heads'][3]=[88,39]
(P/'anatomy-config.json').write_text(json.dumps(config,indent=2)+'\n')
