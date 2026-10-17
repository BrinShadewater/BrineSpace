"""Record source-gate lessons without overwriting concurrent accepted decisions."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent; R=P.parents[1]
e=P/'v4-study/review-evidence.json'; data=json.loads(e.read_text(encoding='utf-8'))
data.update(visualReview='all6 graded whole figures and enlarged head/grip/equipment details viewed beside canonical held; FAILED equipment continuity/head/held join',
            adoption='rejected_until_source_defects_repaired',continuousNativeMotionReviewed=False)
e.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
heading='## Veld South–West source gate — October 2, 2026'
block=heading+'''

Unselected turn study character/veld-cargo-turns-master-family-v1 retains four
authored South–West sources. V2 preserves tucked/small case and broad West head;
V3 compact endpoint improves but interiors face right before left endpoint,
rejected. V4 corrects leftward order; all6whole figures/enlarged grip/equipment
views inspected beside corrected held. Equipment still swaps in poses2/3;
Westhead proxy30 versus held28 and whole held join remain open. Not admitted.

One first-front148ruler, physicalboot registration, bounded source-alpha
extraction; no per-pose rescale or mirrored anatomy. Shared West colour recipe
with entire case/grip band protected across all projections.32source checks pass,
6lossless decoded APNG presentations/original800ms; technical pass does not
override visual failure. Source preview only, no native/continuous/world proof.
No normal selection/controller/owner room changes or Godot run this interval.

Lesson: a better isolated endpoint can still reverse angular order or swap
asymmetric equipment. Inspect nose direction, scanner/cylinder occlusion, case
reach/grip and head projection in EVERY angle before copying a canonical
endpoint or fitting helmets. A fixed colour recipe cannot repair geometry.
Next whole-source repair then immutable shared helmet fit, quarter/half joins,
independent North–West and actual cargo controller/room handoffs. Full Veld
objective remains active/incomplete. Source evidence/HANDOFF in study folder.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
    before=path.read_bytes(); text=before.decode('utf-8');
    if heading in text: continue
    after=(block+text).encode('utf-8'); tmp=path.with_name(path.name+'.veld-turn-source.tmp'); tmp.write_bytes(after)
    assert path.read_bytes()==before,'Concurrent edit; rerun after inspecting '+str(path)
    tmp.replace(path)
print('Source gate/lessons recorded in5maintainedrefs; preserved concurrent content. V4 visual gateFAILED, fullgoalactive.')
