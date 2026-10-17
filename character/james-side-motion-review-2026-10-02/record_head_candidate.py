from pathlib import Path
import json,hashlib,uuid,os
P=Path(__file__).resolve().parent;R=P.parents[1]
guards=[json.loads((P/(stem+'-validation.json')).read_bytes()) for stem in ['package-head-study','package-nine-heads']]
assert all(g['exitCode']==0 and g['realProfileUnchanged'] and not g['timedOut'] for g in guards)
before=json.loads((P/'inputs-before.json').read_bytes());changed=[p for p,h in before.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
section='''## James East cargo nine-head repair candidate — October 2, 2026

`character/james-side-motion-review-2026-10-02` now retains a second built-in
generation: nine 4x head/collar closeups (six gait, three bent pickup), exact
master reference, crop layout, prompt and raw1254x1254 source. Native Godot
packager extracts418x418 cells, normalizes each to64x64, then fits recorded
head/neck rectangles to25x29 at original collar. Original256canvas/pivot/ruler
and RGBA outside the recorded windows remain exact. Windows include collar and
possible backpack pixels; they are not semantic head masks. Local crop/fit is
explicit generated-source packaging, not a whole-body replacement or native
runtime head transform.

Nine candidate PNGs and three master/current/candidate boards reviewed. Upright
head width is closer to master; bent pickup heads look too far forward for the
crouched bodies and need better pitch/collar attachment. Whole candidate remains
UNSELECTED. Missing held/pickup4/unload aliases, turn joins and helmet-visible
faces must be reconciled before family admission. Current selected artwork is
unchanged; no new manifests/normal loader admission or owner acceptance.

Native packaging checks original pixels outside each rectangle: single64576,
nine581120,0fail; engine0/no timeout and strict scratch full owner profile unchanged
both runs. All523frozen current sources/manifests/loader/registry unchanged.
These are packaging invariants, not hundreds of thousands of animation tests.
Three comparison boards reviewed; constructed840ms gait GIF uses six source
poses, not continuous station motion. No gameplay lifecycle check yet warranted
for unselected incomplete source study.

Lesson: closeup authoring reduces unrelated body redraw, but a smaller head can
still lose the needed downward pitch. Keep collar anchors and bent cranial tilt
as separate acceptance requirements; compare full body after extraction. Preserve
source windows and placement, and do not call a rectangular boundary semantic
protection. Shared pose aliases and helmet-visible face must use one coherent
repair. Next finish bent pitch/neck, held/unload/turn joins and paired helmet,
then full source/native review; West hand-edge cleanup and all-set cross-family
context/polish remain open. Full goal active/incomplete; no commit/export.
'''
def atomic(path,data):
    original=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data)
    assert path.read_bytes()==original;os.replace(tmp,path)
for rel in ['docs/CURRENT_STATUS.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    path=R/rel;original=path.read_bytes();add=section.encode();atomic(path,add+b'\n'+original if rel.endswith('CURRENT_STATUS.md') else original+b'\n\n'+add)
path=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md');atomic(path,path.read_bytes()+b'\n\n'+section.encode())
(P/'HEAD_CANDIDATE_HANDOFF.md').write_text('''# Project handoff

Updated: October2,2026 · Project: Brine Space · Task: James East cargo head repair

## Objective and acceptance
Full James animation set/master/style/perspective/proportion/material matching,
then full cross-family polish. Current candidate is incomplete and unselected.

## Accepted decisions and constraints
Preserve original body/crate/wrench/foot/clocks/shared helmet. Master head size,
collar attachment and bent cranial pitch must all match, not just silhouette size.

## Current state
Nine generated head/collar source extractions packaged into original body;
three comparison boards and840ms gait source GIF. Upright size improves;
bent pickup pitch is too forward. No normal selection/manifests changed.

## Verification
Single64576/nine581120outside-window pixel checks pass; strict scratch owner
profile unchanged both native packaging runs. All523frozen inputs unchanged.
All9full-body candidate sources viewed, no continuous native task acceptance.

## Next action
Repair bent pitch/collar and held/pickup4/unload/turn aliases, fit helmet-visible
face coherently, review full sources then native admission. West hand-edge
material cleanup and full-set cross-family/native contexts remain open.
''')
(P/'head-candidate-review.json').write_text(json.dumps({'candidateSelected':False,'candidateSourcesReviewed':9,'comparisonBoardsReviewed':3,'frozenInputs':523,'changedInputs':changed,'nativePackagingOwnerProfileUnchanged':True,'uprightSize':'closer to master','bentPitch':'too forward; pending repair','fullGoalComplete':False},indent=2))
print('Nine-pose candidate review and lessons recorded; current artwork preserved.')
