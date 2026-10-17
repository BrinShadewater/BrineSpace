from pathlib import Path
import json,re,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-bunk-body-settle-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
records=json.loads((O/'records.json').read_text());assert len(records)==80
source_files=list((P/'frames').rglob('*.png'))
previous=json.loads((R/'output/veld-bunk-body-emergency-v1/inputs-after.json').read_text())
assert all(previous[f.relative_to(R).as_posix()]==hashlib.sha256(f.read_bytes()).hexdigest() for f in source_files)
captures=len(list(O.glob('*-room.png')))
note=f'''## Veld partial supported bunk settling death — October 1, 2026

Staged paired body now adds death-bunk-settle-east: five exact authored descent
poses (seated through lying) plus two existing relaxed arm terminal poses. Seven
finite slots/2180ms from full seated start; initial exact180ms incoming hold
and remaining clip begin at actual live progress. Lowering and rising partial
sources both settle toward supported lying contact. Existing20PNGs exactly equal
previous emergency milestone; no repaint, rescale, palette/detail change or new
generated source.14new frame references raise paired manifests to five states/
50references.130source/package checks0failures; exact masters and original first
three state contracts retained. Rebuild build_bare.py,build_helmet.py then
build_settle.py; derived rows explicitly record source reuse.

Loader opt-in supportedBunkDeathMode=settle-v1 tags only this finite state.
Veld death selector requires matching gear, active supported bunk, appropriate
seated/reclining source and matching partial clock. Snapshots retain bounded
entry/rest/local-foot anchors and pose-compatible progress; malformed/foreign
recipes reject. CrewLife.bunk_contact_offset shares original bed formula with
live and dead displays. Exact entrance position/depth retained180ms; subsequent
source/contact/depth advance together until terminal lying support. Existing
held bunk/ground/water recipes remain distinct. Standing/crouching bunk starts
remain incomplete fall coverage; seated lounge sources are another family.
Normal paired art selection remains unchanged/unselected.

Native14813checks0failures/{report['runs'][0]['seconds']}s:80prescribed partial actor
death source API cases (five interiors x lower/rise x two gears x four room
rotations),320actor-file fresh dead restores at same saved world clocks.76source/
offset samples per case,18native sequences/{captures}actual room+exact source captures.
Eight full boards/two paired entrance boards visually reviewed; stationary
navigation foot, actual mattress contact, matte body/head grade and hardware
retain master family. Two source-clock previews include recorded continuous
offsets; browser tab20 observed changing0.00->1.24s beside same pixel-scale masters.
Source preview is separate from actual captured room poses, not continuous native
whole-world playback. Natural death acting/owner acceptance remain open.

Held-bunk regression1306checks0failures/{report['runs'][1]['seconds']}s native engine0,
8actual held deaths/32actor-file restores and all4rotation live poses. Water
regression1953checks0failures/{report['runs'][2]['seconds']}s headless engine0/64actual
oxygen deaths. Allthree engines terminal0/clean logs. Owner{report['realProfileFileCount']}
non-log files unchanged with scratch APPDATA.29targeted production/test/source/
manifest inputs match before/after{report['seconds']}s interval; broader dependencies
not frozen. New paired UID tests test_veld_bunk_body_settle.gd and held regression,
isolated runner run_veld_bunk_body_settle.py; evidence in settle-evidence.json.
This proves source/actor-only mortality/restoration, not new partial-recipe full
RunSave/fresh-scene Continue or naturally triggered room mortality. Current
normal selection cannot produce new staged recipe without explicit overrides.

Lesson: an exact incoming death texture alone does not preserve supported anatomy
through the rest of the fall. Reuse authored poses with explicit finite clock,
gear/source binding and the same continuous furniture contact formula as live
motion; preserve source provenance and validate recipe bounds/pose correspondence.
Separate supported settling from early standing falls and other seat families.
Remaining fresh emergency/partial death Continue, whole-world hazard cadence,
early bunk falls/lounge death sources, normal paired body installation and full
Veld family/master polish. Full goal active/incomplete; no commit/export.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for i,path in enumerate(targets):
    old=path.read_bytes();payload=note.replace('\n','\r\n').encode()
    if note.splitlines()[0].encode() not in old:path.write_bytes(payload+b'\r\n'+old if i==0 else old+b'\r\n'+payload)
handoff=f'''# Project handoff

Updated:2026-10-01 · Project:BrineSpace · Task:Veld master bunk and supported settling

## Objective and acceptance
Complete Veld full animation set/master family consistency, then cross-family
polish. East bunk body/helmet and supported settling are staged. Full goal active;
owner visual acceptance open; no normal paired body selection/commit/export.

## Accepted decisions and constraints
Exact current standing masters; one148/408 anatomical ruler/pooled master grade.
256x272/p128,224/H148 keeps full limbs; original entry/reverse/held clocks/contact.
20PNG source files unchanged by settling; five states/50references per pair total.
Derived settling reuses authored descent and arm relaxation; early standing falls
and lounge deaths remain separate incomplete coverage. Preserve owner geometry.

## Current state
Sources/prompts/builders/manifests, reviews and evidence here. build_settle.py
follows bare/helmet builders. New loader opt-in/death selector and bounded dynamic
recipe use CrewLife shared original bed contact formula; exact180ms incoming hold.
Production Veld marked-bunk East arrival and finite fire-rise hooks installed;
art remains staged. Tests/runners cover body, Continue, lifecycle, approach,
future Continue, emergency and partial settling (each paired UID).

## Verification
130package checks;14813native partial checks/80actor deaths/320actor-file fresh
dead restores at same world clocks;18native sequences/{captures}room+source captures.
Eight complete boards/two entrance boards/browser source-clock previews reviewed.
Latest regressions1306native held and1953headless water checks0fail; allengine0;
72.41/76.11/36.67s,{report['seconds']}s interval,29targeted inputs frozen. Owner2931
non-log files unchanged in scratch APPDATA. Exact20PNG hashes match pre-settling.
Prior169paused full Continue,7121future full Continue,3395controller/service,
9668actual approach and8037emergency/45shared fire checks retain separate scopes.
22fire cases physically reach safe core;6cleared alarms,22gear setters,2blocked
scraps. New partial recipe lacks full RunSave/fresh-scene/future restoration proof.
Source clocks/contact and actor APIs do not certify natural world mortality/cadence.

Failed glove1px/sole-survivor save/disconnected hab/North arrival/fire snap
intervals retained. Owner room layout unchanged; hab scrap blocked by real policy.
Full review/evidence files here and scoped output/veld-bunk-body-* folders.

## Next action
Fresh full-save Continue for fire rise and partial death, then early bunk/lounged
death sources and whole-world hazard cadence; install paired body with lifecycle
proof. Finish remaining Veld families and master/cross-family polish. Normal title
selection and universal room/silhouette acceptance remain unproven.
'''
(P/'HANDOFF.md').write_text(handoff)
files=[R/p for p in ['scripts/veld_npc.gd','scripts/veld_npc.gd.uid','scripts/veld_death_motion.gd','scripts/veld_death_motion.gd.uid','scripts/crew_life.gd','scripts/crew_life.gd.uid','scripts/crew_sprite_player.gd','scripts/crew_sprite_player.gd.uid','tests/test_veld_bunk_body_settle.gd','tests/test_veld_bunk_body_settle.gd.uid','tests/test_veld_bunk_body_settle_held.gd','tests/test_veld_bunk_body_settle_held.gd.uid','tools/run_veld_bunk_body_settle.py']]+[O/n for n in ['native.log','held-regression.log','water-regression.log','validation.json','records.json','inputs-before.json','inputs-after.json']]+[P/n for n in ['bare-manifest.json','helmet-manifest.json','package-checks.json','build_settle.py','settle-review.html']]+list(P.glob('native-settle-*.png'))
(P/'settle-evidence.json').write_text(json.dumps({'validation':report,'packageChecks':130,'nativeChecks':14813,'heldRegressionChecks':1306,'waterRegressionChecks':1953,'partialActorDeathCases':80,'sameClockActorFileRestores':320,'nativeSequences':18,'roomCaptures':captures,'sourceCaptures':captures,'newOrModifiedSourcePNGs':0,'sourcePNGsEqualPreviousEmergencyMilestone':True,'normalManifestSelection':False,'visualReview':'Eight full native/source boards, two paired entrance boards, source-clock browser preview observed','scope':'Prescribed actor-only supported source/death; not new partial full RunSave/fresh-scene Continue or natural world mortality','bindings':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n')
html=P/'index.html';old=html.read_text();link='<p><a href="settle-review.html">Supported settling from partial bunk poses</a></p>'
if link not in old:html.write_text(old+'\n'+link)
print(f'130package/14813partial/1306held/1953water checks;{captures}native/source captures; five lessons and concise handoff saved')
