from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
assert json.loads((P/'packaging-validation.json').read_text())['passed']
for name in ['native-staged','native-behaviour','native-installed','native-installed-behaviour']:
    report=json.loads((P/(name+'-validation.json')).read_text())
    assert report['exitCode']==0 and not report['timedOut'] and report['realProfileUnchanged']
def atomic(file,fn):
    before=file.read_bytes();after=fn(before);tmp=file.with_name(file.name+'.james.tmp');tmp.write_bytes(after)
    if file.read_bytes()!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(file))
    tmp.replace(file)
note='''### James death installed; full-set polish started — September 30, 2026

Eight independently authored ground/water death states installed in both modes.
character/james-death-family-v1, four facing sources, exact prompts/SHA/originals
andv1/v2 repairs retained. Ground entry uses exact selected idle0; water entry
uses exact selected swim0. Each finite clip holds its last authored pose. Retained
clocks: E ground1420ms/water1560ms, other directions2000ms.256x360,p128224,
standing148. Fixed cranial rulersE25/70,S25/72,W25/60,N22/62; floor-contact
registration for ground, reviewed cranial proxies for water, no height fitting.
Selected shared helmets use recorded donor0/1/4 and pitch rotations per pose.

Initial axial water sources stretched projected legs. Local source repairs
shortened legs/soles while preserving skull/torso drawing scale; do not use upright
silhouette height as a ruler for floating/fallen anatomy. Side edits removed extra
goggles; South keeps its actual gold forehead goggles. Review equipment/face
details even when generation was told to preserve them. Original source evidence
and true alpha remain; invisible RGB gradient does not imply an opaque background.

528 package,1045 staged and1044 installed player checks PASS.548 candidate and547
installed controlled mortality checks PASS: actual RoomFlooding.kill accounting,
chooser,6 slots, pause and finite terminal hold,16 room-node cases/96 native
captures. Boards reviewed; owner profile unchanged under scratch APPDATA. The
first installed capture run hit90s timeout after35 captures with no engine errors;
retained timeout report, reran through local240s capture wrapper to terminal PASS.
No oxygen-exhaustion journey or disk-restored terminal-phase proof. Dead snapshot
validity is checked; sprite playback phase is not persisted by that snapshot.
Gameplay mortality/Second Chance and selected clearance remain unchanged.

Literal-loader audit now173bare/171helmet states,3196/3172slots,zero retained
states. This is source coverage, not full-set visual acceptance.41 family review
boards sample344 selected clips against actual directional masters at82px. First
death-ground/recover-air/carry-turn boards reviewed; other boards remain to inspect.
Polish candidates: North recovery broad boots/stance versus master; side-water
death limb-length seam; cargo water turn quarter800ms versus half680ms angular
speed; non-East arrival facing snap; North sleep breathing; disk-restored corpse
terminal phase; furniture/meal/equipment/full travel handoffs. Goal remains active.
See docs/JAMES_DEATH_HANDOFF_2026-09-30.md and
character/james-animation-coverage-2026-09-30/consistency-review/.
'''
headline='''## James death family installed; full-set consistency pass started — September 30, 2026

All8 ground/water death states installed, bare and shared helmet.528 package,
1044 installed player and547 actual installed mortality checks PASS;96 native
captures reviewed, scratch owner profile unchanged. Finite terminal poses retained.
Source audit now zero retained clips:173bare/171helmet states.41 comparison boards
prepared; cross-family proportions/material/motion and complete handoffs remain
open. Coverage is not full-set acceptance. See [handoff](JAMES_DEATH_HANDOFF_2026-09-30.md).

'''
atomic(R/'docs/CURRENT_STATUS.md',lambda b:b if headline.encode() in b else headline.encode()+b)
for file in [R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    atomic(file,lambda b:b if note.encode() in b else b+b'\n\n'+note.encode())
(R/'docs/JAMES_DEATH_HANDOFF_2026-09-30.md').write_text('''# Project handoff

Updated: 2026-09-30 · Project: Brine Space · Task: James death installation and consistency

## Objective and acceptance
Full James animation set followed by cross-family consistency/polish. Source
coverage now has zero retained clips; full-set visual/behavior acceptance remains
open. New death family installed_owner_review_pending.

## Accepted decisions and constraints
Current matte neutral masters, correct anatomical belt tools, independent facings,
fixed anatomical source rulers; falling/floating silhouettes lower naturally.
Ground/water exact current entry poses and retained finite clocks/terminal hold.
Preserve mortality/Second Chance rules; all probes scratch APPDATA.

## Current state
character/james-death-family-v1 plus four facing source folders, selectedv2
source repairs.96 refs,256x360,p128224,standing148. Normal grid literal loaders
and ACTIVE_ASSETS.json installed. Runtime clearance unchanged. Pipeline/bible/
continuation and canonical+installed skill lessons updated. Coverage audit173bare/
171helmet states,3196/3172slots,zero retained states.41 family comparison boards
and344 sampled clip diagnostics in character/james-animation-coverage-2026-09-30/
consistency-review. Only death-ground/recover-air/carry-turn comparison boards
reviewed so far; diagnostics and alpha height are not visual acceptance.

## Verification
528 package,1045 staged and1044 installed player checks PASS.548 candidate and547
installed mortality checks PASS: actual RoomFlooding.kill accounting/chooser,
6slots/case,pause/terminal hold,16clear room nodes,96captures. Both native contact
and installed behavior boards reviewed; owner profiles unchanged. Initial installed
capture run timed out90s after35captures/no errors; retained report, final local240s
wrapper run completed PASS. No live generation or test processes remain.
Direct mortality fixture does not establish oxygen-exhaustion travel. Snapshot
validity is checked, disk-restored terminal sprite phase is not proved.

## Next action
Continue systematic41family visual/motion comparison. Refine North recovery broad
boots/stance, measure side-water death entry proportions, compare water cargo
quarter800ms/half680ms speed; resolve arrival facing snap/North sleep breathing/
disk-restored corpse phase and furniture/meal/equipment/full journeys. Validate
each changed family appropriately, retain prior passing evidence and owner art
decisions. No commit/export/full-set completion.
''',encoding='utf-8')
# The audit's generated next-work paragraph must no longer imply unmade families.
file=R/'character/james-animation-coverage-2026-09-30/audit.py'
before=file.read_text();a=before.index(" 'Current next work:");b=before.index("\n(HERE/'README.md')",a)
replacement=" 'Current work: all listed families now have selected revised sources; zero retained James clips. Continue41-family comparison against current masters and full motion/handoff polish. Read docs/JAMES_DEATH_HANDOFF_2026-09-30.md for checks and outstanding scope. Preserve authored crouch/swim/fallen dimensions; do not force them to standing bounds.', '', 'Runtime selection is not full-set visual, owner or release acceptance.']"
atomic(file,lambda data:(before[:a]+replacement+before[b:]).encode())
print('Recorded death installation and zero-retained coverage milestone; full consistency/polish goal active')
