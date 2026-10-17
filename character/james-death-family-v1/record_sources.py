from pathlib import Path
import json, shutil, hashlib
P=Path(__file__).resolve().parent
for folder in P.parent.glob('james-death-*-v1'):
    origin=folder/'source-origin.json'
    if not origin.exists(): continue
    record=json.loads(origin.read_text())
    source=folder/'source.png'
    if not source.exists(): shutil.copy2(record['original'], source)
    assert source.read_bytes()==Path(record['original']).read_bytes()
    (folder/'source-prompt.txt').write_text(record['prompt'],encoding='utf-8')
    record['sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    origin.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(folder.name, record['sha256'][:12])
