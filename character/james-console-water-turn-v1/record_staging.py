"""Historical staging recorder: refuses to overwrite an installed selection."""
import json
from pathlib import Path
if json.loads((Path(__file__).resolve().parent/"selection.json").read_text()).get("runtimeInstalled",False):
    raise RuntimeError("Already installed; see current installation handoff")
from pathlib import Path
import json, uuid

P = Path(__file__).resolve().parent
R = P.parents[1]
v = json.loads((P / 'native-staged-validation.json').read_text())
e = json.loads((P / 'native-staged-evidence.json').read_text())
package = json.loads((P / 'verification.json').read_text())
log = (P / 'native-staged.log').read_text()
assert v['exitCode'] == 0 and not v['timedOut'] and v['realProfileUnchanged']
assert 'SCRIPT ERROR:' not in log and '\nERROR:' not in log
assert e['checks'] == 522 and e['failures'] == 0 and len(e['results']) == 16
assert package['checks'] == 53 and package['failures'] == 0
selection = {'status': 'staged_native_contacts_pass', 'runtimeInstalled': False,
             'fullSetComplete': False, 'states': ['swim-turn-east-north', 'swim-turn-north-east'],
             'uniqueFrames': 12, 'references': 24, 'packageChecks': 53,
             'nativeChecks': 522, 'contactCases': 16, 'nativePoseSlots': 96,
             'scope': e['scope'], 'pending': ['Actual approach/contact and departure route proof',
                'Conditional selected-clip clearance and normal runtime installation',
                'Whole console activity, interruptions and full cross-family journeys']}
(P / 'selection.json').write_text(json.dumps(selection, indent=2) + '\n', encoding='utf8')

def atomic(path, transform):
    before = path.read_bytes() if path.exists() else b''
    after = transform(before)
    if before == after:
        return
    tmp = path.with_name(path.name + '.james-' + uuid.uuid4().hex + '.tmp')
    tmp.write_bytes(after)
    if (path.read_bytes() if path.exists() else b'') != before:
        tmp.unlink()
        raise RuntimeError('Concurrent edit: ' + str(path))
    tmp.replace(path)

note = '''### James compact flooded-console quarter staged - September 30, 2026

Do not equate failed graph-node/four-unit probes with absent usable space. Fine
two-unit sampling within the unchanged36-unit service radius finds a narrow full-
swim strip6 units behind the raw life-support contact:34 full-profile-safe points
per rotation/gear at y147.5015. Upright tread and all existing East/West/South-to-
North turns still fail there. Static endpoint clearance is not transition clearance.

Independent compact East/North whole-body quarter now bends knees through yaw;
same anatomical proportions/material and exact selected swim endpoints. Fixed25/50
atlas cranial density. First atlas pose4 reached196 native rows (four too many);
independent whole-pose edit uses23/310 cranial density and fixed source-level material
calibration, not height squeezing, limb splicing or per-pose normalization. Its foot
reaches187; full row ends at the North master's192, world rear reach28.22919 instead
of old quarter38.81514. Canonical selected helmet heads own bounded19px ellipses;
body pixels elsewhere exact. Reverse is literal slot/clock/metadata reversal.

53 package and522 clean native checks PASS:two quarter keys,12 unique paired frames,
four rotations/two gear/two directions,96 slots, paused exact pixels and finite master
joins. Whole candidate plus unchanged incoming/destination swim envelopes fit the
fine contact; old quarter and raw contact rejected. Native pack boards and10 native
views reviewed;24 new contact captures retained. Scratch actor/player receive only
candidate manifest and exact candidate clearance, so this is staged CONTACT proof.
Incoming swim is seeded there, not a traversed approach or installed console fix.
Do not promote until actual routing/arrival/departure and contextual clearance are
proved. Original sources/prompts/hashes preserved;12 frame hashes unchanged after
deterministic rebuild. An exact duration-boundary sampling failure was retained;
sample1ms inside slots without changing authored520ms clock. Real profiles unchanged.
See docs/JAMES_CONSOLE_WATER_TURN_HANDOFF_2026-09-30.md. Full James goal active.

'''
for path in [R / 'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',
             R / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
             R / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
             R / 'skills/brinespace-character-pipeline/references/crew-consistency.md',
             Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    atomic(path, lambda b: b if note.encode() in b else b + b'\n' + note.encode())
headline = '''## James compact flooded-console turn staged - September 30, 2026

Fine scan found a full-swim contact6 units behind the original console point.
New compact knee-bent East/North quarter and exact reverse fit it:53 package and
522 native checks PASS,96 staged pose slots; source/native views reviewed. Master
endpoints, density, matte grade, canonical helmets and520ms clock retained. Runtime
unchanged; actual approach/departure proof and installation follow. Profiles unchanged.
[Handoff](JAMES_CONSOLE_WATER_TURN_HANDOFF_2026-09-30.md). Full James goal active.

'''
atomic(R / 'docs/CURRENT_STATUS.md', lambda b: b if headline.encode() in b else headline.encode() + b)
handoff = '''# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James flooded console compact turn

## Objective and acceptance
Full James animation/master consistency and complete cross-family journeys.
Compact quarter staged and native contact proof complete; installed journey still open.

## Accepted decisions and constraints
Keep skull/density/material, exact master endpoints and full collision envelopes.
Solve projection with authored bent legs, not body scaling, limb splices, blockers
or owner-layout changes. Route and complete clip must both fit; full goal active.

## Current state
character/james-console-water-turn-v1:source-v1.png, independent source-pose4-v2.png,
original locations/SHA/prompts/crops, deterministic build, registration, paired12
frames/two exact-reversed quarter keys,53-check verifier, native-staged.gd/evidence.
Runtime grid/controller/registry unchanged this turn. Previous installed dry/wet
safe service routing preserved. Fine space probe under workstation-arrival pack.
Status/pipeline/bible/both skills updated. No native process running.

## Verification
Two-unit sample finds34 points per rotation/gear for full North swim in the36-unit
service disk; nearest contact is original point+(0,6), local(117.0498,147.5015).
No treading or old quarter fits. v1 four-unit foot overshoot corrected by whole-pose
leg-bend edit calibrated23/310; remaining atlas uses25/50. Final rear reach28.22919.
53 package/522 clean native checks PASS,16 staged contact cases,96 slots; old quarter
and raw contact rejected, paused holds/exact finite endpoint proven. Two pack boards
and10 native views reviewed. Sources immutable and12 rebuilt frame hashes unchanged.
Candidate manifest/clearance injected into scratch player/actor; incoming swim seeded
at contact. This is not navigation, full activity, installation or owner acceptance.
24 new captures retained; duration-boundary fixture failure corrected with1ms interior
sampling, authored520ms clock unchanged. Real profiles unchanged in native runs.

## Next action
Prove an actual route to the fine contact with final travel facingEast, then stationary
East-to-North compact turn. Current exact_approach insists final travel headingNorth;
coarse North graph nodes do not fit. A target node near(112,144) can be approachedEast,
then exact fine contact may remainEast; test its entire connector and outgoing/incoming
clip union, not just endpoints. Resolve a James wet-console-specific adjusted contact
within existing service radius and permit stationary equipment-facing turn only if
selected candidate clip fits. Preserve dry hooks/other actors. Departure needs exact
reverse and actual route clearance. Prove the reverse completes at the fine contact
before moving toward a coarse node: its full North-facing intermediate envelope
may collide if movement carries it above the narrow strip. A static clip PASS
does not permit translating that entire clip through an unchecked connector. Native normal installation after both approaches
and full timed console behavior pass. Then full furniture/meal/equipment/exterior
journeys and broad material/motion consistency. Keep original full objective intact.
'''
atomic(R / 'docs/JAMES_CONSOLE_WATER_TURN_HANDOFF_2026-09-30.md', lambda _: handoff.encode())
print('Compact quarter staged:53 package/522 native checks; actual routes/installation next.')
