from pathlib import Path
import json,shutil,hashlib
P=Path(__file__).resolve().parent
for folder in P.parent.glob('james-death-*-v1'):
    origin=folder/'repair-origin.json'
    if not origin.exists():continue
    record=json.loads(origin.read_text())
    if (folder/'source-v1.png').exists():continue
    for name in ['source.png','source-origin.json','source-prompt.txt','source-audit.json','head-candidates.json','head-audition.png']:
        file=folder/name
        if file.exists():file.rename(folder/(name.replace('source','source-v1').replace('head-','head-v1-')))
    (folder/'source-crops').rename(folder/'source-crops-v1')
    shutil.copy2(record['original'],folder/'source.png')
    record['sha256']=hashlib.sha256((folder/'source.png').read_bytes()).hexdigest()
    (folder/'source-origin.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    (folder/'source-prompt.txt').write_text(record['prompt'],encoding='utf-8')
    print('Selected repair source',folder.name)
