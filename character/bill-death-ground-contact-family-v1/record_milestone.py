from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
assert not (P/'candidate-evidence.json').exists(), 'Record later revisions separately.'
reports={};files=[]
for folder,count in [('bill-ground-death-contact-snapshot-v1',21),('bill-ground-death-contact-choice-v1',26),('bill-death-ground-contact-family-native-v1',401),('bill-death-ground-contact-station-v1',149),('bill-death-ground-contact-mortality-v1',598),('bill-death-ground-mortality-candidate-native-v1',459)]:
 out=R/'output'/folder;r=json.loads((out/'validation.json').read_text());assert r['returnCode']==0 and f'{count} checks,0 failures' in (out/'native.log').read_text()
 reports[folder]={'checks':count,**r};files.extend(out/name for name in ['validation.json','native.log','profile-before.json','profile-after.json'])
 if r['nativeScreenshot']:files.append(out/'loaded-water-carry.png')
guard='\n'.join(f"{key}: overall {r['passed']}, {r['seconds']}s, {r['realProfileFileCount']:,} real non-log files, changes {r['realProfileChanges']}" for key,r in reports.items())
summary='''Bill saved contact-aware dry-collapse candidate — October 1, 2026.
Separate12-state/72-literal-reference family retains original4directions and adds
north/south lateral options, paired bare/helmet. Authored source pixels unchanged.
Explicit deathContactMode opt-in marks family textures. Bill/MajorBill-only helper
compares original terminal projected alpha bounds with unpadded registered prop
collision rectangles; if obstructed, choose lateral only when both settled poses
clear all registered props. Open floor, absent variant or unknown geometry retain
original. Both alternatives obstructed retain original: no arbitrary foot teleport
or owner geometry adjustment; broader physical fallback remains unfinished.
Saved death_ground_variant (empty/lateral) is validated dry/dead/axial-only and
restored with existing saved authored entry prefix and cosmetic renderer clock.
Living/wet/unknown/malformed variants rejected; legacy absent field defaults empty.
Normal artwork selection unchanged; this is explicitly loaded candidate behavior.
401 whole-family exact loaded pixel/timing/metadata checks,149 actual station
selection checks and598 mortality/restore checks pass.64 actual oxygen/starvation
deaths:4headings x2gear x2contacts x2causes x2priorposes(kneel/repair).
32 production RunSave disk restores at.65s/2s retain actual restored actor variant,
entry prefix, identity/contact and exact mid-fall/terminal renderer pixels.
21 schema/26 conservative-choice checks pass, including upright default prefix,
open floor, missing options, unknown geometry and blocked lateral landing.
459 original upright mortality/restore regression checks pass.1,654 subsystem checks.
48 actual-choice station captures and16 actual restored terminal captures retained;
counter/aisle boards reviewed at unchanged native crop scale. Counter chooses
lateral for N/S bare/gear; aisle preserves original. Finite terminal remains stable.
First mortality audition598checks/120failures retained with captures/report/log:
fixture cached Bill across RunSave.restore, which REPLACES crew actors. Reacquire
game.bill_npc at every case and immediately after restore before checking identity
or further mutation. Corrected598-pass run is new evidence, not a retroactive pass.
Strict profile-guard outcomes:
'''+guard+'''
Explicit scratch APPDATA throughout. Live owner activity observed previously;
retain all deltas/failed guards, no restoration/retry for a clean interval.
Projected rectangle choice addresses visible counter intrusion; not an anatomical
floor-footprint model or universal collision proof. Upper-body intermediate joins,
both-obstructed fallback, other contacts/hazards/cargo/furniture/bunk, normal loader
binding and fresh-process title Continue remain. No normal-selection acceptance.
Next normal-loader/fresh Continue proof with saved variant, then wider joins and
remaining generic rest/meals/inspection/full-set master consistency/polish.
No owner layout, route/reward/economy, commit or export changes. Full goal active.
Lesson: saved visual variant must be chosen once before death and restored rather
than recomputed without geometry. Restore checks must inspect the newly created
production actor, not a stale reference with plausible fields.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · Brine Space · Task: Bill saved contact-aware collapse

## Objective and acceptance
Complete Bill master-consistent animation set and full cross-animation polish.

## Accepted decisions and constraints
Retain open-floor falls, exact idle/canonical helmets, authored scale/matte grade.
Keep owner geometry and real saves intact; use scratch fixtures. Candidate proof
does not certify normal selection, title Continue or all physical placement.

## Current state
New contact-family manifests/tools/reviews. Narrow edits to Bill snapshot/restore,
bill_ground_death and player metadata. New schema/choice/family/station/mortality
fixtures/runners. Existing 4-direction family and lateral source packages retained.

## Verification
'''+summary+'''
## Next action
Normal loader and fresh-process Continue, then wider joins/placement and remaining
life animation contexts, complete master matching and polish. Goal remains active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files.extend(f for f in P.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.name!='candidate-evidence.json')
for name in ['scripts/bill_ground_death.gd','scripts/bill_npc.gd','scripts/crew_sprite_player.gd']:
 f=R/name;files.extend([f,f.with_suffix(f.suffix+'.uid')])
for name in ['test_bill_ground_death_contact_snapshot','test_bill_ground_death_contact_choice','test_bill_death_ground_contact_family','test_bill_death_ground_contact_station','test_bill_death_ground_contact_mortality']:
 files.extend([R/'tests'/(name+'.gd'),R/'tests'/(name+'.gd.uid')])
files.extend(R/'tools'/name for name in ['run_bill_ground_death_contact_snapshot_validation.py','run_bill_ground_death_contact_choice_validation.py','run_bill_death_ground_contact_family_validation.py','run_bill_death_ground_contact_station_validation.py','run_bill_death_ground_contact_mortality_validation.py'])
failed=R/'output/bill-death-ground-contact-mortality-v1'
for archive in failed.glob('interval-before-*'):
 f=archive/'validation.json'
 if f.exists() and json.loads(f.read_text()).get('returnCode')==1:files.extend([f,archive/'native.log'])
captures={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for folder in ['bill-death-ground-contact-station-v1','bill-death-ground-contact-mortality-v1'] for f in (R/'output'/folder).glob('*.png')}
(P/'candidate-evidence.json').write_text(json.dumps({'status':'saved_contact_candidate_actual_mortality_reviewed','subsystemChecks':1654,'reports':reports,'scope':summary,'frameBindings':json.loads((P/'verification.json').read_text())['sha256'],'captureBindings':captures,'sha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
heading='## Bill saved contact-aware dry-collapse candidate — October 1, 2026\n\n'
for rel in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/rel).open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
f=R/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-death-ground-contact-family-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded saved contact-aware candidate and1,654 subsystem passes; normal/fresh Continue/full polish remain')
