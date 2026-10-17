"""Record the independently checked rest anchors without changing accepted art."""
from pathlib import Path
import json

P=Path(__file__).resolve().parent
R=P.parents[1]
report=json.loads((R/'output/veld-rest-family-selected-v1/validation.json').read_text())
assert report['returnCode']==0
assert '1062 checks,0 failures' in (R/'output/veld-rest-family-selected-v1/native.log').read_text()
assert json.loads((P/'verification.json').read_text())['checks']==265
note='''

## Veld registered rest alignment — October 1, 2026

265 packaging checks now independently reconstruct all eight bare/equipped
sleeping head landmarks from the source registration, confirm an opaque head
pixel, and include the renderer's CELL384*.038 vertical lift at CELL384*.17/H148.
1062 normal-loader/player checks pass, including the real RoomActivity resolver
with retained registered hab_berth_west geometry in a controlled fixture. Five
progress samples through lowering, sleeping and rising verify whole-body offset,
equipment-owned head alignment, full1.84-second progress, unchanged physical
navigation foot and legacy equipment fallback. No source pixels, production
scripts, room selection or owner furnishing changed in this follow-up.

Native25.79s/engine0/zero fixture failures. Strict overall runner FAILED because
last_session.json changed among2931 real non-log files during scratch APPDATA
execution. Attribution remains unproven; preserve the interval without restoring
the owner's file. The prior specialised bunk47-check/eight-capture evidence keeps
its dated scope. Resolver/alignment math is not furnished visual acceptance,
generic world service-loss, routing, fresh-scene Continue or death continuity.
Those checks and seated/life sources/full-set master consistency remain open.

Lesson: a bounded head offset does not establish contact. Independently derive
the registered landmark and renderer lift, then verify combined body/head shifts
reach the resolver target while preserving the navigation foot. Keep mathematical
contact and actual furnished visual evidence separate.
Handoff: character/veld-rest-family-v1/HANDOFF.md. Full Veld goal remains active.
'''
for relative in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md',
                 'docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
                 'skills/brinespace-character-pipeline/references/crew-consistency.md']:
    path=R/relative
    old=path.read_bytes()
    encoded=note.lstrip().encode('utf-8')
    if encoded not in old:
        path.write_bytes(encoded+old if relative=='docs/CURRENT_STATUS.md' else old+note.encode('utf-8'))
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.lstrip().encode('utf-8') not in installed.read_bytes():
    with installed.open('ab') as output:output.write(note.encode('utf-8'))
print('Recorded rest anchor evidence and pipeline/bible/skill lesson.')
