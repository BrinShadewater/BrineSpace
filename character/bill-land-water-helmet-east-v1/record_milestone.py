from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;B=R/'character/bill-land-water-east-v3'
note='''## Bill paired East land/water source bridge — October 2, 2026

V3 replaces only final compact-knee interior; five other V2 poses remain exact
RGBA. Same .27 anatomical scale and frozen V2 neutral curve applied once to
replacement. Final leg shape approaches original compact swim endpoint more
closely in static review; no continuous/native join acceptance. Initial alpha
threshold180 included broad high-alpha halo; >250 core plus3px connected fringe
retains body without that halo. Separate built-in alpha edit shifted/enlarged
figure and was rejected; raw source/prompt retained, never used.

New unselected bill-land-water-helmet-east-v1 fits original shared native East
helmet component at scale1/rotation0 to all four protected V3 bodies. Exact
normal-loaded equipped idle0/swim0 padded using recorded pivot/H148; decoded
hash bindings verified. All pixels outside explicit head region, foreground arm
and shoulder, and body below component remain exact. First enlarged view exposed
collar masking shoulder badge; foreground shoulder restored before final review.
Original donor shell/face/material unchanged; no body repaint or pose rescaling.

Both paired source directions preserve six poses/500ms; all12helmet APNG decoded
frames exact. Bare12decoded frames, five retained poses and timeline checks pass.
Final whole-figure paired board, enlarged neck/shoulder crops and82/54/27density
boards viewed. Technical package/static visual evidence only; no Godot run this
interval or production selection/controller/renderer/owner profile changes.

Lesson: protect foreground shoulder insignia as well as sleeve during canonical
helmet fitting. Alpha thresholds must follow actual source alpha distribution;
an alpha-only generation can still alter position/size and must fail preservation.
Next exact live walking-phase entrance, finite clock/medium/collision admission,
moving native joins, priorities/Continue, cardinal expansion and full library
master/polish. Exit remains reverse-derived; inherited all-wet source metadata
is placeholder, not accepted runtime classification. Full Bill goal incomplete.
Review: character/bill-land-water-helmet-east-v1/index.html. No commit/export.

'''
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 file=R/rel;file.write_text(note+file.read_text(encoding='utf-8'),encoding='utf-8')
for rel in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 file=R/rel;file.write_text(file.read_text(encoding='utf-8')+'\n'+note,encoding='utf-8')
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
installed.write_text(installed.read_text(encoding='utf-8')+'\n'+note,encoding='utf-8')
handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Bill paired East land/water bridge

## Objective and acceptance
Full master-consistent Bill set and cross-family polish. This source milestone
does not complete native transition or full-set acceptance.

## Accepted decisions and constraints
Preserve original endpoints, fixed anatomical scale, matte grade and native
shared helmet; no mirrored anatomy, per-pose height fitting or body repaint.
Existing reversible-work authorization applies; preserve other actors/owner data.

## Current state
Bare V3 compact-knee repair plus helmet V1 protected-component fitting. Build,
registration, source evidence, APNGs and paired/neck/density review files retained.
V3 source alpha attempt rejected for preservation failure. Shoulder-mask overlap
found in first helmet view and corrected through original foreground restoration.
Pipeline/bible/maintained and installed skill lessons/current status updated.

## Verification
Five bare poses RGBA-exact to V2. Exact normal-loaded equipped endpoints bound
to decoded metadata. Four protected-body/foreground checks; helmet native scale1,
rotation0. Both six-frame APNGs decode exact/original500ms. Whole figures,
enlarged joins and82/54/27density reviewed. No Godot run or normal selection.

## Next action
Stage exact live walk-phase entrance and finite-clock/medium/collision-aware
dispatch, then native moving joins, safety/gear/Continue and all cardinals.
Reverse-derived exit and placeholder all-wet classification require deliberate
validation. Water material admission, cargo lifecycle and full-set polish remain.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8');(B/'HANDOFF.md').write_text(handoff,encoding='utf-8')
e=json.loads((P/'helmet-registration.json').read_text());e['staticVisualReview']='Final paired whole figures, enlarged neck/shoulder/arm crops and82/54/27density inspected; collar badge overlap corrected. Native motion/support/continuous join unproven.'
(P/'helmet-registration.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
print('Paired source milestone and alpha/shoulder preservation lessons recorded; full goal remains incomplete.')
