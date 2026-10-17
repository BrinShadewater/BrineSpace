from pathlib import Path
import json,shutil,hashlib
P=Path(__file__).resolve().parent
for d,r in json.loads((P/'source-generation-record.json').read_text()).items():
 p=P.parent/('james-air-'+d+'-v1');origin=r['hint'].split(' as ')[1].split(' by default')[0];assert not (p/'source.png').exists()
 shutil.copy2(origin,p/'source.png');(p/'source-prompt.txt').write_text(r['prompt']);(p/'source-origin.json').write_text(json.dumps(dict(originalPath=origin,sha256=hashlib.sha256((p/'source.png').read_bytes()).hexdigest(),generator='Built-in imagegen',status='candidate requiring anatomy and equipment review'),indent=2)+'\n')
