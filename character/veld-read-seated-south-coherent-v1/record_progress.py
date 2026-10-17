from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
title="Veld South sofa and same-body tablet reading - October 1, 2026"
note="## "+title+"""

Actual default observation sofa South contact reviewed before changing anatomy.
Staged seated height126 versus legacy reader100 exposed a consumer join drift;
not evidence to normalize cardinal occupied heights. Added actual prop front
sort edge+.01 and opt-in dry observation sit/read/enter/exit/rise depth; exact
standing endpoints and unmarked/wet/dead retain natural ordering. Furniture,
contact, service clock, navigation and normal artwork selection unchanged.
90 observation-sofa unit checks pass,4.81s; actual full route/service/render audit
11746checks0failures,86.06s,230source/native pairs,2931non-log owner files unchanged
under scratch APPDATA. Before-depth and depth-only runs10667checks passed but
visual review failed visibility, then reader identity/size. Preserve those scopes.

New staged character/veld-read-seated-south-coherent-v1 uses built-in edit
62bbed37-780e-44c9-a0e8-d6ad9baad405, saved raw/prompt/reference roles. Adopt only
lower forearm/glove/tablet band[105,148,151,185] over exact current South seated
body; head/hair/face/helmet/chest/boots outside band byte-exact. One148/509 ruler,
frozen South material curves; no regenerated wholebody adoption. Twelve-second
finite draw480/hold11040/stow480 keeps existing Veld service duration. Eightstates,
56references/12uniqueRGBA exports,73package checks/16deterministic files. Actual
last-down/first-read and last-read/first-rise source joins exact; candidate held
height126 throughout. Paired source/actual sofa boards visually reviewed.

Lesson: review complete selected consumer joins and actual prop ordering, not
only green source-pack checks. Preserve common body/helmet when authoring bounded
hand actions; do not repair depth with distorted anatomy or per-pose sizing.
Interrupted tablet exit, fresh Continue and normal selection remain separate
milestones; full-set goal active/incomplete. Handoff/evidence in new reading pack.
"""
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 data=path.read_bytes()
 if title.encode() not in data:
  addition=note.encode()+b'\n'
  path.write_bytes(addition+data if path.name=='CURRENT_STATUS.md' else data+b'\n\n'+addition)
hand="""# Project handoff

Updated: 2026-10-01 - Project: BrineSpace - Task: Veld South sofa reading

## Objective and acceptance
Full master-matched Veld animation set, with cross-family motion and identity
review. This milestone removes legacy reader identity/scale/helmet switches from
the staged South sit/read/rise sequence. Owner visual acceptance remains open.

## Accepted decisions and constraints
Retain matte graphite, warm skin/brown hair and selected native helmet, one source
ruler and exact common body. Actual sofa contact looks plausible; do not shrink
South to match cardinal alpha bounds. Existing reversible authorization applies.
No normal artwork adoption, furniture redesign, commit/push/export or owner saves.

## Current state
New source/prompt/generation metadata, bounded fitter and paired manifests here.
Only[105,148,151,185] inserted from generated arm/tablet source; rest of exact
South neutral005 preserved. 256canvas/p128224/H148, finite12sec complete reader,
480ms draw/480ms exact reverse stow plus11040ms hold. Sixposes/bothgears.
Shared CrewLife opted-in observation depth and actual sofa seat_depth added;
unit test/runner and full sofa fixture/runner created. Original South art intact.
Source edit ID62bbed37-780e-44c9-a0e8-d6ad9baad405. Package remains unselected.

## Verification
73package checks,16deterministic files.90actual sofa geometry/depth unitchecks
0failures,4.81sec.11746full native actual prescribed route/service checks,
0failures86.06sec;230records with exact-source/nativePNG each.2931non-log owner
files unchanged, engine0/noerrors, scratch APPDATA. Exact down/read/rise joins.
Paired source/sofa boards reviewed; header metadata scope corrected without a
rerun, original report saved here. Earlier two10667pass runs retained as failed
visual milestones: hidden candidate, then smaller legacy reader/old helmet.
No natural chooser, actual interruption/fresh Continue/owner acceptance claim.

## Next action
Verify actual power/suspend early tablet exits and fresh disk Continue, then
select coherent family once motion/lifecycle evidence supports it. Remaining
North reading, side seated breath, inherited rest/death/water and full-set polish.
"""
(P/'HANDOFF.md').write_text(hand)
south=R/'character/veld-seated-south-coherent-v1/HANDOFF.md'
data=south.read_bytes();marker=b'## Subsequent actual South sofa audit'
if marker not in data:
 south.write_bytes(data+b'\n\n'+marker+b' - October 1, 2026\n\nOriginal candidate scope above remains unchanged. Actual South observation sofa\nnow audited with new common-body reader; see ../veld-read-seated-south-coherent-v1/HANDOFF.md.\n11746checks/0failures and230source/native pairs establish prescribed complete\nservice/render joins. Shared opt-in observation depth fixed; no per-pose resize\nor normal artwork selection. Interruptions/Continue and owner acceptance separate.\n')
files=list(P.glob('*.py'))+list(P.glob('*.json'))+list(P.glob('*.png'))+list(P.glob('*.gif'))+[P/'index.html',P/'HANDOFF.md']+list((P/'sources').glob('*'))+list((P/'frames').rglob('*.png'))
O=R/'output/veld-seated-south-sofa-audit-v1'
files += [f for f in O.iterdir() if f.is_file()]
U=R/'output/observation-sofa-depth-v1';files += [f for f in U.iterdir() if f.is_file()]
files += [R/f for f in ['scripts/crew_life.gd','scripts/crew_room_activity.gd','tests/test_observation_sofa.gd','tests/test_observation_sofa.gd.uid','tests/test_veld_seated_south_sofa_audit.gd','tests/test_veld_seated_south_sofa_audit.gd.uid','tools/run_observation_sofa_depth.py','tools/run_veld_seated_south_sofa_audit.py','character/veld-seated-south-coherent-v1/bare-registration.json','character/veld-seated-south-coherent-v1/frames/bare/sit-down-south/005.png','character/veld-seated-south-coherent-v1/frames/helmet/sit-down-south/005.png','character/veld-seated-south-coherent-v1/sofa-source-joins.png','character/veld-seated-south-coherent-v1/sofa-native-joins.png','character/veld-seated-south-coherent-v1/sofa-review.json']]
files=sorted(set(f for f in files if f.is_file() and f.name!='evidence.json'))
bindings={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(P/'evidence.json').write_text(json.dumps({'scope':'staged common-body South reading and actual prescribed sofa service/render; no normal selection/interruptions/Continue/owner acceptance','bindings':bindings},indent=2)+'\n')
print(json.dumps({'recordedNotes':5,'boundFiles':len(bindings)}))
