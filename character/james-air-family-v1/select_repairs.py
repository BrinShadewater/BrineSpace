from pathlib import Path
import json,shutil,hashlib
P=Path(__file__).resolve().parent
for d,r in json.loads((P/'source-repair-record.json').read_text()).items():
 p=P.parent/('james-air-'+d+'-v1')
 for name in ['source.png','source-audit.json','source-prompt.txt','source-origin.json']:
  dest=p/name.replace('source','source-v1',1)
  if not dest.exists():shutil.copy2(p/name,dest)
 if not (p/'source-crops-v1').exists():shutil.copytree(p/'source-crops',p/'source-crops-v1')
 origin=r['hint'].split(' as ')[1].split(' by default')[0];shutil.copy2(origin,p/'source-v2.png');shutil.copy2(origin,p/'source.png');(p/'source-prompt.txt').write_text(r['prompt']);(p/'source-origin.json').write_text(json.dumps(dict(originalPath=origin,sha256=hashlib.sha256((p/'source.png').read_bytes()).hexdigest(),revision='v2',status='anatomy candidate requiring review'),indent=2)+'\n')
