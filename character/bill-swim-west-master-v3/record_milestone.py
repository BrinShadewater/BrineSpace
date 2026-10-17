"""Record scoped source evidence without rewriting large status files."""
from pathlib import Path
import json

P=Path(__file__).resolve().parent
ROOT=P.parent.parent
review=json.loads((P/'review.json').read_text(encoding='utf-8'))
assert review['decodedAPNGFramesExact']==12 and review['frozenInputsStable']==29
heading='Bill West six-phase master swim candidate and pull rejection - October 2, 2026'
body=f'''New character/bill-swim-west-master-v3 packages six authored phases Extend/Sweep/Pull/Recover/Reach/Glide in bare and helmet. Original148/956 whole-source density, H148, pivot160224 unchanged. Initial320x320 packing FAILED Pull support preservation (right extent333). Enlarged empty canvas to352x320 without character scaling, source/body deformation or pivot movement. All painted isolated support now preserved. No opaque edge pixels in selected pull source, but full body fidelity remains provisional.

Twelve decoded APNG frames exact, each160ms,960ms infinite loop0; two six-frame manifests source_candidate_unselected. Six canonical40x40 helmets native scale1/rotation0 with exact body outside fitting region, foreground and below-donor protection. {review['frozenInputsStable']} targeted input hashes stable. Bounded head proxies Extend138x141/Sweep135x151/Pull145x154/Recover142x151/Reach141x147/Glide138x145 versus original137x141. These are brown-region proxies, not full anatomical approval. Pull retains earlier whole-source translation after head shrink.

Reviewed full paired master/stroke, all neck pairs and entry/wrap boards. Browser normal-speed play and phase advance verified; paused Pull both gears screenshot saved. Sampled source playback does not establish full continuous native motion/contact. Extend chest controls restored to six rectangles, but material still brighter than original hardware. Pull torso broad/upright and hip position changes; recovery/reach progression and body/grade/entry chronology need repair. Newly generated pull-flat-v4 rejected: head enlarged again and requested flatter narrower torso not resolved. Preserve preceding selected provisional pull3 and rejected raw/exact prompt. Built-in imagegen edit mode only; no native test/profile interval or normal runtime adoption.

Lesson: a head-registered six-pose loop can still move hips/torso and change build. Judge shared spine/hip projection and true shoulder-elbow-wrist progression alongside head density and equipment. Widen empty review canvas to preserve support rather than shrink a pose. A local head or torso prompt is a whole-source edit unless measured otherwise; repeated edits of a drifted pull source can retain barrel chest and enlarge head again. Re-author the failed phase from the adjacent good whole-body authority, then independently assess head/control/material changes. Technical protection/APNG checks never certify master fidelity or moving acceptance.

Next re-author compact flat pull from extended authority, review hip/spine/limb continuity and restrained hardware grade across all six, reconcile entry/independent exit, then native motion/contact/resume and guarded admission. North/South master repairs, other-family joins and full-library polish remain. Full Bill objective active/incomplete.'''
targets=[ROOT/'docs/CURRENT_STATUS.md',ROOT/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',ROOT/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for target in targets:
    with target.open('rb') as f:
        f.seek(max(0,target.stat().st_size-131072))
        tail=f.read().decode('utf-8',errors='replace')
    if heading not in tail:
        with target.open('a',encoding='utf-8') as f:f.write('\n\n## '+heading+'\n\n'+body+'\n')

provenance={'mode':'built-in imagegen edit','promptDirectory':'sources','rejectedPullFlat':{'generation':'exec-a66744df-7d3c-4628-95fd-17c7777e18a5','raw':'sources/pull-flat-v4.png','prompt':'sources/pull-flat-prompt-v4.txt','orderedReferences':['sources/pull-head-v3.png','sources/extend-controls-v3.png','../crew-side-masters-v1/bill-side-master-01.png'],'decision':'Rejected: head enlarged and torso flattening unresolved'},'selectedGenerations':{'extend-controls-v3':'exec-dfb82245-caf1-43a0-a206-75d29f864733','sweep-identity-v2':'exec-e8956a81-ab18-41df-8d7b-db5b07223361','pull-head-v3':'exec-03ca88b6-def1-43a5-99f6-b02a0b893b0c','recover-v1':'exec-40d115b7-ed50-46d6-8ca3-cb26d2c039d9','reach-v1':'exec-4f2398cd-d171-4507-858a-8bf3af40b4fe','glide-v1':'exec-86717fd2-e669-40f6-bc63-a2a8c69402be'},'normalSelected':False,'nativeAcceptance':False}
(P/'generation-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 - Project: BrineSpace - Task: Bill full master-consistent set

## Objective and acceptance
Complete all Bill animations, then cross-family consistency/polish. Match original identity, anatomy, size, camera and matte grade; verify motion and integration.

## Accepted decisions and constraints
Original source density148/956; whole-source translation only. Canonical helmet40x40. Existing runtime selection preserved. No mirroring, posed-height fitting or scripted anatomical repairs.

## Current state
Six-phase paired source candidate in this directory,352x320/p160224/H148,960ms loop. build.py, manifests, frames/APNGs, review.json, three review boards, browser-review.png, generation provenance and raw/exact prompts. Pull-flat-v4 rejected; pull3 provisional remains. Six project/installed guidance targets appended.

## Verification
29 frozen inputs stable;12 decoded frames/holds exact; all painted support preserved; six bounded equipment/body protections pass. Three boards and paused browser pair inspected, play/step verified. Visual fidelity FAILED/incomplete: broad pull chest, torso/hip movement, recovery/reach progression and bright hardware. No new native/profile interval. No normal selection.

## Next action
Re-author pull from extend source as primary whole-body authority. Judge spine/hip and limb progression across all six before grading or smoothing; reconcile entry/independent exit and refresh native motion/contact/resume. North/South sources, guarded integration and full-library polish remain.
''',encoding='utf-8')
print('Recorded six guidance targets, handoff and generation provenance; full goal remains incomplete.')
