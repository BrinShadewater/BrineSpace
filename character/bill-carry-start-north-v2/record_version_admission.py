"""Record selected North source-bank evidence and lessons without changing authored art."""
from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;R=P.parents[1]
read=lambda name:json.loads((R/'output'/name/'validation.json').read_text(encoding='utf-8'))
reports={name:read(name) for name in ['bill-carry-source-versions-v1','bill-carry-normal-snapshot-v1','bill-carry-source-version-continue-v1','bill-carry-normal-priority-v1','bill-carry-north-version-priority-v1','bill-carry-normal-regressions-v1','bill-carry-bank-isolation-native-v1']}
assert all(v['passed'] and not v['realProfileChanges'] for v in reports.values())
smoke=json.loads((R/'output/bill-carry-bank-isolation-native-v1/records.json').read_text(encoding='utf-8'))
assert smoke['failures']==0 and len(smoke['records'])==2
f=R/'output/bill-carry-north-version-priority-v1/records.json';priority=json.loads(f.read_text(encoding='utf-8'))
if 'scopeOriginallyWritten' not in priority:priority['scopeOriginallyWritten']=priority['scope']
priority['scope']=priority['scope'].replace('18 controlled actual-main priority cases on natural entry/settle/rise:', '18 controlled selected-main North priority cases on a prescribed collision-clear lane, entry/settle/rise:')
priority['scopeCorrectionOnly']='Post-run wording correction; execution and assertions unchanged. Final completion checks additionally use original generated workshop route.'
f.write_text(json.dumps(priority,indent=2)+'\n')
e=json.loads((P/'version-runtime-evidence.json').read_text(encoding='utf-8'))
e.update({'reports':reports,'checks':{'sourceVersions':1073,'normalSnapshots':604,'freshNorthRestores':692,'normalPriority':479,'northPriority':498,'finalBankIsolationNative':smoke['checks']},'finalBankIsolation':smoke,'verificationRevisions':'Full eight-case native interval, priority and normal regressions preceded the final malformed-bank isolation guard. Final1073/604unit and two actual cold disk restores exercise final guard; complete valid bank motion unchanged. Earlier interval and hash snapshot retained separately.','visualReview':'All eight native before/after pairs reviewed in browser at station scale; both source versions and gears, first-step and arrival. Exact source RGBA, physical root and clock established by fixture. No continuous native-film or broad support/glide acceptance claim.','retainedArtHashCheck':{'inputs':105,'changed':[]},'priority':priority,'goalComplete':False})
(P/'version-runtime-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
phrase='Full travel, interruptions and save/resume remain under review.'
replacement='The new North set is selected for new sessions. Existing saves retain their source version. Save/resume and interruptions pass the current station checks; natural routes and broader contact polish remain under review. <a href="version-continue.html" style="color:#adcddd">View station Continue comparisons</a>'
for name in ['index.html','build_review.py']:
 path=P/name;path.write_text(path.read_text(encoding='utf-8').replace(phrase,replacement),encoding='utf-8')
title='## Bill North carrying version selected with saved-source continuity - October 2, 2026'
milestone='''
Selected normal Bill playback now defaults to articulated North gait2/start2.
It retains original North gait1/start1 sources in a separate loaded bank. Actor and
player checkpoints bind the same supported version; detached loaded-bank admission
validates cache/entry/arrival before changing live state. Restored sessions keep their
version for their lifetime; no mid-pose automatic migration. Unbound legacy saves
enter retained bank with no invented pending program. Other directions, turn matrix,
master art, geometry and ordinary service/priority behavior retained.

1073 source-version guards and604 normal snapshot guards pass.692 native checks,
8 actual scratch disk/fresh selected-main restores: both versions/gears, North
first-step and arrival, same exact RGBA/root/clock, pause and30future ticks. Real
workshop dispatch with prescribed collision-clear North lane, not natural chooser
coverage. All8 native before/after pairs reviewed at station scale;32 unmodified
room/source captures copied into package. Normal priority479 and North priority498
checks pass (18cases each: actual fire dispatch, public gear change and mortality,
15future cancellation ticks). Fire scope does not prove arrival at refuge. North
priority's inherited 'natural' report wording corrected after run; assertions and
execution unchanged, original wording retained. Normal save/Title Continue and
14 bunk disk restores pass, engine0/113.72s. Existing Image.load export warning in
bunk fixture remains. All intervals scratch APPDATA/all2931owner non-log files
unchanged.105 prior recorded art inputs unchanged; no source repaint/rescale/grade.

First604-unit interval failed five assertions: four fixtures removed live North
rows but retained the new recoverable bank; one paired a new actor default with an
old resumed player. Fixtures now remove matching stored rows and bind actor to its
actual player, retaining the missing-source and mixed-version rejection checks.
No production guards weakened. Final604/6.92s and1073/5.55s pass; failed interval
retained. Fresh restores692/299.58s; normal priority479/44.42s;
North priority498/43.70s. Package checks remain separate from visual acceptance.

Final review found partial-bank merge could borrow a missing old North row from
current bank. Require complete paired six-row source/timing banks before admission
or selection, and erase target North keys before applying bank. Four added unit
checks reject incomplete old bank with intact current bank, both gears, without
live mutation. FINAL_SMOKE_CHECKS native checks/two additional cold disk restores of bare
North entry (both versions) pass on final guard. Prior8native/priority/regression
intervals preceded this guard; complete valid bank motion is unchanged, final unit
and focused native checks verify added admission condition. No broad native rerun.

Changed selected player/controller/checkpoint helper and virtual player binding,
targeted tests/runners, review and lessons. Full goal active/incomplete. Next South
stride support/amplitude against cardinal masters, all-direction natural/short-path
contact, floor-case-to-idle and remaining equipment/actions/full cross-family polish.
Handoff: character/bill-carry-start-north-v2/VERSION_ADMISSION_HANDOFF.md.
No commit/export or owner acceptance claim.
'''.replace('FINAL_SMOKE_CHECKS',str(smoke['checks']))
def replace_section(path,title,body,prepend=False):
 text=path.read_text(encoding='utf-8')
 if title in text:
  a=text.index(title);b=text.find('\n## ',a+len(title))
  text=text[:a]+title+'\n'+body+'\n'+(text[b:] if b>=0 else '')
 elif prepend:text=title+'\n'+body+'\n'+text
 else:text+='\n'+title+'\n'+body
 path.write_text(text,encoding='utf-8')
path=R/'docs/CURRENT_STATUS.md';text=path.read_text(encoding='utf-8')
replace_section(path,title,milestone,True)
path=R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md'
replace_section(path,title,milestone)
lesson='''
## Animation source versions and resumed identity - October 2, 2026

A source replacement can preserve frame count, canvas, pivot and timing while
changing the visible saved pose. Bind actor and playback to the same explicit source
version. Validate against a detached loaded bank before changing live playback;
retain old sources for existing saved sessions instead of silently substituting a
new silhouette at the same index. New sessions can select the improved bank while
restored sessions retain theirs. Keep complete quoted manifest paths. Review exact
source RGBA and actual room/root/clock before and after fresh Continue, then future
ticks and priority cancellation. A recoverable retained bank still counts as loaded
art: missing-source fixtures must remove its matching rows too. Mixed actor/player
versions must remain rejected. Require complete paired source/timing bank before
selection and erase old target keys before applying it; partial dictionary merges
must never borrow poses from another version. Four isolated malformed-bank guards
and two focused native cold restores verify final isolation condition. Earlier
eight-case native/priority/regression intervals preceded that guard, with complete
valid bank motion unchanged. Bill North admission:1073 version/604 general unit,
692 native/8fresh restores,479 general and498 North priority checks; normal save and
14bunk restores pass. Both versions/gears' eight station pairs reviewed;105 retained
art inputs unchanged. Scratch full-profile protection. Prescribed North lane is not
natural path/contact coverage; source replay is not native film. Full set/polish open.
'''
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 heading='## Animation source versions and resumed identity - October 2, 2026'
 replace_section(path,heading,lesson.split(heading,1)[1].lstrip())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill North normal source admission

## Objective and acceptance
Full Bill master-matching animation set, then cross-family consistency/polish. This
milestone selects improved North carrying without changing saved-source identity.

## Accepted decisions and constraints
New sessions North gait2/start2; restored sessions retain explicitly bound gait1/start1
or gait2/start2 for their lifetime. No mid-pose migration or owner save/geometry edits.
Exact original protected upper and matte grade retained. No commit/export requested.

## Current state
Selected scripts/bill_carry_player.gd caches both banks and validates detached loaded
source before restore; bill_carry_npc.gd stamps matching actor binding and selects on
validated restore; bill_carry_checkpoint.gd rejects mixed/unknown bindings. Parent
v3 stow_player exposes a virtual binding getter. New version tests/runners and native
version-continue.html/32captured PNGs/evidence live here. Normal tests use selected
checkpoint helper; no source PNG changes. Skills, pipeline, bible and status updated.

## Verification
1073version+604general unit guards;692native/8actual disk/fresh selected-main restores,
both versions/gears, North entry/arrival+30future ticks and pause. All8native before/
after pairs visually reviewed.479general+498North priority checks/18cases each;
normal save/Title Continue and14bunk restores pass. All2931owner non-log files unchanged
under scratch APPDATA.105 prior art inputs unchanged. Existing bunk Image.load export
warning remains. Failed initial unit interval and scope wording correction retained.

Final complete-bank isolation guard follows earlier8native/priority/regression
intervals.1073/604final unit plus two focused cold disk restores pass on finalguard;
valid complete-bank motion unchanged. No implicit fallback to other version allowed.

## Next action
South stride amplitude/support compared against all cardinal masters; natural and
short-path foot contact, floor-case-to-idle, equipment/actions matrix, full-set polish.
Native North lane was prescribed and collision-clear; no natural chooser or full
anatomical contact certification. Full goal active/incomplete.
'''
(P/'VERSION_ADMISSION_HANDOFF.md').write_text(handoff,encoding='utf-8')
inputs=set(json.loads((P/'input-hashes.json').read_text(encoding='utf-8')))
inputs.update(p.relative_to(R).as_posix() for p in (P/'version-captures').glob('*.png'))
for pack in ['bill-carry-north-gait-v1','bill-carry-start-north-v1']:
 for p in (R/'character'/pack).rglob('*'):
  if p.is_file() and (p.suffix=='.png' or p.name.endswith('manifest.json')):inputs.add(p.relative_to(R).as_posix())
for name in ['scripts/bill_carry_checkpoint.gd','tests/test_bill_carry_source_versions_v1.gd','tests/test_bill_carry_source_version_continue_v1.gd','tests/test_bill_carry_north_version_priority_v1.gd','tests/test_bill_carry_normal_snapshot_v1.gd','tests/test_bill_carry_normal_continue_v1.gd','tests/test_bill_carry_normal_priority_v1.gd','tests/test_run_save.gd','tests/test_bill_bunk.gd','tools/run_bill_carry_source_versions_v1_validation.py','tools/run_bill_carry_source_version_continue_v1_validation.py','tools/run_bill_carry_north_version_priority_v1_validation.py','tools/run_bill_carry_normal_regressions_v1_validation.py']:
 inputs.add(name)
for p in [P/'build_version_fixture.py',P/'build_version_review.py',P/'index.html',P/'version-continue.html']:inputs.add(p.relative_to(R).as_posix())
for name in ['tests/test_bill_carry_bank_isolation_native_v1.gd','tests/test_bill_carry_bank_isolation_native_v1.gd.uid','tools/run_bill_carry_bank_isolation_native_v1_validation.py','character/bill-carry-start-north-v2/build_bank_smoke.py','character/bill-carry-start-north-v2/record_version_admission.py']:
 inputs.add(name)
hashes={name:hashlib.sha256((R/name).read_bytes()).hexdigest() for name in sorted(inputs) if (R/name).is_file()}
(P/'version-input-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
print(f'North selection recorded: {len(hashes)} input hashes; 8 reviewed native pairs plus 2 final cold restores; all seven validation intervals pass')
