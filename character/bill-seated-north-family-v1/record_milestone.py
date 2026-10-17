from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
note='''
Bill north sitting family installed — September30,2026. Sixgear states/36refs
select sit-down,seated breathing,sit-rise through normal loader and ACTIVE_ASSETS.
48family checks and291normal native checks pass40.91sec;2,914real non-logfiles
unchanged. Exact standing/seated joins and real default lounge approach/render
reviewed;16power-loss cases preserve source pose/furniture offset and reverse
only performed sitting. Full set goal active;otherquarters/sofa,diskrestores,
inherited partial-sit service cases,remaining life/rest art and final polish open.
Current authority: character/bill-seated-north-family-v1/FAMILY_HANDOFF.md.

Reusable lessons: a finite elapsed API clamps even a looping clip; validate loops
through actual cosmetic playback, and bind Bill's retained cosmetic arrays after
candidate injection. Local boot registration alone does not establish world
contact: Life.offset translates the actor toward actual furniture. Interrupted
reversed clips must retain performed time and furniture translation; at exact
half-open boundaries consult the loaded forward/reverse source indices instead
of applying a blanket epsilon. Actor update ignores delta<=0; use a real minimal
positive simulation tick for interruption evidence. Explicitly type String values
from dynamic Godot script properties. Native default-chair evidence is scoped;
do not infer sofa,otherquarters,diskrestore or otheractor acceptance from it.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill north sitting family installed — September30,2026\n'+note+'\n').encode('utf-8')+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
for name in ['bill-seated-north-coherent-v1','bill-seated-helmet-north-coherent-v1','bill-seated-idle-north-v1']:
 handoff=P.parent/name/'FAMILY_HANDOFF.md'
 if handoff.exists():handoff.write_bytes(('Current selection: ../bill-seated-north-family-v1/FAMILY_HANDOFF.md.\nNorth family installed and native lounge/interruption reviewed. Below retains\nhistorical candidate milestone scope.\n\n').encode('utf-8')+handoff.read_bytes())
native=ROOT/'output/bill-seated-north-selected-lounge-v1';files=[P/'bare-manifest.json',P/'helmet-manifest.json',P/'source-bindings.json',P/'verification.json',ROOT/'tests/playtest_bill_seated_north_lounge.gd',ROOT/'tools/run_bill_seated_north_lounge_validation.py',native/'validation.json',native/'furniture-samples.json',native/'furniture-contact-sheet.png']
evidence={'status':'installed_runtime_reviewed','native':json.loads((native/'validation.json').read_text(encoding='utf-8')),'hashes':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'runtimeFunction':'interrupted_sit_rise_seconds','scope':'Bill normal loader/default lounge chair/bothgear/16powerloss cases;remaining furniture/rest/fullset acceptance pending'}
(P/'installed-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8');print('Recorded Bill selected north sitting family milestone and reusable lessons')
