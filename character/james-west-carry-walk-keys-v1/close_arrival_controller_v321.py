from pathlib import Path
import json,hashlib
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-controller-v321';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
v=json.loads((o/'native_probe-validation.json').read_bytes());n=json.loads((o/'native-evidence.json').read_bytes())
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert (n['checks'],n['failures'])==(122,0) and len(n['observations'])==40
log=(o/'native_probe.log').read_text(encoding='utf-8');assert 'SCRIPT ERROR:' not in log and 'ERROR:' not in log
reg=json.loads((o/'crew_regression-validation.json').read_bytes());assert reg['realProfileUnchanged'] and not reg['profileDelta'];assert reg['exitCode']!=0
paths=[r/'scripts/branforth_npc.gd',r/'scripts/james_cargo_player.gd',r/'scripts/james_workshop_arrival.gd',o/'native_probe.gd',o/'crew_regression.gd',r/'tests/test_branforth_crew.gd']
for f in paths:assert f.with_suffix(f.suffix+'.uid').exists()
(o/'tested-source-hashes.json').write_text(json.dumps(dict(postRunSha256={f.relative_to(r).as_posix():sha(f) for f in paths},note='Recorded after final successful run, not a pre-launch freeze.'),indent=2)+'\n',encoding='utf-8')
report=dict(disposition='normal_arrival_controller_integrated_visual_review_pending',checks=122,failures=0,actualRendererSamples=40,gears=2,incomingDirections=['west','east','south','north'],actualActorDiskRestoreCases=8,normalArrivalControllerChanged=True,normalArtworkChanged=False,latestSourceCandidatesSelected=False,visualMotionAcceptance=False,fullGoalComplete=False,findings=['Actual arrive preserves workshop_unload instead of allowing generic curiosity diagnostics to overwrite idle state. Incoming dry west/east/south facing is optional actor checkpoint data. Existing2s budget is retained.', 'James-owned cargo player selects available gear-specific north turn before unloading, subtracting actual turn duration from unload clock. Normal west/east turn banks available; south missing clip and north facing safely retain direct unloading. No shared renderer or other crew source changed.', '122focused checks pass:40actual renderer samples through normal banks,8full actor snapshot admissions/disk field roundtrips/actual actor restores, legacy missing-field validation, malformed origin rejection, actual main pause, death/flood bypass. Owner profile unchanged. No autonomous route/whole-run checkpoint/titleContinue/motion visual acceptance claim.', 'Earlier selector oracle used literal0.4 rather than actual2.0-timer clock at a floating-point phase boundary; diagnostic revealed this and oracle now uses observable simulation clock. Restore fixture originally used unsafe core center; corrected to actual collision-clear workshop contact. Pause uses main processing, not direct NPC update.', 'Broader existing test_branforth_crew stopped in fixture setup at line60 assigning seed to Nil decision_rng. Exact probe process terminated; profile unchanged. Retained failed log/report, not reported as a regression pass. Full crew regression remains unresolved.'])
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();d=json.loads(old)
d['northArrivalControllerReview']=dict(version=321,file=(o/'review.json').relative_to(r).as_posix(),checks=122,failures=0,normalArrivalControllerChanged=True,normalArtworkChanged=False,visualAcceptance=False)
d['normalChanged']=True;d['normalArtworkChanged']=False;d['normalArrivalControllerChanged']=True
d['nextVisualRepair']='321 connects available normal west/east cargo turns to actual dry arrival and saves incoming facing; unavailable south turn falls back.122focused selector/actor restore/pause checks pass. Existing crew regression fixture stopped at uninitialized RNG setup. Next real autonomous arrival/continuous visual review and full RunSave/Continue/interruptions.317/320source candidates still unselected; return/rise material/support/case and helmet, latest carry/turn master fidelity and all-family polish remain.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
section='''### James actual workshop arrival selector - October3,2026

V321 narrow normal controller/player integration: dry cargo arrival remembers its
incoming facing and returns before generic diagnostics can override unload idle.
James-owned cargo player renders available gear-specific turn to north first,
then unloading from elapsed minus turn duration within unchanged2s stage. Current
normal west/east turns available; missing south clip/north facing keep direct
unload. Optional actor checkpoint field defaults empty for older saves; eligibility
clears it on interruption or invalid restored contact. Existing artwork and review
candidate selections unchanged; no shared grid/other crew edits.

122focused native checks0:40actual renderer samples in2gears/4incoming facings,
8full actor admissions/disk field roundtrips/actual actor restores, legacy field
validation, malformed origin rejection, main pause, death/flood bypass. Scratch
profile fingerprint unchanged. This is selector/actor-state evidence, not visual
motion, autonomous route, whole-run checkpoint or titleContinue acceptance.
Existing broader crew fixture stopped during setup at test_branforth_crew.gd:60
assigning RNG seed to Nil; exact probe stopped, log retained, owner unchanged.
No broad regression pass claimed. Latest317/320source candidates remain unselected.

Lessons: superclass arrival return does not stop subclass diagnostics; preserve
the cargo stage explicitly. Presentation-only water/carry transitions cannot infer
a turn after controller state changes to unload. Save incoming facing and use the
simulation clock, gear-specific clip duration and safe fallback. At exact phase
boundaries use observed2-timer clock, not a nominal test literal. Restore probes
need collision-clear actual room contact; pause is enforced by normal main update,
not by manually calling NPC update. Full visual/master, arrival/lifecycle/Continue
and all-family consistency remain incomplete.
Handoff: character/james-west-carry-walk-keys-v1/arrival-controller-v321/HANDOFF.md.
'''
guides=record_guides(r,section,'### James original-pose unloading return comparison - October3,2026')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James workshop arrival

## Objective and acceptance
Full master-matched animation set, actual gameplay integration and whole-family
polish. Selector/state checks and continuously reviewed visual motion are separate.

## Accepted decisions and constraints
Matte master appearance, fixed support, belt wrench, tablet diagnostics and forward
torch. Preserve stage budgets/resources and owner saves; no other crew/art edits.

## Current state
scripts/james_workshop_arrival.gd plus pairedUID; narrow additions to branforth_npc
and james_cargo_player.321 focused probe/UID/log/evidence/review/post-run hashes;
broader crew regression shim/UID/failed log, UID helper; ledger and five guides.
Normal dry arrival now plays available west/east turn before unload within2s.
South missing turn and north arrival use direct unload. No artwork selection changes.

## Verification
122checks0;40actual renderer samples,8actor disk restores/admissions, optional
legacy field, malformed origin, main pause, death/flood. Owner profile unchanged.
Failed earlier diagnostics corrected actual-clock oracle and unsafe fixture contact.
Broader crew test stops at Nil RNG seed setup line60; retained as failed/unresolved.
No advancing visual/autonomous arrival/whole-run save/titleContinue proof.

## Next action
Exercise real autonomous workshop arrival and continuous paired motion; whole-run
checkpoint/Continue and interruptions. Resolve broader crew fixture setup before
claiming regression coverage.317/320candidate sources still need return/rise
material/support/case and helmet; latest carry/turn master fidelity and all-family
polish remain. Full goal active, no external blocker.
''',encoding='utf-8')
with(p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
print(json.dumps(dict(checks=122,failures=0,rendererSamples=40,actorRestores=8,normalArrivalControllerChanged=True,normalArtworkChanged=False,broaderCrewRegression='fixture_setup_failed',guides=guides,fullGoalComplete=False)))
