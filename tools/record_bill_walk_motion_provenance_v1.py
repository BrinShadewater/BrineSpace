"""Record bounded legacy source trace without reusing historical identity edits."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=['character/bill-walk-east-material-v1/build.py','character/bill-selected-source-audit-2026-10-01-locomotion-v6/source-inventory.json','character/crew-runtime-matte-v1/bill/manifest.json','tools/finish_crew_sprite_edges.py']
report=dict(scope='Bounded inspected source/material lineage only; not exhaustive repository search or proof that no alternate motion source exists.',inputs={path:sha(R/path) for path in paths},findings=['Selected East material builder grades fabric and stamps a historical shared head onto all48 existing source poses; not a gait-motion derivation from one improved full figure.','Underlying runtime-matte manifest records exact selected review-v9 PNGs and timing.','No reusable full-figure gait deformation recipe identified in these inspected files.','Preserve selected sources; do not replay historical local head stamping/grade as new master artwork or claim four keys complete48 motion.'],normalSourcesChanged=False)
(P/'motion-source-trace.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
note='\nBounded East walk source trace: selected material builder grades fabric and stamps historical shared head on48 existing poses; underlying runtime-matte manifest records exact selected review-v9 PNGs/timing. Inspected files do not provide a reusable full-figure gait derivation from one new source. This is not an exhaustive absence claim. Preserve current art and trace evidence; do not replay historical identity stamping/grade as new whole-pose master repair. motion-source-trace.json freezes inspected paths. Continue full48authoring/temporal proof; four keys remain provisional.\n'
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for root in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths += [root/'references/crew-consistency.md',root/'references/source-density.md']
for path in paths:
 with path.open('a',encoding='utf-8') as f:f.write(note)
print('Preserved bounded source trace and historical-method limitation in eight maintained records.')
