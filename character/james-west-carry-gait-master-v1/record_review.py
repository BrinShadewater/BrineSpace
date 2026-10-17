from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
for name in ['contact-a','contact-b','contact-a2']:
    inputs=json.loads((p/(name+'-inputs.json')).read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
    f=p/(name+'-review.json');data=json.loads(f.read_bytes());assert data['protectedOutsideExact'] and data['protectedOutsidePixels']==60960
    data.update(visualReviewPending=False,disposition='rejected_opposite_phase_costume_reassignment' if name=='contact-a2' else 'provisional_same_leading_leg_contact',findings=['Raw and full/detail/station comparison inspected.60960outside lower-body pixels exact; head/torso/case/grip/hips retained.','Gold-seamed image-right leg trails in both A and B; these are NOT opposite phases. A2 keeps same leg geometry but relocates gold seam onto other leg, including upper raw thigh; retained upper pixels expose seam discontinuity.','No complete gait packaged or selected. Native cadence, upper-body carrying dynamics, pickup/unload joins and all other directions remain pending.'])
    f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
section='''### James master-based West cargo contact ownership study — October 2, 2026

character/james-west-carry-gait-master-v1 starts from master-based bare West turn
endpoint (james-carry-headcaps-v1/frames/004.png). Three builtin generated88square
lower-body crops packaged at original density, no fit/regrade. Admission88,172..
176,224 leaves60960outside pixels exact, including master face/torso/case/grip.
All raw/full/detail/station comparisons reviewed and frozen input hashes stable.

A and B contact drafts both advance the plain far leg and trail the gold-seamed
near leg; distinct pixels do not prove alternating gait. A2 explicit ownership
request changes costume instead: same leg geometry, gold seam relocated to far
leg/upper raw thigh; retained upper pixels expose seam discontinuity. A2 rejected,
A/B provisional same-contact studies only. No full gait/manifests/native/selection.
Do not report opposite phases or smooth movement from these sources.

Lesson: inspect limb ownership before requesting opposite phase. A seam landmark
is evidence only when continuous from original hip through thigh/knee/shin; seam
reassignment is not gait alternation. Fixing knees/upper thighs outside admission
can encourage costume swaps instead of a real advancing thigh. Next expand
articulation crop/admission up to hip/thigh roots below case, keep upper body/case
exact, independently redraw real opposed contacts and passing poses. Review
anatomy/costume/contact/material before clocked motion and cargo context testing.
Full master-matched James set and cross-family polish remain active/incomplete;
normal cap/V9/riseV6/caseV7/save bindings unchanged.
Handoff:character/james-west-carry-gait-master-v1/HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':at=old.index(b'### James paired carrying turn');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);assert old==path.read_bytes();os.replace(tmp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West cargo gait

## Objective and acceptance
Full master-matched James animations, then cross-family polish. Active/incomplete.

## Accepted decisions and constraints
Use master-based West carried pose/common256/p128224/body148. No mirroring,
perpose fit/grade, or costume swapping to claim opposite gait. Preserve selections.

## Current state
prepare.py, prepare_b.py, prepare_a2.py and deterministic package helpers;
three raw/prompt/input pairs and native crop/full/contact comparisons. A/B both
plain far leg forward/gold near leg trailing, provisional same-contact sources.
A2 REJECTED: same leg geometry with relocated seam, not opposite step.
record_review.py closed reports and updated five guides. No gait bank/manifest.

## Verification
All three raw/full/detail/station boards inspected.60960outside admitted88x52
pixels exact; upper body/case/grip/head retained. Three pre-call inventories stable,
rasters LFS. No Godot run/profile changes, full gait cadence/context untested.
Original A-leading-leg mismatch missed before B request; recorded, not hidden.

## Next action
Expand local crop/admission to thigh roots below case (current y172 cut locks
upper knees); retain actual hip/costume ownership while advancing full near leg.
Generate true opposed contact plus passing poses; review all anatomy/feet/seam
continuity/matte grade, then body dynamics/helmet pair, gait joins, native cargo
room/interruptions/Continue/versioned admission. Finish other cardinals/full set.

## Source provenance
Builtin A exec-b81cf3c8-6804-466b-9ebd-4cb68ad99e19;
B exec-3d518c9e-be8c-41be-9f79-5e145052242b;
A2 exec-0dd6999c-826f-4768-97bf-750faa3b5268.
Saved contact-a/contact-b/contact-a2 raw.png, prompt.txt, inputs.json;
local deterministic crops only, no geometry fitting or pixel painting.
''',encoding='utf-8')
print('Three generated contacts reviewed; false alternation rejected; five guides/handoff updated. Full goal incomplete.')
