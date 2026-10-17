from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OUT=ROOT/'output/bill-death-ground-mortality-candidate-native-v1'
assert not (P/'lowered-entry-evidence.json').exists(), 'Historical recorder cannot overwrite lowered-entry evidence.'
r=json.loads((OUT/'validation.json').read_text());log=(OUT/'native.log').read_text();assert r['returnCode']==0 and '459 checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and r['nativeScreenshot']
summary=f'''Bill paired dry-collapse actual mortality candidate evidence — October 1, 2026.
64 real survival-trigger cases:4directions x2gear x2causes(oxygen/starvation)
x2prior states(idle/walk) x2cosmetic clock offsets. Existing RoomFlooding.step_crew
invokes actual die path, clears intent, existing grid renderer enters candidate0,
reaches terminal5 after2s and holds on repeated paused sampling.
16 actual RunSave disk write/read/restore roundtrips:4directions x2gear
x2saved elapsed(.65s/2s). Deceased identity/direction/gear and exact rendered
mid-fall or terminal pixels survive restoration. Actor and grid clock snapshots
use current production save APIs; no new save fields/controller changes.
459 native checks0failures in{r['seconds']}s; explicit scratch profile logged,
fresh82px terminal-family board reviewed. Overall validation {r['passed']};
{r['realProfileFileCount']:,} owner non-log files fingerprinted; changes{r['realProfileChanges']}.
Initial run458 checks passed, review PNG export failed due copied stale output
path; failed report/log retained. Corrected path then reran for new render evidence.
Explicit candidate base/equipment injection and cached production animation rows:
this is actual survival/renderer/save proof with candidate art, NOT normal loader
selection or a fresh process/title-screen Continue button test. Direction is fixture
controlled; no actual directional routing/physical clearance assertion here.
Board compares eight terminal candidates only; full station furniture occlusion,
collapse clearances, interruption joins from other actions/cargo/furniture, fine
master identity/helmet projection/material/detail/cadence still need review.
Family remains staged. Previous south/north profile-guard failures stay failures;
this new interval does not retroactively certify them. No real profile restoration,
normal art binding, owner geometry, gameplay reward/economy, commit or export change.
Next physical clearance/actual station visual review and normal selection proof;
generic rest, meals/inspection and full-set consistency/polish remain active scope.
Lesson: explicit candidate rendering must update both player and legacy grid
dictionary/timing views. Save restored pose evidence covers disk restoration in
that loaded process; independently verify normal selection/fresh Continue later.
'''
old=(P/'HANDOFF.md').read_text(encoding='utf-8')
(P/'HANDOFF.md').write_text('# Current mortality evidence — October 1, 2026\n\n'+summary+'\n## Earlier packaging milestone\n\n'+old,encoding='utf-8')
paths=[P/'manifest.json',P/'helmet-manifest.json',P/'prepare_mortality.py',P/'HANDOFF.md',ROOT/'tests/test_bill_death_ground_mortality_candidates.gd',ROOT/'tests/test_bill_death_ground_mortality_candidates.gd.uid',ROOT/'tools/run_bill_death_ground_mortality_candidate_validation.py']+[OUT/name for name in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png']]
e={'status':'staged_candidate','actualSurvivalCases':64,'diskRestoreRoundtrips':16,'nativeChecks':459,'nativeArtPassed':True,'overallPassed':r['passed'],'native':r,'frameBindings':json.loads((P/'verification.json').read_text())['sha256'],'scope':'real survival/production renderer and disk restoration under explicit candidates; physical clearance, other action joins, normal selection/fresh Continue and full art polish pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths}}
(P/'mortality-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
heading='## Bill dry-collapse actual mortality candidate evidence — October 1, 2026\n\n'
for relative in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/relative).open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
f=ROOT/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-death-ground-family-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded actual mortality/candidate renderer/disk restores; physical and normal selection proof remain')
