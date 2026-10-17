from pathlib import Path
import json,shutil,hashlib
P=Path(__file__).resolve().parent
records=json.loads((P/'body-repair-record.json').read_text())
config=json.loads((P/'anatomy-config.json').read_text())
for pair,record in records.items():
 p=P.parent/('james-water-cargo-turn-'+pair+'-v1')
 for name in ['source.png','source-audit.json','source-prompt.txt','source-origin.json']:
  dest=p/name.replace('source','source-v1',1)
  if not dest.exists():shutil.copy2(p/name,dest)
 if not (p/'source-crops-v1').exists():shutil.copytree(p/'source-crops',p/'source-crops-v1')
 origin=record['result'].split(' as ')[1].split(' by default')[0]
 shutil.copy2(origin,p/'source-v2-body-repair.png');shutil.copy2(origin,p/'source.png')
 (p/'source-prompt.txt').write_text(record['prompt'])
 (p/'source-origin.json').write_text(json.dumps(dict(originalPath=origin,revision='v2-body-repair',sha256=hashlib.sha256((p/'source.png').read_bytes()).hexdigest(),helmetDonors='Preserved source-v1 and source-crops-v1; generated v2 heads are unselected'),indent=2)+'\n')
 config[pair].update(helmetDonorFolder='source-crops-v1',helmetDonorAudit='source-v1-audit.json',helmetDonorSource='source-v1.png')
(P/'anatomy-config.json').write_text(json.dumps(config,indent=2)+'\n')
