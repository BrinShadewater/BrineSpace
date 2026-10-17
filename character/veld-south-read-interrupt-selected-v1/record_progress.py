"""Record scoped normal-loader evidence and the separate unresolved fall defect."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-south-read-interrupt-selected-v1'
n=json.loads((O/'validation.json').read_text());data=json.loads((O/'records.json').read_text());review=json.loads((P/'review-evidence.json').read_text())
D=R/'character/veld-south-sofa-fall-diagnostic-v1';d=json.loads((R/'output/veld-south-sofa-fall-diagnostic-v1/validation.json').read_text());diagnostic=json.loads((D/'review-evidence.json').read_text())
assert n['passed'] and d['passed'] and len(review['boards'])==12 and len(diagnostic['boards'])==2
assert len(data['records'])==56 and len(data['futures'])==12
assert all(not r['recipe'] and not r['exactLivingEntrance'] for r in diagnostic['records'])
checks=int(re.search(r'VELD SOUTH READ INTERRUPT SELECTED: (\d+) checks,0 failures',(O/'native.log').read_text())[1])
steps=sum(2*(len(x['reference'])-1) for x in data['futures'])
review['visualReview']='All twelve boards inspected: attached body/arms, stable master palette and shared shell through tablet return and finite rise. Native contact remains visible.'
review['calibration']='H148 throughout. Captured 184x184 standing sources padded36,52 to256x256/p128,224, then all sources displayed at H74; no source rescale/regrade. Replay is submitted source playback, not a continuous native movie.'
(P/'review-evidence.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
diagnostic['visualReview']='Both boards inspected. Legacy fallback jumps from seated tablet source to upright older body, loses sofa visual offset and has unhelmeted initial equipment frames. FAILED visual consistency; technical diagnostic pass does not approve fallback.'
(D/'review-evidence.json').write_text(json.dumps(diagnostic,indent=2)+'\n',encoding='utf-8')
heading='## Veld normally selected South reader interruptions and fall diagnosis - October 2, 2026'
note=f'''
Normal South sofa reader now verified at all14 timed draw/hold/stow slots,
both gears and actual power/suspension service guards:56interruptions.
{checks}native checks/0failures, engine0/clean log, {n['seconds']}s.
All6distinct incoming pixel poses per gear have ordinary RunSave disk/fresh-main
restores plus finite future stow/rise equivalence:12cases/{steps}actor updates,
source/contact/depth/clock/gear/needs/goal and paused source retained. Separate
expected player checks normal selection, not test-only artwork injection.
48targeted inputs unchanged; all2931owner non-log files preserved under scratch
APPDATA. Broader dependencies not frozen. Prescribed default sofa contact,
paused world/stepped actor; not natural chooser/hazard cadence/title Continue.

All12native/source/master boards reviewed,124submitted source/native pairs.
Attached shoulders/hips and arms, brown hair/skin/science-charcoal suit and shared
shell remain coherent through tablet stow/rise. Bare standing endpoint matches
current master exactly. Review pads184standing captures36,52 onto256/p128,224
before half-size H74 display; stretching both canvases to the same square would
invent a scale jump. Interactive replay is exact submitted source playback.
No artwork, production loader/controller, save rule or furniture geometry changed.

Separate normally loaded South sofa fall diagnostic exposes a genuine gap:
no specialised recipe; current dry floor collapse remains legacy fallback.
Both gear cases snap from seated/tablet to an older upright body, lose sofa
offset, and the helmet is absent in initial death frames. Diagnostic technical
pass is NOT visual acceptance. Corrected probe handles absent recipe and waits
for centered camera/source submission; earlier failure/uncentered interval kept.
Latest two actor-level mortality cases/16source-native pairs,63targeted inputs
and owner2931unchanged. No world roster mortality or death Continue claim.

Lesson: audit timed slots and distinct sources separately. Compare future motion
after actual service loss, then audit mortality through the normal loader; staged
fall artwork does not prove it is selected. Preserve full seated entrance,
equipment and registered root/depth before an authored supported-to-floor fall.
Next master-matched South sofa/tablet fall sources and actual world mortality/
Continue, then remaining contexts, broader world cadence and full-library polish.
Full Veld objective remains active/incomplete; owner final acceptance open.
Review: character/veld-south-read-interrupt-selected-v1/review.html.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    old=target.read_text(encoding='utf-8')
    if heading not in old:
        target.write_text(heading+'\n'+note+'\n'+old if target.name=='CURRENT_STATUS.md' else old.rstrip()+'\n\n'+heading+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text(f'''# Project handoff

Updated: 2026-10-02 - Project: BrineSpace - Task: Veld South sofa lifecycle

## Objective and acceptance
Full master-matched animation set and cross-family polish. South reading service
interruptions verified; South seated mortality visually fails. Goal remains active.

## Accepted decisions and constraints
One H148 ruler, canonical matte palette/shared helmet, whole quoted source paths,
preserve actual sofa contact. No owner layout/save changes, commit or export.

## Current state
New paired-UID normal-loader interruption test and isolated runner, plus normal
actor mortality diagnostic and runner. Review generators retain actual captures.
Production artwork/controllers/selection unchanged. Five lesson targets updated.

## Verification
{checks}checks0fail/{n['seconds']}s;56interruptions/12ordinary disk/fresh-main
futures/{steps}actor updates;48inputs/2931owner files unchanged. All12boards and
124native/source pairs reviewed. H148 standing captures padding only.
Fall diagnostic16pairs/2gear cases, both boards reviewed: empty specialised
recipe, upright legacy fallback and initial unhelmeted frames. Corrected terminal
diagnostic is scoped technical evidence; visual result FAILED. Earlier intervals
archived. Default sofa only, main paused/actor stepped; no natural world cadence.

## Next action
Author South sofa-supported fall from exact current body/tablet/head sources and
shared shell, then finite contact/root transition and world mortality/Continue.
Do not merely enable staged floor collapse: upright interior still mismatches
the seated entrance. Remaining contexts/full-library master and motion polish open.
''',encoding='utf-8')
print(json.dumps({'readerChecks':checks,'interruptions':56,'freshFutureCases':12,'actorUpdates':steps,'lessonTargets':len(targets),'fallVisualAcceptance':False}))
