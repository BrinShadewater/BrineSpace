from pathlib import Path
import shutil,json
P=Path(__file__).resolve().parent;archive=P/'revisions/eating-v1'
archive.mkdir(parents=True,exist_ok=True)
for name in ['source-rulers.json','registration.json','material-grade.json','frame-hashes.json','manifest.json','verification.json','candidate-evidence.json','HANDOFF.md','master-comparison.json','contact-sheet.png']:
 target=archive/name
 if not target.exists():shutil.copy2(P/name,target)
if not (archive/'frames').exists():shutil.copytree(P/'frames',archive/'frames')
cfg=json.loads((P/'source-rulers.json').read_text());cfg.update(source='sources/eat-detail-v2.png',generation='exec-a8be08e2-52ab-4707-b320-e87dd2f39a62',heads=[[291,39],[765,39],[1242,39],[291,531],[765,533],[1242,533]],fixedRuler=[.31,.3175],density=1.06)
(P/'source-rulers.json').write_text(json.dumps(cfg,indent=2)+'\n')
print('Preserved v1 exports/evidence; selected authored badge/detail v2 with one fixed ruler')
