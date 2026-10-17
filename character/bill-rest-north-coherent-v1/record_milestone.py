from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
assert not (P/'candidate-evidence.json').exists(),'Record future revisions separately'
reports={};files=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
for folder,count in [('bill-rest-north-candidate-native-v1',109),('bill-rest-north-station-v1',47)]:
    out=R/'output'/folder;r=json.loads((out/'validation.json').read_text());log=(out/'native.log').read_text()
    assert r['returnCode']==0 and f'{count} checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log
    reports[folder]={'checks':count,**r};files.extend(out/name for name in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png'])
    for archive in out.glob('interval-before-*'):files.extend(p for p in archive.iterdir() if p.is_file())
station=R/'output/bill-rest-north-station-v1';contacts=json.loads((station/'contacts.json').read_text());assert len(contacts['records'])==8 and all(s['facing']=='east' and s['bill_bunk'] and 'rest_head' not in s for row in contacts['stationAudit'] for s in row['stations'])
files.append(station/'contacts.json');files.extend(station/row['screenshot'] for row in contacts['records'])
summary='''Bill north generic rest candidate and furniture availability audit — October 1, 2026.
Two independent authored sources exec-c1d5b892-cc6b-4e4d-b663-69ffa565e67d and
exec-7086cca6-bbee-4926-a7e6-6434e82339ff preserve rear Bill identity/pack and
controlled shallow squat→kneel→forearm-supported prone rest, head north/boots
south. Added two planted-boot interiors before extraction to avoid first kneel
jump. Exact selected north idle,256px/p128,224/H148, fixed per-source rulers
[.31,148/425]/[.19,.23], one matte atlas grade each,8 entry poses/800ms, exact
reverse wake/800ms and2 relaxed sleep poses/1200ms.9 package invariants pass.
Initial broad burgundy classification included dark warm suit pixels and gain2.5
brightened shoulders. Restrict source red>70 and selected shoulder y100..125,
red>80 before estimating material gain; native board now matches muted master.
109 native player checks pass including exact restored rest-head metadata.
Native148/82 static board reviewed; continuous motion, fine rear pack/detail/
proportion/perspective joins and breathing remain polish, not owner acceptance.
Bill room renderer now calls existing optional Life.head_alignment like other
crew. New north head offset includes14.592 world-unit draw lift, so future
compatible pillow targets can account for actual renderer translation. Current
specialised east bunk bypasses helper and remains unchanged.
Authoritative availability changed next action: current habitation exposes ONE
specialised EAST Bill bunk in all4 rotations, with no generic north rest_head.
Initial fixture assumed two generic berths;7checks/5failures/0captures retained.
Corrected audit confirms actual selected east bunk and hook bypass:47checks pass,
8 native room captures (entry/rest in4rotations); rotation0 rest visually reviewed.
This is current station availability/bunk regression, NOT north candidate bed
contact or route proof. No geometry replacement to manufacture north acceptance.
North candidate remains unselected; no shared helmet, real compatible furniture,
interruptions, reward boundaries or Continue proof yet. Source legacy berth code
is not evidence that current geometry offers its target. Continue shared north
helmet, remaining south/west rest, then relevant runtime contexts/full-set polish.
'''+ '\n'.join(f"{name}: overall {r['passed']}, {r['seconds']}s, {r['realProfileFileCount']:,} real non-log files, changes {r['realProfileChanges']}" for name,r in reports.items())+'''
Every native probe scratch APPDATA; guard failures preserved, no owner profile
restoration or green-seeking repeat. Native rerun justified by new head metadata/
test; station rerun justified by corrected assumption, not clean-profile attempt.
Lesson: inspect current station data before deriving furniture requirements from
fallback source code. Record unavailable directional contexts separately while
still completing the requested full authored set. Rest pose crown can project
upward as a prone body extends north; never force every lowered pose to the same
standing bounds or infer physical height from crown position alone.
Pipeline, bible and maintained/installed skill updated. Full objective active;
no export, commit, economy, owner layout or specialised bunk replacement.
'''
handoff='# Project handoff\n\nUpdated: October 1, 2026 · Brine Space · Bill north rest\n\n## Objective and acceptance\nFull master-consistent animation set followed by cross-animation polish.\n\n## Accepted decisions and constraints\nExact selected idle, native ruler/matte palette; preserve current specialised east bunk and owner saves.\n\n## Current state\nNew north sources/prompts/build/manifest/frames/preview, fixture/UID and scratch runners; optional Bill rest-head renderer hook. Normal north rest is not selected.\n\n## Verification\n'+summary+'\n## Next action\nShared north helmet, south/west rest, relevant physical contexts and complete cross-animation polish.\n'
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8');files.append(P/'HANDOFF.md')
files.extend(R/name for name in ['scripts/grid_canvas.gd','tests/test_bill_rest_north_candidates.gd','tests/test_bill_rest_north_candidates.gd.uid','tests/test_bill_rest_north_station.gd','tests/test_bill_rest_north_station.gd.uid','tools/run_bill_rest_north_candidate_validation.py','tools/run_bill_rest_north_station_validation.py'])
hashes={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(P/'candidate-evidence.json').write_text(json.dumps({'reports':reports,'nativeSubsystemChecks':156,'packageChecks':9,'normalSelected':False,'northFurnitureProven':False,'stationAvailability':'current specialised east bunk only, all4 rotations','visualScope':'native148/82 candidate board and rotation0 selected bunk rest screenshot; continuous motion/physical north context unproven','sha256':hashes},indent=2)+'\n',encoding='utf-8')
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (R/name).open('a',encoding='utf-8') as f:f.write('\n\n## Bill north rest and current furniture audit — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-rest-north-coherent-v1/HANDOFF.md.\n')
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n\n## Bill north rest and current furniture audit — October 1, 2026\n\n'+summary)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill north rest and current furniture audit — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-rest-north-coherent-v1/HANDOFF.md.\n\n').encode()+status.read_bytes())
print('Recorded north rest109 native checks plus47 current-bunk audit checks; no north furniture acceptance')
