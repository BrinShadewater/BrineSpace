from pathlib import Path
import json,hashlib,os,uuid,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'stance-inbetween-v38';motion=p/'motion-review-v37'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((motion/'inputs.json').read_bytes())
assert all(sha(r/f)==v for f,v in inputs['sourceSha256'].items())
original=json.loads((p/'finite-bridge-v36/inputs.json').read_bytes())
normal={f:v for f,v in original['preLaunchSha256'].items() if f in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json']}
assert len(normal)==2 and all(sha(r/f)==v for f,v in normal.items())
report=json.loads((out/'review.json').read_bytes())
report.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='rejected_standing_like_stance_does_not_bridge_profile_change',findings=['Raw, paired whole and enlarged leg comparisons actually reviewed. New legs remain broad and standing-like; near boot does not provide the requested inward progression to V20. Pixel differences do not establish chronological motion.', 'Upper head/case above147 exact and59218 pixels outside admission exact; protection checks certify packaging only. No native run or adoption warranted for rejected source.', 'Browser V37 stepped all four forward poses and inspected reversed first endpoint. Original playback observations show advancement/loops but do not certify continuous visual inspection of all49 walking frames.'],fullGoalComplete=False)
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n')
(out/'generation-index.json').write_text(json.dumps(dict(state='terminal_copied',rawSha256=sha(out/'raw.png'),promptFile=(out/'prompt.txt').relative_to(r).as_posix(),inputsFile=(out/'inputs.json').relative_to(r).as_posix(),disposition=report['disposition'],normalChanged=False),indent=2)+'\n')
motion_review=dict(sourceSha256=inputs['sourceSha256'],browserForwardSlotsReviewed=[0,1,2,3],browserReverseSlotsReviewed=[0],continuousVisualMotionReviewed=False,sourceAcceptance=False,normalChanged=False,previewServerSession=88016,previewServerTerminal=True,temporaryBrowserTabClosed=True,findings=['First leg transition visibly changes a broad two-boot stance into a narrow profile in one step.', 'V35 upper pose still carries a broader case than V16 walk0; case and chest projection change at final join.', 'Standing carry has a more three-quarter body projection than side-on walking. Assess coherent body/case rotation together; a leg-only weight-shift prompt does not resolve the whole-view discrepancy. Case shrink may include projection, so do not infer physical rescaling from screen width alone.', 'V38 generated intermediate rejected as standing-like after paired native-source comparisons. No normal dispatch/room/Continue evidence added.'],fullGoalComplete=False)
(motion/'review-acceptance.json').write_text(json.dumps(motion_review,indent=2)+'\n')
section='''### James carrying projection and first-step review — October 2, 2026

V37 browser review stepped all four paired preparation poses and inspected the
reversed first endpoint. Previous playing observations demonstrate advancement,
not uninterrupted inspection of all49 walking frames. First stance change remains
abrupt. Standing carry projects more three-quarter than side-on walking; final
case/chest projection changes at the join. Compare coherent body rotation and case
orientation together. Screen-width changes alone do not prove physical resizing.

V38 builtin leg-only weight-shift source generated, copied, normalized once and
packaged with59218 outside pixels/head/case above147 exact; paired body below110
exact. Raw and paired whole/enlarged-leg boards actually reviewed. Rejected: remains
standing-like and does not provide the requested inward stance progression. Pixel
differences and preserved boundaries do not certify chronological advancement.
Do not lengthen playback or add this pose merely to hide the failed view transition.

Normal grid/ACTIVE_ASSETS hashes exact to V36; current cargo binding unchanged.
Preview server88016 terminated after review, temporary tab closed, generation
terminal/copied; no Godot run or owner-profile access this review. Full set unfinished.
Next use coherent actual turn anatomy to bridge body/case projection, then inspect
full chronology, native scale and actual cargo/rooms/interruptions/Continue before
versioned adoption. Preserve V30 selected diagnostic cleanup and V31 inventory.
Evidence:character/james-west-carry-walk-keys-v1/motion-review-v37/review-acceptance.json;
character/james-west-carry-walk-keys-v1/stance-inbetween-v38/review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index(b'### James West finite carrying preparation candidate');new=old[:at]+entry+b'\n'+old[at:]
    else:new=old+b'\n'+entry
    tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert f.read_bytes()==old;os.replace(tmp,f)
handoff='''# Project handoff

Updated: October 2, 2026 · James carrying projection review

## Objective and accepted decisions
Complete master-matched James set and full consistency polish. Incomplete.
Matte original masters, correct equipment, fixed height/ground registration.

## Current state and changed files
V37 local review page and exact52 paired frame images retained; browser stepped all
four forward poses. V38 leg weight-shift trial rejected after raw/paired source review.
New prepare/package/close helpers and review records retained, five guides updated.
Normal loader/registry/cargo binding remain unchanged; no commit/PR/export.

## Verification and limitations
V38 upper/head/case above147 and59218 outside pixels exact, paired body below110
exact. Technical packing passes, visual chronology fails. No native/room test for
rejected source. V37 observed playback advancement does not establish continuous
all-frame visual review. Server88016 terminal, temporary browser tab closed and
generation terminal/copied. No real owner save access.

## Next action
Bridge actual body/case projection coherently: standing is more three-quarter than
side-on walking. Review an actual turn anatomy guide rather than repeatedly asking
for a vague fractional leg shift. Then full motion/native scale, normal cargo rooms,
distance/gear/interruptions/Continue and versioned adoption, followed by full-set polish.
'''
(out/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in [out,motion] for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(x.encode() for x in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(v38Disposition=report['disposition'],guidesUpdated=5,lfsRasters=len(rasters),normalChanged=False,continuousVisualReview=False,fullGoalComplete=False)))
