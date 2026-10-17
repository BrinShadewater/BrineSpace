from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
r=json.loads((P/'master-revision-review.json').read_text());a=json.loads((P/'anatomy-audit.json').read_text());v=json.loads((P/'revision-verification.json').read_text())
assert all(x['unchangedFrames']==[0,1,2,3,4,6,7] and x['decodedFrames']==8 for x in v.values())
heading='Bill South squat original-master pose and restrained matte candidate - October 2, 2026'
body="""Sibling character/bill-water-exit-south-v4 replaces only pose5 in both gears. Seven other bare/helmet poses exactly match precedingV3, including selected endpoint contexts. Original whole-source density148/1295, common320x352 canvas/p160224/H148 retained; no posed-height fitting. Canonical upright shell refitted at native scale1/rotation0. Six bounded body-protection fitting checks and16decodedAPNGframes/holds exact; finite500ms loop1.

First three-reference edit exec-d529bf20-756f-46f9-baf4-f93f67aef7be rejected: head/collar/body enlarged, red unit82 vs master74 and brighter metal. Original-master-only pose exec-5072d35e-5151-455a-b592-b46b85466b3c improves head, but cloth brighter. Same-source material edit exec-9fc905da-a4f5-4f14-8862-958d005c57f2 selected as provisional pose5, darkens cloth while retaining visible fine quilting. All raws/exact prompts/provenance retained. Built-in imagegen edit mode; nondestructive candidate only.

Bounded semantic hair/red diagnostics master135/74, priorV3squat152/77, master-only141/75, graded143/77; neutral bounded-body median master72.67, priorV3squat61, master-only78.33, graded56.33, precedingnearstand59. These are local colour proxies, not complete anatomy or material certification. Material edit opaque bounds [200,289,825,1351] to [199,289,827,1351]; alpha/mask not exact. Treat it as whole-source replacement, not protected colour-only pixels.

Inspected original master, three new raws, fixed-density before/after/master/selected-idle comparison, full16posepaired board, six neck pairs and browser sampled-motion board. Head closer to master and cloth darker; canonical collar connected in inspected source. Squat topology retained, actual contact/camera/segments/head/full grade and moving joins remain provisional. Browser48advancing quarter samples, labels1..6 in each gear; final helmetpose5 paused screenshot. Labels precede screenshots and may cross holds; no exact temporal binding or full normal-speed/native continuity acceptance.

No Godot/profiles accessed this source turn. Prior South4235/0 native interval covers sourceV3 only; this new candidate needs refreshed native evidence. No normal selection/production admission.

Lesson: use original master as sole pose edit target when action references import enlarged anatomy. Independently recognizable chest hardware helps diagnose drawing density. Material-only instructions can still change silhouette/alpha; record whole-source replacement honestly. Enlarging semantic ROIs can switch largest component from hair to face; preserve ROI/edge evidence and never compare those incompatible measurements as anatomy proof.

Next updated South native source bank contact/motion and scratch checkpoint/TitleContinue; remaining cardinal master/contact audits, normal admission/cargo lifecycle and full-library consistency/polish. Full objective active/incomplete.
"""
for rel in ['exit-review.json','helmet-review.json']:
 q=json.loads((P/rel).read_text());q['visualReview']='Inspected full paired source board and six neck pairs; changedpose5 closer to master with darker cloth. Full contact/motion/master acceptance pending.';q['nativeAcceptance']=False;q['normalSelected']=False;(P/rel).write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
 with f.open('rb') as stream:stream.seek(max(0,f.stat().st_size-131072));tail=stream.read()
 if heading.encode() not in tail:
  with f.open('a',encoding='utf-8') as stream:stream.write('\n## '+heading+'\n\n'+body+'\n')
(P/'HANDOFF.md').write_text('# Project handoff\n\n## Objective\nFull Bill animation set matching masters, then full-library consistency/polish. Active/incomplete.\n\n## Accepted decisions\nOriginal source drawing density, canonical equipment, nondestructive candidate; preserve normal selections and owner profiles.\n\n## Current state\n'+body+'\n## Changed files\nVersioned source raws/prompts, build.py/build_helmet.py/anatomy_audit.py/build_paired_review.py, verify_revision.py, frames/manifests/APNGs, source/neck/master boards, browser screenshots/metadata, review/provenance, record_milestone.py and six guidance files. Copied previous AUTHORING and prior-v3-record_milestone.py are historical, not current native evidence.\n\n## Verification\nSeven unchanged poses per gear;16decoded frames/holds, endpoints exact;6bounded canonical fits. Source visual inspection and48quarter samples only. No refreshed native/profile interval for this bank.\n\n## Next action\nRefresh South native contact/motion with this candidate, then scratch resume and normal admission when remaining visual fidelity is established; complete full-library polish.\n',encoding='utf-8')
print(json.dumps(dict(changedPose=5,unchangedPerGear=7,decodedFrames=16,guidanceFiles=6,nativeAcceptance=False,goal='active/incomplete')))
