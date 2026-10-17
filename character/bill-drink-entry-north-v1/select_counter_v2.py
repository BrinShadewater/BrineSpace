from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent
archive=P/'revisions/counter-reach-v1'
if not archive.exists():
    archive.mkdir(parents=True)
    for name in ['frames','manifest.json','registration.json','source-rulers.json','frame-hashes.json','verification.json','candidate-evidence.json','HANDOFF.md','contact-sheet.png']:
        path=P/name
        if path.is_dir():shutil.copytree(path,archive/name)
        elif path.exists():shutil.copy2(path,archive/name)
cfg=json.loads((P/'source-rulers.json').read_text())
cfg['sources']['primary']={'source':'sources/pickup-counter-v2.png','generation':'exec-a3b388ed-144e-4dd0-8ab7-b238b8f60895','heads':[[336,73],[768,73],[1199,73],[336,552],[768,552],[1199,552]],'count':6,'density':.94,'fixedRuler':[.338,.3574]}
cfg['sourceCorrection']='Raised right-arm north cup counter reach; actual native contact review required'
(P/'source-rulers.json').write_text(json.dumps(cfg,indent=2)+'\n',encoding='utf-8')
