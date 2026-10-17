from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
r=json.loads((P/'master-revision-review.json').read_text());audit=json.loads((P/'anatomy-audit.json').read_text())
assert r['decodedFramesChecked']==16 and len(r['unchangedBareFrames'])==6
heading='Bill South rising head and matte source refinement — October 2, 2026'
body=f'''Sibling bill-water-exit-south-v3 retains six bare poses exactly and replaces
whole rising squat5 and near-standing6 sources. Built-in revisions
exec-444193cd-af5b-4a55-b555-6de757731ec2 and
exec-62107536-4f67-4cb8-8bbe-3c08182334d0; raw/exact prompts and ordered reference
hashes saved. Original whole-source drawing density148/1295 retained, no posed
height fitting. Canonical helmet refitted from same original pitch resources.
16decodedRGBAframes/holds exact, finite loop1 and exact selected endpoints.

Bounded hair/red-unit semantic audit: master135/74px, old squat159/76, old
nearstand153/76, new squat152/77, new nearstand137/74. Hair widths suggest old
head mismatch rather than uniform torso drawing-density error. Nearstand closer,
squat still about13percent broader in this proxy. ROI-edge flags retained: clipped
component heights invalid; proxies do not prove whole-head/segment/perspective.
Neutral-body diagnostic medians69to61 squat and72.33to59 nearstand. Bounded neutral
ROI is not full grade proof. Source prompts materially reauthor poses rather than
establish colour-only pixel protection. Original/rejected predecessors retained.

{r['visualReview']}

Actual source-browser quarter playback both gears:63advancing screenshots,
observed labels1..7 each; pausedinitial0 each. Fixed common screen crop, sheet
inspected. AX labels precede screenshot and may cross holds; no normal chronology,
fresh native or full continuous motion/contact acceptance. Prior South4235/0
native interval tested preceding SouthExitV2 bank, not these replacements. No
runtime selection or owner-profile/game access this turn.

Lesson: measure independently recognisable hardware alongside hair/head proxies
before changing whole-source scale. Different head and chest-unit ratios indicate
local anatomy discrepancy; resizing the entire posed figure would worsen matching
torso density. Retain numeric proxy limits and all source drift honestly. Check
matte/detail and selected normal endpoints visually even when diagnostics improve.

Next remaining South squat/head/grade/segment/hardware/pose-join and native
contact/motion refinement, updated native bank interval, checkpoint/TitleContinue,
normal admission/cargo lifecycle and complete cross-family consistency/polish.
Full Bill objective active/incomplete. Preview bill-water-exit-south-v3/index.html.
'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
 with f.open('rb') as s:s.seek(max(0,f.stat().st_size-131072));tail=s.read()
 if heading.encode() not in tail:
  with f.open('a',encoding='utf-8') as s:s.write('\n## '+heading+'\n\n'+body+'\n')
(P/'HANDOFF.md').write_text('# Project handoff\n\nUpdated: October2,2026 · Bill South rising source refinement\n\n## Objective and acceptance\nFull Bill set matching masters, then whole-library consistency/polish. Active/incomplete.\n\n## Accepted decisions\nTwo whole-source corrections; fixed original density; six bare frames exact. No posed-size fit or new normal selection.\n\n## Current state\n'+body+'\n## Changed files\nTwo sources/prompts, build.py, regenerated bare/helmet frames/manifests/APNGs, paired/neck/master boards, anatomy_audit.py/json, master-revision-review.json, source/helmet reports, paired preview, browser-review/63screens; AUTHORING and six guidance files. Prior copied evidence named prior-v1-browser-review and prior-v2-helmet-browser-review.\n\n## Verification\n16decodedframes/holds exact,6bareframes exact; common-scale master/body/neck and sampled browser sheets inspected. No fresh native interval.\n\n## Next action\nSouth remaining master/grade/pose refinement, updated native review/contact/checkpoint/Continue, normal admission and entire-library polish.\n',encoding='utf-8')
(P/'AUTHORING.md').write_text('''# Bill South rising master revisions

Built-in image generation; complete source revisions retained locally.

- [Near-standing source](sources/near-standing-master-v3.png), [exact prompt](sources/near-standing-master-prompt-v3.txt).
- [Rising squat source](sources/rising-squat-master-v3.png), [exact prompt](sources/rising-squat-master-prompt-v3.txt).

Ordered references: previous corresponding V1 pose, original South master, selected matte native idle. Execution IDs/reference hashes: master-revision-review.json. Original fixed density148/1295; no posed-height fitting. anatomy_audit.py/json records bounded semantic diagnostics and ROI clipping caveats. master-comparison.png compares exact prior/current poses against original master at shared density and selected idle. Six unchanged poses and endpoints exact; whole two sources reauthored, not colour-only protection. Prior rejected grade sources preserved. build.py resets review metadata on rebuild; preserve/reapply inspection scope. build_helmet.py refits canonical resources; build_paired_review.py restores preview only. Prior native interval belongs to V2, not this revision. See HANDOFF.md.
''',encoding='utf-8')
print(json.dumps(dict(guidanceFiles=6,decodedFrames=16,unchangedBareFrames=6,browserSamples=63,goal='active/incomplete')))
