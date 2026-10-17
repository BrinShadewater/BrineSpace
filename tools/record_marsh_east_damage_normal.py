"""Record inspected full normal East damage checkpoint milestone."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-injury-material-v1'
MARKER='## Marsh East normal damage family admission and full Continue — October 2, 2026'
LESSON='''
## Marsh East normal damage family admission and full Continue — October 2, 2026

Normal catalog selects complete East dry candidate01 and white-fluid injury/
rise candidate01 provisionally. No source rewrite, runtime or save-format change.
Selected first dip37x140 versus idle32x147:7row articulation reduction; dark
sole material distinct from ivory boot uppers. Source01 neutral30x147 is sampled density evidence,
not exact selected body dimensions. Head/torso/moving/prone polish remains open.

356native checks pass:20full RunSave checkpoints,20fresh actual visible Title
Continues,40native/source captures,20exact original/restored pairs. Six dry holds
plus20secsettled; sixfall/sixrise and completion before first normal idle draw.
Whole actor/player/source/root parity, restored pause, finite nonfatal completion
to fresh selected idle0 and dead settled hold verified. Actual transmission
Continue acknowledged and overlay gone before capture; exact normal factory and
ordered catalog, no injected study manifest/subclass. Normal costs/failures,
prescribed clear furnished site and paused peers/world.105bounded inputs stable;
2931owner non-log files unchanged under scratchAPPDATA;exit0/engine0.
All20pairs on four boards and three four-facing family sheets inspected.

New tests/test_marsh_east_damage_production.gd with pairedUIDci8ehdamn4v76 is
companions/native with900s timeout; classification verified. tests/index.json
metadata added after launch, outside105input interval.71body manifests,
228selectedstates/1190slots are coverage counts, not full master acceptance.
Earlier249dry/404injury studies retain dated staged scope; full normal Save/
Continue is current scoped East evidence. Selection.json records current
provisional admission, while source requests/recipes retain original provenance.

Family held review: complete East figures and white coolant unobscured, warm
ivory/sage retained; visible glove-side droplets and stationary puddle persist
through recovery, fading before exact idle0. East final dark boot sole/heel surfaces remain
matte charcoal; boot uppers judged separately. West old head/shoulder/detail
joins need their own master repair; no equal perspective widths or per-pose height
normalization. South and East remain provisional head/body/prone motion studies.
Full Save/Continue boards do not prove realtime/browser motion, articulated limb
contact, natural traffic or entire family acceptance.

Review:character/marsh-east-injury-material-v1/normal-review-v1/index.html.
Next: West native collapse and white-fluid/rise family, then full-set
consistency/motion polish. Full Marsh objective remains active and incomplete.
'''
def append_once(path):
    with path.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
    if not present:
        with path.open('a',encoding='utf-8') as stream:stream.write(LESSON)
def main():
    review=BASE/'normal-review-v1'
    assessment={'allTwentyPairsInspected':True,'allThreeFacingFamilyBoardsInspected':True,'pairedBoards':[f'paired-{i}.png' for i in range(4)],'familyBoards':[f'family-{a}.png' for a in ['death-ground','injury-ground','injury-rise']],
      'artStatus':'Provisional selected East whole body and white fluid; master/moving/family polish open.',
      'observations':['All20original/Continued pairs show unobscured complete East figures with exact source parity.','Warm ivory/sage body and charcoal exposed rear soles preserved; dry shutdown distinct from white-fluid injury.','Screen-right separated droplets and stationary puddle reviewed in held renderer poses; exact floor and idle joins.','West older head/shoulder/detail density joins still need own-master comparison. South/East prone and lowered anatomy remain provisional.'],
      'pending':'Realtime moving review, articulated limb world contact, natural traffic and entire family acceptance.'}
    (review/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    runpy.run_path(str(ROOT/'tools/publish_marsh_east_damage_normal.py'),run_name='__main__')
    evidence=json.loads((review/'verification.json').read_text());assert evidence['checks']==356
    for folder in ['marsh-east-collapse-material-v1','marsh-east-injury-material-v1']:
        path=ROOT/'character'/folder/'selection.json';selection=json.loads(path.read_text())
        selection.update(status='normal provisional material source; full checkpoint/visible Continue verified; family art polish open',latestNormalEvidence={'path':'character/marsh-east-injury-material-v1/normal-review-v1/verification.json','checks':356,'fullCheckpoints':20,'freshVisibleTitleContinues':20,'exactOriginalContinuedPairs':20,'ownerFilesUnchanged':2931,'nativeVisualReview':True,'familyVisualReview':True},fullGoalComplete=False)
        path.write_text(json.dumps(selection,indent=2)+'\n')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:append_once(path)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh East normal damage

## Objective and acceptance
Full Marsh master-matched set and consistency/polish active/incomplete.
East damage family provisionally selected; normal full Save/Continue verified.

## Accepted decisions and constraints
Complete dry candidate01 and white-fluid injury/rise candidate01, exact idle.
No anatomy patch/pose fitting/recolor/mirror. Rear charcoal soles intentional.
Normal flags/save rules, owner profile/layouts preserved. Art acceptance provisional.

## Current state
Catalog appends two East manifests;71body entries,228selectedstates/1190slots.
Normal review has40views/20pairs and3four-facing family boards, all inspected.
New native checkpoint test/pairedUID, install/prepare/fingerprint/publish/record
helpers and native test registration. Both rootselection.json updated. Pipeline,
bible/status and byte-identical skill mirrors record proof and open art work.
West complete sources01/02 retained/packaged, unselected, native review pending.

## Verification
356checks/20full saves/20fresh visible TitleContinues/20exact original-restored
pairs; actor/player/source/root parity, pause, settled death, finite response and
fresh idle join.105bounded inputs stable;2931owner files unchanged;0fail/engine0/
exit0. Native classification verified; index metadata outside launched interval.
All20native pairs and3family boards inspected. Not moving/contact/full-set acceptance.

## Next action
Native West source02 collapse study, independent white-fluid/rise and normal
checkpoint family; then West repair and full-set master/style/proportion/grade
motion polish. Do not equate selected-state counts with completed art acceptance.
'''
    (ROOT/'docs/MARSH_EAST_DAMAGE_NORMAL_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded normal East damage milestone; full Marsh goal active.')
if __name__=='__main__':main()
