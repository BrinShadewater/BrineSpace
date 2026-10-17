from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;H=P.parent/'bill-water-exit-helmet-east-v1'
note='''## Bill lower water-exit midpoint and paired helmet — October 2, 2026

New V2 inserts one lower articulated pose between V1 tucked-swimmer interior
and planted kneel. New two-midpoint generation enlarged anatomy and was rejected;
direct edit of original top-right source preserves useful source scale. Both raws/
exact prompts retained. Only edited component used; six original V1 packaged
poses copied RGBA-exact, no dependence on generated preservation of other figures.
Same.24body scale, frozen entryV2neutral grade once on new midpoint, alpha>250/
3pxfringe. First90ms interior split45/45, original500ms retained. Seven decoded
APNGframes exact; crown181->145->108 replaces73px rise with36/37px increments.
Original-master/full sequence and82/54/27density boards inspected. Pose progression
improved, not full continuous/support/contact/master acceptance.

New paired helmet exit retains exact normal captured swim2/walk0 endpoints and
all five authored bare bodies. Immutable native shared East helmet scale1/rotation0;
explicit head erasure only, body outside head region, front shoulder/badge/arm and
below-component pixels asserted exact. SevenAPNGframes decode exact/500ms.
Paired whole figures/enlarged neck-shoulder crops viewed; shell identity stable,
no new observed badge erasure. Captured endpoints are30Hz samples from actual
normal route; no exact60Hz runtime transition or future gait phase admission.

No Godot run/native bridge/production selection/renderer/controller or owner
profile changes. Medium/contact metadata intentionally unassigned. Next staged
finite clock with exact live outgoing phase and target gait handoff (bare grid
clock versus helmet player), collision/support/material/native moving joins,
priority/gear/death/Continue, other cardinals; full master/cross-family polish
and cargo lifecycle remain. Full Bill goal active/incomplete. No commit/export.

Lesson: explicit numeric anatomical size is insufficient in loose generative
atlas composition. Direct original-cell pose edit gives a stronger scale ruler;
freeze other packaged poses rather than trusting pixel preservation. Subdivide
existing hold for inserted source timing, but smaller crown gaps do not prove
anatomical/contact smoothness. Reviews:character/bill-water-exit-east-v2/index.html
and character/bill-water-exit-helmet-east-v1/index.html.

'''
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 f=R/rel;f.write_text(note+f.read_text(encoding='utf-8'),encoding='utf-8')
for rel in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=R/rel;f.write_text(f.read_text(encoding='utf-8')+'\n'+note,encoding='utf-8')
f=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md');f.write_text(f.read_text(encoding='utf-8')+'\n'+note,encoding='utf-8')
handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Bill lower water-exit midpoint/helmet pair

## Objective and acceptance
Full Bill set follows original masters in identity, perspective, proportions,
size/material, then cross-family consistency and polish. Source milestone only.

## Accepted decisions and constraints
Preserve exact original endpoints/bodies, common scale, frozen matte curve,
native shared helmet; no per-pose normalization/rigid rotation/body repaint.
Existing reversible-work authorization; preserve other actors and owner profile.

## Current state
Bare exitV2/build, two prompts/raw attempts, seven poses/manifest/registration,
master/density/APNG review. Rejected enlarged two-midpoint draft kept. Direct
top-right source edit supplies only one new pose; six originals remain exact.
Helmet exitV1/build, native donor crop, five protected bodies, actual sampled
normal endpoints, paired/neck/APNG review. Records/pipeline/bible/skills updated.

## Verification
Seven bare frames decode exact/500ms; original six RGBA exact. Shared.24scale/
frozen neutral curve. Seven helmet frames exact/500ms, body outside explicit
head region, shoulder/arm/below-component exact; helmet scale1/rotation0.
Master+game densities and paired whole figures/enlarged neck crops reviewed.
First crown rise split36/37pixels; no continuous/native/contact acceptance.
No Godot run, owner profile access or normal production changes.

## Next action
Stage exact60Hz outgoing walking/swimming phase, finite playback clock, destination
gait restart/handoff and collision/support/medium/material; native moving joins.
Different bare/helmet walking clock paths must coordinate. Gear/death/priorities/
Continue, all cardinal bridges, cargo lifecycle and full-library polish remain.
Full goal active/incomplete; no commit/export.
'''
for folder in [P,H]:
 (folder/'HANDOFF.md').write_text(handoff,encoding='utf-8')
 file=folder/'registration.json';e=json.loads(file.read_text());e['sourceFrameSHA256']={x.relative_to(folder).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in (folder/'frames').rglob('*.png')};e['staticVisualReview']='Whole poses and enlarged neck/shoulder or original-master/density views inspected; initial source progression improved. No continuous/native/contact acceptance.';file.write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
print('Paired seven-pose source milestone/scale-preservation lesson recorded; full goal incomplete.')
