from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent
e=json.loads((P/'review.json').read_text(encoding='utf-8'))
h=json.loads((P/'helmet-registration.json').read_text(encoding='utf-8'))
assert e['decodedPairedAPNGFramesExact']==14 and len(e['registrations'])==5
assert h['decodedAPNGFramesExact']==7 and len(h['frames'])==5
note='''## Bill independently articulated West water exit source — October 2, 2026

New unselected character/bill-water-exit-west-v1 provides five new exit poses:
low bent elbow/palm plant, higher palm push, hands-and-knees tuck, half-kneel,
near-standing rise. Not reversed entrance or mirrored East artwork. Seven poses
per gear500ms, holds60/50/60/70/100/100/60. Exact V4 standing/swimming endpoint
contexts padded320/p160224/H148; these are static contexts, not dynamic actual
gait-boundary proof. Full Bill goal active/incomplete, normal selection unchanged.

Built-in imagegen raw/prompts saved locally immediately. Generations:
low-elbowV2 exec-134922ab-ad2c-4206-9aeb-f780df4bba6e,
palm-pushV1 exec-6465e38a-c512-44d5-930c-c57a6b4c4621,
knee-tuckV1 exec-7605a6b8-faea-43ff-8e93-672ac9b06c94,
half-kneelV1 exec-0d91d7ff-e11a-4c95-ac05-d2a0609c0389,
riseV2 exec-9dc957e9-ac5d-4978-909d-7ad92100511e.
Rejected low elbowV1 exec-da3e75a8-5a64-4442-bc9b-44e8c803e555 expanded
head/body and boot spread; target-only narrow retry retained composition more
closely. First high palm pose kept later in sequence rather than passed as low.
RiseV1 exec-abb53574-6d53-42bd-a6e3-ce6cb5daf0ee enlarged head and insufficient
knee bend; anatomical source edit V2 reduces head and lowers through joint bend.
Prompt wording does not prove unchanged source pixels or anatomical lengths.

All actual1254square→320wholecanvas scale0.2551834131, largest opaque component
plus3px fringe, wholepose translations to shared support224 and explicit crowns
131172/130160/133150/147120/15792. No per-pose height/width fit or limb rotation.
Support alignment is a source drawing convention, not proof of physical floor
contact or buoyancy: normal navigation anchor and water depth remain distinct.
Seven bare APNGframes/holds exact and seven helmet APNGframes/holds exact.
Fourteen alpha160figures connected; diagnostic, not anatomy/motion acceptance.

Canonical original West40x40shell native scale1/rotation0, five protected fits;
two old normal helmet endpoint contexts retained RGBA exact with inventory pivot
checks. Initial inherited head erase polygon removed collar pixels behind shell:
native5x neck crops exposed gaps even though outside-mask/body checks passed.
Tightened erase mask and foreground-right collar restoration at crown(+8,+23);
neck crops re-reviewed, joins better. Body outside allowed head pixels and below
shell/foreground protections exact. Mask is source-family-specific; do not copy
this threshold as universal anatomy. Original master/shared ruler, all paired
poses and neck crops reviewed. Interior matte quilting/insignia/detail closer;
face warmth/head fidelity, normal endpoint materials, support trajectory and
continuous full-speed motion remain pending. No in-game exit/clearance/wet
material/interruptions/checkpoint/Continue validation, no normal admission.

Reproducible build.py/build_helmet.py/build_review.py, manifests,14frames,
two source APNGs, provenance/diagnostics/master+paired+neck boards and paused
paired player saved. Player duration derives from matching gear manifests,
plays one500ms action per click; do not judge its reset as a locomotion loop.
No Godot test/profile access this interval. Previous3051-check corrected V4
West entry proof preserved; it does not cover this new exit candidate.
Review:character/bill-water-exit-west-v1/index.html. Handoff same folder/HANDOFF.md.

Lesson: pose support and material can look good while scale/identity drifts.
Reject enlarged local edits; preserve raw, retry narrowly, compare common density.
Near-standing size errors need anatomical source repairs rather than whole-body
resize. Allowed-mask assertions can still erase a collar inside the mask: inspect
head/neck/shoulder crops and preserve actual garment joins around canonical shell.
Next exit full motion/endpoint master consistency, current-bank native entry+exit,
interruptions/checkpoint/Continue, North/South bridges, cargo lifecycle and full
Bill cross-family master/style/perspective/size/proportion/matte-grade polish.

'''
h['visualReview']='Complete paired and native5x head/collar crops reviewed after collar mask repair; joins retained. Full master identity/material and continuous station motion pending.'
(P/'helmet-registration.json').write_text(json.dumps(h,indent=2)+'\n',encoding='utf-8')
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
    p=R/rel;t=p.read_text(encoding='utf-8')
    if heading not in t:p.write_text(note+t,encoding='utf-8')
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    t=p.read_text(encoding='utf-8')
    if heading not in t:p.write_text(t+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2,2026 · BrineSpace · Bill separate West water exit source

## Objective and acceptance
Complete Bill set matching original masters, style, perspective, anatomy, scale
and matte grade, followed by cross-family polish. Full goal remains incomplete.

## Accepted decisions and constraints
Original RIGHT master faces West/LEFT. New articulated exit, no reversal/mirror.
Common320/p160224/H148, wholecanvas density and wholepose translations only.
Canonical native helmet, pose-specific collar protection. Preserve concurrent
crew/owner data and previously verified V4 West entry proof.

## Current state
New bill-water-exit-west-v1: five new interior source poses, bare/helmet seven
frames500ms; raw/prompts/rejected candidates, builders/manifests/APNGs, review
JSON/master+paired+neck boards and paused one-shot player. Six guidance files
updated with source repair/registration/mask lessons. Normal runtime unchanged.

## Verification
14decoded APNGframes/holds exact, exact endpoint contexts, all painted support
retained during registration. Five helmet fits protect body/foreground;14alpha
connected diagnostics. Master/common-scale/paired/neck boards reviewed; larger
low pose rejected, rise head/knees repaired, collar erase gap corrected.
No native exit or physical support/source-phase/material proof. Full identity,
normal endpoint grade/detail and continuous motion acceptance remain pending.
No Godot/profile access. Existing entry3051check proof covers entry only.

## Next action
Full-motion exit and endpoint comparison; native paired entry/exit with exact
loaded bank assertions/frozen normal sources. Then interruption/Continue and
North/South bridges, cargo lifecycle and full Bill cross-family polish.
''',encoding='utf-8')
e['sourceMilestoneRecorded']=True
e['rawAndPromptSHA256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (P/'sources').iterdir() if p.is_file() and ('canvas' in p.name or 'prompt' in p.name)}
(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
print('Recorded separate West exit source candidate and open acceptance scope in six guidance files.')
