"""Bind combined source and opt-in actual mortality proof with honest scopes."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reports={}
for name in ['veld-death-ground-family-candidate-v1','veld-dry-death-entry-candidate-v1','veld-water-death-entry-v1']:
    o=R/'output'/name;reports[name]=json.loads((o/'validation.json').read_text());assert reports[name]['returnCode']==0
    assert '0 failures' in (o/'native.log').read_text()
index=R/'tests/index.json';data=json.loads(index.read_text())
for key,reason in [('test_veld_death_ground_family_candidate','Combined dry source/player and native148/82 family review'),('test_veld_dry_death_entry_candidate','Actual dry oxygen deaths with candidate injection and native incoming/lowered/corpse review')]:
    if key not in data['subsystems']['veld-dry-death']:data['subsystems']['veld-dry-death'].append(key)
    data['lanes'][key]={'lane':'native','reason':reason}
index.write_text(json.dumps(data,indent=2)+'\n')
note='''

## Veld combined dry family and opt-in mortality entrances — October 1, 2026

Four independent cardinal source packs assembled as8states/48whole-res-path references in character/veld-death-ground-family-v1.152combined source/contract/master-entry/current per-direction hash checks and269actual combined-player checks pass. Native148/82 family boards reviewed. No source pixels regraded/resized for assembly. deathEntryMode lowered-start-v1 opt-in uses existing lowered-entry metadata; legacy rows remain unchanged. Veld death controller now captures dry last-drawn whole texture, holds180ms, starts authored interior1 for upright/walk or2 for kneel/repair (stand uses observed extent). Existing veld_water_death checkpoint key retained for saved dry selectors; validator separates dry/wet state and limits dry start to1/2. Candidate-injected production Flood.step_crew produced64dry oxygen deaths,1,859checks0failures: four facings/two gears/idle-walk-kneel-repair/two starting clocks; exact entrance, held pose, correct lowered first interior, finite corpse and validated paused in-memory actor/player restore. Water regression64oxygen deaths/1,954checks passes. This is not normal dry selection, fresh disk Continue, cargo/gesture/bunk entrance or furnished footprint proof.

Strict runner results all FAILED profile guards despite engine0/checks0failures: family6.21s, dry39.61s, water39.61s; each2,931real non-log files and last_session.json delta under explicit scratchAPPDATA. Earlier dry1,859checks/32failures retained: nominal180ms at clock17.43 subtracts to0.17999999999999972, still in held entrance. Single-case scratch probe confirmed actual incoming texture, expected first2; its launch lacked before/after real-profile fingerprints and supports only that boundary diagnosis, not a clean-profile claim. Probe's internal engine log/scope preserved. It overwrote the earlier review image; do not claim the archived first-failure image binds the earlier full test. Corrected fixture samples180.001ms and passes. No production timing weakened to make checks green. Normal loader/ACTIVE_ASSETS unchanged. Full goal active; remaining dry family fresh Continue/world joins, generic rest/life and broad master/detail/material/perspective/motion polish. Handoff:character/veld-death-ground-family-v1/HANDOFF.md.

Lesson: assemble source candidates by verifying current frame hashes AND actual combined manifest resolution. Package equality alone does not prove NPC mortality. Preserve last rendered pose and select lowered interiors semantically; standing-entry source slots must not reset a kneeling caller. Sample logical frame boundaries just after the boundary at nonzero visual clocks, preserving pre-boundary assertions; confirm real texture/state before editing unexplained failures. Every diagnostic launch needs the same scratch APPDATA and complete owner before/after fingerprint guard as the main fixture. A scratch-only unguarded probe has a narrower evidence scope and must be recorded explicitly.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    p=R/rel;old=p.read_bytes()
    if note.lstrip().encode() not in old:p.write_bytes(note.lstrip().encode()+old if rel=='docs/CURRENT_STATUS.md' else old+note.encode())
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.lstrip().encode() not in installed.read_bytes():
    with installed.open('ab') as f:f.write(note.encode())
(P/'HANDOFF.md').write_text('''# Project handoff

Updated:2026-10-01 · Project:BrineSpace · Task:Veld combined dry family/actual entrances

## Objective and acceptance
Full master-matched Veld animation set and whole-set polish remain active/incomplete. Source family and opt-in actual mortality entry milestone only; no owner acceptance/normal dry selection.

## Accepted decisions and constraints
Four independent master cameras, exact selected standing entries, per-source fixed body ruler/material grade and directional native helmets. Preserve original1420ms finite corpse. Whole res paths; no mirrored/dynamically assembled runtime frame references. Keep legacy dry rows until selected pack supports opt-in lowered entry. Retain existing checkpoint key for compatibility. Preserve concurrent actor work and owner profile data.

## Changed files and current state
This folder: combined bare/helmet manifests, build/record scripts,152check source report,48hash-bound frame refs and all-direction review boards/page. Combined player fixture/UID/runner; opt-in actual dry death fixture/UID/runner in tests/tools. scripts/veld_death_motion.gd accepts dry opt-in and retains exact incoming pose, choosing authored interior1/2; scripts/veld_npc.gd saves dry selectors in existing veld_water_death field. scripts/grid_canvas.gd and ACTIVE_ASSETS unchanged. Tests index and current status/continuation/pipeline/bible/maintained+installed consistency reference updated.

## Checks and visual limits
152source/contract/master-entry/current evidence checks;269combined player checks.64actual candidate-injected dry oxygen deaths/1,859checks pass for idle/walk/kneel/repair, both gears/four directions/two clocks, exact hold/interior/finite corpse and paused in-memory actor/player restore.64water regression deaths/1,954checks pass. Native148/82 family and82incoming/lowered/corpse boards reviewed; not a furnished-room rendering or whole-set motion certification. Every current runner overall FAILED: last_session.json delta among2,931non-log real files; family6.21s, dry/water39.61s, explicit scratchAPPDATA. Previous32boundary failures and narrow unguarded scratch probe retained with limitations. No attribution/restoration/clean-profile claim. Full-test first-failure image was overwritten by diagnostic; its archived image cannot certify original run scope.

## Remaining work and next action
Extend entrances to carry/unload/pickup/gesture/turn/stand and furniture-specific life poses; inspect transient height/neck/body jumps and cargo release. Test production disk save and fresh-scene/process Continue for entry/interior/corpse under scratch guard. Review actual furnished-room corpse clearance/occlusion before normal selection. Then generic rest/life and full-set identity/material/detail/perspective/motion polish. No blocker; continue existing goal.
''',encoding='utf-8')
paths=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='evidence.json']
for rel in ['scripts/veld_death_motion.gd','scripts/veld_death_motion.gd.uid','scripts/veld_npc.gd','scripts/veld_npc.gd.uid','tests/test_veld_death_ground_family_candidate.gd','tests/test_veld_death_ground_family_candidate.gd.uid','tests/test_veld_dry_death_entry_candidate.gd','tests/test_veld_dry_death_entry_candidate.gd.uid','tools/run_veld_death_ground_family_candidate.py','tools/run_veld_dry_death_entry_candidate.py','tests/index.json']:
    paths.append(R/rel)
for name in reports:
    o=R/'output'/name
    paths.extend(o/n for n in ['native.log','validation.json','profile-before.json','profile-after.json','native-contact.png'])
paths.append(R/'output/veld-death-ground-family-candidate-v1/native-small.png')
for name in ['boundary-probe-engine.log','boundary-probe-scope.json']:paths.append(R/'output/veld-dry-death-entry-candidate-v1'/name)
evidence={'normalDrySelection':False,'sourceChecks':152,'familyPlayerChecks':269,'actualDryChecks':1859,'actualDryDeaths':64,'wetRegressionChecks':1954,'reports':reports,'files':{p.relative_to(R).as_posix():sha(p) for p in paths},'remaining':['broader incoming pose/gear/cargo/furniture joins','fresh disk Continue','actual world clearance/occlusion','rest/life/full-set matching and final polish']}
(P/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps({'boundFiles':len(paths),'sourceChecks':152,'familyPlayerChecks':269,'dryChecks':1859,'wetRegressionChecks':1954,'normalDrySelection':False}))

