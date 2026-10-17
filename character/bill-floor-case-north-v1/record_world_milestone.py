"""Record reviewed staged world contact, separately from normal lifecycle admission."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-floor-case-world-v1'
d=json.loads((O/'records.json').read_text(encoding='utf-8'));v=json.loads((O/'validation.json').read_text(encoding='utf-8'))
assert v['passed'] and not v['realProfileChanges'] and d['failures']==0 and len(d['records'])==12
inputs=json.loads((P/'registration.json').read_text(encoding='utf-8'))['protectedInputs']
for name,digest in inputs.items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest
files=list(inputs)+['scripts/bill_carry_player.gd','scripts/bill_carry_npc.gd','scripts/crew_sprite_player.gd','scripts/grid_canvas.gd','scripts/room_content_canvas.gd','scripts/main.gd','character/bill-floor-case-north-v1/workshop_preview.gd','character/bill-floor-case-north-v1/floor-case-north.png','tests/test_bill_floor_case_world_v1.gd','tools/run_bill_floor_case_world_v1_validation.py']
hashes={name:hashlib.sha256((R/name).read_bytes()).hexdigest() for name in files}
(P/'world-input-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
evidence={'validation':v,'records':d,'reviewer':'Codex agent','visualReview':'All12native room/source presentations and both fixed-anchor boards reviewed. Original terminal case is visible between boots; staged idle retains a case hint, and departure reveals the complete prop at unchanged floor location. Captured body/head/helmet and matte suit retained. New prop geometry/material are inferred; sparse static samples do not certify full temporal join/contact.','normalSelectionChanged':False,'candidateRenderer':'workshop_preview.gd explicitly selected only by fixture; prop in actual retained sorted room queue. Physical foot local anchor, source baseline220 vsactor224 gives1.764324room-unit depth behind standing actor. No extra crew shadow or globally elevated draw layer.','scope':d['scope'],'failuresRetained':'Initial compile conflict PIXEL_SCALE in inherited room renderer; stopped exact fixture process, no owner changes. Second strict depth check failed because fixture double-added14.592visual offset. Corrected physical anchor; strict guard retained. Failed logs/validation archived; no failed capture-retention claim.','sourceProtection':'Four recorded native/master input hashes unchanged. New broader hash list post-run; no prelaunch freeze claim.','remaining':['Normal world ownership/lifetime/room-removal and save/Continue admission','Continuous terminal join/contact and full motion review','Cardinal service-loss carry return and priority','Remaining action/equipment/full-family polish']}
(P/'world-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
section='''## Bill staged fixed floor-case native contact — October 2, 2026

Unselected workshop_preview.gd inserts the generated North case as a normal
retained sorted prop. Physical room-local foot anchor stays fixed; source floor
baseline220/pivot224 places sort depth1.764324room units behind standing Bill.
No crew-sized prop shadow, forced global layer, actor/raster/geometry changes.
Fixture selects only the workshop renderer; normal Bill actor/player and actual
generated cargo route/next-activity departure stay live under actor60Hz stepping.

217native checks/0fail, engine0/49.32s; both gears,12native room/source pairs.
Terminal, idle baseline, staged idle and8/24/48unit departure captures reviewed;
both fixed-floor-anchor boards viewed. Case stays at unload point and reveals
as Bill leaves. Captured stature/head/helmet/matte body remain coherent. New
case geometry/material inferred from occluded source; static samples do not
certify complete continuous join/support. All2931owner non-log files unchanged
under scratch APPDATA;4recorded source/master hashes unchanged. Broader hash
snapshot post-run, not prelaunch-frozen. No normal selection, world lifetime,
room-removal/ownership, save/Continue or interruption admission yet.

First fixture compile failed on inherited PIXEL_SCALE name; exact fixture process
stopped, profile unchanged. Second fixture execution failed strict depth guard:
fixture added14.592world visual bias already cancelled by main/grid transforms.
Corrected to actual physical foot; strict guard retained. Failed logs/validation
archived, no failed-capture preservation claim. Final anchor equals actor at
(-112,128), prop126.235676 before actor128, retained slots1before2, both gears.
Lesson: derive final draw anchor through actual consumer transforms and review
physical/root/depth separately; do not paste a generic screen offset onto props.
Next normal candidate world lifetime/save/Continue policy, continuous unload join,
source-bound service-loss return and remaining Bill set/cross-family polish.
Full goal incomplete. Review:character/bill-floor-case-north-v1/world-review.html;
NATIVE_HANDOFF.md. No commit/export.

'''
for file in [R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 s=file.read_text(encoding='utf-8')
 if section.splitlines()[0] not in s:file.write_text(section+s,encoding='utf-8')
lesson='''
## Floor prop anchor through the actual crew consumer — October 2, 2026

Main's crew position subtracts.038cell, and grid's room transform adds it back.
A prop copied from physical foot must not add that14.592world-unit bias again.
Check the final submitted room actor/root and prop depth before changing art or
weakening a sort guard. Bill staged case source baseline220/pivot224 is1.764324
world units behind actor at65.28/148scale. Use the actual retained prop queue,
not an extra actor/crew shadow or a global foreground overlay. Fixed floor anchor
must stay unchanged as the normal next activity moves the actor away. Two gears,
217native guards/12reviewed pairs show fixed48unit departure here; no normal
lifetime/save/Continue or full continuous-motion acceptance follows from that.
Evidence: character/bill-floor-case-north-v1/world-evidence.json.
'''
for file in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 s=file.read_text(encoding='utf-8')
 if lesson.splitlines()[1] not in s:file.write_text(s+lesson,encoding='utf-8')
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill fixed case world study

## Objective and acceptance
Complete master-matched Bill set and full cross-family motion/material polish.
Floor cargo must remain coherent through unload/idle and departure.

## Accepted decisions and constraints
Staged fixture-only workshop renderer, normal Bill actor/player unchanged.
Preserve owner geometry, source version policy and scratch APPDATA. No export.

## Current state
workshop_preview.gd/UID injects a separate floor prop into actual retained sorted
room queue. Source anchor is actual room-local foot; case220/actor224baseline.
Added native test/UID, runner, preparation/board/evidence helpers. Original12room/
source pairs copied into world-captures; world-review.html retains fixed focus.
Updated current status/continuation/pipeline/bible and both skill references.

## Verification
217native checks0fail/49.32s, engine0, both gears. Actual generated workshop route
and normal next-activity departure, paused world/actor60Hz. Case remains fixed
through8/24/48unit departure, behind stationary boots. All12presentations/two
boards reviewed: captured stature, head/helmet/matte body consistent. Four source
hashes unchanged; wider hashes post-run. All2931owner non-log files preserved.
Prior compile collision and double-offset depth failure retained as logs/reports;
fixed fixture with strict depth guard intact. No continuous film/contact claim.

## Next action
Define staged world lifetime/ownership and room-removal behavior; pair saved
floor anchor with ordinary save/Continue. Review continuous terminal source join.
Then cardinal carry service-loss return/priority and remaining equipment/actions,
full cross-family motion/master/grade polish. Normal floor prop not selected;
full goal active/incomplete. Source study HANDOFF.md remains historical evidence.
'''
(P/'NATIVE_HANDOFF.md').write_text(handoff,encoding='utf-8')
print('Staged native fixed-anchor milestone recorded; normal selection unchanged.')
