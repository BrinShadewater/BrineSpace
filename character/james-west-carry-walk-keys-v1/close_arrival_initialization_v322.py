from pathlib import Path
import json,hashlib
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-controller-v322';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
before=json.loads((o/'constructor-before.json').read_bytes());after=json.loads((o/'constructor-evidence.json').read_bytes())
assert before['baseRng'] and not before['cargoRng'] and before['baseSpawn']!=before['cargoSpawn'] and before['baseMaintenance']!=before['cargoMaintenance']
assert after['cargoRng'] and after['cargoSpawn']==after['baseSpawn'] and after['cargoMaintenance']==after['baseMaintenance']
for name in ['constructor_probe','native_probe','crew_regression']:
 v=json.loads((o/(name+'-validation.json')).read_bytes());assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
 log=(o/(name+'.log')).read_text(encoding='utf-8');assert 'SCRIPT ERROR:' not in log and 'ERROR:' not in log
assert 'BRANFORTH THREE CREW: PASS; minimum separation 32.01' in (o/'crew_regression.log').read_text(encoding='utf-8')
n=json.loads((o/'native-evidence.json').read_bytes());assert(n['checks'],n['failures'],len(n['observations']))==(122,0,40)
paths=[r/'character/james-cargo-return-bridges-v1/return_actor.gd',r/'scripts/branforth_npc.gd',r/'scripts/james_cargo_player.gd',r/'scripts/james_workshop_arrival.gd',r/'tests/test_branforth_crew.gd']+[o/(name+'.gd') for name in ['constructor_probe','native_probe','crew_regression']]
assert all(f.with_suffix('.gd.uid').exists() for f in paths)
(o/'tested-source-hashes.json').write_text(json.dumps(dict(postRunSha256={f.relative_to(r).as_posix():sha(f) for f in paths},note='Recorded after successful tests, not pre-launch freeze.'),indent=2)+'\n',encoding='utf-8')
review=dict(disposition='engineering_initialization_restored_regressions_pass',constructorBefore=before,constructorAfter=after,arrivalChecks=122,arrivalFailures=0,actualRendererSamples=40,crewRegression='PASS',crewRegressionMode='headless',minimumCrewSeparation=32.01,ownerProfilesUnchanged=True,normalEngineeringInitializationChanged=True,normalArtworkChanged=False,fullGoalComplete=False,findings=['Constructor-only comparison disproved initial startup-race hypothesis: direct engineering actor has private RNG, engineering spawn and maintenance preferences; cargo subclass had Nil RNG,zero spawn and base crew preferences. Cargo return _init omitted explicit parent constructor. Added super(), retaining its own clearance setup.', 'Three-crew regression now reaches its assertions. Legacy fixture initially retained James cargo extension after erasing James actor. That inconsistent bound packet correctly rejects. Fixture now separately asserts rejection then erases modern extension when simulating older schema. Save validation remains strict.', 'Constructor comparison passes; native actual arrival selector/actor restore/pause122checks0 and40renderer samples pass after production constructor change. Existing three-crew regression passes headless: movement/traffic, modern disk snapshot/playback restoration, malformed save rejection and older actor/crew-absent schemas. All scratch profile before/after checks unchanged.', 'No artwork change or new owner visual acceptance. No autonomous arrival/advancing motion/title-screen Continue proof. Latest317/320sources remain unselected; unloading master/material/support/case and helmet, latest cargo/turn and all-family consistency remain.'])
(o/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();d=json.loads(old)
d['engineeringInitializationReview']=dict(version=322,file=(o/'review.json').relative_to(r).as_posix(),arrivalChecks=122,arrivalFailures=0,crewRegression='PASS',normalEngineeringInitializationChanged=True,normalArtworkChanged=False)
d['nextVisualRepair']='322 restores engineering constructor in normal cargo subclass; private RNG/spawn/service identity and broad three-crew regression now pass, arrival122checks0 retained. Next actual autonomous workshop arrival/continuous paired motion and full arrival RunSave/titleContinue/interruptions.317/320candidate source material/support/rise/case and helmet, latest cargo/turn master fidelity and whole-family polish remain.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
section='''### James cargo constructor identity and crew regression - October3,2026

V322 constructor-only evidence finds normal cargo subclass skipped engineering
initialization: Nil private RNG,zero spawn offset and base crew service preferences
versus direct James RNG,(-48,32) spawn and engineering services. Explicit super()
in return_actor._init restores intended identity while keeping cargo clearance.
This was a real inheritance defect; initial startup-race hypothesis was disproved.
No artwork selection change. Constructor before/after receipts retained.

Arrival selector/actual actor disk restore/pause122native checks0 and40renderer
samples pass again after constructor fix. Existing three-crew regression passes
headless: movement/traffic (minimum32.01), modern disk state/playback, malformed
save rejection, older schemas missing James/crew. Its legacy fixture previously
deleted James but retained the modern actor-bound cargo extension; now asserts
that inconsistent packet rejects, then removes extension to model a genuine older
schema. Production checkpoint guards remain strict. All scratch owner fingerprints
unchanged. Shared validation helper gains optional headless mode; pairedUIDs kept.

Lessons: inspect actual subclass construction before calling Nil RNG a fixture
race. Animation wrappers must preserve engineering constructor identity and private
random stream. Historical-schema fixtures must remove later dependent extensions,
while retaining explicit inconsistent-packet rejection. Headless crew regression
and native selector checks do not prove visual motion or title-screen Continue.
Next autonomous arrival/advancing paired review and full arrival lifecycle; latest
317/320art unselected, master/material/support/case/helmet and all-family polish open.
Handoff: character/james-west-carry-walk-keys-v1/arrival-controller-v322/HANDOFF.md.
'''
guides=record_guides(r,section,'### James actual workshop arrival selector - October3,2026')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James initialization/regression

## Objective and acceptance
Full master-matched James set, real integration and whole-family consistency.
Constructor/selector/crew tests do not establish full visual acceptance.

## Accepted decisions and constraints
Preserve original engineering identity/private RNG, matte masters, fixed support,
belt wrench, tablet diagnostics/forward torch, normal costs and owner progress.

## Current state
return_actor._init now explicitly initializes engineering superclass. Narrow legacy
fixture correction in tests/test_branforth_crew.gd retains bound-packet rejection.
run_validation.py optional headless mode.322 constructor evidence before/after,
native122selector probe, headlesscrew shim, logs/reviews/post-run source hashes,
pairedUIDs; ledger/five guides. Normal artwork/candidate selections unchanged.

## Verification
Constructor RNG/spawn/service profile matches direct James. Arrival122checks0,
40renderer samples and actor restores/pause pass. Three-crew regression PASS
headless, minimum separation32.01, modern/older disk saves and playback. Owner
profiles unchanged in every run. Earlier legacy failure log preserved. No new
visual motion/autonomous arrival/title-screen Continue evidence.

## Next action
Actual autonomous workshop arrival and advancing paired review; full arrival
checkpoint/titleContinue/interruptions.317/320candidate return/rise material,
support/case and helmet remain; latest cargo/turn master fidelity and all-family
polish open. Full goal active, no external blocker.
''',encoding='utf-8')
with(p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
print(json.dumps(dict(constructorMatched=True,arrivalChecks=122,arrivalFailures=0,crewRegression='PASS',minimumSeparation=32.01,guides=guides,normalArtworkChanged=False,fullGoalComplete=False)))
