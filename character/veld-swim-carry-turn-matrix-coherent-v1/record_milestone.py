from pathlib import Path
import json
H=Path(__file__).resolve().parent;R=H.parents[1]
n=json.loads((H/'native-evidence.json').read_text());c=json.loads((H/'controller-evidence.json').read_text());v=json.loads((H/'validation-checks.json').read_text());assert n['checks']==1491 and c['checks']==34612 and c['validation']['passed'] and v['failures']==0
title='Veld cargo swimming turn matrix and controller phases staged — September30,2026'
body='''All12cargo turn directions consolidated24gearstates/192exact refs:quarters800ms,four derived halves original12refs/680ms and exact duplicated cardinal middle90ms.1108source/package and1491actual-player checks PASS.96actual work/pickup/return controller cases pass34612checks;48cargo cases each exercise all12half phases,6distinct work exits in each8direction/gear groups,exact pickup/cargo joins. Engine errors0;2914owner non-log files unchanged. Initial fixture local-timing-property failure archived and repaired. Native half148/82/54 and light after-middle browser sample reviewed;50fps4s full-speed reel retained. [Handoff](../character/veld-swim-carry-turn-matrix-coherent-v1/FAMILY_HANDOFF.md),[review](http://127.0.0.1:8791/character/veld-swim-carry-turn-matrix-coherent-v1/?v=full-cargo-v1). Full-body/world journeys,interruptions/save and promotion next;remaining life/distress/recovery/death/full-set polish still open. Runtime unchanged;full goal active.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
 q=R/rel;old=q.read_bytes()
 if title.encode() not in old:q.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Cargo half matrices and actual phase coverage — September30,2026

Preserve each family’s actual half-turn contract rather than inferring two quarter
durations. Veld cargo halves retain12slots/680ms,including two exact cardinal middle
slots totalling90ms. Consolidate copied frames with source/evidence hashes and
compare every original metadata field; keep explicit actual master endpoints.
Exercise new halves through real work/pickup/cargo return, assert every12slot is
observed and check exact selected pixels against elapsed motion start; named cases
alone do not prove phase coverage. Use player timing/equipment_timing dictionaries,
not function-local clip_timing. Preserve failed probe intervals and reject engine
errors.96controller cases and all-frame loaded-player proof do not certify full
world clearance, continuous visual smoothness or owner acceptance. Evidence:
character/veld-swim-carry-turn-matrix-coherent-v1/FAMILY_HANDOFF.md.
'''
for q in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 if b'Cargo half matrices and actual phase coverage' not in q.read_bytes():
  with q.open('ab') as out:out.write(lesson.encode())
print('Full cargo matrix/controller milestone and reusable lessons recorded.')
