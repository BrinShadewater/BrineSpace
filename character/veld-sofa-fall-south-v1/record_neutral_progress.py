"""Record a verified neutral source/native milestone without claiming admission."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-sofa-fall-south-neutral-staged-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
visual=json.loads((P/'neutral-native-review-evidence.json').read_text());assert visual['visualReview']=='all14boards-reviewed'
text='''## Veld South sofa empty-handed fall branch - October 2, 2026

Neutral reader entrances no longer join tablet-held slump interiors. Paired staged
death-sofa-neutral-south keeps exact current reader000 entrance, two authored
forearm/waist patches and exact shared brace/floor source aliases. Built-in two
raw edits/prompts/execution retained; first retained tablet and was rejected.
Second whole sheet changed shading: only recorded bounded patches admitted.
All remaining head/hair/helmet/body pixels outside native windows byte-exact to
reviewed tablet fall; one pooled edit-source grade uses original master targets.
Same H148 ruler,256x272/p128224,1.52s clock; no new equipment or pose rescale.
61neutral package checks pass, byte-identical rebuild including original frames.

Opt-in selector binds actual neutral incoming pixels to full reader000, including
retained exits, and exact candidate entrance to current loaded source. Saved
branch must match allowed reader neutral slots0/13, enter0 or exit3; wrong branch
rejected. Both families remain staged, absent normal loader/ACTIVE_ASSETS.
Native staged actual actor API:1526checks0fail,14entrances/56actor-file restores,
70malformed guards; source clock, fixed foot/support/floor depth independently
checked. All14boards/126native-source pairs reviewed. Both neutral endpoints in
both gears remain empty-handed through attached glove/waist/helmet fall.
Whole owner2931non-log files and87targeted inputs unchanged in final interval.
Initial technical pass had concurrent grid_canvas mutation: dependency-frozen
aggregate FAILED, retained. Repeated against current renderer; no test weakening.

Lesson: join prop state as well as silhouette. A neutral live entrance cannot
transition into a tablet-held interior. Classify actual loaded source pixels,
preserve reviewed identity/equipment outside bounded authored repairs, and reject
full-sheet incidental drift. A source/native actor restore does not certify world
mortality, ordinary RunSave/future Continue, or final visual acceptance.
Next actual world death and disk/fresh-main future checks, interrupted reader
exits, then normal paired admission; remaining South sit/rise entrances and
full-library master/motion polish still open. Full Veld goal active/incomplete.
Review: character/veld-sofa-fall-south-v1/neutral-review.html.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
    old=target.read_text(encoding='utf-8');assert text.splitlines()[0] not in old
    target.write_text(text+'\n'+old if target.name=='CURRENT_STATUS.md' else old.rstrip()+'\n\n'+text,encoding='utf-8')
handoff='''# Project handoff

Updated: 2026-10-02 - Project: BrineSpace - Task: Veld South sofa falls

## Objective and acceptance
Full master-matched Veld set and cross-family polish active/incomplete. Paired
tablet and empty-hand sofa falls staged; world/ordinary Continue admission open.

## Accepted decisions and constraints
Exact incoming whole pose, H148 ruler, matte master grade/native shared shell.
Preserve props and reviewed head/body outside authored forearm/waist windows.
Keep owner geometry, navigation foot and normal save eligibility unchanged.

## Current state
Neutral raw1/2/prompts/provenance, build_neutral.py, paired neutral manifests,
six newframes plus six existing aliases, registration/grade/source/native review.
Source-pixel-based opt-in branch selector, matching strict saved-slot validation.
Normal loader/ACTIVE_ASSETS remain unchanged. Original staged evidence retained.

## Verification
61neutral package checks/rebuild pass;1526native checks0fail/14actor deaths,
56actor-file restores,70malformed guards.14boards/126pairs reviewed.
87inputs/all2931owner non-log files unchanged final interval. Initial native
technical pass retained as aggregateFAILED due concurrent renderer mutation.
Scope remains paused-world prescribed sofa/actor mortality, no full RunSave.

## Next action
Actual world mortality, ordinary disk/fresh-main future equivalence across both
branches and interrupted read-exit contexts; then normal paired admission.
Remaining South sit/rise death entries and full-library consistency/polish open.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
print(json.dumps({'updatedDocs':len(targets),'fullGoal':'active/incomplete','normalAdmission':False}))
