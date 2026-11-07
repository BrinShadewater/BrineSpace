"""Bind broader entries, scoped room review and completed fresh-scene disk proof."""
from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parent.parent;P=R/'character/veld-death-ground-family-v1';O=R/'output'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reports={};summaries={};paths=[]
names=['veld-dry-death-role-entry-candidate-v1','veld-dry-death-station-candidate-v1','veld-dry-death-continue-candidate-v1']
for name in names:
    folder=O/name;report=json.loads((folder/'validation.json').read_text());log=(folder/'native.log').read_text()
    assert report['returnCode']==0 and '0 failures' in log and 'ERROR:' not in log
    final=[line for line in log.splitlines() if 'VELD DRY DEATH' in line][-1]
    reports[name]=report;summaries[name]=final
    paths.extend(folder/n for n in ['validation.json','native.log','profile-before.json','profile-after.json'])
paths.extend((O/names[0])/n for n in ['native-contact.png','east-west-role-crops.png'])
station=O/names[1];records=json.loads((station/'contacts.json').read_text())['records']
assert len(records)==64 and not any(r['projectionProxyOverlaps'] for r in records if r['phase']=='terminal')
paths.extend(station/r['screenshot'] for r in records);paths.extend(station/n for n in ['contacts.json','counter-contact-review.png','aisle-contact-review.png','final-room.png'])
# The Continue process started before the cargo-only branch expansion. Preserve
# its actually loaded controller rather than binding new bytes to an old run.
old=(R/'scripts/veld_death_motion.gd').read_bytes().replace(b'if entry_key.begins_with("stand-") or entry_key.begins_with("pickup-") or entry_key.begins_with("unload-"):',b'if entry_key.begins_with("stand-"):')
previous=json.loads((P/'evidence.json').read_text())['files']['scripts/veld_death_motion.gd']
assert hashlib.sha256(old).hexdigest()==previous,'Cannot reconstruct the loaded Continue revision exactly'
revision=P/'revisions/standing-kneel-controller-v1.gd.txt';revision.parent.mkdir(exist_ok=True);revision.write_bytes(old);paths.append(revision)
index=R/'tests/index.json';data=json.loads(index.read_text())
for suffix,reason in [('role_entry','Actual cargo/action/partial-turn deaths and native pose join review'),('station','Owner galley geometry and native64contact captures'),('continue','Candidate-injected fresh-scene disk staged Continue at entry/interior/corpse')]:
    key='test_veld_dry_death_'+suffix+'_candidate'
    if key not in data['subsystems']['veld-dry-death']:data['subsystems']['veld-dry-death'].append(key)
    data['lanes'][key]={'lane':'native','reason':reason}
    paths.extend([R/f'tests/{key}.gd',R/f'tests/{key}.gd.uid',R/f'tools/run_veld_dry_death_{suffix}_candidate.py'])
index.write_text(json.dumps(data,indent=2)+'\n');paths.append(index)
paths.extend([R/'scripts/veld_death_motion.gd',R/'scripts/veld_death_motion.gd.uid',R/'tools/build_veld_dry_death_contact_review.py',Path(__file__)])
paths.extend(p for p in (P/'entry-audit-v1').rglob('*') if p.is_file())
guard='; '.join(f"{n}:overall={r['passed']},seconds={r['seconds']},files={r['realProfileFileCount']},changes={r['realProfileChanges']}" for n,r in reports.items())
note=f'''

## Veld broader dry entrances, galley contacts and candidate disk Continue — October 1, 2026

{'; '.join(summaries.values())}. Role inputs carry/pickup/unload/interact/stand/actual partial carry-turn across4directions/two gears/two clocks. Exact last-drawn texture, held entrance, current projected camera, authored interiors/finite corpse and paused in-memory restore checked; requested source-row assertion prevents idle fallbacks. First native role review showed crouched unload rising into bend despite pixel checks. Pickup/unload/stand now select kneeling interior2 when actual incoming extent is below78% of standing; revised2931checks/96oxygen deaths pass. Prior2883pass report/native captures retained: it is not a visual acceptance of that lift. Crate release still abrupt when authored lowering begins; ordinary task anatomy/grade (including cooler old kneel sleeves) remains full-set polish.

64actual native galley captures at two navigation-clear counter/aisle anchors: before-kneel/exact entry/first interior/corpse, four cameras/both gear.213checks pass; terminal silhouettes visually clear at those contacts and16terminal projection rectangles have zero registered prop intersections. Projection bounding box is a conservative visual proxy, not a floor/anatomical collision certificate or universal room clearance. Native screenshot crops preserve all pixels; design-space anchors scale uniformly from1920px into1280px capture. Existing dry family remains staged; grid/ACTIVE_ASSETS normal overrides unchanged. Fresh-scene disk staged Continue restores entry/interior/corpse for8direction/gear groups, preserving validated selectors, clock, world foot and exact paused pixels. Uses actual recovered Bill pod as survivor and normal failure/checkpoint rules. Candidate injection is explicit; this is not normal-loader or fresh-process/title-button proof.

Strict guards: {guard}. All engines/checks pass but every overall runner fails its last_session.json owner delta; retain fingerprints and failed intervals, no attribution/restoration/clean-profile claim. Earlier Continue fixture parse error is archived. Continue process cached the previous standing/kneel controller before cargo-only branch edit; exact old SHA reconstructs and binds revisions/standing-kneel-controller-v1.gd.txt. Kneel branch unchanged, current role revision separately tested; no claim that this disk run exercised new cargo branches.

Lesson: inspect actual incoming-to-first-interior native joins, not just capture equality. A held low action can still jump upward after the hold. Bound state-aware lowering to observed phase and verify no fallback rows. Record source revision actually loaded by long-running engines; current file hashes cannot certify bytes changed during that process. Distinguish room screenshot/projection proxy evidence from physical footprint and broad furniture compatibility. Remaining bunk/seated/life entrances, cargo release, normal selection/fresh-process Continue and complete rest/life/master/style/perspective/detail/material/motion polish keep the full goal active. Handoff:character/veld-death-ground-family-v1/ROLE_WORLD_HANDOFF.md.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    p=R/rel;prior=p.read_bytes()
    if note.lstrip().encode() not in prior:p.write_bytes(note.lstrip().encode()+prior if rel=='docs/CURRENT_STATUS.md' else prior+note.encode())
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
if note.lstrip().encode() not in installed.read_bytes():
    with installed.open('ab') as f:f.write(note.encode())
handoff=f'''# Project handoff

Updated:2026-10-01 · Project:BrineSpace · Task:Veld broader dry entrances/world/disk

## Objective and acceptance
Full matching Veld animation set and whole-set polish remain active/incomplete. Broader role, two galley contacts and candidate fresh-scene disk milestone only; no owner/full-set visual acceptance.

## Accepted decisions and constraints
Four independent master cameras, fixed body/material rulers and canonical directional helmets. Keep actual drawn incoming texture; standing/kneel and lowered pickup/unload/stand enter appropriate authored slot1/2. Preserve existing checkpoint key and legacy empty data, normal failure/survivor rules and owner profile. Candidate injection; normal loader/registry unchanged.

## Changed files and current state
scripts/veld_death_motion.gd cargo/stand phase-aware branch; paired UID preserved. Three dedicated test/UID/runner pairs for role_entry, station and continue. Native contact crop utility, entry-audit-v1 review page/boards and current/previous source revision evidence. Tests index plus status/continuation/pipeline/bible/maintained+installed skill lessons updated.

## Verification and limits
{'; '.join(summaries.values())}.
Role inputs exercise actual Flood.step_crew oxygen death with current requested pose rows and projected partial-turn facing. Native role lift discovered/repaired; revised joins reviewed. Cargo release still abrupt.64native galley captures reviewed at counter/aisle; no terminal prop projection intersection there, not universal footprint proof. Disk staged Continue uses actual pod survivor/normal save validation, exact entry/interior/corpse pixels/world foot/clock/paused state. Explicit candidate load in each fresh scene, no normal-loader/fresh-process/title UI claim. Continue cached original standing/kneel controller; exact old file reconstructed against bound SHA, new cargo branch separately verified.
Strict profile results: {guard}. Failed guards/deltas and prior fixture parse error preserved; no clean-profile claim.

## Remaining work and next action
Bunk/seated/life death entrances and equipment switches; cargo release and half-turn intermediate camera polish. Test normal-loader/fresh-process Continue and broader furnished contacts before selection. Old kneel sleeves are cooler than the matched collapse; renew those action families against masters. Generic rest/life and full-set identity/proportion/perspective/material/detail/motion audit remain. Keep existing active goal; no blocker/commit/export.
'''
(P/'ROLE_WORLD_HANDOFF.md').write_text(handoff);paths.append(P/'ROLE_WORLD_HANDOFF.md')
evidence={'normalSelection':False,'summaries':summaries,'reports':reports,'continuedControllerSha256':previous,'currentControllerSha256':sha(R/'scripts/veld_death_motion.gd'),'files':{p.relative_to(R).as_posix():sha(p) for p in paths},'scope':'current role/mortality and two-contact world visuals; previous unchanged kneel-controller fresh-scene disk, no normal/fresh-process/general furniture acceptance'}
(P/'role-world-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print(json.dumps({'boundFiles':len(paths),'summaries':summaries,'normalSelection':False}))
