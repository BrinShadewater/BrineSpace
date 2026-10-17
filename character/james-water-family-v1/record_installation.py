from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
def atomic(path,fn):
 before=path.read_bytes();after=fn(before);tmp=path.with_name(path.name+'.james.tmp');tmp.write_bytes(after)
 if path.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
 tmp.replace(path)
for name in ['native-installed','native-installed-routes']:
 report=json.loads((P/(name+'-validation.json')).read_bytes());assert report['exitCode']==0 and report['realProfileUnchanged']
entry='''## James directional water family installed - 2026-09-30

Installed16 tread/swim/start/stop states,96 bare+96 shared-helmet references.
Literal paired manifests selected by the normal James grid loader and registry.
Selected-alpha world65.28px clearance replaces swim/tread profiles; transition
profiles include new starts/stops and actual retained water turns, preserving the
prior conservative envelope. Other action profiles unchanged. Render anchor's
subtract/add0.038-cell adjustments cancel; no extra world offset was introduced.
2054 actual installed loader/clock/transition checks and2029 installed route checks
PASS, zero failures; scratch profiles unchanged. Eight real routes in authored
maintenance/storage rooms, both modes/four initial facings; north uses connected
south pair in reverse. Actual NPC lazy clearance verified; camera-following native
captures and actor-on/off visibility reviewed. East start touches a nonblocking
console prop rectangle for two samples; no navigation blocker contact, native
image gap reviewed. This is not full flood/exterior/traffic or all-layout proof.
Inventory now52 retained bare states. Water turns/cargo/pickup, salvage/distress/
recovery/death and cross-family polish remain. Owner acceptance remains pending.
Arrival activity chooses east, so non-east swim->stop facing snaps remain a noted
cross-family behavior/animation polish item, not certified smooth by route arrival.
See docs/JAMES_WATER_HANDOFF_2026-09-30.md and family/station-review.gif.

'''
lesson='''

### James water clearance and real-route verification - 2026-09-30

Derive conservative visible alpha bounds from the selected frames at65.28/native
standingHeight and their actual pivot. Track retained water turns in transition
envelopes until their artwork is replaced. Inspect the complete coordinate chain:
James main position subtracts0.038 cells and the renderer adds it back, so the
world anchor is exactly NPC.foot. Adding only the draw adjustment would shift
collision incorrectly. Staged data injection does not prove installed lazy NPC
clearance or normal grid selection; rerun those paths after paired installation.
Native capture framing is part of the review: UI covered south destinations and
north starts in the first board. Recenter on the actor and compare actor on/off;
retain rejected framing. Use the actual authored default layout in current-room
proof, not an empty defaults file intended for a retained furniture fixture.
Navigation blockers and the complete prop rectangle list have different meaning:
James east start has91/61 nonzero-alpha pixels in a nonblocking console rectangle,
with no nearby navigation blocker and a visible art gap in reviewed native images.
Report those contacts rather than shrinking sprites, removing furniture or declaring
all prop rectangles collision. A completed route can still change activity facing:
arrival chooses east and non-east swim->stop snaps remain for cross-family polish.
Mutable NPC paths empty on arrival; save route size before assigning a duplicate.
Player.motion retains an empty clip entry after completion; observe that field,
not Dictionary.is_empty(), to stop a route fixture. Changing fixture profiles
requires clearing swim-link/reach caches before comparing retained behavior.
Evidence: docs/JAMES_WATER_HANDOFF_2026-09-30.md.
'''
for rel,text,prepend in [('docs/CURRENT_STATUS.md',entry,True),('docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',entry,False),('docs/ASSET_PIPELINE_AND_WORKFLOW.md',lesson,False),('docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',lesson,False),('skills/brinespace-character-pipeline/references/crew-consistency.md',lesson,False)]:
 path=R/rel;marker=text.strip().splitlines()[0].encode()
 if marker not in path.read_bytes():atomic(path,lambda b,t=text.encode(),p=prepend:t+b if p else b+t)
path=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if lesson.strip().splitlines()[0].encode() not in path.read_bytes():atomic(path,lambda b:b+lesson.encode())
def selection(b):
 m=json.loads(b);m.update(status='installed_owner_review_pending',runtimeInstalled=True,routeVerification='installed-route-evidence.json',routeVisualReview='native-installed-route-contact.png',pending=['Water turns and carrying water families','Salvage/distress/recovery/death families','Cross-family material/anatomical/motion consistency and polish','Non-east route arrival facing continuity (activity selects east before swim stop)','Owner review; production-wide flood/exterior/traffic scope unproven']);m['verification'].update(installedLoaderChecks=2054,installedRouteChecks=2029,installedRoutes=8,failures=0,realProfileUnchanged=True);return (json.dumps(m,indent=2)+'\n').encode()
atomic(P/'selection.json',selection)
baseline=P/'retained-clearance.json'
if not baseline.exists():baseline.write_text(json.dumps(json.loads((P/'clearance-evidence.json').read_bytes())['prior'],indent=2)+'\n')
handoff='''# Project handoff

Updated: 2026-09-30 · Project: C:/Users/Alex/Documents/Brine Space · Task: James directional water family

## Objective and acceptance
Continue the full master/style/perspective/scale/proportion/material-matched set,
then cross-animation consistency/polish.16 water states now installed bare/helmet;
full-set goal active, owner acceptance pending.

## Accepted decisions and constraints
Matte graphite/silver/muted gold; fixed asymmetric belt wrench/backpack; independent
facings. Old grayscale clips guide motion, not proportions. One anatomical scale
per source sheet, exact loop/start endpoints and reversed stop. Existing reversible
authorization covers installation. Preserve all raw/rejected sources and prompts.

## Current state
Four james-water-{east,south,west,north}-v1 folders contain sources/prompts/extraction,
registered-ungraded poses, bare/helmet manifests/hashes/frames and explicit anchors.
Family build/fit_helmets helpers reproduce192 refs. Common256x276/pivot128128,
standing148; loops960ms/start-stop520ms. Fixed anatomical scales E.5/S.480769/
W.471698/N.468085; north interior v4 fixed22/106 separate source density, unsupported
cross removed. Source/helmet origins recorded. Fixed master gold/matte grade with
owned heads; independent helmet water pitches at native shell35/39/35/33.
South stroke3 head anchorY571->544 avoids goggles above helmet. Rear helmet donors
2/3 yaw rejected; original overhead gloves restored. All source joins unchanged.
Literal manifests installed in scripts/grid_canvas.gd; paired branforth-water
registry entries in ACTIVE_ASSETS.json. Chief-engineer-branforth-v2/clearance.json
swim/tread now derive exact selected alpha at world65.28px. Transition union
includes actual retained water-turn pixels and original conservative bounds;
other action fields preserved. Original clearance saved as retained-clearance.json.
Native station-review.gif and fresh native-installed route/contact images retained.
Inventory173 bare3204 slots/171 helmet3180 slots,52 retained bare states.

## Verification
695 bare+548 helmet packaging checks PASS.2054 actual installed grid-loader,
192 selected pixels/metadata/clock slots and pause/start-stop checks PASS.2029
installed real-route checks PASS: eight routes, both modes/four initial facings,
actual James route_between/smooth_route/move, lazy selected NPC clearance and normal
grid rendering.200 sampled navigation envelopes clear actual blockers; camera-
following captures/actor-on-off and48 installed contact samples reviewed. Scratch
APPDATA reports actual owner profile unchanged. Source/staged proof retained.
North uses connected south pair in reverse. Earlier empty-default fixture northern
pair had no route with either retained or new profiles; those failures/diagnostics
preserved, not proof about every current north doorway. First camera board obscured
south/north actors with UI; fixed camera board retained and reviewed. East first two
start samples touch nonblocking console rectangle91/61 alpha pixels/mode, with no
navigation blocker contact and a native visual gap. Cosmetic contact evidence kept.
No full expedition oxygen/death, exterior, concurrent traffic or all-layout claim.

## Next action
Remake12 ordinary water-turn states as independent four quarter-turn sources and
checked joined halves, using exact installed prone-swim endpoints/world pivots.
Then swim-carry/cargo turns/pickup, salvage/distress/air recovery/ground and water
death. Cross-family polish includes activity arrival forcing east before stop,
which can snap from a non-east swim to east stop; route arrival passing is not
smooth-facing proof. Full-set and owner review remain unproven; keep goal active.
'''
atomic(R/'docs/JAMES_WATER_HANDOFF_2026-09-30.md',lambda b:handoff.encode())
audit=R/'character/james-animation-coverage-2026-09-30/audit.py'
atomic(audit,lambda b:b.replace(b'Current next work: swimming/tread, water start/stop and turns, then cargo/salvage/distress/recovery/death.',b'Current next work: water turns/carry/pickup, then salvage/distress/recovery/death. All16 directional tread/swim/start/stop states are installed in both modes; actual192-slot loader and eight authored maintenance/storage routes reviewed. Selected alpha clearance and exact joins are installed; non-east activity-arrival facing snap remains for cross-family polish.'))
print('Installed water milestone,52 retained states and explicit cross-family polish limits recorded')
