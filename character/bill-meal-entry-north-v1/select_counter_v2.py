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
cfg['sources']['primary']={'source':'sources/pickup-counter-v2.png','generation':'exec-479bc9c5-11c2-4694-86ca-24e2fc57cba2','heads':[[384,77],[768,77],[1151,77],[384,538],[768,537],[1151,537]],'count':6,'density':.97,'fixedRuler':[.337,.345]}
cfg['sourceCorrection']='Raised north counter reach; actual native contact review required'
(P/'source-rulers.json').write_text(json.dumps(cfg,indent=2)+'\n',encoding='utf-8')
