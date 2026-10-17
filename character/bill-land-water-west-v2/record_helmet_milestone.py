from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
f=P/'helmet-registration.json';e=json.loads(f.read_text())
e['browserReview']={'url':'http://127.0.0.1:8791/character/bill-land-water-west-v2/?v=helmet-pair-v1','loadedPairedViews':True,'pauseVerifiedAtMs':144,'scrubVerifiedAtMs':230,'nextPoseVerifiedAtMs':270,'screenshot':'browser-paired-preview.png','scope':'UI load/pause/scrub/step and push-off still inspected. Not uninterrupted motion or native station acceptance.'}
f.write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
note='''## Bill West canonical helmet entry source pairing — October 2, 2026

Paired unselected compact West entry V2 with immutable40x40canonical native West
head/helmet from bill-cargo-helmet-west-v1/sources/canonical-head.png. Five fits
use scale1/rotation0; original already selected shell/face grade unchanged. Two
standing/swim endpoint contexts padded exactly from actual normal-loaded sources,
checked against flood inventory hashes/pivots184/p92172 and208x184/p8688.
New helmet manifest/seven frames/APNG500ms, build_helmet.py, registration/hashes,
full paired board and fourteen head/collar4x crops. All five body-outside-head and
foreground masks exact; lower bodies exact. Seven decoded APNG frames/holds exact;
seven alpha160 silhouettes each have one substantial component (>20pixels).

Source review caught first mask restoring old bare chin under shell; corrected
left foreground cutoff from crown+22 to+33, with separate far-glove region22px
left/+18down. Final neck seams and original shell identity plausible in stills.
Connected alpha and exact protected pixels do not certify anatomical/motion
acceptance. Standing helmet endpoint suit visibly darker/warmer than newly
authored intermediate blue-graphite fabric; patch/detail/material polish open.

New paired browser player supports500ms timeline, pause, scrubbing, stepping and
quarter-speed option. Browser3 loaded both views, paused144ms, scrubbed230ms
push-off and stepped270ms lift. Push-off still inspected; screenshot retained.
No uninterrupted full-motion acceptance inferred. build_review_page.py preserves
UI/evidence; record_helmet_milestone.py adds browser witness and this guidance.
No new raster generation or Godot/profile writes this turn. Earlier raw prompts
and V1 bank retained. Normal Bill renderer/actor/source selection unchanged.

Lesson: foreground preservation masks can reintroduce erased face/chin pixels.
Review exposed shell bottom/neck at common native density, use distinct actual
glove and sleeve regions, and retain protected-body assertions. Original native
equipment consistency is separate from body grade and live source-phase joins.
Next full West source/material motion pass, actual dynamic gait/medium/collision
native bridge and interrupted/save/Continue proof, then North/South bridges and
full Bill cross-family master/style/perspective/size/proportion/matte-grade polish.
Goal active/incomplete. Review:character/bill-land-water-west-v2/index.html.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
    p=R/rel;t=p.read_text(encoding='utf-8')
    if heading not in t:p.write_text(note+t,encoding='utf-8')
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    t=p.read_text(encoding='utf-8')
    if heading not in t:p.write_text(t+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October2,2026 · BrineSpace · Bill West paired water-entry candidate

## Objective and acceptance
Complete full Bill set matching original masters/style/perspective/anatomy/grade,
then cross-family polish. Paired source revision is not full-set acceptance.

## Accepted decisions and constraints
Original West master is left-facing right figure; no East mirror. Common148 ruler,
320/p160224. Native canonical helmet40x40 scale1/rotation0. Exact selected endpoint
context and protected bare bodies; moving actual gait sources are a later bridge.

## Current state
Bare seven compact entry poses and new paired helmet seven poses/manifest/APNG,
500ms each. build_helmet.py, build_review_page.py, helmet-registration.json, full
paired and neck comparison boards, browser-paired-preview.png, interactive player.
V1 historical bank/raw sources/prompts retained. Six guidance files updated.

## Verification
Five body/foreground protection assertions, two exact normal-loaded padded gear
endpoints, seven helmet APNG decoded frames/holds, seven connected alpha160 figures.
Full paired board and all fourteen neck crops reviewed; first bare chin-restoration
error corrected. Browser load/pause144/scrub230/step270/push-off still verified.
Helmet shell/neck improved. Darker/warmer standing gear endpoint versus intermediate
fabric, patch/detail and continuous motion remain. No new Godot/profile writes,
normal source admission or West native/save/Continue proof this turn.

## Next action
Resolve body material/detail in actual source motion, stage West dynamic boundary/
material/geometry bridge, then native interruption/save/Continue. Remaining cardinal
bridges/cargo lifecycle/full Bill fidelity/polish remain. Goal active/incomplete.
''',encoding='utf-8')
print('Canonical West helmet pairing milestone recorded; six guidance files updated.')
