from pathlib import Path
import json,hashlib,uuid,os
P=Path(__file__).resolve().parent;R=P.parents[1]
native=json.loads((P/'family-v2-native-evidence.json').read_bytes());guard=json.loads((P/'validate-family-v2-validation.json').read_bytes());export=json.loads((P/'east-family-v2-evidence.json').read_bytes())
assert native['failures']==0 and export['failures']==0 and guard['exitCode']==0 and guard['realProfileUnchanged']
before=json.loads((P/'inputs-before.json').read_bytes());changed=[p for p,h in before.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert set(changed)<= {'scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json'},changed
turn_review=json.loads((P/'east-turn-join-review.json').read_bytes());assert turn_review['priorSideBanksSelectionUnchanged']
files=['bent-head-target.png','head-closeup-master.png','bent-head-prompt.txt','bent-head-generated-v2.png','head-closeup-generated.png','east-family-v2-bare-manifest.json','east-family-v2-helmet-manifest.json','package-east-family-v2.gd']+[r['candidate'] for r in export['records']]
hashes={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in files}
section=f'''## James East cargo full paired head-family candidate — October 2, 2026

`character/james-side-motion-review-2026-10-02` now stages East pickup/carry/unload:
18bare slots with repaired smaller heads,18retained original shared-helmet refs,
paired manifests. New built-in three-bent-head source2172x724, explicit724-cell
extraction, prompt/master/target retained. Bent cranial tilt now looks toward the
crate and collar attachment is improved. One upright authored head reused for
pickup4/5; unload is exact reverse of repaired pickup after proving all six
original full RGBA aliases exact. Original clocks/pivot128/224/ruler148 retained.
Body/crate/wrench RGBA outside recorded head/collar rectangles exact; rectangles
include collar/backpack pixels and are not semantic head masks. Helmet art remains
original because its selected shell/face follows its own master.

All36paired refs viewed in three master/current/candidate boards. Actual
CrewSpritePlayer staged manifest admission: {native['checks']}checks0fail/18native
paired148/82/54/27captures reviewed. This is source-clock/scale preview, not
normal grid or actor/task/Continue/turn acceptance. Native review caught original
goggle/face fragments outside the earlier30px gait extraction. Final gait window
128/71/36/32 clears them, preserving all original RGBA beyond that window.
Both intermediate extraction runs/sources/native evidence archived. Final export
{export['checks']}outside-window pixel/alias checks0fail; these are packaging
invariants, not that many gameplay tests.9metadata/clock checks pass.
Strict scratch full owner profile unchanged; terminal engine0/no timeout.
All521frozen source/manifests unchanged; shared loader/registry bytes changed
during concurrent character work. Fresh ordered resolution confirms all14James
side banks still select the original recorded manifests. Three source-clock
GIFs are constructed review media; no uninterrupted native world-motion claim.

Lesson: verify full RGBA reverse aliases before sharing repaired sources. Scale
preview must cover every source slot: a narrow head window can leave tiny old
goggle fragments even when all outside-window tests pass. Account for the full
old head silhouette, preserve the exact lower body, and review the resulting
cranial pose/collar in full-body context. Keep original paired helmet when already
master-matching; a bare repair does not justify repainting the shell.

Candidate remains UNSELECTED pending all East-connected turn source/head joins
and actual native task lifecycle. Next reconcile the current ordered turn banks,
matching revised held head to entrances/returns, then normal-loader/task/Continue
validation. West hand-edge material cleanup, other context and full-set
cross-family polish remain open. Full James goal active/incomplete; no owner
acceptance/commit/export.

Fresh ordered turn audit resolves six East-connected dry turns in both gears:
92source slots,16boards, all reviewed beside both directional idle/carry anchors.
Includes East/West half turns, not just North/South quarter turns. Bare East and
near-East cranial/cheek silhouette still exceeds the repaired cargo head; joining
now would produce a proportion switch. Helmet shell remains visually coherent at
these source poses; no shell redraw warranted. Preserve directional intermediate
gaze, collar/body/crate and clocks while repairing bare head joins. Actual motion
and gameplay continuity are still unverified. No normal-selection changes here.
'''
def atomic(path,data):
    original=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data)
    assert path.read_bytes()==original;os.replace(tmp,path)
for rel in ['docs/CURRENT_STATUS.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    path=R/rel;original=path.read_bytes();add=section.encode();atomic(path,add+b'\n'+original if rel.endswith('CURRENT_STATUS.md') else original+b'\n\n'+add)
path=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md');atomic(path,path.read_bytes()+b'\n\n'+section.encode())
handoff=f'''# Project handoff

Updated: October2,2026 · Project: Brine Space · Task: James East cargo head family

## Objective and acceptance
Full James set/master/style/perspective/proportion/material alignment, then all
cross-family polish. Current candidate is unselected; full goal incomplete.

## Accepted decisions and constraints
Master head size and bent gaze/collar, belt wrench/crate/body/pivot/clocks retained.
Original shared helmet is paired unchanged; source-pixel boundary is rectangular.

## Current state
18new bare/18original helmet refs and paired East pickup/carry/unload manifests.
Three bent heads rebuilt, held4/5 repaired; six unload reverse aliases shared.
Final gait window removes leftover old goggles. Intermediate evidence archived.
Three source boards/GIFs and18native scale captures reviewed. No production edits.

## Verification
9metadata/clock checks;{native['checks']}staged player source/scale checks0fail;
{export['checks']}outside-window/alias checks0fail. Scratch full owner profile
unchanged;521frozen sources/manifests unchanged. Shared loader/registry changed
concurrently; fresh resolution confirms14side banks unchanged. All92East-connected
turn slots/16boards reviewed; bare head seam remains, helmet shell coherent at
sampled source clocks. No actor/task/turn/Continue acceptance yet.

## Next action
Repair East and near-East bare turn head joins across quarter and half-turn aliases.
Then normal selection and actual native task/Continue checks. West hand-edge and
remaining full-set contexts/cross-family polish remain open.
'''
atomic(P/'HEAD_CANDIDATE_HANDOFF.md',handoff.encode())
(P/'family-v2-review-evidence.json').write_text(json.dumps({'selected':False,'sourceReferencesReviewed':36,'nativeCapturesReviewed':18,'nativeChecks':native['checks'],'packagingChecks':export['checks'],'sourceHashes':hashes,'frozenInputs':523,'changedInputs':changed,'turnLifecycleAcceptance':False,'fullGoalComplete':False},indent=2))
print('Full paired source-family milestone and lessons recorded in five guides and handoff.')
